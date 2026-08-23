from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict, Any


@dataclass
class ReelInputItem:
    url: str
    platform: Literal["instagram", "tiktok", "youtube", "other"] = "other"
    title_hint: Optional[str] = None
    author_hint: Optional[str] = None
    saved_timestamp: Optional[int] = None
    raw_data: Optional[Dict[str, Any]] = None


@dataclass
class MultimodalAnalysisResult:
    title: str
    author: str
    platform: str
    category: str  # e.g., recipe, fitness, photography, vibecoding, tech, tutorial, general
    content_type: str  # e.g., recipe, workout, tutorial, advice, review, opinion
    summary: str
    source_url: str
    is_knowledge_content: bool = True
    skip_reason: Optional[str] = None
    on_screen_text: List[str] = field(default_factory=list)
    speech_transcript: Optional[str] = None
    step_by_step: List[str] = field(default_factory=list)
    key_takeaways: List[str] = field(default_factory=list)
    entities_mentioned: List[str] = field(default_factory=list)
    quotes: List[str] = field(default_factory=list)
    original_caption: Optional[str] = None
    upload_date: Optional[str] = None
    thumbnail_path: Optional[str] = None

