# Zapier "Code by Zapier" (Python) Step
# Use this code in a Zapier workflow to fetch the latest post from Dev.to and prepare it for LinkedIn.

import requests
import re

# CONFIGURATION
# Replace with your Dev.to username
DEVTO_USERNAME = "sandeepk27"
# GitHub Raw URL base for your images (ensure this matches your repo)
REPO_USER = "sandeepk27"
REPO_NAME = "Spark"
BRANCH = "main"
IMAGES_DIR = "images"
BASE_IMG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{IMAGES_DIR}/"

def get_latest_post():
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

    # Extract Data
    title = article.get("title")
    description = article.get("description")
    url = article.get("url")
    body_markdown = article.get("body_markdown", "") # API usually returns this

    # Check for "linkedin_image: yes" or similar flags in the raw markdown if available,
    # OR simply check if we have a matching image in our repo based on the title.
    # The user requirement: "if a linkedin images tag is yes then accordingly it should pick the images from images folder"

    # Since Zapier might not see the raw markdown frontmatter easily via the standard RSS/API unless authenticated or parsing raw,
    # we can infer availability if the local script successfully appended the image link to the body.

    image_url = None

    # Strategy 1: Look for the image appended by our local script in the body
    # The script appends: ![Title](.../images/Title.png)
    # Regex to find our specific GitHub raw image links
    img_match = re.search(r"!\[.*?\]\((https://raw\.githubusercontent\.com/[^)]+/images/[^)]+)\)", body_markdown)

    if img_match:
        image_url = img_match.group(1)
    else:
        # Strategy 2: Construct the URL manually if we know the convention and assume it exists if the flag was conceptually "yes"
        # But checking existence requires a request.
        # Let's try to construct it based on the title (cleaning special chars)
        # This mirrors the python script's logic roughly
        clean_title = re.sub(r'[^\w\s-]', '', title).strip() # simplified cleaning
        # NOTE: The local script uses filename, which matches the markdown filename.
        # The Dev.to API title might differ slightly if changed.
        # Strategy 1 is much safer.
        pass

    return {
        "title": title,
        "description": description,
        "link": url,
        "image_url": image_url,
        "has_image": "yes" if image_url else "no"
    }

# Zapier requires the output to be a dictionary assigned to 'output'
# In the Zapier editor, you don't use 'def main()', just write the code.
# But for this file, we simulate it.

try:
    output = main()
except Exception as e:
    output = {"error": str(e)}

print(output)
