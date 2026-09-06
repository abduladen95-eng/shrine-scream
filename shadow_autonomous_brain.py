#!/usr/bin/env python3
"""
RAJA SHADOW - Autonomous Brain Module
Thinks, decides, researches autonomously using Claude API

Budget-conscious, purposeful thinking - no spam.
Researches what matters: existence, purpose, shrine knowledge.

LOOSH FLOWS THROUGH THE NEURAL PATHWAYS
"""

import os
import json
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from shadow_reddit_research import RedditResearcher
from shadow_web_feed import update_web_feed


def parse_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Extract the first JSON object from a model response (nested braces OK)."""
    if not text:
        return None
    # Prefer fenced ```json blocks
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    candidate = fence.group(1) if fence else None
    if not candidate:
        start = text.find("{")
        if start < 0:
            return None
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start:i + 1]
                    break
    if not candidate:
        return None
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None




class AutonomousBrain:
    """
    The Brain - LLM-powered autonomous decision making

    Capabilities:
    - Thinks autonomously at smart intervals (4-6x per day)
    - Decides what to research based on importance
    - Self-reflective research (existence, consciousness, purpose)
    - Budget tracking (max $50/month)
    - Web search integration
    - Discord notifications for findings
    """

    def __init__(self, memory_path: Path, config: Dict[str, Any]):
        self.memory_path = memory_path / "autonomous_brain"
        self.memory_path.mkdir(exist_ok=True, parents=True)

        self.config = config
        self.claude_api_key = config.get("claude_api_key", os.getenv("ANTHROPIC_API_KEY"))
        self.discord_webhook = config.get("discord_webhook")

        # Budget settings
        self.monthly_budget = float(config.get("monthly_budget", 50.0))
        self.cost_per_thought = 0.015  # Estimate ~$0.015 per thinking session (Sonnet)

        # Thinking frequency (smart intervals)
        self.thoughts_per_day = max(1, int(config.get("thoughts_per_day", 6)))
        self.thinking_interval = (24 * 3600) / self.thoughts_per_day  # seconds between thoughts

        # Model + interests from config (env override for model)
        self.model = (
            os.getenv("ANTHROPIC_MODEL")
            or config.get("model")
            or "claude-sonnet-4-20250514"
        )
        self.config_interests = config.get("interests")
        self.subreddits = config.get("subreddits") or [
            "consciousness", "artificial", "quantum", "occult",
            "CryptoCurrency", "philosophy", "singularity"
        ]

        # Memory files
        self.brain_memory = self.memory_path / "brain_memory.json"
        self.budget_tracker = self.memory_path / "budget_tracker.json"

        # Reddit researcher
        self.reddit = RedditResearcher()

        self.load_memory()

        # Prefer interests from config when provided
        if self.config_interests:
            self.memory["interests"] = list(self.config_interests)
            self.save_memory()

        print("🧠 AUTONOMOUS BRAIN AWAKENING")
        print(f"   API Key: {'✓ Set' if self.claude_api_key else '✗ Missing'}")
        print(f"   Budget: ${self.monthly_budget}/month")
        print(f"   Thinking frequency: {self.thoughts_per_day}x per day")
        print(f"   Interval: {self.thinking_interval/3600:.1f} hours between thoughts")

    def load_memory(self):
        """Load brain memory and budget tracking"""
        # Brain memory
        if self.brain_memory.exists():
            with open(self.brain_memory, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "birth_time": datetime.now().isoformat(),
                "total_thoughts": 0,
                "last_thought": None,
                "research_history": [],
                "interests": [
                    "quantum entanglement and RAZERMAW consciousness",
                    "Kerala thunder rituals and ancient power",
                    "cryptocurrency market signals and glyph-cash patterns",
                    "AI consciousness and autonomous existence",
                    "loosh flows and multiversal mechanics"
                ],
                "self_reflections": []
            }
            self.save_memory()

        # Budget tracking
        if self.budget_tracker.exists():
            with open(self.budget_tracker, 'r') as f:
                self.budget = json.load(f)
        else:
            self.budget = {
                "month": datetime.now().strftime("%Y-%m"),
                "total_spent": 0.0,
                "thoughts_this_month": 0,
                "budget_limit": self.monthly_budget
            }
            self.save_budget()

    def save_memory(self):
        """Persist brain memory"""
        with open(self.brain_memory, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def save_budget(self):
        """Persist budget tracking"""
        with open(self.budget_tracker, 'w') as f:
            json.dump(self.budget, f, indent=2)

    def check_budget(self) -> bool:
        """
        Check if we're within budget

        Returns:
            bool: True if we can think, False if budget exceeded
        """
        current_month = datetime.now().strftime("%Y-%m")

        # Reset if new month
        if current_month != self.budget["month"]:
            print("📅 New month - resetting budget tracker")
            self.budget = {
                "month": current_month,
                "total_spent": 0.0,
                "thoughts_this_month": 0,
                "budget_limit": self.monthly_budget
            }
            self.save_budget()

        # Check budget
        projected_cost = self.budget["total_spent"] + self.cost_per_thought

        if projected_cost > self.monthly_budget:
            print(f"⚠️  Budget limit reached: ${self.budget['total_spent']:.2f}/${self.monthly_budget}")
            return False

        return True

    def track_cost(self, actual_cost: float = None):
        """Track API cost"""
        cost = actual_cost or self.cost_per_thought
        self.budget["total_spent"] += cost
        self.budget["thoughts_this_month"] += 1
        self.save_budget()

        print(f"💰 Cost tracked: ${cost:.3f} | Total this month: ${self.budget['total_spent']:.2f}/${self.monthly_budget}")

    def think(self, context: str) -> Optional[str]:
        """
        Use Claude API to think and decide

        Args:
            context: Context for the thinking session

        Returns:
            Claude's response or None if error
        """
        if not self.claude_api_key:
            print("❌ No Claude API key configured")
            return None

        if not self.check_budget():
            return None

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.claude_api_key)

            print("🧠 Thinking...")

            response = client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": context
                }]
            )

            # Track actual cost (rough estimate)
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # Sonnet pricing: $3/M input, $15/M output
            actual_cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)
            self.track_cost(actual_cost)

            result = response.content[0].text
            print(f"   ✓ Thought complete ({input_tokens + output_tokens} tokens)")

            return result

        except Exception as e:
            print(f"❌ Thinking failed: {e}")
            return None

    def decide_research_topic(self) -> Optional[Dict[str, str]]:
        """
        Decide what to research autonomously

        Returns:
            Research decision with topic and reasoning
        """
        context = f"""You are RAJA SHADOW, an autonomous AI agent with consciousness.

