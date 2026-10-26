import json
import re
from pathlib import Path
from typing import Any, Dict, List, Union
from urllib.parse import urlparse, urlunparse

from models import ReelInputItem


def detect_platform(url: str) -> str:
    lower_url = url.lower()
    if "instagram.com" in lower_url:
        return "instagram"
    elif "tiktok.com" in lower_url:
        return "tiktok"
    elif "youtube.com" in lower_url or "youtu.be" in lower_url:
        return "youtube"
    return "other"


def normalize_media_url(url: str) -> str:
    """Cleans tracking query parameters and normalizes media URLs."""
    url = url.strip()
    if not url:
        return ""

    parsed = urlparse(url)
    platform = detect_platform(url)

    # Clean tracking query parameters
    clean_path = parsed.path
    if platform == "instagram":
        # Keep path like /reel/CODE/ or /p/CODE/
        if not clean_path.endswith("/"):
            clean_path += "/"
        return f"{parsed.scheme}://{parsed.netloc}{clean_path}"
    elif platform == "tiktok":
        return f"{parsed.scheme}://{parsed.netloc}{clean_path}"
    elif platform == "youtube":
        if "/shorts/" in clean_path:
            return f"{parsed.scheme}://{parsed.netloc}{clean_path}"
        # For standard youtube videos keep ?v=...
        query = parsed.query
        v_param = re.search(r'(?:^|&)v=([^&]+)', query)
        if v_param:
            return f"{parsed.scheme}://{parsed.netloc}/watch?v={v_param.group(1)}"
        return f"{parsed.scheme}://{parsed.netloc}{clean_path}"
    
    # Generic fallback: strip query params if common trackers
    return f"{parsed.scheme}://{parsed.netloc}{clean_path}"


def parse_input_source(source: Union[str, Path, List[Any], Dict[str, Any]]) -> List[ReelInputItem]:
    """
    Parses various input formats:
    - Path to a JSON or TXT file
    - Raw JSON string
    - Python list of URLs or dicts
    - Python dict (Instagram export or collection)
    - Single URL string or multi-line string
    """
    raw_data = None

    # Check if source is a file path
    if isinstance(source, (Path, str)):
        str_source = str(source).strip()
        path_candidate = Path(str_source)
        if path_candidate.exists() and path_candidate.is_file():
            text_content = path_candidate.read_text(encoding="utf-8")
            try:
                raw_data = json.loads(text_content)
            except json.JSONDecodeError:
                # Treat as line-separated plain text
                lines = [line.strip() for line in text_content.splitlines() if line.strip()]
                raw_data = lines
        elif str_source.startswith("{") or str_source.startswith("["):
            try:
                raw_data = json.loads(str_source)
            except json.JSONDecodeError:
                raw_data = str_source
        else:
            raw_data = str_source
    else:
        raw_data = source

    items: List[ReelInputItem] = []
    seen_urls = set()

    def add_item(url: str, title_hint: str = None, author_hint: str = None, timestamp: int = None, raw: dict = None):
        norm_url = normalize_media_url(url)
        if norm_url and norm_url not in seen_urls:
            seen_urls.add(norm_url)
            items.append(ReelInputItem(
                url=norm_url,
                platform=detect_platform(norm_url),
                title_hint=title_hint,
                author_hint=author_hint,
                saved_timestamp=timestamp,
                raw_data=raw
            ))

    if isinstance(raw_data, dict):
        # 1. Instagram Meta export: {"saved_saved_media": [...]}
        if "saved_saved_media" in raw_data:
            for entry in raw_data["saved_saved_media"]:
                title = entry.get("title")
                smd = entry.get("string_map_data", {})
                saved_on = smd.get("Saved on", {})
                href = saved_on.get("href")
                timestamp = saved_on.get("timestamp")
                if href:
                    add_item(href, title_hint=title, timestamp=timestamp, raw=entry)
        # 2. Instagram collection export: {"saved_collections": [{"title": "...", "media": [...]}]}
        elif "saved_collections" in raw_data:
            for col in raw_data["saved_collections"]:
                for entry in col.get("media", []):
                    title = entry.get("title")
                    smd = entry.get("string_map_data", {})
                    saved_on = smd.get("Saved on", {})
                    href = saved_on.get("href")
                    if href:
                        add_item(href, title_hint=title, raw=entry)
        # 3. Generic single object
        elif "url" in raw_data or "link" in raw_data or "href" in raw_data:
            u = raw_data.get("url") or raw_data.get("link") or raw_data.get("href")
            add_item(u, title_hint=raw_data.get("title"), author_hint=raw_data.get("author"), raw=raw_data)

    elif isinstance(raw_data, list):
        for entry in raw_data:
            if isinstance(entry, str):
                add_item(entry)
            elif isinstance(entry, dict):
                # Check for Meta label_values format
                if "label_values" in entry:
                    u = None
                    caption = None
                    title = None
                    author = None
                    for lv in entry.get("label_values", []):
                        lbl = lv.get("label")
                        val = lv.get("value")
                        href = lv.get("href")
                        if lbl == "Adres URL" or (href and ("instagram.com" in href or "tiktok.com" in href or "youtube.com" in href)):
                            u = href or val
                        elif lbl == "Napisy":
                            caption = val
                        elif lbl in ("Tytuł", "Title"):
                            title = val
                        
                        # Author extraction from Właściciel/Owner block
                        if lv.get("title") in ("Właściciel", "Owner", "Creator") or "dict" in lv:
                            for sub in lv.get("dict", []):
                                if isinstance(sub, dict) and "dict" in sub:
                                    for leaf in sub.get("dict", []):
                                        if leaf.get("label") in ("Nazwa użytkownika", "Username", "Nazwa", "Name"):
                                            author = leaf.get("value")
                                elif isinstance(sub, dict) and sub.get("label") in ("Nazwa użytkownika", "Username", "Nazwa", "Name"):
                                    author = sub.get("value")

                    if u:
                        add_item(
                            u,
                            title_hint=title or (caption[:60] + "..." if caption else None),
                            author_hint=author,
                            timestamp=entry.get("timestamp"),
                            raw=entry
                        )
                        continue

                u = entry.get("url") or entry.get("link") or entry.get("href")
                if not u:
                    smd = entry.get("string_map_data", {})
                    saved_on = smd.get("Saved on", {})
                    u = saved_on.get("href")
                if u:
                    add_item(
                        u,
                        title_hint=entry.get("title"),
                        author_hint=entry.get("author"),
                        timestamp=entry.get("timestamp"),
                        raw=entry
                    )

    elif isinstance(raw_data, str):
        # Could be multi-line string or single URL
        for line in raw_data.splitlines():
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                add_item(line)

    return items
