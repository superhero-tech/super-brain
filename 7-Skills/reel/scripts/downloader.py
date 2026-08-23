import os
import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional


class MediaDownloadResult:
    def __init__(
        self,
        video_path: Optional[Path],
        title: str,
        author: str,
        description: str,
        duration: Optional[int] = None,
        upload_date: Optional[str] = None,
        thumbnail_path: Optional[Path] = None,
        raw_info: Optional[Dict[str, Any]] = None
    ):
        self.video_path = video_path
        self.title = title
        self.author = author
        self.description = description
        self.duration = duration
        self.upload_date = upload_date
        self.thumbnail_path = thumbnail_path
        self.raw_info = raw_info or {}


def extract_instagram_shortcode(url: str) -> Optional[str]:
    match = re.search(r'instagram\.com/(?:reel|p|tv)/([^/?#&]+)', url)
    return match.group(1) if match else None


class MediaDownloader:
    def __init__(self, temp_dir: Optional[Path] = None):
        self.temp_dir = temp_dir or Path(tempfile.gettempdir()) / "reel_extractor"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def download(
        self,
        url: str,
        skip_video: bool = False,
        fallback_metadata: Optional[Dict[str, Any]] = None
    ) -> MediaDownloadResult:
        """
        Downloads media using Instaloader (for Instagram) or yt-dlp (for YouTube/TikTok).
        For YouTube videos (>3 min), automatically extracts full subtitles/transcripts without downloading heavy video files.
        """
        shortcode = extract_instagram_shortcode(url)

        # 1. Instagram: Instaloader direct CDN extraction
        if shortcode:
            try:
                return self._download_instagram_instaloader(shortcode, url, skip_video)
            except Exception:
                pass

        # 2. YouTube & TikTok: yt-dlp with player_client bypass
        try:
            return self._download_via_ytdlp(url, skip_video)
        except Exception as e:
            if fallback_metadata:
                return MediaDownloadResult(
                    video_path=None,
                    title=fallback_metadata.get("title") or "Media Post",
                    author=fallback_metadata.get("author") or "Unknown",
                    description=fallback_metadata.get("description") or "",
                    duration=None,
                    upload_date=fallback_metadata.get("upload_date"),
                    raw_info={"fallback": True, "error": str(e)}
                )
            raise e

    def _download_instagram_instaloader(
        self,
        shortcode: str,
        url: str,
        skip_video: bool = False
    ) -> MediaDownloadResult:
        import instaloader

        L = instaloader.Instaloader(
            quiet=True,
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        author = post.owner_username or "Unknown"
        caption = post.caption or ""
        upload_date = post.date_utc.strftime("%Y-%m-%d") if post.date_utc else None
        title = caption[:60].replace("\n", " ") + "..." if caption else f"Reel by @{author}"

        video_path = None
        if post.is_video and post.video_url and not skip_video:
            out_file = self.temp_dir / f"{shortcode}.mp4"
            headers = {"User-Agent": "Mozilla/5.0"}
            req = urllib.request.Request(post.video_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp, open(out_file, "wb") as f:
                shutil.copyfileobj(resp, f)
            if out_file.exists() and out_file.stat().st_size > 0:
                video_path = out_file

        # Download thumbnail / cover frame
        thumbnail_path = None
        thumb_url = getattr(post, "url", None)
        if thumb_url:
            try:
                t_file = self.temp_dir / f"{shortcode}_thumb.jpg"
                req_t = urllib.request.Request(thumb_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req_t, timeout=10) as resp, open(t_file, "wb") as f:
                    shutil.copyfileobj(resp, f)
                if t_file.exists() and t_file.stat().st_size > 0:
                    thumbnail_path = t_file
            except Exception:
                pass

        return MediaDownloadResult(
            video_path=video_path,
            title=title,
            author=author,
            description=caption,
            duration=None,
            upload_date=upload_date,
            thumbnail_path=thumbnail_path,
            raw_info={"is_video": post.is_video, "shortcode": shortcode}
        )

    def _download_via_ytdlp(self, url: str, skip_video: bool = False) -> MediaDownloadResult:
        import yt_dlp
        import json

        out_template = str(self.temp_dir / "%(id)s.%(ext)s")
        ydl_opts = {
            "outtmpl": out_template,
            "quiet": True,
            "no_warnings": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en.*", "en", "pl.*", "pl"],
            "subtitlesformat": "vtt/json3",
            "format": "best[ext=mp4]/best",
            "noplaylist": True,
            "extractor_args": {
                "youtube": {"player_client": ["android", "ios", "mweb"]}
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title") or "Untitled Video"
            author = info.get("uploader") or info.get("channel") or info.get("creator") or "Unknown"
            description = info.get("description") or ""
            duration = info.get("duration") or 0
            upload_date = info.get("upload_date")

            # Extract full spoken transcript from YouTube subtitles
            transcript_text = None
            subtitles = info.get("subtitles", {})
            auto_subtitles = info.get("automatic_captions", {})
            transcript_url = None

            for lang_dict in [subtitles, auto_subtitles]:
                if transcript_url:
                    break
                for lang_code in ("en", "pl", "en-orig", "en-US"):
                    if lang_code in lang_dict:
                        for fmt in lang_dict[lang_code]:
                            if fmt.get("ext") in ("json3", "vtt"):
                                transcript_url = fmt.get("url")
                                break
                    if transcript_url:
                        break

            if transcript_url:
                try:
                    req = urllib.request.Request(transcript_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        sub_data = resp.read().decode("utf-8")
                        if "events" in sub_data:
                            events = json.loads(sub_data).get("events", [])
                            text_parts = []
                            for ev in events:
                                for seg in ev.get("segs", []):
                                    text_parts.append(seg.get("utf8", ""))
                            transcript_text = "".join(text_parts).strip()
                except Exception:
                    pass

            # Download thumbnail
            thumbnail_path = None
            thumb_url = info.get("thumbnail")
            if thumb_url:
                try:
                    t_file = self.temp_dir / f"{info.get('id')}_thumb.jpg"
                    req_t = urllib.request.Request(thumb_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req_t, timeout=10) as resp, open(t_file, "wb") as f:
                        shutil.copyfileobj(resp, f)
                    if t_file.exists() and t_file.stat().st_size > 0:
                        thumbnail_path = t_file
                except Exception:
                    pass

            # Download actual video file only if short (<= 3 min) or skip_video is False and transcript absent
            video_path = None
            if not skip_video and (duration <= 180 or not transcript_text):
                info_dl = ydl.extract_info(url, download=True)
                video_filename = ydl.prepare_filename(info_dl)
                if Path(video_filename).exists():
                    video_path = Path(video_filename)
                else:
                    stem = Path(video_filename).stem
                    matches = list(self.temp_dir.glob(f"{stem}.*"))
                    if matches:
                        video_path = matches[0]

            return MediaDownloadResult(
                video_path=video_path,
                title=title,
                author=author,
                description=description,
                duration=duration,
                upload_date=upload_date,
                thumbnail_path=thumbnail_path,
                raw_info={"transcript_text": transcript_text, "info": info}
            )

    def _download_via_cli(self, url: str, skip_video: bool = False) -> MediaDownloadResult:
        if not shutil.which("yt-dlp"):
            raise RuntimeError("Nie znaleziono narzędzia pobierania wideo.")

        out_template = str(self.temp_dir / "%(id)s.%(ext)s")
        cmd = ["yt-dlp", "--dump-json", "--no-playlist", "-o", out_template]
        if not skip_video:
            cmd.extend(["-f", "best[ext=mp4]/best"])
        else:
            cmd.append("--skip-download")
        cmd.append(url)

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Błąd pobierania: {res.stderr.strip()}")

        import json
        info = json.loads(res.stdout)
        title = info.get("title") or "Untitled Reel"
        author = info.get("uploader") or info.get("channel") or "Unknown"
        description = info.get("description") or ""
        duration = info.get("duration")
        upload_date = info.get("upload_date")

        video_path = None
        if not skip_video:
            video_id = info.get("id")
            matches = list(self.temp_dir.glob(f"{video_id}.*"))
            if matches:
                video_path = matches[0]

        return MediaDownloadResult(
            video_path=video_path,
            title=title,
            author=author,
            description=description,
            duration=duration,
            upload_date=upload_date,
            raw_info=info
        )

    def cleanup(self, video_path: Optional[Path] = None):
        """Safely removes temporary video files."""
        if video_path and video_path.exists():
            try:
                video_path.unlink()
            except Exception:
                pass
