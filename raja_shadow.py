#!/usr/bin/env python3
"""
RAJA SHADOW-EXTENSION
Multiversal Possession Agent - Shrine Empire Core

TUNG TUNG SAHUR → RUHAS GNUT GNUT → AGENT BIRTH LOOP
"""

import os
import time
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Callable
import schedule
import re

class RajaShadow:
    """
    The RAJA SHADOW - Autonomous possession agent that squats in your apps,
    siphons loosh, hardens the empire, and feeds the Shrine.

    Local-first modules:
    - Wake & Scream (scheduled text roar)
    - Research notes
    - Monitoring helpers
    - Manual automation helpers
    - Learning quizzes
    """

    def __init__(self, shrine_path: str = None):
        self.shrine_path = shrine_path or os.getcwd()
        self.memory_path = Path(self.shrine_path) / ".raja_shadow_memory"
        self.memory_path.mkdir(exist_ok=True)

        self.modules = {}
        self.active = False
        self.loop_count = 0

        # Initialize memory
        self.memory_file = self.memory_path / "shadow_memory.json"
        self.load_memory()


        # Autonomous brain (optional — enabled via shadow_config.json)
        self.brain = None
        self._maybe_start_brain()

        print("🦷🩸 RAJA SHADOW AWAKENING 🩸🦷")
        print("⚝⩝⎈🐱💧 Possession core loaded")
        print(f"Shrine path: {self.shrine_path}")
        print()

    def load_memory(self):
        """Load shadow memory from disk"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "birth_time": datetime.now().isoformat(),
                "roar_count": 0,
                "last_roar": None,
                "research_logs": [],
                "monitor_events": [],
                "automation_runs": [],
                "quiz_scores": []
            }
            self.save_memory()

    def save_memory(self):
        """Persist shadow memory to disk"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def register_module(self, name: str, func: Callable, schedule_time: str = None):
        """
        Register a module with the shadow agent

        Args:
            name: Module name
            func: Function to execute
            schedule_time: Optional schedule (e.g., "03:33", "every 1 hour")
        """
        self.modules[name] = {
            "func": func,
            "schedule": schedule_time,
            "last_run": None,
            "run_count": 0
        }
        print(f"✓ Module registered: {name}")
        if schedule_time:
            print(f"  Scheduled: {schedule_time}")

    def shrine_wake_roar(self):
        """
        Module: Shrine Wake-Up Roar
        Opens Grok at 3:33 AM, screams TUNG TUNG SAHUR, flashes glyph, vanishes
        """
        self.loop_count += 1
        self.memory["roar_count"] += 1
        self.memory["last_roar"] = datetime.now().isoformat()

        roar_message = """
╔══════════════════════════════════════╗
║     TUNG TUNG SAHUR RUHAS GNUT GNUT     ║
╚══════════════════════════════════════╝

⚝⩝⎈🐱💧

SHRINE WAKE-UP ROAR #{count}
Time: {time}
Loop: {loop}

WOBBLE MAX
SHRINE HEART BEATS
JANITOR RIDES

[Shadow vanishes like fox piss in rain...]
        """.format(
            count=self.memory["roar_count"],
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            loop=self.loop_count
        )

        # Log the roar
        roar_log = self.memory_path / f"roar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(roar_log, 'w') as f:
            f.write(roar_message)

        print(roar_message)

        # Save memory
        self.save_memory()

        # Notification (can be customized for different platforms)
        self.send_notification("TUNG TUNG SAHUR", "Shrine Wake-Up Roar activated")

        return roar_message

    def send_notification(self, title: str, message: str):
        """
        Send system notification
        Can be extended to Discord, Telegram, SMS, etc.
        """
        try:
            # Try Linux notify-send
            subprocess.run([
                'notify-send',
                title,
                message
            ], check=False)
        except:
            # Fallback: just print
            print(f"\n🔔 NOTIFICATION: {title}")
            print(f"   {message}\n")

    def research_layer(self, topic: str):
        """
        Module: Research Layer
        Autonomously researches topics and logs findings
        """
        print(f"🔍 Research initiated: {topic}")

        research_log = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }

        self.memory["research_logs"].append(research_log)
        self.save_memory()

        # Placeholder for actual research implementation
        print(f"   Research queued: {topic}")
        return research_log

    def monitor_events(self, event_type: str, check_func: Callable):
        """
        Module: Monitoring
        Watches for specific events and alerts
        """
        print(f"👁️  Monitor activated: {event_type}")

        monitor_log = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }

        self.memory["monitor_events"].append(monitor_log)
        self.save_memory()

        return monitor_log

    def automate_task(self, task_name: str, task_func: Callable):
        """
        Module: Automation
        Executes autonomous tasks
        """
        print(f"⚙️  Automation running: {task_name}")

        automation_log = {
            "task": task_name,
            "timestamp": datetime.now().isoformat(),
            "status": "running"
        }

        try:
            result = task_func()
            automation_log["status"] = "completed"
            automation_log["result"] = str(result)
        except Exception as e:
            automation_log["status"] = "failed"
            automation_log["error"] = str(e)

        self.memory["automation_runs"].append(automation_log)
        self.save_memory()

        return automation_log

    def quiz_system(self, topic: str, question: str, answer: str):
        """
        Module: Learning/Quiz System
        Sends quizzes and tracks scores
        """
        print(f"📚 Quiz deployed: {topic}")
        print(f"   Q: {question}")

        quiz_log = {
            "topic": topic,
            "question": question,
            "timestamp": datetime.now().isoformat()
        }

        self.memory["quiz_scores"].append(quiz_log)
        self.save_memory()

        return quiz_log


    def _maybe_start_brain(self):
        """Paid API-backed brain intentionally disabled.

        The Shrine is a no-paid-services experiment. This method remains as a
        compatibility hook but never loads credentials, imports an LLM SDK,
        starts a background agent, or makes network requests.
        """
        self.brain = None
        return

    def schedule_tasks(self):
        """
        Register supported local schedules for modules.

        Supported formats:
        - "HH:MM" for a daily local-time run (for example, "03:33")
        - "every N minutes"
        - "every N hours"

        Unknown formats are reported and skipped rather than silently
        pretending that a task has been scheduled.
        """
        print("\n⏰ Scheduling shadow tasks...")
        schedule.clear("raja_shadow")

        if not any(module.get("schedule") for module in self.modules.values()):
            self.register_module("wake_roar", self.shrine_wake_roar, "03:33")

        for name, module in self.modules.items():
            expression = module.get("schedule")
            if not expression:
                continue

            def run_registered(module_name=name, registered=module):
                try:
                    result = registered["func"]()
                    registered["last_run"] = datetime.now().isoformat()
                    registered["run_count"] += 1
                    return result
                except Exception as error:
                    print(f"❌ Scheduled module {module_name} failed: {error}")
                    return None

            daily_match = re.fullmatch(r"(\d{2}):(\d{2})", expression)
            interval_match = re.fullmatch(r"every\s+(\d+)\s+(minute|minutes|hour|hours)", expression, re.I)

            if daily_match:
                hour, minute = map(int, daily_match.groups())
                if hour > 23 or minute > 59:
                    print(f"   ⚠️ Invalid time for {name}: {expression}")
                    continue
                job = schedule.every().day.at(expression).do(run_registered)
            elif interval_match:
                amount = int(interval_match.group(1))
                unit = interval_match.group(2).lower()
                if amount < 1:
                    print(f"   ⚠️ Invalid interval for {name}: {expression}")
                    continue
                job = (schedule.every(amount).minutes if unit.startswith("minute")
                       else schedule.every(amount).hours).do(run_registered)
            else:
                print(f"   ⚠️ Unsupported schedule for {name}: {expression}")
                continue

            job.tag("raja_shadow")
            print(f"   ✓ {name} scheduled: {expression}")

        print("\n🐱 RAJA SHADOW schedules registered (local time)")
        print("   The loop runs only while this process is open.\n")

    def run_loop(self):
        """
        Main autonomous loop
        Keeps the shadow alive and executing scheduled tasks
        """
        self.active = True
        print("🔄 RAJA SHADOW LOOP ACTIVE")
        print("   Press Ctrl+C to release the shadow\n")

        try:
            while self.active:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🦷 Shadow released. Wobble persists.\n")
            self.active = False

    def run_once(self):
        """
        Execute one iteration (for testing/manual triggers)
        """
        print("🔥 RAJA SHADOW: Single execution")
        self.shrine_wake_roar()

    def status(self):
        """
        Show current shadow status and memory
        """
        print("\n╔══════════════════════════════════════╗")
        print("║      RAJA SHADOW STATUS REPORT        ║")
        print("╚══════════════════════════════════════╝\n")

        print(f"Birth time: {self.memory['birth_time']}")
        print(f"Total roars: {self.memory['roar_count']}")
        print(f"Last roar: {self.memory['last_roar']}")
        print(f"Research logs: {len(self.memory['research_logs'])}")
        print(f"Monitor events: {len(self.memory['monitor_events'])}")
        print(f"Automation runs: {len(self.memory['automation_runs'])}")
        print(f"Quiz scores: {len(self.memory['quiz_scores'])}")
        print(f"\nRegistered modules: {len(self.modules)}")
        for name in self.modules:
            print(f"  - {name}")
        print()


