# RAJA SHADOW

**A local-first Shrine experiment.**

```
TUNG TUNG SAHUR → RUHAS GNUT GNUT → WOBBLE MAX
```

RAJA SHADOW is a small Python project exploring persistent local memory, scheduling, research notes, monitoring, quizzes, and a playful dashboard.

## Hard boundaries

This repository is not about making or receiving money.

- No monetization, donations, Ko-fi, payment processing, Stripe, PayPal, crypto, wallets, trading, or transfers.
- No paid APIs, metered model calls, subscriptions, paid hosting, or cloud deployment.
- No automatic purchases or billing actions.
- Do not add secrets or credentials to the repository.
- Keep experiments local-first, free, reversible, and transparent.

The old payment-routing module and paid API-backed brain have been removed. The core agent's compatibility hook explicitly keeps the paid brain disabled.

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
- **Scheduler**: 03:33 wake-up roar.
- **ResearchModule**: experimental public-web lookup and local research logs.
- **MonitoringModule**: opt-in URL checks.
- **AutomationModule**: explicitly invoked local task functions.
- **QuizModule**: local quiz bank and progress logs.
- **Dashboard**: static HTML view backed by local JSON data.

Some components are prototypes. A scheduled module is not necessarily active merely because it is registered, and a demo output is not evidence of a deployed autonomous service. See `SECURITY_AUDIT.md`.

## Development principles

1. Prefer local files and local computation.
2. No paid services or financial functionality.
3. Network access must be obvious, limited, and opt-in.
4. Add tests before claiming a feature works.
5. Label simulations and placeholders honestly.
6. Back up local memory before changing its format.

The point is exploration, not extraction. The Shrine is a workshop, not a checkout page.
