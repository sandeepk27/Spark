import os
import re

# CONFIGURATION
REPO_USER = "sandeepk27"   # Ensure this is correct
REPO_NAME = "Spark"        # Ensure this is correct (Case Sensitive!)
BRANCH = "main"
POSTS_DIR = "posts"
IMAGES_DIR = "images"

# List of extensions to check
SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]

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
                
                # Get the filename without extension (e.g., "Day 7")
                base_name = os.path.splitext(filename)[0]
                
                found_image_name = None
                
                # Loop through extensions to find a matching file
                for ext in SUPPORTED_EXTENSIONS:
                    potential_image = base_name + ext
                    potential_path = os.path.join(IMAGES_DIR, potential_image)
                    
                    if os.path.exists(potential_path):
                        found_image_name = potential_image
                        break # Stop looking once found

                if found_image_name:
                    # Construct the public URL
                    public_url = BASE_IMG_URL + found_image_name
                    print(f"Found image: {found_image_name}. Injecting: {public_url}")
                    
                    # Regex to add or replace cover_image in Front Matter
                    if "cover_image:" in content:
                        content = re.sub(r"cover_image:.*", f"cover_image: {public_url}", content)
                    else:
                        content = re.sub(r"(title:.*)", f"\\1\ncover_image: {public_url}", content)
                    
                    # Write the changes back to the file
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                else:
                    print(f"Warning: 'auto_image: true' found in {filename} but no image (png/jpg/jpeg) found in {IMAGES_DIR}")

if __name__ == "__main__":
    process_files()
