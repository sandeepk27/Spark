import os
import re

# CONFIGURATION
REPO_USER = "sandeepk27"  # CHANGE THIS to your GitHub username
REPO_NAME = "Spark"       # CHANGE THIS to your Repo name
BRANCH = "main"
POSTS_DIR = "posts"
IMAGES_DIR = "images"

# The base URL for raw images on GitHub
BASE_IMG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{IMAGES_DIR}/"

def process_files():
    # Loop through all markdown files in posts/
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if user set auto_image: true
            if "auto_image: true" in content:
                print(f"Processing {filename}...")
                
                # Check if corresponding image exists
                image_name = filename.replace(".md", ".png") # Assumes PNG
                image_path = os.path.join(IMAGES_DIR, image_name)
                
                if os.path.exists(image_path):
                    # Construct the public URL
                    public_url = BASE_IMG_URL + image_name
                    print(f"Found image! Injecting: {public_url}")
                    
                    # Regex to add or replace cover_image in Front Matter
                    # If cover_image exists, replace it. If not, add it after title.
                    if "cover_image:" in content:
                        content = re.sub(r"cover_image:.*", f"cover_image: {public_url}", content)
                    else:
                        content = re.sub(r"(title:.*)", f"\\1\ncover_image: {public_url}", content)
                    
                    # Write the changes back to the file
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                else:
                    print(f"Warning: 'auto_image: true' found but no image at {image_path}")

if __name__ == "__main__":
    process_files()
  
