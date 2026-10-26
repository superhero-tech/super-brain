import abc
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from models import MultimodalAnalysisResult


class BaseMultimodalAnalyzer(abc.ABC):
    @abc.abstractmethod
    def analyze_video(
        self,
        video_path: Optional[Path],
        metadata: Dict[str, Any],
        source_url: str,
        platform: str
    ) -> MultimodalAnalysisResult:
        pass


def build_system_prompt() -> str:
    from config import load_user_preferences
    prefs = load_user_preferences()
    accepted = "\n".join([f"  - {t}" for t in prefs.get("accepted_topics", [])])
    rejected = "\n".join([f"  - {r}" for r in prefs.get("rejected_topics", [])])

    return f"""
You are an expert multimodal intelligence agent analyzing short-form video and social media content (Instagram Reel, TikTok, YouTube Shorts, or photo posts) for a personal Second Brain knowledge base.
Your goal is to extract deep, actionable, concrete knowledge without losing any detail, or determine if the post should be filtered out based on the user's preferences.

USER KNOWLEDGE FOCUS (Accept if relevant):
{accepted}

USER REJECTION CRITERIA (Set is_knowledge_content=false if matched):
{rejected}

CRITICAL FILTER (is_knowledge_content):
- TRUE if the post contains actionable knowledge, tutorials, recipes, photography guides/settings, tech tips, workout techniques, coding advice, tools reviews, book recommendations, or meaningful concepts aligned with user focus.
- FALSE if the post is purely personal lifestyle (selfies, private vacation photos of friends/models posing, generic greetings, ads for fashion/lingerie without actionable guides, pure party/festival video clips with no substance, or matched rejection criteria).

EXHAUSTIVE EXTRACTION RULES:
1. COMPLETE ON-SCREEN TEXT (OCR): Transcribe EVERY single bullet point, checklist item, step, title, parameter, code command, or measurement visible on the video/images word-for-word. If the creator shows a 10-point or 20-point checklist or wall of text, extract ALL points individually into `on_screen_text` and `step_by_step`. Never abbreviate with "etc." or summarize away list items.
2. VERBATIM SPOKEN AUDIO: Transcribe the complete spoken voiceover / dialogue word-for-word into `speech_transcript`.
3. VISUAL ACTIONS & DEMONSTRATION: Watch what is actually being demonstrated, explained, or shown.
4. CAPTION & METADATA: Use the original caption and author description provided in the prompt as supplementary context.

Categorize the topic appropriately (e.g. 'tutorial', 'workflow', 'insight', 'technology', 'method', 'productivity', 'general').
Identify content_type: 'tutorial', 'advice', 'walkthrough', 'review', 'concept', 'opinion'.

Output MUST be a single valid JSON object with EXACTLY this structure:
{{
  "is_knowledge_content": true / false,
  "skip_reason": "Short reason for filtering out if is_knowledge_content is false, or null",
  "title": "Concise, descriptive title describing the technique / knowledge",
  "author": "Creator name or handle",
  "category": "technology | coding | photography | recipe | workout | business | general",
  "content_type": "tutorial | advice | walkthrough | review | concept | opinion",
  "summary": "2-4 sentence summary of the core knowledge.",
  "on_screen_text": ["on-screen text 1", "checklist item 2", "full point 3..."],
  "speech_transcript": "Verbatim spoken dialogue word-for-word, or null if only background music",
  "step_by_step": ["Step 1: ...", "Step 2: ...", "Point 3: ..."],
  "key_takeaways": ["Concrete tip 1", "Insight 2"],
  "entities_mentioned": ["Tool/Camera/Product 1", "Entity 2"],
  "quotes": ["Direct quote"]
}}

Be concrete and exhaustive. Never use vague filler words. Include exact parameters, numbers, steps, code commands, or tools mentioned.
"""


