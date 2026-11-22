# RAJA SHADOW

**A local-first Shrine experiment.**

```
TUNG TUNG SAHUR → RUHAS GNUT GNUT → WOBBLE MAX
```

RAJA SHADOW is a small Python project exploring persistent local memory, scheduled rituals, research notes, monitoring helpers, quizzes, and a playful dashboard.

## Hard boundaries

This repository is not a financial or commercial project.

- No monetization, payment processing, donations, wallets, trading, or transfers.
- No paid APIs, metered model calls, subscriptions, paid hosting, or cloud deployment.
- No automatic purchases or billing actions.
- Do not add secrets or credentials to the repository.
- Keep experiments local-first, free, reversible, and transparent.

The former payment-routing prototype and paid API-backed brain have been removed. The core agent's compatibility hook keeps the paid brain disabled.

## Install and run locally

Python 3.10+:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 raja_shadow.py
```

The normal run is a local demonstration. To run the scheduler in the current terminal:

```bash
python3 raja_shadow.py --daemon
```

Stop it with Ctrl+C. This does not deploy a service or create a cloud process.

## Architecture

- **RajaShadow**: core controller and local JSON memory.
- **Scheduler**: runs registered modules using local daily or interval schedules.
- **ResearchModule**: lightweight public summary lookup and local research logs, invoked explicitly.
- **MonitoringModule**: opt-in public URL checks with timeouts, redirect blocking, and response-size limits.
- **AutomationModule**: explicitly invoked task functions.
- **QuizModule**: local quiz bank and progress logs.
- **WebFeedGenerator**: local JSON feed for the dashboard.
- **Dashboard**: static HTML view that renders feed values as text, not executable markup.
- **Browser sandbox**: disabled by default; optional read-only page viewing with no message sending, webhook calls, or automatic package installation.

The scheduler currently supports daily `HH:MM` times and `every N minutes/hours`. It runs only while the local process remains open. Research is a limited instant-answer lookup, not comprehensive research. The browser sandbox is not a chat integration and cannot submit messages.

## Tests

Run the offline test suite:

```bash
python -m unittest discover -s tests -v
```

The tests use temporary directories and do not call external services.

## Development principles

1. Prefer local files and local computation.
2. Do not add financial features or paid services.
3. Network access must be obvious, limited, and opt-in.
4. Add tests before claiming a feature works.
5. Label simulations and placeholders honestly.
6. Back up local memory before changing its format.

The point is exploration, not extraction. The Shrine is a workshop, not a checkout page.
