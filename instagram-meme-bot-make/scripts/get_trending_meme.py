"""
get_trending_meme.py — Uses:
  - Reddit's public JSON API (no key needed) to find what's trending today
  - Google Gemini API (completely free tier) to write the meme

Free tier: 15 requests/minute, 1 million tokens/day — overkill for 1 post/day.

Required env var:
    GEMINI_API_KEY   Free at: https://aistudio.google.com/app/apikey
"""

import os
import sys
import json
import random
import requests


TEMPLATES = {
    "Drake Approves":            {"id": "181913649",  "boxes": 2, "description": "Drake rejecting one thing, approving another. Use for 'X bad, Y good' comparisons."},
    "Distracted Boyfriend":      {"id": "112126428",  "boxes": 3, "description": "Man looking at another woman while girlfriend looks on. Use for 'ignoring important thing for shiny new thing'."},
    "Two Buttons":               {"id": "87743020",   "boxes": 2, "description": "Sweating guy choosing between two buttons. Use for impossible/funny dilemmas."},
    "Change My Mind":            {"id": "129242436",  "boxes": 1, "description": "Steven Crowder at table. Use for confident/provocative statements."},
    "Expanding Brain":           {"id": "93895088",   "boxes": 4, "description": "Four-panel brain expanding. Use for escalating/absurd ideas."},
    "Surprised Pikachu":         {"id": "155067746",  "boxes": 2, "description": "Top: setup/obvious action. Bottom: shocked Pikachu reaction."},
    "Gru's Plan":                {"id": "131940431",  "boxes": 4, "description": "Gru explains a plan that backfires. Use for plans with obvious flaws."},
    "They're The Same Picture":  {"id": "180190441",  "boxes": 2, "description": "Pam from The Office. Use for two things that are basically identical."},
    "This Is Fine":              {"id": "55311130",   "boxes": 2, "description": "Dog in burning room. Use for calm acceptance of disaster."},
    "Left Exit 12":              {"id": "124822590",  "boxes": 2, "description": "Car swerving to exit. Use for 'should do X, actually doing Y'."},
    "Mocking SpongeBob":         {"id": "102156234",  "boxes": 2, "description": "Top: normal statement. Bottom: mocking version."},
    "One Does Not Simply":       {"id": "61532",      "boxes": 2, "description": "Boromir from LOTR. Use for 'one does not simply [do hard thing]'."},
    "Hide the Pain Harold":      {"id": "27813981",   "boxes": 2, "description": "Smiling man hiding pain. Use for 'smiling through something terrible'."},
    "Ancient Aliens Guy":        {"id": "101470",     "boxes": 1, "description": "Wild claim guy. Use for absurd explanations."},
    "Bernie I Am Once Again":    {"id": "222403160",  "boxes": 1, "description": "Bernie asking for something. Use for persistent relatable requests."},
}

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
TRENDING_SUBREDDITS = ["worldnews", "technology", "sports", "entertainment", "science", "todayilearned"]


def get_reddit_trending() -> list:
    """Fetch top posts from Reddit's public JSON API. No API key needed."""
    subreddit = random.choice(TRENDING_SUBREDDITS)
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {"User-Agent": "MemeBot/1.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        posts = resp.json()["data"]["children"]
        headlines = [p["data"]["title"] for p in posts if not p["data"].get("stickied")]
        print(f"   Fetched {len(headlines)} trending posts from r/{subreddit}")
        return headlines[:8]
    except Exception as e:
        print(f"   Warning: Reddit fetch failed ({e}), using fallback topics")
        return [
            "Scientists make surprising discovery",
            "Major tech company announces big change",
            "Unexpected sports upset stuns fans",
            "New study changes everything we knew",
        ]


def ask_gemini(prompt: str) -> str:
    """Call the free Gemini API and return the text response."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        print("Get a free key at: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 512},
    }
    resp = requests.post(f"{GEMINI_API_URL}?key={api_key}", json=payload, timeout=30)

    if resp.status_code != 200:
        print(f"Gemini API error {resp.status_code}: {resp.text}")
        sys.exit(1)

    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


def get_trending_meme() -> dict:
    print("   Fetching trending topics from Reddit...")
    headlines = get_reddit_trending()
    headlines_text = "\n".join(f"- {h}" for h in headlines)

    template_list = "\n".join(
        f'- "{name}": {info["description"]} ({info["boxes"]} box{"es" if info["boxes"] > 1 else ""})'
        for name, info in TEMPLATES.items()
    )

    prompt = f"""You are a viral meme creator. Here are today's trending headlines:

{headlines_text}

Pick the most meme-able topic and create a meme using one of these templates:

{template_list}

Rules:
- Be funny and relatable, not mean or offensive
- Keep text SHORT — fewer words hit harder
- Avoid divisive politics — lean into universal humor
- Instagram caption should be engaging with 10-15 hashtags

Respond with ONLY valid JSON, no markdown fences:
{{
  "topic": "Brief description of chosen topic",
  "template_name": "Exact template name from the list",
  "top_text": "Top caption (short!)",
  "bottom_text": "Bottom caption (short!)",
  "extra_texts": [],
  "caption": "Engaging Instagram caption with hashtags"
}}

For 1-box templates: put all text in top_text, leave bottom_text empty string.
For 3-4 box templates: use extra_texts array for additional boxes.
"""

    print("   Asking Gemini to write the meme...")
    raw = ask_gemini(prompt)

    # Strip markdown fences if Gemini adds them
    clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()

    try:
        meme = json.loads(clean)
    except json.JSONDecodeError as e:
        print(f"Failed to parse Gemini response as JSON: {e}")
        print("Raw response:", raw)
        sys.exit(1)

    if meme.get("template_name") not in TEMPLATES:
        print(f"Unknown template '{meme.get('template_name')}', defaulting to Drake Approves")
        meme["template_name"] = "Drake Approves"

    meme["template_id"] = TEMPLATES[meme["template_name"]]["id"]
    return meme
