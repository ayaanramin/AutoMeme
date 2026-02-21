"""
upload_to_cloudinary.py — Uploads a local image to Cloudinary
and returns a public URL that Instagram can fetch.

Required env var:
    CLOUDINARY_URL  e.g. cloudinary://API_KEY:API_SECRET@CLOUD_NAME
"""

import os
import sys
import cloudinary
import cloudinary.uploader


def _configure():
    url = os.environ.get("CLOUDINARY_URL")
    if not url:
        print("❌ ERROR: CLOUDINARY_URL secret is not set.")
        print("   Get it from: https://console.cloudinary.com → Dashboard")
        sys.exit(1)
    cloudinary.config(cloudinary_url=url)


def upload_image(file_path: str) -> str:
    """
    Upload an image to Cloudinary and return its secure public URL.
    Uses a fixed public_id so old uploads get overwritten automatically,
    keeping your Cloudinary storage clean.
    """
    _configure()

    result = cloudinary.uploader.upload(
        file_path,
        resource_type="image",
        public_id="instagram_daily_meme",
        overwrite=True,
        invalidate=True,          # Bust CDN cache so Instagram always gets the fresh image
    )

    url = result.get("secure_url")
    if not url:
        print("❌ Cloudinary upload failed:", result)
        sys.exit(1)

    return url
