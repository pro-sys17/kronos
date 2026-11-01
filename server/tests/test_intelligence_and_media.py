"""
Test suite for KRONOS Advanced Intelligence, Media Playback & Follow-up Context Resolution.
"""

import sys
import unittest
import asyncio
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from app.core.ai_brain import AIBrain
from app.core.intent.hinglish import HinglishProcessor
from app.core.intent.classifier import IntentClassifier, IntentType


class TestIntelligenceAndMedia(unittest.TestCase):
    """Verifies media playback, website opening, and follow-up intelligence."""

    def setUp(self):
        self.brain = AIBrain()

    def tearDown(self):
        asyncio.run(self.brain.close())

    def test_spotify_media_resolution(self):
        plan = self.brain._check_media_request("spotify open karke uske dil ko krar aya song play kar")
        self.assertIsNotNone(plan)
        self.assertEqual(plan["issue_id"], "SYS-MEDIA-SPOTIFY")
        self.assertEqual(len(plan["actions"]), 1)
        self.assertIn("spotify:search:", plan["actions"][0]["command"])
        self.assertIn("dil", plan["actions"][0]["command"])

    def test_youtube_media_resolution(self):
        plan = self.brain._check_media_request("youtube pe dil ko krar aya song play kar")
        self.assertIsNotNone(plan)
        self.assertEqual(plan["issue_id"], "SYS-MEDIA-YOUTUBE")
        self.assertIn("youtube.com/results?search_query=", plan["actions"][0]["command"])

    def test_browser_url_resolution(self):
        plan = self.brain._check_media_request("chrome open krke pornhub open kar")
        self.assertIsNotNone(plan)
        self.assertEqual(plan["issue_id"], "SYS-BROWSER-URL")
        self.assertIn("chrome.exe", plan["actions"][0]["command"])
        self.assertIn("https://www.pornhub.com", plan["actions"][0]["command"])

    def test_follow_up_clone_status_check(self):
        history = [
            {"role": "user", "content": "ye le https://github.com/charlesyu108/spotify-cli.git"},
            {"role": "assistant", "content": "Spotify-cli clone kar raha hoon."}
        ]
        plan = self.brain._check_follow_up_request("hogai kya", history=history)
        self.assertIsNotNone(plan)
        self.assertEqual(plan["issue_id"], "SYS-STATUS-SPOTIFY-CLI")
        self.assertIn("spotify-cli", plan["actions"][0]["command"])
        self.assertIn("C:\\Users\\Professor\\spotify-cli", plan["summary"])

    def test_follow_up_commands_inquiry(self):
        history = [
            {"role": "user", "content": "ye le https://github.com/charlesyu108/spotify-cli.git"},
            {"role": "assistant", "content": "Spotify-cli clone kar raha hoon."}
        ]
        plan = self.brain._check_follow_up_request("add to ho gya pr ab tun cmds batao na iske", history=history)
        self.assertIsNotNone(plan)
        self.assertEqual(plan["issue_id"], "SYS-CMDS-SPOTIFY-CLI")
        self.assertIn("spotify-cli play", plan["summary"])
        self.assertIn("spotify-cli pause", plan["summary"])
        self.assertIn("spotify-cli volume", plan["summary"])

    def test_recent_entity_extraction(self):
        history = [
            {"role": "user", "content": "clone https://github.com/charlesyu108/spotify-cli.git"}
        ]
        entity = HinglishProcessor.extract_recent_entity(history)
        self.assertEqual(entity, "spotify-cli")

    def test_follow_up_intent_classification(self):
        res1 = IntentClassifier.classify("hogai kya")
        self.assertEqual(res1.intent, IntentType.FOLLOW_UP_REQUEST)

        res2 = IntentClassifier.classify("kaha he cmds")
        self.assertEqual(res2.intent, IntentType.FOLLOW_UP_REQUEST)


if __name__ == "__main__":
    unittest.main()
