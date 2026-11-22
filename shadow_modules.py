#!/usr/bin/env python3
"""
RAJA SHADOW - Additional Modules

Small local-first helpers for research notes, URL monitoring, automation,
and quizzes. Network access happens only when a caller explicitly invokes
a research or monitoring method.
"""

import hashlib
import ipaddress
import json
import socket
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlsplit

import requests


def _validate_public_http_url(url: str) -> str:
    """Accept only HTTP(S) URLs whose host resolves exclusively to public IPs."""
    if not isinstance(url, str) or len(url) > 2048:
        raise ValueError("URL must be a string no longer than 2048 characters.")

    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https URLs are supported.")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("URL must have a hostname and no embedded credentials.")
    if parsed.port not in (None, 80, 443):
        raise ValueError("Only standard HTTP/HTTPS ports are allowed.")

    host = parsed.hostname.rstrip(".").lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost"):
        raise ValueError("Localhost addresses cannot be monitored.")

    try:
        addresses = {ipaddress.ip_address(host)}
    except ValueError:
        try:
            addresses = {
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))
            }
        except OSError as error:
            raise ValueError(f"Hostname could not be resolved: {error}") from error

    if not addresses or any(not address.is_global for address in addresses):
        raise ValueError("Private, local, and reserved network addresses are blocked.")

    return url


class ResearchModule:
    """Fetch a lightweight public summary and save a local research note."""

    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path) / "research"
        self.memory_path.mkdir(parents=True, exist_ok=True)

    def research_topic(self, topic: str) -> Dict[str, Any]:
        if not isinstance(topic, str) or not topic.strip() or len(topic) > 300:
            raise ValueError("Topic must contain 1 to 300 characters.")

        clean_topic = topic.strip()
        log = {
            "topic": clean_topic,
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "findings": [],
        }

        try:
            response = requests.get(
                "https://api.duckduckgo.com/",
                params={"q": clean_topic, "format": "json", "no_html": 1},
                timeout=(3, 8),
                headers={"User-Agent": "RajaShadowLocalExperiment/1.0"},
            )
            response.raise_for_status()
            data = response.json()
            if data.get("Abstract"):
                log["findings"].append({
                    "source": "DuckDuckGo Instant Answer",
                    "abstract": data["Abstract"],
                    "url": data.get("AbstractURL", ""),
                })
            else:
                log["note"] = (
                    "No instant-answer summary was returned. This is a lightweight "
                    "lookup, not comprehensive web research."
                )
        except (requests.RequestException, ValueError) as error:
            log["status"] = "incomplete"
            log["error"] = str(error)

        filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        (self.memory_path / filename).write_text(
            json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return log


class MonitoringModule:
    """Monitor explicitly supplied public URLs without following redirects."""

    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path) / "monitoring"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.watch_cache: Dict[str, str] = {}

    def monitor_url(self, url: str, check_type: str = "status") -> Dict[str, Any]:
        if check_type not in {"status", "content", "json"}:
            raise ValueError("check_type must be status, content, or json.")

        log: Dict[str, Any] = {
            "url": url,
            "check_type": check_type,
            "timestamp": datetime.now().isoformat(),
            "status": "checking",
        }

        try:
            safe_url = _validate_public_http_url(url)
            response = requests.get(
                safe_url,
                timeout=(3, 8),
                allow_redirects=False,
                stream=True,
                headers={"User-Agent": "RajaShadowLocalExperiment/1.0"},
            )
            try:
                log["http_status"] = response.status_code
                if 300 <= response.status_code < 400:
                    log["result"] = "redirect_blocked"
                elif check_type == "status":
                    log["result"] = "up" if response.status_code == 200 else "down"
                else:
                    chunks = []
                    size = 0
                    for chunk in response.iter_content(chunk_size=16384):
                        size += len(chunk)
                        if size > 1_000_000:
                            raise ValueError("Response exceeded the 1 MB monitoring limit.")
                        chunks.append(chunk)
                    body = b"".join(chunks)
                    if check_type == "content":
                        digest = hashlib.sha256(body).hexdigest()
                        previous = self.watch_cache.get(safe_url)
                        log["result"] = "changed" if previous and previous != digest else "unchanged"
                        self.watch_cache[safe_url] = digest
                    else:
                        log["data"] = json.loads(body.decode(response.encoding or "utf-8"))
                        log["result"] = "retrieved"
                log["status"] = "completed"
            finally:
                response.close()
        except (requests.RequestException, ValueError, OSError) as error:
            log["status"] = "failed"
            log["error"] = str(error)

        filename = f"monitor_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        (self.memory_path / filename).write_text(
            json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return log


class AutomationModule:
    """Run a caller-supplied Python function and record its outcome."""

    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path) / "automation"
        self.memory_path.mkdir(parents=True, exist_ok=True)

    def execute_task(self, task_name: str, task_func, *args, **kwargs) -> Dict[str, Any]:
        log: Dict[str, Any] = {
            "task": str(task_name),
            "timestamp": datetime.now().isoformat(),
            "status": "running",
        }
        try:
            log["result"] = str(task_func(*args, **kwargs))
            log["status"] = "completed"
        except Exception as error:
            log["status"] = "failed"
            log["error"] = str(error)

        filename = f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        (self.memory_path / filename).write_text(
            json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return log


class QuizModule:
    """A small local quiz bank."""

    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path) / "quizzes"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.quiz_bank = self.load_quiz_bank()

    def load_quiz_bank(self) -> List[Dict[str, str]]:
        quiz_file = self.memory_path / "quiz_bank.json"
        if quiz_file.exists():
            try:
                data = json.loads(quiz_file.read_text(encoding="utf-8"))
                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    return data
            except (OSError, json.JSONDecodeError):
                pass

        default_quizzes = [
            {
                "topic": "Law 11",
                "question": "What is a healthy version of being indispensable?",
                "answer": "Be reliable and useful without making others dependent on you.",
                "hint": "Trust grows when people remain free to choose.",
            },
            {
                "topic": "Shrine Wisdom",
                "question": "What does TUNG TUNG SAHUR mean in Shrine lore?",
                "answer": "A wake-up roar, mirrored as RUHAS GNUT GNUT.",
                "hint": "Read the chant through the mirror.",
            },
            {
                "topic": "Shrine Wisdom",
                "question": "What makes an experiment trustworthy?",
                "answer": "Clear limits, honest records, and results that can be checked.",
                "hint": "Mystery is not a substitute for evidence.",
            },
        ]
        quiz_file.write_text(json.dumps(default_quizzes, indent=2, ensure_ascii=False), encoding="utf-8")
        return default_quizzes

    def send_quiz(self, topic: str = None) -> Dict[str, Any]:
        quizzes = self.quiz_bank
        if topic:
            quizzes = [quiz for quiz in quizzes if quiz.get("topic") == topic]
        if not quizzes:
            return {}

        quiz = quizzes[0]
        log = {
            "quiz": quiz,
            "timestamp": datetime.now().isoformat(),
            "status": "ready",
        }
        filename = f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        (self.memory_path / filename).write_text(
            json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return log


def demo_modules():
    """Run only local examples; network examples are intentionally omitted."""
    memory_path = Path(".raja_shadow_memory")
    automation = AutomationModule(memory_path)
    automation.execute_task("local_example", lambda: "The Shrine is operational.")
    quiz = QuizModule(memory_path)
    quiz.send_quiz("Shrine Wisdom")
    print("Local module demonstration complete. No external services were contacted.")


if __name__ == "__main__":
    demo_modules()
