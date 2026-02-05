#!/usr/bin/env python3
"""
RAJA SHADOW - Replit Deployment Entry Point

Serves the brain activity widget at / and runs the autonomous
brain loop in a background thread.

Webhook endpoints:
  POST /kofi/webhook    - Ko-fi donation webhook
  POST /patreon/webhook - Patreon membership webhook

Required environment variables (set in Replit Secrets):
  ANTHROPIC_API_KEY  - Your Anthropic API key
  DISCORD_WEBHOOK    - Discord webhook URL for notifications

Optional:
  BRAIN_BUDGET            - Monthly API budget in USD (default: 20.0)
  BRAIN_THOUGHTS_PER_DAY  - Research cycles per day (default: 6)
  KOFI_WEBHOOK_SECRET     - Ko-fi webhook secret for signature verification
  PATREON_WEBHOOK_SECRET  - Patreon webhook secret for signature verification
"""

import os
import json
import hmac
import hashlib
import threading
from pathlib import Path
from datetime import datetime

import requests
from flask import Flask, send_file, jsonify, request

app = Flask(__name__)

MEMORY_PATH = Path(".raja_shadow_memory")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def notify_discord(message: str):
    """Post a message to the configured Discord webhook."""
    if not DISCORD_WEBHOOK:
        return
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=5)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Brain widget + feed
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Ko-fi webhook
# ---------------------------------------------------------------------------

from shadow_kofi_eel import KofiEel

_kofi_eel = KofiEel(MEMORY_PATH, {
    "kofi_verification_token": os.getenv("KOFI_WEBHOOK_SECRET", ""),
    "kofi_webhook_secret": os.getenv("KOFI_WEBHOOK_SECRET", ""),
    "silent_mode": True,
    "destinations": [],
})


@app.route("/kofi/webhook", methods=["POST"])
def kofi_webhook():
    try:
        # Verify signature if secret is configured
        signature = request.headers.get("X-Kofi-Signature", "")
        raw_data = request.get_data(as_text=True)
        if not _kofi_eel.verify_webhook(raw_data, signature):
            return jsonify({"error": "Invalid signature"}), 401

        # Ko-fi sends form-encoded data with a JSON string in the 'data' field
        data = request.form.get("data", "{}")
        donation_data = json.loads(data)

        # Process + log via existing KofiEel
        result = _kofi_eel.process_donation(donation_data)

        # Discord notification
        amount = donation_data.get("amount", "?")
        currency = donation_data.get("currency", "")
        from_name = donation_data.get("from_name", "Anonymous")
        message = donation_data.get("message", "")
        notify_discord(
            f"💰 **Ko-fi donation** — {amount} {currency} from **{from_name}**"
            + (f"\n> {message}" if message else "")
        )

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/kofi/stats")
def kofi_stats():
    return jsonify(_kofi_eel.get_stats())


# ---------------------------------------------------------------------------
# Patreon webhook
# ---------------------------------------------------------------------------

PATREON_SECRET = os.getenv("PATREON_WEBHOOK_SECRET", "")


def _verify_patreon(payload: bytes, signature: str) -> bool:
    """Verify Patreon webhook HMAC-SHA256 signature."""
    if not PATREON_SECRET:
        return True
    expected = hmac.new(
        PATREON_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


@app.route("/patreon/webhook", methods=["POST"])
def patreon_webhook():
    try:
        raw_payload = request.get_data()  # bytes for HMAC
        signature = request.headers.get("X-Patreon-Signature", "")

        if not _verify_patreon(raw_payload, signature):
            return jsonify({"error": "bad signature"}), 401

        data = json.loads(raw_payload)
        event_type = data.get("event_type", "unknown")

        # Pull member name and pledge amount from Patreon's included resources
        member_name = "Anonymous"
        amount = 0
        for resource in data.get("included", []):
            attrs = resource.get("attributes", {})
            if resource.get("type") == "member":
                member_name = attrs.get("name", member_name)
            if resource.get("type") == "pledge":
                amount = attrs.get("amount_in_cents", 0) / 100

        # Log to disk
        log_dir = MEMORY_PATH / "patreon"
        log_dir.mkdir(exist_ok=True, parents=True)
        log_file = log_dir / f"patreon_{datetime.now().strftime('%Y%m%d')}.json"
        with open(log_file, "a") as f:
            f.write(json.dumps({
                "event": event_type,
                "member": member_name,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
            }) + "\n")

        # Discord notification
        emoji = {
            "member.pledge.create": "🎉",
            "member.pledge.update": "📝",
            "member.pledge.delete": "👋",
        }.get(event_type, "📌")
        notify_discord(f"{emoji} **Patreon [{event_type}]** — **{member_name}** (${amount}/mo)")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Autonomous brain (background thread)
# ---------------------------------------------------------------------------

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
