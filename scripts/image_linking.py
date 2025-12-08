import os
import re
import urllib.parse  # <--- NEW IMPORT

# CONFIGURATION
REPO_USER = "sandeepk27"
REPO_NAME = "Spark"
BRANCH = "main"
POSTS_DIR = "posts"
IMAGES_DIR = "images"

# Extensions to look for
SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]

# Base URL
BASE_IMG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{IMAGES_DIR}/"

def process_files():
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if "auto_image: true" in content:
                print(f"Processing {filename}...")
                
                base_name = os.path.splitext(filename)[0]
                found_image_name = None
                
                # Find matching image
                for ext in SUPPORTED_EXTENSIONS:
                    potential_image = base_name + ext
                    potential_path = os.path.join(IMAGES_DIR, potential_image)
                    if os.path.exists(potential_path):
                        found_image_name = potential_image
                        break

                if found_image_name:
                    # --- THE FIX: URL ENCODE THE IMAGE NAME ---
                    # This turns "Day 7.png" into "Day%207.png"
                    encoded_name = urllib.parse.quote(found_image_name)
                    public_url = BASE_IMG_URL + encoded_name
                    
                    print(f"Found image. Injecting: {public_url}")
                    
                    if "cover_image:" in content:
                        content = re.sub(r"cover_image:.*", f"cover_image: {public_url}", content)
                    else:
                        content = re.sub(r"(title:.*)", f"\\1\ncover_image: {public_url}", content)
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                else:
                    print(f"Warning: Image not found for {filename}")

if __name__ == "__main__":
    process_files()
