#!/usr/bin/env python3
"""
Interactive Setup & Onboarding for Reel & Short Video Ingestion.
Configures API key, multimodal model, content filtering rules, and provides Instagram & Free Tier guides.
"""

import json
import os
import sys
from pathlib import Path

from config import (
    find_config_file,
    find_env_file,
    load_env,
    load_user_preferences,
    save_user_preferences,
)


def print_header(title: str):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def print_free_tier_guide():
    print_header("🎁 HOW TO GET A FREE GOOGLE AI STUDIO API KEY (FREE TIER)")
    print("""
Google AI Studio offers a completely free Free Tier with no credit card required:
• 15 requests per minute (RPM)
• 1,500 requests per day (RPD)
• 1,000,000 tokens per minute (TPM)
• Full multimodal video, audio, and image analysis for $0.00!

Step-by-step (takes 30 seconds):
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account (Gmail).
3. Click the blue 'Create API key' button.
4. Select 'Create API key in new project' (or select an existing project).
5. Copy the generated API key (e.g. starts with AIzaSy... or AQ...).
""")


def print_instagram_export_guide():
    print_header("📥 HOW TO EXPORT YOUR SAVED POSTS & REELS FROM INSTAGRAM")
    print("""
To export your saved bookmarks in JSON format from Instagram:

1. Open Instagram (in the mobile app or browser).
2. Go to your Profile -> Menu (three bars) -> 'Accounts Center'.
3. Select 'Your information and permissions'.
4. Click 'Download your information' -> 'Download or transfer information'.
5. Select 'Some of your information'.
6. In the list, check only: 'Saved posts and collections'.
7. In the export settings:
   - ⚠️ FORMAT: Select 'JSON' (do not select HTML!).
   - DATE RANGE: Select 'All time'.
   - MEDIA QUALITY: Low or Medium (speeds up archive preparation).
8. Click 'Create files'.
9. Meta will prepare your ZIP archive (typically takes 5–30 minutes).
10. Download the archive from the email, extract it, and pass 'your_saved_posts.json':
    python3 extract_reels.py /path/to/your_saved_posts.json
""")


def inspect_vault_context() -> list:
    """Discovers context from Super Brain if running inside vault."""
    script_dir = Path(__file__).resolve().parent
    vault_root = script_dir.parents[2] if len(script_dir.parents) >= 3 else script_dir
    discovered_topics = []

    about_file = vault_root / "8-System" / "about.md"
    if about_file.exists():
        content = about_file.read_text(encoding="utf-8")
        if "Sardinista" in content or "fish" in content.lower():
            discovered_topics.append("Sardinista & tinned fish reviews")
        if "photo" in content.lower() or "fujifilm" in content.lower():
            discovered_topics.append("Photography & camera settings")
        if "gym" in content.lower() or "fitness" in content.lower():
            discovered_topics.append("Fitness & workout techniques")
        if "cook" in content.lower() or "recipe" in content.lower():
            discovered_topics.append("Cooking & recipes")
        if "vibecod" in content.lower() or "ai" in content.lower():
            discovered_topics.append("AI & Vibecoding")

    return discovered_topics


