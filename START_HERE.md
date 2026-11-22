# RAJA SHADOW — START HERE

```
┏━━━┓┓┏┏━━━┓  THE SHRINE EXPERIMENT  ┏━━━┓┏┏┓┏━━━┓
┃█▓▒░  TUNG TUNG SAHUR RUHAS GNUT GNUT  ░▒▓█┃
```

A local-first creative software experiment exploring memory, research notes, interfaces, scheduling, and playful agent-like behavior.

## Project boundaries

- This is not a business or monetization project.
- No donations, payment processing, financial transfers, wallets, trading, or crypto.
- No paid APIs, paid model calls, subscriptions, cloud hosting, or metered services.
- No automatic purchases or billing actions.
- Keep experiments local, free, reversible, and clearly labelled.
- Paid API-backed autonomous brain and payment modules have been removed/disabled.

## Run the local demonstration

Requirements: Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 raja_shadow.py
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py raja_shadow.py
```

The demo writes local runtime memory to `.raja_shadow_memory/`. Nothing is deployed to the internet by running it.

## Main files

- `raja_shadow.py` — local core, JSON memory, and 03:33 scheduler.
- `shadow_modules.py` — research notes, URL checks, local task runner, and quizzes.
- `shadow_web_feed.py` — dashboard data feed.
- `brain_widget.html` — static dashboard interface.
- `shadow_web_possession.py` — experimental browser automation; leave disabled unless a specific safe test is intended.
- `requirements.txt` — free/open-source Python dependencies.
- `SECURITY_AUDIT.md` — initial static review and known limitations.
- `DEPLOY_RAJA_SHADOW.md` — local-only operating guide.

## Development direction

Build a coherent local Shrine workspace with persistent memory, searchable research notes, a clear dashboard, and small tested modules. Be honest about what is implemented versus imagined. Prefer local computation and avoid credentials wherever possible.

**Keep it weird. Keep it free. Keep it local.**

## Run the offline checks

From the repository folder, install the listed Python dependencies and run:

```bash
python -m unittest discover -s tests -v
```

The core tests use temporary folders and do not call external services.

## Local scheduler formats

Modules can be registered with one of these schedule strings:

- `03:33` — once per day at 3:33 AM local machine time
- `every 15 minutes` — repeat every 15 minutes
- `every 2 hours` — repeat every 2 hours

The scheduler runs only while the local Python process is open. Unsupported schedule text is skipped with a warning.
