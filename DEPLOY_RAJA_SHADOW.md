# RAJA SHADOW — Local Experiment Guide

The Shrine is a creative, local-first experiment. It is not a business, payment system, or paid autonomous service.

## Non-negotiable project boundaries

- No Ko-fi, donations, payment processing, Stripe, PayPal, cryptocurrency transfers, or monetization.
- No paid APIs, paid model calls, cloud hosting, VPS, subscriptions, or metered services.
- Do not add credentials, payment destinations, billing integrations, or automatic purchases.
- The optional API-backed brain is disabled in `raja_shadow.py`. Do not re-enable it.
- Keep experiments local and reversible. Network features must be opt-in, documented, and use free/public resources only when appropriate.

## Run the basic local demonstration

Requirements: Python 3.10+ and the packages listed in `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 raja_shadow.py
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py raja_shadow.py
```

The default run is a local demonstration. It writes runtime state under `.raja_shadow_memory/`.

## What is safe to experiment with

- Local JSON memory and research notes.
- The terminal-based 03:33 wake-up roar.
- The static dashboard and local data visualization.
- Small, testable Python modules that do not require paid accounts or external services.

## Before adding a feature

1. Confirm it does not introduce a paid API, subscription, hosting bill, payment flow, or financial transfer.
2. Prefer local computation and local files.
3. Add tests for the behavior.
4. Make network access opt-in and clearly visible.
5. Never commit secrets or personal data.
6. Document limitations honestly. A simulated feature must be labelled as simulated.

## Running the scheduler

The scheduler can be run locally with:

```bash
python3 raja_shadow.py --daemon
```

This only runs on the machine where the command is started. It does not deploy anything to the internet or provide 24/7 cloud hosting. Stop it with Ctrl+C.

## Project philosophy

The point is to explore ideas, memory, interfaces, and playful agent-like behavior without turning the experiment into a product or a bill. Keep it weird. Keep it local. Keep it free.
