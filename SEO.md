# SEO & Growth Guide

## Getting More Views
You asked about getting more views after deployment. Since your blog is automated, your focus should be on **Content Quality** and **Distribution**.

### 1. Run the SEO Check
We have added a script to help you optimize your posts before publishing.
Run it locally:
```bash
python scripts/seo_check.py
```
It will check for:
- **Title Length:** Ensure it's catchy but not cut off by Google (40-60 chars).
- **Description:** This becomes the meta description. Make it a "hook" (150-160 chars).
- **Tags:** Use all 4 allowed slots on Dev.to. Mix broad (e.g., `python`) and specific (e.g., `pyspark`).

### 2. Cross-Posting & Canonical URLs
You are already posting to Dev.to and LinkedIn (great!).
- **If you have a personal blog:** Ensure you add `canonical_url: https://yourblog.com/post-url` to the frontmatter of your Markdown files. This tells Google your site is the original source, preventing duplicate content penalties.
- **Medium / Hashnode:** You can expand the `publish.yml` to post there too, but always link back to the original.

### 3. Engagement
- **LinkedIn:** The new script posts a link. Engage with comments on that post.
- **Twitter/X:** Consider adding a step to tweet your new posts.
- **Newsletters:** If you have an email list, automate sending the RSS feed from Dev.to.

### 4. Content Optimization
- **Images:** Your `img: true` setup is excellent. Visuals increase click-through rates significantly.
- **Intro:** The first paragraph determines if a user stays. Make it punchy.
- **Series:** You are writing a "Spark Mastery Series". Interlink your posts! (e.g., "Check out [Day 6](./Day%206.md)").

## Automation
The repository now contains:
- `scripts/seo_check.py`: validaties your SEO metadata.
- `scripts/image_linking.py`: Supports `linkedin_image: yes` to auto-link images for cross-posting.
