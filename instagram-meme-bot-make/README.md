# 😂 Instagram AI Meme Bot — Make.com version

Posts a daily AI-generated topical meme to Instagram using Make.com for the Instagram connection.

## How It Works

Reddit (free) → Gemini AI (free) → Imgflip (free) → Cloudinary (free) → Make.com webhook → Instagram

## Cost: $0

All services used are on free tiers.

## Setup

### Step 1 — GitHub repo
Create a private GitHub repo and upload all project files.

### Step 2 — Get a free Gemini API Key
Go to https://aistudio.google.com/app/apikey → sign in with Google → Create API Key

### Step 3 — Imgflip account
Sign up free at https://imgflip.com

### Step 4 — Cloudinary account
Sign up free at https://cloudinary.com → Dashboard → copy your Cloudinary URL

### Step 5 — Set up Make.com (this replaces all the Meta API pain)

1. Go to https://make.com → Sign up free
2. Click "Create a new scenario"
3. Click the + button to add a module → search for "Webhooks" → select "Custom webhook"
4. Click "Add" → name it "Meme Webhook" → click Save
5. Copy the webhook URL it gives you — save it!
6. Click the + to add another module after the webhook → search "Instagram for Business"
7. Connect your Instagram account when prompted (Make.com handles all the auth for you)
8. Select "Create a Photo Post"
9. Map the fields:
   - Photo URL → select "image_url" from the webhook data
   - Caption → select "caption" from the webhook data
10. Click OK → turn the scenario ON (toggle in bottom left)
11. Set the schedule to "Immediately" (it runs when triggered by webhook)

That's it! Make.com is now listening for your GitHub Action to send it a meme.

### Step 6 — Add secrets to GitHub
Repo → Settings → Secrets and variables → Actions → New repository secret

| Secret Name      | Value                          |
|------------------|-------------------------------|
| GEMINI_API_KEY   | from aistudio.google.com      |
| IMGFLIP_USERNAME | your imgflip username         |
| IMGFLIP_PASSWORD | your imgflip password         |
| CLOUDINARY_URL   | from cloudinary.com dashboard |
| MAKE_WEBHOOK_URL | the webhook URL from Step 5   |

### Step 7 — Test it
Repo → Actions tab → "Daily Meme Post" → Run workflow
If it's green, check your Instagram!

## Changing the posting time
Edit .github/workflows/daily_meme.yml:
  - cron: '0 11 * * *'   # 11:00 AM UTC
Use https://crontab.guru to pick your time.

## Project Structure
instagram-meme-bot/
├── .github/workflows/daily_meme.yml   <- GitHub Actions schedule
├── scripts/
│   ├── main.py                        <- Orchestrator
│   ├── get_trending_meme.py           <- Reddit + Gemini AI
│   ├── create_meme_image.py           <- Imgflip API
│   ├── upload_to_cloudinary.py        <- Image hosting
│   └── post_to_instagram.py           <- Sends to Make.com webhook
├── requirements.txt
└── README.md
