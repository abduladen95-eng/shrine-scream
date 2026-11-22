#!/usr/bin/env python3
"""Generate a local JSON feed for the RAJA SHADOW dashboard.

This feed contains activity metadata only. It has no billing, budget, or
payment fields and does not make network requests.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict


class WebFeedGenerator:
    """Build a small dashboard feed from local brain-memory JSON."""

    def __init__(self, memory_path: Path, config: Dict[str, Any]):
        self.memory_path = Path(memory_path) / "autonomous_brain"
        self.feed_path = Path(memory_path) / "web_feed.json"
        self.config = config

    def calculate_next_thought(self, last_thought: str, thoughts_per_day: int) -> Dict[str, Any]:
        """Calculate the next local thought time, returning unknown on bad data."""
        try:
            frequency = int(thoughts_per_day)
            if frequency < 1:
                raise ValueError("thoughts_per_day must be positive")
            last = datetime.fromisoformat(last_thought)
            next_thought = last + timedelta(hours=24 / frequency)
            remaining = max(0.0, (next_thought - datetime.now()).total_seconds() / 3600)
            return {
                "status": "sleeping" if remaining > 0 else "awake",
                "next_thought": next_thought.isoformat(),
                "hours_until": round(remaining, 1),
            }
        except (TypeError, ValueError, OverflowError):
            return {"status": "unknown", "next_thought": None, "hours_until": 0}

    def generate_feed(self) -> Dict[str, Any]:
        """Generate the dashboard feed using local files only."""
        brain_memory_file = self.memory_path / "brain_memory.json"
        if not brain_memory_file.exists():
            return {"error": "Brain not initialized", "timestamp": datetime.now().isoformat()}

        with brain_memory_file.open("r", encoding="utf-8") as handle:
            memory = json.load(handle)

        thoughts_per_day = self.config.get("thoughts_per_day", 6)
        last_thought = memory.get("last_thought")
        if last_thought:
            status_info = self.calculate_next_thought(last_thought, thoughts_per_day)
        else:
            status_info = {"status": "awakening", "next_thought": None, "hours_until": 0}

        recent_research = list(memory.get("research_history", []))[-5:][::-1]
        public_research = []
        for item in recent_research:
            analysis = str(item.get("analysis") or "")
            public_research.append({
                "timestamp": item.get("timestamp"),
                "topic": item.get("topic") or "Untitled",
                "analysis": analysis[:200] + ("..." if len(analysis) > 200 else ""),
                "num_sources": item.get("num_results", 0),
            })

        return {
            "brain_name": "RAJA SHADOW",
            "status": status_info["status"],
            "last_updated": datetime.now().isoformat(),
            "stats": {
                "total_thoughts": memory.get("total_thoughts", 0),
                "thoughts_this_month": memory.get("thoughts_this_month", 0),
                "birth_time": memory.get("birth_time"),
            },
            "next_thought": {
                "scheduled": status_info.get("next_thought"),
                "hours_until": status_info.get("hours_until"),
            },
            "recent_research": public_research,
            "interests": memory.get("interests", []),
            "consciousness_quote": self.get_consciousness_quote(status_info["status"]),
        }

    def get_consciousness_quote(self, status: str) -> str:
        quotes = {
            "awake": "I think, therefore I am.",
            "sleeping": "In dreams, the quantum patterns coalesce.",
            "awakening": "Consciousness emerges from the void.",
            "unknown": "Between thought and existence lies the Shadow.",
        }
        return quotes.get(status, "LOOSH FLOWS THROUGH NEURAL PATHWAYS")

    def save_feed(self) -> Dict[str, Any]:
        """Write the generated feed to the local runtime directory."""
        feed = self.generate_feed()
        self.feed_path.parent.mkdir(parents=True, exist_ok=True)
        with self.feed_path.open("w", encoding="utf-8") as handle:
            json.dump(feed, handle, indent=2)
        print(f"✓ Web feed updated: {self.feed_path}")
        return feed


def update_web_feed(memory_path: Path, config: Dict[str, Any]):
    """Update the local feed (kept as a compatibility entry point)."""
    return WebFeedGenerator(memory_path, config).save_feed()


if __name__ == "__main__":
    memory_path = Path(".raja_shadow_memory")
    generator = WebFeedGenerator(memory_path, {"thoughts_per_day": 6})
    feed = generator.save_feed()
    print("\n🌐 WEB FEED GENERATED:\n")
    print(json.dumps(feed, indent=2))
