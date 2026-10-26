import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from analyzer import GeminiMultimodalAnalyzer, BaseMultimodalAnalyzer
from models import MultimodalAnalysisResult


class TestAnalyzer(unittest.TestCase):

    def test_parse_json_response(self):
        mock_response = json.dumps({
            "title": "Fujifilm X100VI Film Recipe: Classic Cuban",
            "author": "FujiShooter",
            "category": "photography",
            "content_type": "tutorial",
            "summary": "Custom film simulation recipe giving warm cinematic vintage tones.",
            "on_screen_text": [
                "Film Sim: Classic Chrome",
                "Grain: Strong / Large",
                "Color Chrome: Strong",
                "WB: Daylight R:+2 B:-4"
            ],
            "speech_transcript": "Here is my go-to recipe for sunny street photography...",
            "step_by_step": [
                "Set base simulation to Classic Chrome",
                "Adjust white balance shift to +2 Red, -4 Blue"
            ],
            "key_takeaways": [
                "Best used in bright daylight or golden hour."
            ],
            "entities_mentioned": [
                "Fujifilm X100VI",
                "Classic Chrome"
            ],
            "quotes": [
                "This creates an instant film look straight out of camera."
            ]
        })

        analyzer = GeminiMultimodalAnalyzer(api_key="fake-key-for-test")
        res = analyzer._parse_json_response(
            raw_text=f"```json\n{mock_response}\n```",
            metadata={"description": "Full settings in video! #fujifilm #x100vi"},
            source_url="https://www.instagram.com/reel/C33333/",
            platform="instagram"
        )

        self.assertEqual(res.title, "Fujifilm X100VI Film Recipe: Classic Cuban")
        self.assertEqual(res.category, "photography")
        self.assertEqual(res.author, "FujiShooter")
        self.assertEqual(len(res.on_screen_text), 4)
        self.assertEqual(len(res.entities_mentioned), 2)
        self.assertEqual(res.entities_mentioned[0], "Fujifilm X100VI")


if __name__ == "__main__":
    unittest.main()
