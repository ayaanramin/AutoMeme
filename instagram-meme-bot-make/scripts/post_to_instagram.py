"""
post_to_instagram.py — Sends the meme to a Make.com webhook,
which then posts it to Instagram automatically.

This avoids all the Meta Developer API complexity.

Required env var:
    MAKE_WEBHOOK_URL   Your Make.com webhook URL (see README for setup)
"""

import os
import sys
import requests


def post_image(image_url: str, caption: str):
    webhook_url = os.environ.get("MAKE_WEBHOOK_URL")
    if not webhook_url:
        print("ERROR: MAKE_WEBHOOK_URL is not set.")
        sys.exit(1)

    payload = {
        "image_url": image_url,
        "caption": caption,
    }

    print(f"   Sending to Make.com webhook...")
    resp = requests.post(webhook_url, json=payload, timeout=30)

    if resp.status_code == 200:
        print("   Make.com accepted the request!")
    else:
        print(f"   Make.com error {resp.status_code}: {resp.text}")
        sys.exit(1)
