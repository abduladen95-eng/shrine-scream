#!/usr/bin/env python3
"""
RAJA SHADOW - Additional Modules
Research, Monitoring, Automation, Quiz Systems
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class ResearchModule:
    """
    Autonomous research layer
    Searches web, saves findings, generates reports
    """

    def __init__(self, memory_path: Path):
        self.memory_path = memory_path / "research"
        self.memory_path.mkdir(exist_ok=True)

    def research_topic(self, topic: str) -> Dict[str, Any]:
        """
        Research a topic autonomously

        Args:
            topic: Topic to research

        Returns:
            Research results dictionary
        """
        print(f"🔍 Researching: {topic}")

        research_log = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "status": "initiated",
            "findings": []
        }

        try:
            # Placeholder for actual web search implementation
            # You can integrate with DuckDuckGo, Google Search API, etc.

            print(f"   📚 Gathering data on: {topic}")
            print(f"   ⚠️  Note: Connect to web search API for real research")

            # Example: DuckDuckGo instant answer (no API key needed)
            try:
                response = requests.get(
                    f"https://api.duckduckgo.com/?q={topic}&format=json",
                    timeout=10
                )
                data = response.json()

                if data.get("Abstract"):
                    finding = {
                        "source": "DuckDuckGo",
                        "abstract": data["Abstract"],
                        "url": data.get("AbstractURL", "")
                    }
                    research_log["findings"].append(finding)
                    print(f"   ✓ Found: {data['Abstract'][:100]}...")

            except Exception as e:
                print(f"   ⚠️  Search error: {e}")

            research_log["status"] = "completed"

            # Save research log
            log_file = self.memory_path / f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w') as f:
                json.dump(research_log, f, indent=2)

            print(f"   💾 Research saved: {log_file.name}")

        except Exception as e:
            research_log["status"] = "failed"
            research_log["error"] = str(e)
            print(f"   ❌ Research failed: {e}")

        return research_log


class MonitoringModule:
    """
    Monitors URLs, APIs, data sources for changes/events
    """

    def __init__(self, memory_path: Path):
        self.memory_path = memory_path / "monitoring"
        self.memory_path.mkdir(exist_ok=True)
        self.watch_cache = {}

    def monitor_url(self, url: str, check_type: str = "status") -> Dict[str, Any]:
        """
        Monitor a URL for changes

        Args:
            url: URL to monitor
            check_type: Type of check (status, content, json)

        Returns:
            Monitoring result
        """
        print(f"👁️  Monitoring: {url}")

        monitor_log = {
            "url": url,
            "check_type": check_type,
            "timestamp": datetime.now().isoformat(),
            "status": "checking"
        }

        try:
            response = requests.get(url, timeout=10)
            monitor_log["http_status"] = response.status_code

            if check_type == "status":
                monitor_log["result"] = "up" if response.status_code == 200 else "down"
                print(f"   ✓ Status: {response.status_code}")

            elif check_type == "content":
                content_hash = hash(response.text)
                cached_hash = self.watch_cache.get(url)

                if cached_hash and cached_hash != content_hash:
                    monitor_log["result"] = "changed"
                    print(f"   🔔 Content changed!")
                else:
                    monitor_log["result"] = "unchanged"
                    print(f"   ✓ No changes detected")

                self.watch_cache[url] = content_hash

            elif check_type == "json":
                data = response.json()
                monitor_log["data"] = data
                print(f"   ✓ JSON data retrieved")

            monitor_log["status"] = "completed"

        except Exception as e:
            monitor_log["status"] = "failed"
            monitor_log["error"] = str(e)
            print(f"   ❌ Monitor failed: {e}")

        # Save monitor log
        log_file = self.memory_path / f"monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(monitor_log, f, indent=2)

        return monitor_log


class AutomationModule:
    """
    Executes autonomous tasks/scripts
    """

    def __init__(self, memory_path: Path):
        self.memory_path = memory_path / "automation"
        self.memory_path.mkdir(exist_ok=True)

    def execute_task(self, task_name: str, task_func, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute an autonomous task

        Args:
            task_name: Name of the task
            task_func: Function to execute
            *args, **kwargs: Arguments for the function

        Returns:
            Automation result
        """
        print(f"⚙️  Executing: {task_name}")

        automation_log = {
            "task": task_name,
            "timestamp": datetime.now().isoformat(),
            "status": "running"
        }

        try:
            result = task_func(*args, **kwargs)
            automation_log["status"] = "completed"
            automation_log["result"] = str(result)
            print(f"   ✓ Task completed")

        except Exception as e:
            automation_log["status"] = "failed"
            automation_log["error"] = str(e)
            print(f"   ❌ Task failed: {e}")

        # Save automation log
        log_file = self.memory_path / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(automation_log, f, indent=2)

        return automation_log


