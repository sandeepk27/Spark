import os
import re
import sys

# Configuration
POSTS_DIR = "posts"

def analyze_post(filepath):
    issues = []
    warnings = []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse frontmatter
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

    # Check Title
    title = frontmatter.get("title", "")
    if not title:
        issues.append("Missing title in frontmatter.")
    elif len(title) < 10:
        warnings.append(f"Title is too short ({len(title)} chars). Aim for 40-60 chars for better CTR.")
    elif len(title) > 65:
        warnings.append(f"Title is too long ({len(title)} chars). Google may truncate it (keep under 60).")

    # Check Description
    description = frontmatter.get("description", "")
    if not description:
        issues.append("Missing description in frontmatter.")
    elif len(description) < 50:
        warnings.append(f"Description is too short ({len(description)} chars). Aim for 150-160 chars.")
    elif len(description) > 170:
        warnings.append(f"Description is too long ({len(description)} chars). Google truncates around 160 chars.")

    # Check Tags
    tags_str = frontmatter.get("tags", "")
    tags = [t.strip() for t in tags_str.split(",")] if tags_str else []
    if len(tags) < 3:
        warnings.append(f"Too few tags ({len(tags)}). Dev.to allows up to 4. Use meaningful tags for discovery.")

    # Check Content Length (Word Count)
    # Simple whitespace split
    words = body.split()
    word_count = len(words)
    if word_count < 300:
        warnings.append(f"Content is thin ({word_count} words). Aim for 600+ words for better ranking.")

    # Keyword check (Basic)
    # Check if primary tags appear in the first 100 words of body
    intro_text = " ".join(words[:100]).lower()
    for tag in tags:
        if tag.lower() not in intro_text:
            # This is a soft warning, tags might be generic like "python"
            pass
            # warnings.append(f"Tag '{tag}' not found in introduction. Consider mentioning it early.")

    return issues, warnings

def main():
    print("running SEO check...")
    print("-" * 40)

    has_issues = False

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            issues, warnings = analyze_post(filepath)

            if issues or warnings:
                print(f"FILE: {filename}")
                for issue in issues:
                    print(f"  [ERROR] {issue}")
                    has_issues = True
                for warning in warnings:
                    print(f"  [WARN]  {warning}")
                print("-" * 40)

    if not has_issues:
        print("No critical SEO issues found! Good job.")
    else:
        # Don't fail the build for warnings, only if you want to enforce strict rules
        # sys.exit(1)
        pass

if __name__ == "__main__":
    main()
