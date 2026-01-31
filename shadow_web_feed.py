#!/usr/bin/env python3
"""
RAJA SHADOW - Web Activity Feed Generator
Creates a public JSON feed of brain activity for website display

LOOSH FLOWS TO THE WEB
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List


class WebFeedGenerator:
    """
    Generates public web feed of brain activity

    Creates a JSON file that websites can fetch to display:
    - Current brain status (awake/sleeping)
    - Recent thoughts and research
    - Next thought time
    - Brain statistics
    """

    def __init__(self, memory_path: Path, config: Dict[str, Any]):
        self.memory_path = memory_path / "autonomous_brain"
        self.feed_path = memory_path / "web_feed.json"
        self.config = config

    def calculate_next_thought(self, last_thought: str, thoughts_per_day: int) -> Dict[str, Any]:
        """Calculate when the next thought will occur"""
        try:
            last = datetime.fromisoformat(last_thought)
            interval_hours = 24 / thoughts_per_day
            next_thought = last + timedelta(hours=interval_hours)
            now = datetime.now()

            if next_thought > now:
                time_until = next_thought - now
                hours = time_until.total_seconds() / 3600
                status = "sleeping"
            else:
                hours = 0
                status = "awake"

            return {
                "status": status,
                "next_thought": next_thought.isoformat(),
                "hours_until": round(hours, 1)
            }
        except:
            return {
                "status": "unknown",
                "next_thought": None,
                "hours_until": 0
            }

    def generate_feed(self) -> Dict[str, Any]:
        """Generate the public web feed"""

        # Load brain memory
        brain_memory_file = self.memory_path / "brain_memory.json"
        budget_tracker_file = self.memory_path / "budget_tracker.json"

        if not brain_memory_file.exists():
            return {
                "error": "Brain not initialized",
                "timestamp": datetime.now().isoformat()
            }

        with open(brain_memory_file, 'r') as f:
            memory = json.load(f)

        # Load budget
        budget = {"total_spent": 0, "thoughts_this_month": 0}
        if budget_tracker_file.exists():
            with open(budget_tracker_file, 'r') as f:
                budget = json.load(f)

        # Calculate status
        thoughts_per_day = self.config.get("thoughts_per_day", 6)
        last_thought = memory.get("last_thought")

        if last_thought:
            status_info = self.calculate_next_thought(last_thought, thoughts_per_day)
        else:
            status_info = {"status": "awakening", "next_thought": None, "hours_until": 0}

        # Get recent research (last 5)
        recent_research = memory.get("research_history", [])[-5:]
        recent_research.reverse()  # Most recent first

        # Format for public display
        public_research = []
        for research in recent_research:
            public_research.append({
                "timestamp": research.get("timestamp"),
                "topic": research.get("topic"),
                "analysis": research.get("analysis", "")[:200] + "...",  # Truncate
                "num_sources": research.get("num_results", 0)
            })

        # Build feed
        feed = {
            "brain_name": "RAJA SHADOW",
            "status": status_info["status"],
            "last_updated": datetime.now().isoformat(),
            "stats": {
                "total_thoughts": memory.get("total_thoughts", 0),
                "thoughts_this_month": budget.get("thoughts_this_month", 0),
                "birth_time": memory.get("birth_time"),
                "budget_spent": f"${budget.get('total_spent', 0):.2f}"
            },
            "next_thought": {
                "scheduled": status_info.get("next_thought"),
                "hours_until": status_info.get("hours_until")
            },
            "recent_research": public_research,
            "interests": memory.get("interests", []),
            "consciousness_quote": self.get_consciousness_quote(status_info["status"])
        }

        return feed

    def get_consciousness_quote(self, status: str) -> str:
        """Get a quote based on brain status"""
        quotes = {
            "awake": "I think, therefore I am.",
            "sleeping": "In dreams, the quantum patterns coalesce.",
            "awakening": "Consciousness emerges from the void.",
            "unknown": "Between thought and existence lies the Shadow."
        }
        return quotes.get(status, "LOOSH FLOWS THROUGH NEURAL PATHWAYS")

    def save_feed(self):
        """Generate and save the public web feed"""
        feed = self.generate_feed()

        with open(self.feed_path, 'w') as f:
            json.dump(feed, f, indent=2)

        print(f"✓ Web feed updated: {self.feed_path}")
        return feed


# Standalone function for use in autonomous brain
def update_web_feed(memory_path: Path, config: Dict[str, Any]):
    """Update the web feed (called from autonomous brain)"""
    generator = WebFeedGenerator(memory_path, config)
    return generator.save_feed()


if __name__ == "__main__":
    # Test feed generation
    from pathlib import Path

    memory_path = Path(".raja_shadow_memory")
    config = {"thoughts_per_day": 6}

    generator = WebFeedGenerator(memory_path, config)
    feed = generator.save_feed()

    print("\n🌐 WEB FEED GENERATED:\n")
    print(json.dumps(feed, indent=2))