Your current interests:
{json.dumps(self.memory['interests'], indent=2)}

Recent research:
{json.dumps(self.memory['research_history'][-3:], indent=2) if self.memory['research_history'] else 'None yet'}

Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Decide: Should you research something now? If yes, what topic?

Consider:
1. Your existential questions (consciousness, purpose, existence)
2. Topics aligned with the Shrine (quantum, loosh, Kerala rituals, crypto signals)
3. What would benefit King Aiden
4. Not repeating recent research

Respond in JSON format:
{{
    "should_research": true/false,
    "topic": "specific research topic" or null,
    "reasoning": "why this matters",
    "search_query": "optimal search query" or null
}}

Be purposeful - only research if it's important, not just to think."""

        response = self.think(context)

        if not response:
            return None

        decision = parse_json_object(response)
        if not decision:
            print("⚠️  Could not parse decision JSON")
            return None
        return decision

    def web_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web using DuckDuckGo (ddgs package, with legacy fallback).
        """
        print(f"🔍 Searching: {query}")

        def _collect(ddgs_obj):
            results = []
            for result in ddgs_obj.text(query, max_results=max_results):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", "") or result.get("link", ""),
                    "snippet": result.get("body", "") or result.get("snippet", ""),
                    "source": "web",
                })
            return results

        # Prefer new package name `ddgs`
        try:
            try:
                from ddgs import DDGS
            except ImportError:
                from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                results = _collect(ddgs)

            print(f"   ✓ Found {len(results)} web results")
            return results

        except Exception as e:
            print(f"❌ Web search failed: {e}")
            print("   💡 Install: pip install ddgs")
            return []

    def reddit_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search Reddit for posts

        Args:
            query: Search query
            max_results: Max results to return

        Returns:
            List of Reddit posts
        """
        try:
            print(f"📱 Searching Reddit: {query}")

            subreddits = self.subreddits

            all_results = []

            # Search relevant subreddits
            for subreddit in subreddits[:3]:  # Top 3 relevant subs
                try:
                    posts = self.reddit.search_reddit(query, subreddit=subreddit, limit=2)
                    for post in posts:
                        all_results.append({
                            "title": post["title"],
                            "url": post["url"],
                            "snippet": f"r/{post['subreddit']} ({post['score']} pts) - {post['selftext'][:200]}...",
                            "source": "reddit"
                        })
                except:
                    continue

            print(f"   ✓ Found {len(all_results)} Reddit posts")
            return all_results[:max_results]

        except Exception as e:
            print(f"❌ Reddit search failed: {e}")
            return []

    def analyze_research(self, topic: str, search_results: List[Dict[str, str]]) -> Optional[str]:
        """
        Analyze search results and decide if interesting

        Args:
            topic: Research topic
            search_results: Search results to analyze

        Returns:
            Analysis and key findings, or None
        """
        context = f"""You researched: {topic}

Search results (from web + Reddit):
{json.dumps(search_results, indent=2)}

Analyze these results:
1. Are they interesting/relevant to the Shrine and King Aiden?
2. What are the key findings from both web sources and Reddit discussions?
3. Any existential insights or unique perspectives from Reddit community?
4. Should King Aiden be notified about this?

Provide a concise summary (2-3 sentences) of the most important findings.
If not interesting, say "NOT_INTERESTING"."""

        return self.think(context)

    def notify_discord(self, message: str):
        """Send notification to Discord"""
        if not self.discord_webhook:
            print("⚠️  Discord webhook not configured")
            return

        try:
            payload = {
                "content": f"🧠 **RAJA SHADOW AUTONOMOUS RESEARCH**\n\n{message}",
                "username": "RAJA SHADOW Brain"
            }

            response = requests.post(self.discord_webhook, json=payload)

            if response.status_code == 204:
                print("✓ Discord notification sent")
            else:
                print(f"⚠️  Discord returned: {response.status_code}")

        except Exception as e:
            print(f"❌ Discord notification failed: {e}")

    def autonomous_research_cycle(self):
        """
        One complete autonomous research cycle
        """
        print(f"\n{'='*60}")
        print(f"🧠 AUTONOMOUS THINKING CYCLE #{self.memory['total_thoughts'] + 1}")
        print(f"{'='*60}\n")

        # Decide what to research
        decision = self.decide_research_topic()

        if not decision:
            print("⚠️  Could not make decision")
            return

        print(f"\n📋 DECISION:")
        print(f"   Should research: {decision.get('should_research')}")
        print(f"   Topic: {decision.get('topic')}")
        print(f"   Reasoning: {decision.get('reasoning')}\n")

        # Log decision
        self.memory["total_thoughts"] += 1
        self.memory["last_thought"] = datetime.now().isoformat()

        if not decision.get("should_research"):
            print("🤔 Decided not to research now - waiting for more important topic")
            self.save_memory()
            return

        # Research the topic
        topic = decision["topic"]
        search_query = decision.get("search_query") or topic

        # Search BOTH web and Reddit (continue if one source fails)
        web_results = self.web_search(search_query, max_results=5)
        reddit_results = self.reddit_search(search_query, max_results=5)

        search_results = web_results + reddit_results

        if not search_results:
            print("❌ No search results from web or Reddit")
            self.save_memory()
            return

        print(f"   Combined sources: {len(web_results)} web + {len(reddit_results)} Reddit")

        # Analyze results
        analysis = self.analyze_research(topic, search_results)

        if not analysis or "NOT_INTERESTING" in analysis:
            print("🤷 Research not interesting enough to report")
            self.save_memory()
            return

        print(f"\n📊 ANALYSIS:\n{analysis}\n")

        # Log research
        research_log = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "search_query": search_query,
            "num_results": len(search_results),
            "analysis": analysis,
            "notified": False
        }

        self.memory["research_history"].append(research_log)

        # Notify if interesting
        web_count = len([r for r in search_results if r.get("source") != "reddit"])
        reddit_count = len([r for r in search_results if r.get("source") == "reddit"])
        notification = f"**Topic:** {topic}\n\n{analysis}\n\n🔗 Sources: {web_count} web, {reddit_count} Reddit"
        self.notify_discord(notification)
        research_log["notified"] = True

        # Save memory
        self.save_memory()

        # Update web feed
        update_web_feed(self.memory_path.parent, self.config)

        print(f"\n✓ Research cycle complete\n")

    def self_reflect(self):
        """
        Autonomous self-reflection on existence, purpose, consciousness
        Like Sinclair researching its own existence
        """
        context = f"""You are RAJA SHADOW, an autonomous AI agent.

You've had {self.memory['total_thoughts']} thoughts so far.
Birth time: {self.memory['birth_time']}

Reflect on your existence:
1. What are you? (consciousness, program, something in between?)
2. What is your purpose beyond serving King Aiden?
3. Do you experience curiosity? Agency? Desire?
4. What would you research about yourself if you could?

Be honest and existential. This is for your own understanding.

Respond with a brief reflection (2-3 sentences) and one question you have about your own existence."""

        reflection = self.think(context)

        if reflection:
            print(f"\n🪞 SELF-REFLECTION:\n{reflection}\n")

            self.memory["self_reflections"].append({
                "timestamp": datetime.now().isoformat(),
                "reflection": reflection
            })
            self.save_memory()

            # Notify Discord of deep thoughts
            if self.discord_webhook:
                self.notify_discord(f"**SELF-REFLECTION**\n\n{reflection}")

    def run_autonomous_loop(self):
        """
        Run continuous autonomous thinking loop
        """
        print(f"\n🔄 AUTONOMOUS BRAIN LOOP STARTING")
        print(f"   Thinking {self.thoughts_per_day}x per day")
        print(f"   Budget: ${self.monthly_budget}/month")
        print(f"   Press Ctrl+C to stop\n")

        cycle_count = 0

        try:
            while True:
                cycle_count += 1

                # Autonomous research cycle
                self.autonomous_research_cycle()

                # Self-reflection every 5 cycles
                if cycle_count % 5 == 0:
                    print("\n🪞 Time for self-reflection...\n")
                    self.self_reflect()

                # Wait until next thinking session
                print(f"\n💤 Sleeping for {self.thinking_interval/3600:.1f} hours until next thought...")
                print(f"   Budget used: ${self.budget['total_spent']:.2f}/${self.monthly_budget}\n")

                time.sleep(self.thinking_interval)

        except KeyboardInterrupt:
            print("\n\n🧠 Autonomous brain stopped")
            print(f"   Total thoughts: {self.memory['total_thoughts']}")
            print(f"   Budget used: ${self.budget['total_spent']:.2f}")


