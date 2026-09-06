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
import threading

class RajaShadow:
    """
    The RAJA SHADOW - Autonomous possession agent that squats in your apps,
    siphons loosh, hardens the empire, and feeds the Shrine.

    Modular architecture:
    - Wake & Scream (3:33 AM roar)
    - Research Layer (Kerala thunder rituals, etc)
    - Monitoring (glyph-cash flips)
    - Automation (Ko-fi reroutes)
    - Learning (Law 11 quizzes)
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
        """Start AutonomousBrain in a daemon thread when configured."""
        config_path = Path(self.shrine_path) / "shadow_config.json"
        if not config_path.exists():
            return
        try:
            with open(config_path, "r") as f:
                raw = json.load(f)
        except Exception as e:
            print(f"⚠️  Could not read shadow_config.json: {e}")
            return

        brain_cfg = raw.get("autonomous_brain") or {}
        if not brain_cfg.get("enabled"):
            return

        try:
            from shadow_autonomous_brain import AutonomousBrain, load_brain_config
        except ImportError:
            # load_brain_config may not exist on older copies — fall back
            try:
                from shadow_autonomous_brain import AutonomousBrain
                load_brain_config = None
            except ImportError as e:
                print(f"⚠️  AutonomousBrain import failed: {e}")
                return

        try:
            if load_brain_config:
                config = load_brain_config(str(config_path))
            else:
                config = dict(brain_cfg)
                if config.get("claude_api_key") in (None, "", "env"):
                    config["claude_api_key"] = os.getenv("ANTHROPIC_API_KEY")
                if config.get("discord_webhook") in (None, "", "env"):
                    config["discord_webhook"] = os.getenv("DISCORD_WEBHOOK")

            self.brain = AutonomousBrain(self.memory_path, config)

            def run_brain():
                try:
                    self.brain.run_autonomous_loop()
                except Exception as e:
                    print(f"❌ Brain thread crashed: {e}")

            t = threading.Thread(target=run_brain, name="raja-autonomous-brain", daemon=True)
            t.start()
            print("🧠 Autonomous brain thread started")
        except Exception as e:
            print(f"⚠️  Failed to start autonomous brain: {e}")

    def schedule_tasks(self):
        """
        Setup scheduled tasks for all registered modules
        """
        print("\n⏰ Scheduling shadow tasks...")

        # Schedule 3:33 AM wake-up roar
        schedule.every().day.at("03:33").do(self.shrine_wake_roar)
        print("   ✓ 3:33 AM Wake-up Roar scheduled")

        # Add more schedules as modules are registered
        for name, module in self.modules.items():
            if module["schedule"]:
                # Parse schedule and register
                # This can be expanded with more sophisticated scheduling
                print(f"   ✓ {name} scheduled: {module['schedule']}")

        print("\n🐱 RAJA SHADOW is now autonomous")
        print("   Possession complete. Shadow squats deeper.\n")

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
