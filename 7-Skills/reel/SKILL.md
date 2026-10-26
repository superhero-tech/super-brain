---
name: reel
description: Extracts structured knowledge and insights from saved short-form videos (Instagram Reels, TikToks, YouTube Shorts) in batch or single URLs. Uses multimodal video analysis (on-screen text OCR, speech, and visual demonstrations) to turn multimedia bookmarks into clean notes in 2-Inbox/ ready for ingest.
---

# Reel & Short Video Ingestion (`/reel`)

Extracts actionable knowledge, step-by-step guides, visual thumbnails, and structured notes from saved Instagram Reels, TikToks, and YouTube videos (from single links, URL lists, or Meta/Instagram JSON bookmark exports). Uses deep multimodal video analysis (Gemini Multimodal API + Instaloader/yt-dlp) to convert video bookmarks into clean source notes in `2-Inbox/`.

## When to use

- You have accumulated saved video bookmarks (Instagram Reels, TikToks, YouTube Shorts, or longer tutorials) and want to process them into your second brain in bulk or individually.
- The video content is heterogeneous: some have critical text hardcoded on screen (OCR) with background music, some have spoken voiceover, and some rely on visual demonstrations.
- You want visual context (embedded cover frame / thumbnail) saved into `2-Inbox/assets/` and linked directly in the markdown note.
- You want to filter out irrelevant or private posts (e.g. personal selfies, friend vacation photos, modeling/fashion ads without guides) and keep only high-signal knowledge aligned with your goals.
- You want the video turned into a structured, permanent note in `2-Inbox/` ready to be compiled into `4-Knowledge/`.

## Requirements & Free Tier Setup

The skill uses Python scripts located in `7-Skills/reel/scripts/`:

```bash
cd 7-Skills/reel/scripts
pip install -r requirements.txt
```

### 🎁 How to get a free API key in 30 seconds (Google AI Studio Free Tier):
Google AI Studio provides a completely free **Free Tier** with no credit card required:
- **15 requests per minute (RPM)**
- **1,500 requests per day (RPD)**
- **1,000,000 tokens per minute (TPM)**
- Full multimodal video, audio, and image analysis for **$0.00 / 0 PLN**!

**Setup steps:**
1. Visit [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) and sign in with your Google account.
2. Click **"Create API key"** -> select **"Create API key in new project"**.
3. Copy the generated key and run `/reel setup` (or save it to `.env` as `GEMINI_API_KEY=...`).

## How to invoke

- `/reel setup` – Runs the interactive onboarding interview (topic preferences, filter rules, model selection, API key).
- `/reel https://www.instagram.com/reel/DF.../` – Processes a single reel.
- `/reel https://www.youtube.com/watch?v=...` – Processes a YouTube video.
- `/reel saved_posts.json` – Processes a batch JSON file.
- `/reel saved_posts.json --limit 20 --offset 15` – Processes a specific batch slice.
- `/reel saved_posts.json --dry-run` – Previews items without downloading or calling the API.

---

## 📺 3-Tier Strategy for Video Processing & YouTube

To balance cost, speed, and analytical depth:

1. **Short-Form Videos (Reels, TikToks, YouTube Shorts ≤ 3 min)**:
   - **Full Multimodal Analysis**: The `.mp4` video file is downloaded and uploaded to Gemini File API. Gemini performs frame-by-frame OCR, motion tracking, demonstration analysis, and audio transcript.
   - **Cost**: ~$0.0005 USD / 0.00 in Free Tier.

2. **Long YouTube Videos (> 3 min) — Fast & Free Track (Default)**:
   - **Instant Subtitles Extraction**: `yt-dlp` extracts official/auto-generated word-for-word subtitles and chapters in 1–2 seconds without downloading hundreds of megabytes of video.
   - **Gemini Synthesis**: Gemini analyzes the complete spoken transcript (e.g. 5,000 words in a 21-min lecture) and outputs a comprehensive structured note with steps, key takeaways, and quotes.
   - **Cost**: ~$0.0004 USD / execution time: ~5–8 seconds.

3. **Long Videos with Full Frame-by-Frame Video Analysis (`--full-video`)**:
   - For complex software tutorials or visual lectures where on-screen UI/sliders are essential, downloads the full MP4.
   - Prompts with an estimated duration and token usage before proceeding.

---

## 🖼️ Thumbnails & Visual Reference Frames

Every processed reel and video automatically extracts a cover frame or thumbnail to `2-Inbox/assets/{slug}.jpg` and embeds it directly beneath the note title:
```markdown
# Note Title
![Cover Frame](assets/note-slug.jpg)
```
This provides instant visual recognition in Obsidian and Markdown viewers.

---

## 📥 How to Export Your Saved Bookmarks from Instagram

1. Open Instagram -> Profile -> Menu (three bars) -> **Accounts Center**.
2. Select **Your information and permissions** -> **Download your information** -> **Download or transfer information**.
3. Choose **Some of your information** -> check only: **Saved posts and collections**.
4. Configure export settings:
   - ⚠️ **Format**: Select **JSON** (do not select HTML!).
   - **Date range**: **All time**.
   - **Media quality**: Low or Medium (speeds up archive generation).
5. Click **Create files**.
6. When Meta emails your ZIP archive (typically 5–30 mins), download and extract it, then run:
   ```bash
   python3 7-Skills/reel/scripts/extract_reels.py /path/to/your_saved_posts.json
   ```
