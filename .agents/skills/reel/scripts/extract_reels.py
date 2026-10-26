#!/usr/bin/env python3
"""
Reel & Short Video Extractor CLI.
Processes Instagram Reels, TikToks, and YouTube Shorts into clean, structured Second Brain notes in 2-Inbox/.
"""

import argparse
import os
import sys
import warnings
from pathlib import Path
from typing import List, Optional

# Suppress urllib3 LibreSSL / deprecation warnings
warnings.filterwarnings("ignore")

from analyzer import GeminiMultimodalAnalyzer
from config import get_gemini_api_key, load_env
from downloader import MediaDownloader
from formatter import format_source_note
from models import ReelInputItem
from url_parser import parse_input_source


def detect_default_out_dir() -> Path:
    """Detects 2-Inbox in Super Brain vault or creates local inbox directory."""
    script_dir = Path(__file__).resolve().parent
    vault_root = script_dir.parents[2] if len(script_dir.parents) >= 3 else script_dir

    inbox = vault_root / "2-Inbox"
    if inbox.exists() and inbox.is_dir():
        return inbox
    
    local_inbox = Path.cwd() / "2-Inbox"
    local_inbox.mkdir(parents=True, exist_ok=True)
    return local_inbox


def process_items(
    items: List[ReelInputItem],
    out_dir: Path,
    limit: Optional[int] = None,
    offset: int = 0,
    dry_run: bool = False,
    model_name: str = "gemini-3.5-flash-lite"
) -> List[Path]:
    """Downloads media, runs multimodal analysis with Gemini, and saves formatted markdown notes."""
    total_found = len(items)

    # Apply offset and limit
    if offset > 0:
        items = items[offset:]
    if limit and limit > 0:
        items = items[:limit]

    print("=" * 65)
    print("🎬 REEL & SHORT VIDEO MULTIMODAL INGESTION")
    print("=" * 65)
    print(f"📦 Total discovered items : {total_found}")
    print(f"⏩ Processing offset       : {offset}")
    print(f"🎯 Items in this batch     : {len(items)}")
    print(f"📂 Output directory        : {out_dir.resolve()}")
    print(f"🧠 Multimodal model        : {model_name}")
    print("=" * 65 + "\n")

    if dry_run:
        print("🔍 DRY-RUN MODE (No downloads or API calls):")
        for idx, item in enumerate(items, 1):
            print(f"  [{idx}/{len(items)}] [{item.platform.upper()}] {item.url}")
            if item.title_hint:
                print(f"         Title: {item.title_hint}")
            if item.author_hint:
                print(f"         Author: @{item.author_hint}")
        print("\n✅ Dry run completed.")
        return []

    # Verify Gemini API key
    api_key = get_gemini_api_key(interactive=True)
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is required to run multimodal analysis.", file=sys.stderr)
        sys.exit(1)

    downloader = MediaDownloader()
    analyzer = GeminiMultimodalAnalyzer(api_key=api_key, model_name=model_name)
    created_notes: List[Path] = []
    skipped_items = []

    for idx, item in enumerate(items, 1):
        print(f"[{idx}/{len(items)}] ⏳ Processing: {item.url} ...")
        video_path = None
        dl_res = None

        try:
            # Prepare fallback metadata from parsed export
            caption_hint = item.raw_data.get("caption") if item.raw_data else item.title_hint
            fallback_meta = {
                "title": item.title_hint or "Social Media Post",
                "author": item.author_hint or "Unknown",
                "description": caption_hint or "",
            }

            # 1. Download metadata and video (Instaloader for Instagram, yt-dlp for YouTube/TikTok)
            engine_name = "Instaloader CDN" if item.platform == "instagram" else "yt-dlp"
            print(f"   ⬇️ Downloading metadata & media ({engine_name})...")
            dl_res = downloader.download(item.url, skip_video=False, fallback_metadata=fallback_meta)
            video_path = dl_res.video_path

            # If title/author/caption missing in dl_res, fill from input hints
            if (not dl_res.author or dl_res.author == "Unknown") and item.author_hint:
                dl_res.author = item.author_hint
            if (not dl_res.description) and caption_hint:
                dl_res.description = caption_hint

            if video_path:
                print(f"   🎥 Downloaded video file: '{dl_res.title}' by @{dl_res.author}")
            else:
                print(f"   📄 Using metadata & full post caption: '{dl_res.title[:50]}...' by @{dl_res.author}")

            # 2. Multimodal analysis via Gemini
            print(f"   🧠 Multimodal analysis with Gemini ({model_name})...")
            metadata = {
                "title": dl_res.title,
                "author": dl_res.author,
                "description": dl_res.description,
                "upload_date": dl_res.upload_date,
                "transcript_text": dl_res.raw_info.get("transcript_text") if hasattr(dl_res, "raw_info") and dl_res.raw_info else None
            }
            analysis = analyzer.analyze_video(
                video_path=video_path,
                metadata=metadata,
                source_url=item.url,
                platform=item.platform
            )

            # Check if this is actionable knowledge or filtered out
            if not analysis.is_knowledge_content:
                reason = analysis.skip_reason or "Non-knowledge or private content filtered out"
                print(f"   🚫 FILTERED OUT: {reason}")
                skipped_items.append((item.url, reason, dl_res.author))
                continue

            # 3. Format and save note
            analysis.thumbnail_path = dl_res.thumbnail_path
            note_file = format_source_note(analysis, out_dir)
            created_notes.append(note_file)
            print(f"   ✅ Saved note to 2-Inbox/: {note_file.name}")
            print(f"      🏷️ Category: {analysis.category} | Type: {analysis.content_type}")
            if analysis.on_screen_text:
                print(f"      👁️ Detected {len(analysis.on_screen_text)} on-screen OCR text lines")
            if analysis.step_by_step:
                print(f"      📝 Extracted {len(analysis.step_by_step)} protocol steps")

        except Exception as e:
            print(f"   ⚠️ Failed to process {item.url}: {e}", file=sys.stderr)
        finally:
            if video_path:
                downloader.cleanup(video_path)
        print()

    print("=" * 65)
    print("🏁 BATCH INGESTION SUMMARY")
    print("=" * 65)
    print(f"✅ Ingested notes saved to 2-Inbox/: {len(created_notes)}/{len(items)}")
    if skipped_items:
        print(f"\n🚫 Filtered out items ({len(skipped_items)}):")
        for url, reason, author in skipped_items:
            print(f"   - [@{author}] {url}\n     Reason: {reason}")

    if created_notes:
        print(f"\n📂 New source notes in: {out_dir.resolve()}")
        for n in created_notes:
            print(f"   - {n.name}")

    return created_notes


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured knowledge, guides, and insights from Instagram Reels, TikToks, and Shorts."
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="URL, path to JSON file (Meta export or list), TXT file, or raw JSON string"
    )
    parser.add_argument(
        "-i", "--input",
        dest="input_file",
        help="Alias for input source file or URL"
    )
    parser.add_argument(
        "-o", "--out-dir",
        default=None,
        help="Output directory for generated notes (default: 2-Inbox in Super Brain)"
    )
    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=None,
        help="Limit the number of videos to process"
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Offset index to start processing from (0-indexed)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse input and display item list without downloading or calling API"
    )
    parser.add_argument(
        "--model",
        default="gemini-3.5-flash-lite",
        help="Gemini model to use (default: gemini-3.5-flash-lite)"
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run the interactive onboarding & setup interview"
    )
    parser.add_argument(
        "--setup-key",
        action="store_true",
        help="Configure or update your GEMINI_API_KEY in .env"
    )

    args = parser.parse_args()

    if args.setup:
        import setup
        setup.run_onboarding()
        return

    if args.setup_key:
        get_gemini_api_key(interactive=True)
        return

    source_input = args.source or args.input_file
    if not source_input:
        parser.print_help()
        print("\nUsage examples:")
        print("  python3 extract_reels.py 'https://www.instagram.com/reel/C12345/'")
        print("  python3 extract_reels.py saved_posts.json --limit 20 --offset 15")
        print("  python3 extract_reels.py saved_posts.json --dry-run")
        sys.exit(0)

    out_dir = Path(args.out_dir) if args.out_dir else detect_default_out_dir()

    items = parse_input_source(source_input)
    if not items:
        print(f"❌ Error: No valid media URLs found in: {source_input}", file=sys.stderr)
        sys.exit(1)

    process_items(
        items=items,
        out_dir=out_dir,
        limit=args.limit,
        offset=args.offset,
        dry_run=args.dry_run,
        model_name=args.model
    )


if __name__ == "__main__":
    main()
