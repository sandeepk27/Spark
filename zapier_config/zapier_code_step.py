# Zapier "Code by Zapier" (Python) Step
# Use this code in a Zapier workflow to fetch the latest post from Dev.to and prepare it for LinkedIn.

import requests
import re

# CONFIGURATION
# Replace with your Dev.to username
DEVTO_USERNAME = "sandeepk27"

def get_latest_post():
    # Fetch the latest article from Dev.to API
    url = f"https://dev.to/api/articles?username={DEVTO_USERNAME}&per_page=1"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()
        if articles:
            return articles[0]
    return None

def main():
    article = get_latest_post()
    if not article:
        return {"status": "no_article_found"}

    # Extract Standard Data
    title = article.get("title")
    description = article.get("description")
    url = article.get("url")
    body_markdown = article.get("body_markdown", "")

    # Logic:
    # 1. We ALWAYS want to post the blog link (`url`).
    # 2. We extract image URL if available.

    image_url = None

    # Priority 1: Check for hidden comment (injected when devto_content_image: no)
    # Format: <!-- LINKEDIN_IMAGE_SOURCE: https://... -->
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
        "link": url,         # The Blog Link (Main content)
        "image_url": image_url, # Custom Image (if "yes"), else None/Null
        "use_custom_image": "yes" if image_url else "no"
    }

# Zapier Output Handling
try:
    output = main()
except Exception as e:
    output = {"error": str(e)}

print(output)
