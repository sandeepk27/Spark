import os
import re
import urllib.parse

# CONFIGURATION
REPO_USER = "sandeepk27"
REPO_NAME = "Spark"
BRANCH = "main"
POSTS_DIR = "posts"
IMAGES_DIR = "images"
COVER_IMAGES_DIR = "cover_images"  # NEW DIRECTORY

# Extensions to look for
SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]

# Base URLs
BASE_CONTENT_IMG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{IMAGES_DIR}/"
BASE_COVER_IMG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{COVER_IMAGES_DIR}/"

def find_image(base_name, search_dir):
    """Helper to find an image file with supported extensions."""
    for ext in SUPPORTED_EXTENSIONS:
        potential_image = base_name + ext
        potential_path = os.path.join(search_dir, potential_image)
        if os.path.exists(potential_path):
            return potential_image
    return None

def process_files():
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Flags detection
            has_auto_image = "auto_image: true" in content or "img: true" in content
            has_linkedin_image = "linkedin_image: yes" in content or "linkedin_image: true" in content
            has_devto_cover = "devto_cover: yes" in content or "cover: yes" in content

            # Global Trigger
            should_process = has_auto_image or has_linkedin_image or has_devto_cover

            if should_process:
                print(f"Processing {filename}...")
                base_name = os.path.splitext(filename)[0]
                
                # --- PROCESS CONTENT IMAGE (images/) ---
                # Triggered by: auto_image, img: true, linkedin_image
                if has_auto_image or has_linkedin_image:
                    content_image_name = find_image(base_name, IMAGES_DIR)
                    if content_image_name:
                        encoded_name = urllib.parse.quote(content_image_name)
                        public_url = BASE_CONTENT_IMG_URL + encoded_name

                        print(f"Found content image: {content_image_name}")

                        # Append to body if not present
                        if public_url not in content:
                            image_markdown = f"\n\n![{base_name}]({public_url})\n"
                            content += image_markdown
                            print(f"Appended content image to body of {filename}")
                    else:
                        print(f"No content image found for {filename} in {IMAGES_DIR}/")

                # --- PROCESS COVER IMAGE (cover_images/) ---
                # Triggered ONLY by: devto_cover: yes or cover: yes
                if has_devto_cover:
                    cover_image_name = find_image(base_name, COVER_IMAGES_DIR)
                    if cover_image_name:
                        encoded_name = urllib.parse.quote(cover_image_name)
                        public_url = BASE_COVER_IMG_URL + encoded_name

                        print(f"Found cover image: {cover_image_name}")

                        # Update or Add cover_image in frontmatter
                        # Use robust regex with MULTILINE and start/end anchors
                        if re.search(r"^cover_image:.*$", content, flags=re.MULTILINE):
                            content = re.sub(r"^cover_image:.*$", f"cover_image: {public_url}", content, flags=re.MULTILINE)
                            print("Updated existing cover_image")
                        else:
                            # Add after title
                            if re.search(r"^title:.*$", content, flags=re.MULTILINE):
                                content = re.sub(r"^(title:.*)$", f"\\1\ncover_image: {public_url}", content, flags=re.MULTILINE)
                                print("Added new cover_image field")
                            else:
                                # Fallback if title not found (rare)
                                print("Warning: Could not find title line to inject cover_image")
                    else:
                        print(f"Warning: devto_cover: yes set but no image found in {COVER_IMAGES_DIR}/")

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

if __name__ == "__main__":
    process_files()