def run_onboarding():
    print_header("🎬 REEL INGEST — INTERACTIVE ONBOARDING & SETUP")
    print("Welcome! This wizard will help you configure your knowledge preferences,")
    print("content filtering rules, Gemini multimodal model, and free API key.\n")

    # 1. Instagram Export Guide
    show_guide = input("Would you like to view the Instagram data export guide? (Y/n): ").strip().lower()
    if show_guide != "n":
        print_instagram_export_guide()
        input("Press Enter to continue setup...")

    # 2. Topic Preferences and Filtering Criteria
    print_header("🎯 STEP 1: TOPIC FOCUS & CONTENT FILTERING RULES")
    print("Your Second Brain should store only high-signal, actionable knowledge.")
    print("Let's define which topics to ingest into 2-Inbox/ and which to filter out.\n")

    vault_topics = inspect_vault_context()
    if vault_topics:
        print("💡 Discovered focus areas from your Second Brain profile:")
        for vt in vault_topics:
            print(f"   • {vt}")
        print()

    prefs = load_user_preferences()

    print("Default accepted knowledge categories:")
    for idx, top in enumerate(prefs.get("accepted_topics", []), 1):
        print(f"  [{idx}] {top}")

    custom_add = input("\nEnter additional topics you care about (comma-separated, or press Enter to skip): ").strip()
    if custom_add:
        added = [t.strip() for t in custom_add.split(",") if t.strip()]
        prefs["accepted_topics"].extend(added)

    print("\nDefault REJECTED categories (filtered out as private / non-knowledge):")
    for idx, rej in enumerate(prefs.get("rejected_topics", []), 1):
        print(f"  [-] {rej}")

    custom_rej = input("\nEnter additional categories to strictly reject (e.g. memes, politics, fashion ads, or press Enter): ").strip()
    if custom_rej:
        rejs = [r.strip() for r in custom_rej.split(",") if r.strip()]
        prefs["rejected_topics"].extend(rejs)

    save_user_preferences(prefs)
    print(f"\n✅ Saved filtering preferences to: {find_config_file().name}")

    # 3. Multimodal Model Selection
    print_header("🧠 STEP 2: SELECT GEMINI MULTIMODAL MODEL")
    print("Choose the model for simultaneous video, on-screen OCR, and audio analysis:\n")
    print("  [1] gemini-3.5-flash-lite  (RECOMMENDED / Lowest cost - fractions of a cent, ideal for video)")
    print("  [2] gemini-3.6-flash       (Mid-tier - fast, high reasoning capability)")
    print("  [3] gemini-3.7-flash       (Latest Flash model)")
    print("  [4] gemini-3.1-pro-preview (Maximum precision and advanced reasoning)")

    model_choice = input("\nSelect model number [1-4] (default: 1): ").strip()
    model_map = {
        "1": "gemini-3.5-flash-lite",
        "2": "gemini-3.6-flash",
        "3": "gemini-3.7-flash",
        "4": "gemini-3.1-pro-preview"
    }
    selected_model = model_map.get(model_choice, "gemini-3.5-flash-lite")
    print(f"Selected model: {selected_model}")

    # 4. Gemini API Key & Free Tier Guide
    print_header("🔑 STEP 3: GEMINI API KEY SETUP")
    load_env()
    current_key = os.environ.get("GEMINI_API_KEY", "")

    if current_key:
        masked = current_key[:6] + "..." + current_key[-4:]
        print(f"Detected existing API key: {masked}")
        change_key = input("Would you like to change it or view the Free Tier guide? (y/N): ").strip().lower()
        if change_key == "y":
            current_key = ""

    if not current_key:
        print_free_tier_guide()
        current_key = input("Paste your GEMINI_API_KEY: ").strip()

    # Save to .env
    env_file = find_env_file()
    env_lines = []
    if env_file.exists():
        env_lines = env_file.read_text(encoding="utf-8").splitlines()

    new_lines = []
    has_key = False
    has_model = False
    for line in env_lines:
        if line.strip().startswith("GEMINI_API_KEY="):
            new_lines.append(f"GEMINI_API_KEY={current_key}")
            has_key = True
        elif line.strip().startswith("GEMINI_MODEL="):
            new_lines.append(f"GEMINI_MODEL={selected_model}")
            has_model = True
        else:
            new_lines.append(line)
    if not has_key:
        new_lines.append(f"GEMINI_API_KEY={current_key}")
    if not has_model:
        new_lines.append(f"GEMINI_MODEL={selected_model}")

    env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    os.environ["GEMINI_API_KEY"] = current_key
    os.environ["GEMINI_MODEL"] = selected_model

    # 5. Connection Test
    print_header("✨ STEP 4: VERIFY CONNECTION")
    print("Testing connection with Gemini API...")
    try:
        from google import genai
        client = genai.Client(api_key=current_key)
        res = client.models.generate_content(
            model=selected_model,
            contents="Respond with one word: Ready!"
        )
        print(f"✅ Connection to {selected_model} verified successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Connection test returned: {e}")

    print_header("🚀 SETUP COMPLETED SUCCESSFULLY!")
    print("You can now process videos in two ways:")
    print("  1. In chat with agent: /reel path/to/file.json")
    print("  2. In CLI terminal: python3 extract_reels.py path/to/file.json --limit 10\n")


if __name__ == "__main__":
    run_onboarding()