class GeminiMultimodalAnalyzer(BaseMultimodalAnalyzer):
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.5-flash-lite"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model_name = os.environ.get("GEMINI_MODEL", model_name)
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

    def analyze_video(
        self,
        video_path: Optional[Path],
        metadata: Dict[str, Any],
        source_url: str,
        platform: str
    ) -> MultimodalAnalysisResult:
        caption = metadata.get("description", "")
        title_hint = metadata.get("title", "")
        author_hint = metadata.get("author", "Unknown")

        # Try Google GenAI SDK (official modern SDK) first, fallback to google.generativeai
        try:
            return self._analyze_via_genai_sdk(video_path, metadata, source_url, platform)
        except ImportError:
            return self._analyze_via_legacy_sdk(video_path, metadata, source_url, platform)

    def _analyze_via_genai_sdk(
        self,
        video_path: Optional[Path],
        metadata: Dict[str, Any],
        source_url: str,
        platform: str
    ) -> MultimodalAnalysisResult:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=self.api_key)
        uploaded_file = None

        try:
            contents = []

            # 1. Upload video if available
            if video_path and video_path.exists():
                uploaded_file = client.files.upload(file=str(video_path))
                # Wait for video processing
                while uploaded_file.state.name == "PROCESSING":
                    time.sleep(2)
                    uploaded_file = client.files.get(name=uploaded_file.name)
                
                if uploaded_file.state.name == "FAILED":
                    raise RuntimeError(f"Gemini File API failed to process video: {uploaded_file.error}")
                
                contents.append(uploaded_file)

            # 2. Add text prompt and metadata
            system_prompt = build_system_prompt()
            transcript_context = ""
            if metadata.get("transcript_text"):
                transcript_context = f"\nFull Video Subtitles / Spoken Transcript:\n{metadata.get('transcript_text')}\n"

            prompt_text = (
                f"{system_prompt}\n\n"
                f"--- CONTEXT ---\n"
                f"Source URL: {source_url}\n"
                f"Platform: {platform}\n"
                f"Title Hint: {metadata.get('title')}\n"
                f"Creator Hint: {metadata.get('author')}\n"
                f"Original Post Caption:\n{metadata.get('description', '')}\n"
                f"{transcript_context}"
            )
            contents.append(prompt_text)

            # 3. Call Gemini
            response = client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )

            raw_json = response.text
            return self._parse_json_response(raw_json, metadata, source_url, platform)

        finally:
            if uploaded_file:
                try:
                    client.files.delete(name=uploaded_file.name)
                except Exception:
                    pass

    def _analyze_via_legacy_sdk(
        self,
        video_path: Optional[Path],
        metadata: Dict[str, Any],
        source_url: str,
        platform: str
    ) -> MultimodalAnalysisResult:
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        uploaded_file = None

        try:
            contents = []

            if video_path and video_path.exists():
                uploaded_file = genai.upload_file(path=str(video_path))
                while uploaded_file.state.name == "PROCESSING":
                    time.sleep(2)
                    uploaded_file = genai.get_file(uploaded_file.name)

                if uploaded_file.state.name == "FAILED":
                    raise RuntimeError("Gemini File API failed to process video.")

                contents.append(uploaded_file)

            system_prompt = build_system_prompt()
            prompt_text = (
                f"{system_prompt}\n\n"
                f"--- CONTEXT ---\n"
                f"Source URL: {source_url}\n"
                f"Platform: {platform}\n"
                f"Title Hint: {metadata.get('title')}\n"
                f"Creator Hint: {metadata.get('author')}\n"
                f"Original Post Caption:\n{metadata.get('description', '')}\n"
            )
            contents.append(prompt_text)

            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={"response_mime_type": "application/json", "temperature": 0.2}
            )
            response = model.generate_content(contents)
            return self._parse_json_response(response.text, metadata, source_url, platform)

        finally:
            if uploaded_file:
                try:
                    genai.delete_file(uploaded_file.name)
                except Exception:
                    pass

    def _parse_json_response(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        source_url: str,
        platform: str
    ) -> MultimodalAnalysisResult:
        # Strip markdown code blocks if wrapped
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback regex extraction of json
            match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                raise ValueError(f"Could not parse Gemini JSON response: {raw_text[:200]}")

        return MultimodalAnalysisResult(
            title=data.get("title") or metadata.get("title") or "Untitled Reel",
            author=data.get("author") or metadata.get("author") or "Unknown",
            platform=platform,
            category=data.get("category", "general"),
            content_type=data.get("content_type", "tutorial"),
            summary=data.get("summary", ""),
            source_url=source_url,
            is_knowledge_content=data.get("is_knowledge_content", True),
            skip_reason=data.get("skip_reason"),
            on_screen_text=data.get("on_screen_text") or [],
            speech_transcript=data.get("speech_transcript"),
            step_by_step=data.get("step_by_step") or [],
            key_takeaways=data.get("key_takeaways") or [],
            entities_mentioned=data.get("entities_mentioned") or [],
            quotes=data.get("quotes") or [],
            original_caption=metadata.get("description"),
            upload_date=metadata.get("upload_date")
        )
