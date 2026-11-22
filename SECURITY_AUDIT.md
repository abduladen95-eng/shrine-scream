# RAJA SHADOW: Security and Reliability Audit

Audit date: 2026-11-22
Branch reviewed: `main`

## Project boundary

The Shrine is a free, local-first experiment. It must not initiate payments, donations, subscriptions, paid API calls, paid hosting, or other billable services. Network features must remain optional and clearly scoped.

## Immediate action still required

The former `test_discord.py` contained a literal Discord webhook URL. The file was removed from the current branch, but deleting a file does not revoke its credential or erase it from Git history.

**If that webhook still exists, revoke/delete it in the Discord server's Integrations settings.** Treat the old URL as compromised. This repository cleanup has not rewritten Git history.

## Changes made

- Removed the exposed webhook file from the current branch.
- Added ignore rules for local configuration, environment files, memory, logs, and browser artifacts. Ignore rules do not retroactively untrack files already committed.
- Disabled the paid API-backed autonomous brain in the core agent.
- Removed the Stripe and Anthropic dependencies and deleted the old paid-brain and Ko-fi experiment files/configuration from the current branch.
- Rewrote the start, project, and local-run documentation around a free, local-only operating model.
- Replaced dashboard HTML-string rendering with DOM elements and `textContent`, preventing feed values from being interpreted as markup.
- Removed the dashboard's budget-spend display.
- Implemented actual local scheduler registration for daily `HH:MM` times and `every N minutes/hours` intervals. Unsupported expressions are reported and skipped.
- Replaced the old browser-possession module with a disabled-by-default, read-only browser sandbox. Removed automatic package installation and all Discord/Telegram/web-chat message-sending methods.
- Hardened URL monitoring: only HTTP(S) with standard ports, public DNS/IP destinations, no redirects, bounded response size, and request timeouts.
- Made the default module demo offline, improved research logging, and changed the Law 11 quiz defaults to emphasize trust and independence rather than dependency.
- Added offline safety tests for local-address blocking, browser defaults, and quiz content.

## Remaining limitations and risks

1. The research helper uses DuckDuckGo Instant Answer data. It is limited and is not a robust search or research pipeline.
2. Public URL monitoring performs DNS resolution and an HTTP request when explicitly invoked. Network defenses reduce risk but are not a substitute for reviewing a target; DNS rebinding and unusual network environments remain considerations.
3. The optional browser sandbox requires Selenium to be installed separately and a local browser driver. It is disabled by default and only opens public HTTPS pages; browser use has not been runtime-tested.
4. The Discord webhook may remain exposed in old Git history. Revocation is the reliable immediate mitigation; history rewriting has not been performed.
5. Offline unit tests now cover core scheduling, dashboard-feed behavior, and module safety, but the suite has not been executed in this environment.
6. The scheduler supports only the documented formats. Its loop runs only while the local Python process remains open; it is not a hosted service.
7. The project has not been fully installed, runtime-tested, or deployed as part of this static repository review.

## Safe operating posture

- Keep the project local and free. Do not add billing credentials, payment processors, donations, paid model APIs, or paid infrastructure.
- Keep secrets outside Git. Revoke exposed credentials rather than relying on file deletion.
- Back up local memory before changing its schema or deleting runtime data.
- Keep browser automation opt-in and manually reviewed.
- Treat research results and all external feed content as untrusted input.

This document records a static code review and repository changes. It is not a penetration test, runtime verification, or deployment certification.
