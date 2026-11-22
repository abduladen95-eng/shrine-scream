"""Offline tests for the local dashboard feed."""
import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta

from shadow_web_feed import WebFeedGenerator


class WebFeedGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.brain_dir = self.root / "autonomous_brain"
        self.brain_dir.mkdir()
        self.generator = WebFeedGenerator(self.root, {"thoughts_per_day": 6})

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_memory(self, payload):
        (self.brain_dir / "brain_memory.json").write_text(
            json.dumps(payload), encoding="utf-8"
        )

    def test_missing_memory_returns_clear_error(self):
        feed = self.generator.generate_feed()
        self.assertEqual(feed["error"], "Brain not initialized")

    def test_feed_contains_activity_but_no_financial_fields(self):
        self.write_memory({
            "total_thoughts": 4,
            "thoughts_this_month": 2,
            "birth_time": "2026-01-01T00:00:00",
            "last_thought": datetime.now().isoformat(),
            "research_history": [{
                "timestamp": "2026-01-01T00:00:00",
                "topic": "Mirror logic",
                "analysis": "A local note",
                "num_results": 1,
            }],
        })
        feed = self.generator.generate_feed()
        self.assertEqual(feed["stats"]["total_thoughts"], 4)
        self.assertNotIn("budget_spent", feed["stats"])
        self.assertNotIn("total_spent", feed["stats"])
        self.assertEqual(feed["recent_research"][0]["topic"], "Mirror logic")

    def test_invalid_thought_frequency_returns_unknown(self):
        result = self.generator.calculate_next_thought(
            datetime.now().isoformat(), 0
        )
        self.assertEqual(result["status"], "unknown")
        self.assertIsNone(result["next_thought"])

    def test_save_feed_creates_parent_directory(self):
        missing_root = self.root / "nested" / "memory"
        generator = WebFeedGenerator(missing_root, {"thoughts_per_day": 6})
        result = generator.save_feed()
        self.assertTrue(generator.feed_path.exists())
        self.assertEqual(result["error"], "Brain not initialized")


if __name__ == "__main__":
    unittest.main()
