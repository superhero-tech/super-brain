import datetime
import re
from pathlib import Path
from typing import Optional

from models import MultimodalAnalysisResult


def slugify(text: str) -> str:
    """Generates a clean file-system-safe slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text[:50] if text else "reel"


def format_source_note(
    analysis: MultimodalAnalysisResult,
    output_dir: Path,
    date_str: Optional[str] = None
) -> Path:
    """
    Formats the analysis result into a clean markdown source note
    following Super Brain vault conventions.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    today = date_str or datetime.date.today().isoformat()
    slug = slugify(analysis.title)
    filename = f"{today}-reel-{slug}.md"
    target_path = output_dir / filename

    # Prevent overwriting existing file with exact same name
    counter = 1
    while target_path.exists():
        filename = f"{today}-reel-{slug}-{counter}.md"
        target_path = output_dir / filename
        counter += 1

    # Prepare topics list
    topics = [analysis.category] if analysis.category else ["general"]
    if analysis.content_type and analysis.content_type != analysis.category:
        topics.append(analysis.content_type)

    clean_title = analysis.title.replace('"', '\\"')
    yaml_lines = [
        "---",
        f"date: {today}",
        f'title: "{clean_title}"',
        f"author: {analysis.author or 'Unknown'}",
        f"source: {analysis.source_url}",
        "topics:"
    ]
    for t in topics:
        yaml_lines.append(f"  - {t}")
    yaml_lines.extend([
        f"source_type: {analysis.platform if analysis.platform != 'other' else 'reel'}",
        f"content_type: {analysis.content_type or 'general'}",
        "---",
        ""
    ])

    # Handle thumbnail asset copying and embedding
    thumb_md = ""
    if analysis.thumbnail_path and Path(analysis.thumbnail_path).exists():
        try:
            import shutil
            assets_dir = output_dir / "assets"
            assets_dir.mkdir(parents=True, exist_ok=True)
            dest_thumb = assets_dir / f"{slug}.jpg"
            shutil.copy2(analysis.thumbnail_path, dest_thumb)
            thumb_md = f"![Cover Frame](assets/{slug}.jpg)\n"
        except Exception:
            pass

    body_lines = [
        f"# {analysis.title}",
        ""
    ]
    if thumb_md:
        body_lines.append(thumb_md)

    body_lines.extend([
        "## Summary",
        analysis.summary.strip() if analysis.summary else "Brak podsumowania.",
        ""
    ])

    # Step-by-step or recipe or protocol
    if analysis.step_by_step:
        section_title = "Recipe / Step-by-Step" if analysis.category == "recipe" else "Step-by-Step / Detailed Protocol"
        body_lines.append(f"## {section_title}")
        for idx, step in enumerate(analysis.step_by_step, 1):
            body_lines.append(f"{idx}. {step}")
        body_lines.append("")

    # Full Spoken Transcript
    if analysis.speech_transcript:
        body_lines.append("## Full Audio Transcript (Verbatim)")
        body_lines.append(analysis.speech_transcript.strip())
        body_lines.append("")

    # On-screen OCR text
    if analysis.on_screen_text:
        body_lines.append("## Complete On-Screen Text & OCR Checklist")
        for txt in analysis.on_screen_text:
            body_lines.append(f"- `{txt}`")
        body_lines.append("")

    # Key takeaways
    if analysis.key_takeaways:
        body_lines.append("## Key Takeaways & Practical Tips")
        for tip in analysis.key_takeaways:
            body_lines.append(f"- {tip}")
        body_lines.append("")

    # Entities
    if analysis.entities_mentioned:
        body_lines.append("## Mentioned Entities & Tools")
        for entity in analysis.entities_mentioned:
            body_lines.append(f"- **{entity}**")
        body_lines.append("")

    # Quotes
    if analysis.quotes:
        body_lines.append("## Notable Quotes")
        for q in analysis.quotes:
            body_lines.append(f"> \"{q}\"")
            body_lines.append("")

    # Source & caption
    body_lines.extend([
        "## Source & Original Caption",
        f"- **URL**: {analysis.source_url}",
        f"- **Creator**: {analysis.author}",
        f"- **Platform**: {analysis.platform.capitalize()}"
    ])
    if analysis.upload_date:
        body_lines.append(f"- **Uploaded**: {analysis.upload_date}")

    if analysis.original_caption:
        body_lines.extend([
            "",
            "### Post Caption",
            "```text",
            analysis.original_caption.strip(),
            "```"
        ])

    body_lines.append("")
    full_content = "\n".join(yaml_lines) + "\n".join(body_lines)
    target_path.write_text(full_content, encoding="utf-8")
    return target_path
