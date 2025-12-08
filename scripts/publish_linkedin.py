import os
import re
import sys
import requests
import json

# Configuration
POSTS_DIR = "posts"
LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN")

def get_linkedin_urn():
    """Fetches the LinkedIn URN for the authenticated user."""
    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return f"urn:li:person:{data['id']}"
    else:
        print(f"Error fetching LinkedIn profile: {response.text}")
        return None

def publish_to_linkedin(filepath, content, urn):
    """Publishes a post to LinkedIn."""

    # Extract frontmatter
    frontmatter = {}
    body = ""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_frontmatter = parts[1]
            body = parts[2]
            for line in raw_frontmatter.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    title = frontmatter.get("title", "New Blog Post")
    description = frontmatter.get("description", "")
    devto_url = frontmatter.get("devto_url")
    cover_image = frontmatter.get("cover_image")

    if not devto_url:
        print(f"Skipping {filepath}: No devto_url found.")
        return False

    print(f"Publishing {filepath} to LinkedIn...")

    # Construct the share text
    share_text = f"{title}\n\n{description}\n\nRead more here: {devto_url}"

    # LinkedIn API Payload
    # Using ugcPosts endpoint which is versatile
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    payload = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": share_text
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": description
                        },
                        "originalUrl": devto_url,
                        "title": {
                            "text": title
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # If we have a cover image, we might want to ensure LinkedIn uses it.
    # Usually passing the URL in 'originalUrl' is enough for LinkedIn to scrape it.
    # But if we want to be explicit, we could add 'thumbnails' list if supported by ARTICLE category,
    # but 'originalUrl' is usually sufficient for articles.

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print(f"Successfully published {filepath} to LinkedIn.")
        return True
    else:
        print(f"Failed to publish {filepath}. Status: {response.status_code}, Response: {response.text}")
        return False

def update_file_status(filepath, content):
    """Updates the file to mark it as published to LinkedIn."""
    # We need to insert linkedin_posted: true into frontmatter
    # We can assume the content passed is the original content

    # Simple regex replace to add the field
    # Look for the last line of frontmatter (which is ---)
    # Actually, simpler to just replace "---" with "linkedin_posted: true\n---"
    # But we need to do it only on the second "---"

    parts = content.split("---", 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        if "linkedin_posted: true" not in frontmatter:
            new_frontmatter = frontmatter + "linkedin_posted: true\n"
            new_content = "---" + new_frontmatter + "---" + parts[2]

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filepath} with linkedin_posted: true")

def process_files():
    if not LINKEDIN_ACCESS_TOKEN:
        print("LINKEDIN_ACCESS_TOKEN is not set. Skipping LinkedIn publishing.")
        return

    urn = get_linkedin_urn()
    if not urn:
        print("Could not retrieve LinkedIn URN. Aborting.")
        return

    print(f"Using LinkedIn URN: {urn}")

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse frontmatter to check status
            # We don't use a full yaml parser to avoid dependencies, just simple check
            is_published_devto = "devto_url:" in content
            is_published_linkedin = "linkedin_posted: true" in content

            if is_published_devto and not is_published_linkedin:
                success = publish_to_linkedin(filepath, content, urn)
                if success:
                    update_file_status(filepath, content)

if __name__ == "__main__":
    process_files()
