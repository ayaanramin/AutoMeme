"""
create_meme_image.py — Calls the Imgflip API to generate a meme image
and saves it locally as a JPEG.

Required env vars:
    IMGFLIP_USERNAME   Your Imgflip username (free account at imgflip.com)
    IMGFLIP_PASSWORD   Your Imgflip password

Free accounts work fine — images will have a small Imgflip watermark.
Upgrade to Imgflip Pro ($9/mo) to remove it.
"""

import os
import sys
import requests


IMGFLIP_API = "https://api.imgflip.com/caption_image"


def create_meme_image(meme: dict, output_path: str = "/tmp/meme.jpg") -> str:
    """
    Generate a meme image using Imgflip and save it to output_path.
    Returns the path to the saved image.
    """
    username = os.environ.get("IMGFLIP_USERNAME")
    password = os.environ.get("IMGFLIP_PASSWORD")

    if not username or not password:
        print("❌ ERROR: IMGFLIP_USERNAME or IMGFLIP_PASSWORD is not set.")
        sys.exit(1)

    # Build the text boxes payload
    # Imgflip uses boxes[0][text], boxes[1][text], etc.
    texts = [meme.get("top_text", ""), meme.get("bottom_text", "")]
    texts += meme.get("extra_texts", [])

    data = {
        "template_id": meme["template_id"],
        "username":    username,
        "password":    password,
        "font":        "impact",
        "max_font_size": 50,
    }

    for i, text in enumerate(texts):
        if text:  # Only add non-empty boxes
            data[f"boxes[{i}][text]"] = text
            data[f"boxes[{i}][color]"] = "#ffffff"
            data[f"boxes[{i}][outline_color]"] = "#000000"

    response = requests.post(IMGFLIP_API, data=data, timeout=30)
    result = response.json()

    if not result.get("success"):
        print("❌ Imgflip API error:", result.get("error_message", result))
        sys.exit(1)

    image_url = result["data"]["url"]
    print(f"   Imgflip URL: {image_url}")

    # Download the image locally
    img_response = requests.get(image_url, timeout=30)
    img_response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(img_response.content)

    return output_path
