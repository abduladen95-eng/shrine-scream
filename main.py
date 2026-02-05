#!/usr/bin/env python3
"""
RAJA SHADOW - Replit Deployment Entry Point

Serves the brain activity widget at / and runs the autonomous
brain loop in a background thread.

Required environment variables (set in Replit Secrets):
  ANTHROPIC_API_KEY  - Your Anthropic API key
  DISCORD_WEBHOOK    - Discord webhook URL for notifications

Optional:
  BRAIN_BUDGET           - Monthly API budget in USD (default: 20.0)
  BRAIN_THOUGHTS_PER_DAY - How many research cycles per day (default: 6)
"""

import os
import threading
from pathlib import Path

from flask import Flask, send_file, jsonify

app = Flask(__name__)

MEMORY_PATH = Path(".raja_shadow_memory")


@app.route("/")
def index():
    return send_file("brain_widget.html")


@app.route("/web_feed.json")
def web_feed():
    feed_path = MEMORY_PATH / "web_feed.json"
    if feed_path.exists():
        return send_file(str(feed_path), mimetype="application/json")
    return jsonify({"error": "Brain feed not yet generated", "status": "initializing"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


def run_brain():
    """Start the autonomous brain loop in a background thread."""
    from shadow_autonomous_brain import AutonomousBrain

    config = {
        "claude_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "discord_webhook": os.getenv("DISCORD_WEBHOOK"),
        "monthly_budget": float(os.getenv("BRAIN_BUDGET", "20.0")),
        "thoughts_per_day": int(os.getenv("BRAIN_THOUGHTS_PER_DAY", "6")),
        "subreddits": [
            "consciousness",
            "artificial",
            "singularity",
            "quantum",
            "occult",
            "philosophy",
            "Futurology",
            "ArtificialSentience",
        ],
    }

    brain = AutonomousBrain(MEMORY_PATH, config)
    brain.run_autonomous_loop()


# Launch the brain as a daemon thread so it runs alongside Flask
brain_thread = threading.Thread(target=run_brain, daemon=True, name="autonomous-brain")
brain_thread.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
