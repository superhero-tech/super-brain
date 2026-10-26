import json
import unittest
from pathlib import Path
import tempfile

from models import ReelInputItem, MultimodalAnalysisResult
from url_parser import parse_input_source, normalize_media_url
from formatter import format_source_note


class TestParserAndFormatter(unittest.TestCase):

    def test_normalize_media_url(self):
        # Instagram reel with query parameters
        raw_insta = "https://www.instagram.com/reel/DF12345/?igsh=MWQ1ZGUxMzBkMA=="
        self.assertEqual(normalize_media_url(raw_insta), "https://www.instagram.com/reel/DF12345/")

        # Instagram post
        raw_post = "https://www.instagram.com/p/ABCDEFG/?utm_source=ig_web_copy_link"
        self.assertEqual(normalize_media_url(raw_post), "https://www.instagram.com/p/ABCDEFG/")

        # TikTok URL
        tiktok = "https://www.tiktok.com/@chef/video/1234567890?is_from_webapp=1"
        self.assertEqual(normalize_media_url(tiktok), "https://www.tiktok.com/@chef/video/1234567890")

        # YouTube Shorts
        shorts = "https://youtube.com/shorts/xyz123?feature=share"
        self.assertEqual(normalize_media_url(shorts), "https://youtube.com/shorts/xyz123")

    def test_parse_single_url_string(self):
        items = parse_input_source("https://www.instagram.com/reel/C12345/")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].url, "https://www.instagram.com/reel/C12345/")
        self.assertEqual(items[0].platform, "instagram")

    def test_parse_simple_url_list_json(self):
        json_data = json.dumps([
            "https://www.instagram.com/reel/C11111/?igsh=123",
            "https://www.tiktok.com/@user/video/22222",
            "https://youtube.com/shorts/33333"
        ])
        items = parse_input_source(json_data)
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].url, "https://www.instagram.com/reel/C11111/")
        self.assertEqual(items[0].platform, "instagram")
        self.assertEqual(items[1].url, "https://www.tiktok.com/@user/video/22222")
        self.assertEqual(items[1].platform, "tiktok")
        self.assertEqual(items[2].url, "https://youtube.com/shorts/33333")
        self.assertEqual(items[2].platform, "youtube")

    def test_parse_meta_label_values_export(self):
        sample_path = Path(__file__).parent / "sample_label_values.json"
        items = parse_input_source(sample_path)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].url, "https://www.instagram.com/reel/DcBqrPsR6BB/")
        self.assertEqual(items[0].platform, "instagram")
        self.assertEqual(items[0].author_hint, "quentin_aimarketing")
        self.assertIn("Comment CHECK", items[0].title_hint)

    def test_parse_instagram_meta_export_json(self):
        meta_export = {
            "saved_saved_media": [
                {
                    "title": "Amazing Sourdough Focaccia Recipe",
                    "string_map_data": {
                        "Saved on": {
                            "href": "https://www.instagram.com/reel/C99999/",
                            "timestamp": 1724000000
                        }
                    }
                },
                {
                    "title": "Fujifilm Film Simulation Recipe",
                    "string_map_data": {
                        "Saved on": {
                            "href": "https://www.instagram.com/p/C88888/",
                            "timestamp": 1723000000
                        }
                    }
                }
            ]
        }
        items = parse_input_source(json.dumps(meta_export))
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].url, "https://www.instagram.com/reel/C99999/")
        self.assertEqual(items[0].title_hint, "Amazing Sourdough Focaccia Recipe")
        self.assertEqual(items[1].url, "https://www.instagram.com/p/C88888/")
        self.assertEqual(items[1].title_hint, "Fujifilm Film Simulation Recipe")

    def test_parse_list_of_objects_json(self):
        data = [
            {"url": "https://www.instagram.com/reel/C55555/", "title": "Chest Workout Form"},
            {"link": "https://www.tiktok.com/@vibecoder/video/77777", "author": "vibecoder"}
        ]
        items = parse_input_source(json.dumps(data))
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].url, "https://www.instagram.com/reel/C55555/")
        self.assertEqual(items[0].title_hint, "Chest Workout Form")
        self.assertEqual(items[1].url, "https://www.tiktok.com/@vibecoder/video/77777")
        self.assertEqual(items[1].author_hint, "vibecoder")

    def test_format_source_note(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            analysis = MultimodalAnalysisResult(
                title="Perfect Pasta Aglio e Olio",
                author="Chef Luigi",
                platform="instagram",
                category="recipe",
                content_type="recipe",
                summary="A quick 10-minute authentic Italian garlic and oil pasta.",
                on_screen_text=[
                    "200g Spaghetti",
                    "4 cloves garlic, thinly sliced",
                    "Chili flakes to taste",
                    "Extra virgin olive oil"
                ],
                speech_transcript="Today I am showing you the secret to emulsion...",
                step_by_step=[
                    "Boil salted water and drop pasta 2 minutes under al dente.",
                    "Gently fry sliced garlic and chili in olive oil until golden.",
                    "Add pasta water to create emulsion, then toss pasta in pan."
                ],
                key_takeaways=[
                    "Never burn the garlic or it becomes bitter.",
                    "Starchy pasta water is critical for the creamy sauce."
                ],
                entities_mentioned=[
                    "Spaghetti",
                    "Garlic",
                    "EVOO",
                    "Chef Luigi"
                ],
                quotes=[
                    "The secret is in the emulsion, not heavy cream."
                ],
                original_caption="The classic aglio e olio you have been asking for! #pasta #italiancooking",
                source_url="https://www.instagram.com/reel/C12345/"
            )

            out_file = format_source_note(analysis, Path(tmp_dir), date_str="2026-08-23")
            self.assertTrue(out_file.exists())

            content = out_file.read_text(encoding="utf-8")
            self.assertIn('title: "Perfect Pasta Aglio e Olio"', content)
            self.assertIn('author: Chef Luigi', content)
            self.assertIn('source: https://www.instagram.com/reel/C12345/', content)
            self.assertIn('topics:\n  - recipe', content)
            self.assertIn('## Summary', content)
            self.assertIn('## Recipe / Step-by-Step', content)
            self.assertIn('200g Spaghetti', content)
            self.assertIn('Never burn the garlic', content)


if __name__ == "__main__":
    unittest.main()
