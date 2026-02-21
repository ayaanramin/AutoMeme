"""
main.py — Runs daily via GitHub Actions.
1. Uses Claude AI + web search to find a trending topic
2. Generates meme text for a classic template
3. Creates the meme image via Imgflip
4. Uploads to Cloudinary for a public URL
5. Posts to Instagram
"""

from get_trending_meme import get_trending_meme
from create_meme_image import create_meme_image
from upload_to_cloudinary import upload_image
from post_to_instagram import post_image


def main():
    print("🚀 Starting daily meme poster...")

    # 1. Ask Claude what's trending and generate meme content
    print("\n🤖 Asking Claude for today's trending meme...")
    meme = get_trending_meme()
    print(f"   Template : {meme['template_name']}")
    print(f"   Topic    : {meme['topic']}")
    print(f"   Top text : {meme['top_text']}")
    print(f"   Bottom   : {meme['bottom_text']}")
    print(f"   Caption  : {meme['caption']}")

    # 2. Generate the meme image via Imgflip
    print("\n🖼️  Generating meme image...")
    image_path = create_meme_image(meme)
    print(f"   Saved to: {image_path}")

    # 3. Upload to Cloudinary
    print("\n☁️  Uploading to Cloudinary...")
    public_url = upload_image(image_path)
    print(f"   URL: {public_url}")

    # 4. Post to Instagram
    print("\n📸 Posting to Instagram...")
    post_image(image_url=public_url, caption=meme["caption"])
    print("\n✅ Done! Meme posted successfully.")


if __name__ == "__main__":
    main()
