import os
import re
import urllib.parse
from PIL import Image, ImageOps  # Requires: pip install Pillow

# CONFIGURATION
REPO_USER = "sandeepk27"
REPO_NAME = "Spark"
BRANCH = "main"
POSTS_DIR = "posts"
IMAGES_DIR = "images"
COVER_IMAGES_DIR = "cover-images"

# Dev.to Recommended Dimensions
DEVTO_WIDTH = 1000
DEVTO_HEIGHT = 420

SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]

BASE_CONTENT_IMG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{IMAGES_DIR}/"
BASE_COVER_IMG_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{COVER_IMAGES_DIR}/"

def find_image(base_name, search_dir):
    for ext in SUPPORTED_EXTENSIONS:
        potential_image = base_name + ext
        potential_path = os.path.join(search_dir, potential_image)
        if os.path.exists(potential_path):
            return potential_image, potential_path
    return None, None

def check_flag(flag_name, content):
    pattern = fr"{flag_name}:\s*['\"]?(yes|true|on)['\"]?"
    return bool(re.search(pattern, content, re.IGNORECASE))

def resize_for_devto(image_path):
    """
    Resizes and center-crops the image to 1000x420px.
    Overwrites the original file.
    """
    try:
        with Image.open(image_path) as img:
            # Check if resize is actually needed to save processing time
            if img.size == (DEVTO_WIDTH, DEVTO_HEIGHT):
                return

            print(f"Resizing {image_path} from {img.size} to ({DEVTO_WIDTH}, {DEVTO_HEIGHT})...")
            
            # ImageOps.fit performs a 'Smart Crop' (Center Crop)
            processed_img = ImageOps.fit(img, (DEVTO_WIDTH, DEVTO_HEIGHT), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            
            # Save it back overwriting the original
            processed_img.save(image_path)
            print(f"✅ Resize successful: {image_path}")
            
    except Exception as e:
        print(f"❌ Failed to resize image {image_path}: {e}")

def process_files():
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            has_auto_image = check_flag("auto_image", content) or check_flag("img", content)
            has_linkedin_image = check_flag("linkedin_image", content)
            has_devto_cover = check_flag("devto_cover", content) or check_flag("cover", content)
            
            hide_content_image = bool(re.search(r"devto_content_image:\s*['\"]?(no|false)['\"]?", content, re.IGNORECASE))
            show_content_image = not hide_content_image

            should_process = has_auto_image or has_linkedin_image or has_devto_cover

            if should_process:
                print(f"Processing {filename}...")
                base_name = os.path.splitext(filename)[0]
                
                # --- 1. CONTENT IMAGE ---
                if has_auto_image or has_linkedin_image:
                    content_image_name, _ = find_image(base_name, IMAGES_DIR)
                    if content_image_name:
                        encoded_name = urllib.parse.quote(content_image_name)
                        public_url = BASE_CONTENT_IMG_URL + encoded_name
                        
                        visible_markdown = f"\n\n![{base_name}]({public_url})\n"
                        hidden_markdown = f"\n\n\n"

                        if public_url not in content:
                            if show_content_image:
                                content += visible_markdown
                            else:
                                content += hidden_markdown
                            print(f" injected content image.")

                # --- 2. COVER IMAGE (WITH RESIZE) ---
                if has_devto_cover:
                    cover_image_name, cover_image_path = find_image(base_name, COVER_IMAGES_DIR)
                    if cover_image_name:
                        # RESIZE STEP
                        resize_for_devto(cover_image_path)
                        
                        encoded_name = urllib.parse.quote(cover_image_name)
                        public_url = BASE_COVER_IMG_URL + encoded_name

                        if re.search(r"^cover_image:.*$", content, flags=re.MULTILINE):
                            content = re.sub(r"^cover_image:.*$", f"cover_image: {public_url}", content, flags=re.MULTILINE)
                            print("Updated existing cover_image")
                        else:
                            if re.search(r"^title:.*$", content, flags=re.MULTILINE):
                                content = re.sub(r"^(title:.*)$", f"\\1\ncover_image: {public_url}", content, flags=re.MULTILINE)
                                print("Added new cover_image field")
                    else:
                        print(f"Warning: Cover image requested but not found in {COVER_IMAGES_DIR}")

                # This write block must be aligned with the 'if should_process:' block
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

if __name__ == "__main__":
    process_files()