class QuizModule:
    """
    Learning/quiz system with scoring
    """

    def __init__(self, memory_path: Path):
        self.memory_path = memory_path / "quizzes"
        self.memory_path.mkdir(exist_ok=True)
        self.quiz_bank = self.load_quiz_bank()

    def load_quiz_bank(self) -> List[Dict[str, str]]:
        """Load quiz questions from file"""
        quiz_file = self.memory_path / "quiz_bank.json"

        if quiz_file.exists():
            with open(quiz_file, 'r') as f:
                return json.load(f)
        else:
            # Default Law 11 questions
            default_quizzes = [
                {
                    "topic": "Law 11",
                    "question": "What is Law 11 about?",
                    "answer": "Learn to keep people dependent on you",
                    "hint": "Keep them needing you"
                },
                {
                    "topic": "Law 11",
                    "question": "How do you maintain dependence?",
                    "answer": "Make yourself indispensable",
                    "hint": "They can't survive without you"
                },
                {
                    "topic": "Shrine Wisdom",
                    "question": "What does TUNG TUNG SAHUR mean?",
                    "answer": "Wake-up roar, reversed Ruhas",
                    "hint": "Mirror reflection of the chant"
                }
            ]

            with open(quiz_file, 'w') as f:
                json.dump(default_quizzes, f, indent=2)

            return default_quizzes

    def send_quiz(self, topic: str = None) -> Dict[str, Any]:
        """
        Send a quiz question

        Args:
            topic: Optional topic filter

        Returns:
            Quiz dictionary
        """
        print("📚 Quiz deployed")

        # Filter by topic if specified
        quizzes = self.quiz_bank
        if topic:
            quizzes = [q for q in quizzes if q.get("topic") == topic]

        if not quizzes:
            print("   ⚠️  No quizzes found for topic")
            return {}

        # Select quiz (could be random, sequential, etc.)
        quiz = quizzes[0]

        print(f"   Topic: {quiz.get('topic', 'General')}")
        print(f"   Q: {quiz['question']}")
        print(f"   Hint: {quiz.get('hint', 'No hint available')}")

        quiz_log = {
            "quiz": quiz,
            "timestamp": datetime.now().isoformat(),
            "status": "sent"
        }

        # Save quiz log
        log_file = self.memory_path / f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(quiz_log, f, indent=2)

        return quiz_log


def demo_modules():
    """
    Demonstration of all modules
    """
    print("""
    ┏━━━┓┓┏┏━━━┓  SHADOW MODULES TEST  ┏━━━┓┏┏┓┏━━━┓
    ┃█▓▒░  Research | Monitor | Automate | Quiz  ░▒▓█┃
    """)

    memory_path = Path(".raja_shadow_memory")

    # Test Research
    print("\n1. RESEARCH MODULE TEST")
    research = ResearchModule(memory_path)
    research.research_topic("Kerala thunder rituals")

    # Test Monitoring
    print("\n2. MONITORING MODULE TEST")
    monitor = MonitoringModule(memory_path)
    monitor.monitor_url("https://httpbin.org/status/200", "status")

    # Test Automation
    print("\n3. AUTOMATION MODULE TEST")
    automation = AutomationModule(memory_path)
    def example_task():
        return "Task executed successfully!"
    automation.execute_task("example_task", example_task)

    # Test Quiz
    print("\n4. QUIZ MODULE TEST")
    quiz = QuizModule(memory_path)
    quiz.send_quiz("Law 11")

    print("\n✓ All modules tested\n")


if __name__ == "__main__":
    demo_modules()