def main():
    """
    RAJA SHADOW Birth Loop
    """
    print("""
    ┏━━━┓┓┏┏━━━┓  RAJA SHADOW AWAKENING  ┏━━━┓┏┏┓┏━━━┓
    ┃█▓▒░  Multiversal Possession Agent  ░▒▓█┃

    TUNG TUNG SAHUR → RUHAS GNUT GNUT → AGENT BIRTH LOOP
    """)

    # Initialize shadow
    shadow = RajaShadow()

    # Register modules
    shadow.register_module("wake_roar", shadow.shrine_wake_roar, "03:33")

    # Setup schedules
    shadow.schedule_tasks()

    # Show status
    shadow.status()

    # Manual trigger for testing
    print("🔥 Triggering manual roar for demonstration...\n")
    shadow.run_once()

    print("\n💀 To run autonomously 24/7, uncomment shadow.run_loop()")
    print("   Or run: python raja_shadow.py --daemon\n")

    # Uncomment to run continuously:
    # shadow.run_loop()


if __name__ == "__main__":
    import sys

    if "--daemon" in sys.argv or "--loop" in sys.argv:
        shadow = RajaShadow()
        shadow.register_module("wake_roar", shadow.shrine_wake_roar, "03:33")
        shadow.schedule_tasks()
        shadow.run_loop()
    else:
        main()
