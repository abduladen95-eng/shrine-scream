"""Offline safety tests for the local Shrine helper modules."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from shadow_modules import MonitoringModule, QuizModule, _validate_public_http_url
from shadow_web_possession import WebPossession


class URLSafetyTests(unittest.TestCase):
    def test_monitor_rejects_localhost_before_network_access(self):
        with tempfile.TemporaryDirectory() as folder:
            monitor = MonitoringModule(Path(folder))
            with patch("shadow_modules.requests.get") as get:
                result = monitor.monitor_url("http://localhost/admin")
            self.assertEqual(result["status"], "failed")
            get.assert_not_called()

    def test_monitor_rejects_private_ip(self):
        with self.assertRaises(ValueError):
            _validate_public_http_url("http://127.0.0.1/")

    def test_monitor_rejects_non_http_scheme(self):
        with self.assertRaises(ValueError):
            _validate_public_http_url("file:///etc/passwd")

    def test_browser_sandbox_is_disabled_by_default(self):
        browser = WebPossession()
        self.assertFalse(browser.open_page("https://example.com"))
        self.assertIsNone(browser.driver)

    def test_browser_sandbox_rejects_local_ip(self):
        with self.assertRaises(ValueError):
            WebPossession._validate_url("https://127.0.0.1/")

    def test_browser_sandbox_rejects_non_https(self):
        with self.assertRaises(ValueError):
            WebPossession._validate_url("http://example.com/")


class QuizSafetyTests(unittest.TestCase):
    def test_default_quiz_promotes_independence_not_dependency(self):
        with tempfile.TemporaryDirectory() as folder:
            quiz = QuizModule(Path(folder))
            answers = " ".join(item.get("answer", "") for item in quiz.quiz_bank).lower()
            self.assertIn("without making others dependent", answers)


if __name__ == "__main__":
    unittest.main()