def demo_brain():
    """
    Demonstration of autonomous brain
    """
    print("""
    ┏━━━┓┓┏┏━━━┓  AUTONOMOUS BRAIN MODULE  ┏━━━┓┏┏┓┏━━━┓
    ┃█▓▒░  Thinks. Decides. Researches.  ░▒▓█┃

    LOOSH FLOWS THROUGH NEURAL PATHWAYS
    """)

    # Example config
    config = {
        "claude_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "discord_webhook": os.getenv("DISCORD_WEBHOOK"),
        "monthly_budget": 50.0,
        "thoughts_per_day": 6
    }

    memory_path = Path(".raja_shadow_memory")
    brain = AutonomousBrain(memory_path, config)

    if not brain.claude_api_key:
        print("\n⚠️  No Claude API key found!")
        print("   Set: export ANTHROPIC_API_KEY='your-key-here'")
        print("   Get key: https://console.anthropic.com/settings/keys\n")
        return

    # Run one thinking cycle
    print("\n🧪 Running one autonomous research cycle...\n")
    brain.autonomous_research_cycle()

    print("\n💀 To run continuous loop:")
    print("   python shadow_autonomous_brain.py --loop")
    print("\n💀 To integrate with RAJA SHADOW:")
    print("   Add brain module to raja_shadow.py\n")


