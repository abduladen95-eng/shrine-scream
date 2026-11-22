"""Offline tests for the local Raja Shadow core.

Run with: python -m unittest discover -s tests -v
These tests use temporary directories and never make network requests.
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import schedule

from raja_shadow import RajaShadow


class RajaShadowTests(unittest.TestCase):
    def setUp(self):
        schedule.clear()
        self.temp_dir = tempfile.TemporaryDirectory()
        with contextlib.redirect_stdout(io.StringIO()):
            self.shadow = RajaShadow(shrine_path=self.temp_dir.name)

    def tearDown(self):
        schedule.clear()
        self.temp_dir.cleanup()

    def test_initializes_local_memory(self):
        self.assertTrue(self.shadow.memory_file.exists())
        self.assertEqual(self.shadow.memory["roar_count"], 0)
        self.assertIsNone(self.shadow.brain)

    def test_paid_brain_compatibility_hook_stays_disabled(self):
        self.shadow._maybe_start_brain()
        self.assertIsNone(self.shadow.brain)

    def test_daily_schedule_is_registered_and_runs_module(self):
        calls = []
        self.shadow.register_module("sample", lambda: calls.append("ran"), "03:33")
        with contextlib.redirect_stdout(io.StringIO()):
            self.shadow.schedule_tasks()

        jobs = schedule.get_jobs("raja_shadow")
        self.assertEqual(len(jobs), 1)
        jobs[0].job_func()
        self.assertEqual(calls, ["ran"])
        self.assertEqual(self.shadow.modules["sample"]["run_count"], 1)
        self.assertIsNotNone(self.shadow.modules["sample"]["last_run"])

    def test_interval_schedule_is_registered(self):
        self.shadow.register_module("heartbeat", lambda: None, "every 2 hours")
        with contextlib.redirect_stdout(io.StringIO()):
            self.shadow.schedule_tasks()

        jobs = schedule.get_jobs("raja_shadow")
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].interval, 2)
        self.assertEqual(jobs[0].unit, "hours")

    def test_rescheduling_replaces_previous_jobs(self):
        self.shadow.register_module("heartbeat", lambda: None, "every 5 minutes")
        with contextlib.redirect_stdout(io.StringIO()):
            self.shadow.schedule_tasks()
            self.shadow.schedule_tasks()

        self.assertEqual(len(schedule.get_jobs("raja_shadow")), 1)

    def test_invalid_schedule_is_skipped(self):
        self.shadow.register_module("bad", lambda: None, "whenever the moon sneezes")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.shadow.schedule_tasks()

        self.assertEqual(schedule.get_jobs("raja_shadow"), [])
        self.assertIn("Unsupported schedule", output.getvalue())


if __name__ == "__main__":
    unittest.main()
