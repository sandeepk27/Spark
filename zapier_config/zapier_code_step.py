# Zapier "Code by Zapier" (Python) Step
# Use this code in a Zapier workflow to fetch the latest post from Dev.to and prepare it for LinkedIn.

import requests
import re
from datetime import datetime, timezone

# CONFIGURATION
# Replace with your Dev.to username
DEVTO_USERNAME = "sandeepk27"
# Maximum age in hours to consider a post "new".
# If a post was published older than this threshold, we skip posting to LinkedIn.
# This prevents reposting old articles if content is updated.
MAX_AGE_HOURS = 24

def get_latest_post():
    # Fetch the latest article from Dev.to API
    url = f"https://dev.to/api/articles?username={DEVTO_USERNAME}&per_page=1"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()
        if articles:
            return articles[0]
    return None

def check_age(published_at_str):
    """Returns True if the post is recent (within MAX_AGE_HOURS), False otherwise."""
    if not published_at_str:
        return True # Default to processing if no date found

    try:
        # Dev.to format: "2025-12-08T16:14:15Z"
        # Parse ISO format (handling Z for UTC)
        published_at = datetime.strptime(published_at_str.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
        now = datetime.now(timezone.utc)

        diff = now - published_at
        hours_old = diff.total_seconds() / 3600

        return hours_old < MAX_AGE_HOURS
    except Exception as e:
        return True # Fallback on error

def main():
    article = get_latest_post()
    if not article:
        return {"status": "no_article_found", "should_post": "no"}

    # Extract Standard Data
    title = article.get("title")
    description = article.get("description")
    url = article.get("url")
    published_at = article.get("published_at")
    body_markdown = article.get("body_markdown", "")

    # Logic 1: Check Age (Prevent reposting on edits)
    is_new = check_age(published_at)
    if not is_new:
        return {
            "status": "skipped_old_post",
            "should_post": "no",
            "reason": f"Post is older than {MAX_AGE_HOURS} hours"
        }

    # Logic 2: Extract Image
    image_url = None

    # Priority 1: Check for hidden comment (injected when devto_content_image: no)
    hidden_match = re.search(r"<!-- LINKEDIN_IMAGE_SOURCE: (https://raw\.githubusercontent\.com/[^ ]+) -->", body_markdown)
    if hidden_match:
        image_url = hidden_match.group(1)

    # Priority 2: Check for visible image (injected when devto_content_image: yes or default)
    if not image_url:
        img_match = re.search(r"!\[.*?\]\((https://raw\.githubusercontent\.com/[^)]+/images/[^)]+)\)", body_markdown)
        if img_match:
            image_url = img_match.group(1)

    return {
        "title": title,
        "description": description,
        "link": url,
        "image_url": image_url,
        "use_custom_image": "yes" if image_url else "no",
        "should_post": "yes"
    }

# Zapier Output Handling
try:
    output = main()
except Exception as e:
    output = {"error": str(e), "should_post": "no"}

print(output)