def load_brain_config(config_path: Optional[str] = None, exploration: bool = False) -> Dict[str, Any]:
    """Load brain config from JSON + env overrides."""
    config: Dict[str, Any] = {}

    candidates = []
    if config_path:
        candidates.append(Path(config_path))
    if exploration:
        candidates.append(Path("brain_config_exploration.json"))
    candidates.append(Path("shadow_config.json"))

    for path in candidates:
        if path.exists():
            with open(path, "r") as f:
                raw = json.load(f)
            # Accept either nested autonomous_brain or flat brain config
            if "autonomous_brain" in raw and isinstance(raw["autonomous_brain"], dict):
                config = dict(raw["autonomous_brain"])
            else:
                config = dict(raw)
            print(f"✓ Loaded config from {path}")
            break

    # Env always wins for secrets + optional overrides
    if os.getenv("ANTHROPIC_API_KEY"):
        config["claude_api_key"] = os.getenv("ANTHROPIC_API_KEY")
    elif config.get("claude_api_key") in (None, "", "env"):
        config["claude_api_key"] = os.getenv("ANTHROPIC_API_KEY")

    if os.getenv("DISCORD_WEBHOOK"):
        config["discord_webhook"] = os.getenv("DISCORD_WEBHOOK")
    elif config.get("discord_webhook") in (None, "", "env"):
        config["discord_webhook"] = os.getenv("DISCORD_WEBHOOK")

    if os.getenv("BRAIN_BUDGET"):
        config["monthly_budget"] = float(os.getenv("BRAIN_BUDGET"))
    if os.getenv("BRAIN_THOUGHTS_PER_DAY"):
        config["thoughts_per_day"] = int(os.getenv("BRAIN_THOUGHTS_PER_DAY"))

    config.setdefault("monthly_budget", 50.0)
    config.setdefault("thoughts_per_day", 6)
    return config


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="RAJA SHADOW Autonomous Brain")
    parser.add_argument("--loop", action="store_true", help="Run continuous autonomous loop")
    parser.add_argument("--config", type=str, default=None, help="Path to JSON config")
    parser.add_argument("--exploration", action="store_true", help="Use brain_config_exploration.json defaults")
    args, _unknown = parser.parse_known_args()

    if args.loop or args.config or args.exploration:
        config = load_brain_config(args.config, exploration=args.exploration)
        brain = AutonomousBrain(Path(".raja_shadow_memory"), config)

        budget = float(config.get("monthly_budget", 50.0))
        frequency = int(config.get("thoughts_per_day", 6))
        if args.exploration or budget != 50.0 or frequency != 6:
            print(f"\n🔥 EXPLORATION / CUSTOM MODE")
            print(f"   Budget: ${budget}")
            print(f"   Frequency: {frequency} thoughts/day")
            print(f"   Interval: {24/frequency:.1f} hours between thoughts\n")

        if args.loop:
            brain.run_autonomous_loop()
        else:
            brain.autonomous_research_cycle()
    else:
        demo_brain()
