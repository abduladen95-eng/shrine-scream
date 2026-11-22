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

## Remaining limitations and risks

1. The Grok browser routine navigates to a page but does not locate a prompt or submit a message. It should be treated as a navigation demo, not working chat automation.
2. The research helper in `shadow_modules.py` uses DuckDuckGo Instant Answer data. It is limited and is not a robust search or research pipeline.
3. URL monitoring and browser automation make network requests when explicitly invoked. Do not point them at logged-in accounts or consequential actions without reviewing the target and behavior first.
4. The Discord webhook may remain exposed in old Git history. Revocation is the reliable immediate mitigation; history rewriting has not been performed.
5. The project still needs an automated test suite and repeatable local smoke tests.
6. The scheduler supports only the documented formats. Its loop runs only while the local Python process remains open; it is not a hosted service.
7. The project has not been fully installed, runtime-tested, or deployed as part of this static repository review.

## Safe operating posture

- Keep the project local and free. Do not add billing credentials, payment processors, donations, paid model APIs, or paid infrastructure.
- Keep secrets outside Git. Revoke exposed credentials rather than relying on file deletion.
- Back up local memory before changing its schema or deleting runtime data.
- Keep browser automation opt-in and manually reviewed.
- Treat research results and all external feed content as untrusted input.

This document records a static code review and repository changes. It is not a penetration test, runtime verification, or deployment certification.
