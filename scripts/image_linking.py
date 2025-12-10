import os
import re
import urllib.parse

# CONFIGURATION
REPO_USER = "sandeepk27"
REPO_NAME = "Spark"
BRANCH = "main"
POSTS_DIR = "posts"
IMAGES_DIR = "images"
COVER_IMAGES_DIR = "cover-images"

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

def check_flag(flag_name, content):
    """
    Checks for flag: yes/true with or without quotes, case insensitive.
    Matches: flag: yes, flag: 'yes', flag: "true", flag: true
    """
    pattern = fr"{flag_name}:\s*['\"]?(yes|true|on)['\"]?"
    return bool(re.search(pattern, content, re.IGNORECASE))

def process_files():
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # --- SMART FLAG DETECTION (Regex) ---
            # Now works with: 'yes', "yes", true, or yes
            has_auto_image = check_flag("auto_image", content) or check_flag("img", content)
            has_linkedin_image = check_flag("linkedin_image", content)
            has_devto_cover = check_flag("devto_cover", content) or check_flag("cover", content)
            
            # Check for explicit "no" to hide content image
            # Matches: devto_content_image: 'no' or no or false
            hide_content_image = bool(re.search(r"devto_content_image:\s*['\"]?(no|false)['\"]?", content, re.IGNORECASE))
            show_content_image = not hide_content_image

            should_process = has_auto_image or has_linkedin_image or has_devto_cover

            if should_process:
                print(f"Processing {filename}...")
                base_name = os.path.splitext(filename)[0]
                
                # --- 1. PROCESS CONTENT IMAGE (images/) ---
                # Triggered by: auto_image, img, linkedin_image
                if has_auto_image or has_linkedin_image:
                    content_image_name = find_image(base_name, IMAGES_DIR)
                    if content_image_name:
                        encoded_name = urllib.parse.quote(content_image_name)
                        public_url = BASE_CONTENT_IMG_URL + encoded_name

                        print(f"Found content image: {content_image_name}")

                        # Prepare injection strings
                        visible_markdown = f"\n\n![{base_name}]({public_url})\n"
                        hidden_markdown = f"\n\n\n"

                        # Check if link already exists to avoid duplicates
                        if public_url not in content:
                            if show_content_image:
                                content += visible_markdown
                                print(f"Appended visible content image to {filename}")
                            else:
                                content += hidden_markdown
                                print(f"Appended hidden content image to {filename}")
                    else:
                        if has_auto_image: # Only warn if user explicitly asked for it
                            print(f"Warning: Content image requested but not found in {IMAGES_DIR}/")

                # --- 2. PROCESS COVER IMAGE (cover-images/) ---
                # Triggered ONLY by: devto_cover
                if has_devto_cover:
                    cover_image_name = find_image(base_name, COVER_IMAGES_DIR)
                    if cover_image_name:
                        encoded_name = urllib.parse.quote(cover_image_name)
                        public_url = BASE_COVER_IMG_URL + encoded_name

                        print(f"Found cover image: {cover_image_name}")

                        # Update or Add cover_image in frontmatter
                        # Regex finds the line start ^ to end $ to ensure clean replacement
                        if re.search(r"^cover_image:.*$", content, flags=re.MULTILINE):
                            content = re.sub(r"^cover_image:.*$", f"cover_image: {public_url}", content, flags=re.MULTILINE)
                            print("Updated existing cover_image")
                        else:
                            # Add after title
                            if re.search(r"^title:.*$", content, flags=re.MULTILINE):
                                content = re.sub(r"^(title:.*)$", f"\\1\ncover_image: {public_url}", content, flags=re.MULTILINE)
                                print("Added new cover_image field")
                    else:
                        print(f"Warning: devto_cover: yes set but no image found in {COVER_IMAGES_DIR}/")

                # Save changes
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

if __name__ == "__main__":
    process_files()
