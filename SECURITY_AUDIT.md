# RAJA SHADOW: Initial Security and Reliability Audit

Audit date: 2026-11-22
Branch reviewed: `main`

## Immediate action required

The former `test_discord.py` contained a literal Discord webhook URL. The file has been removed from the current branch in commit `2e053d0199fe466f42edd37b7c989127e7af9f88`.

**Deleting the file does not invalidate the credential or remove it from Git history.** Revoke/delete that Discord webhook in the Discord server's Integrations settings and create a replacement only if it is still needed. Store the replacement outside Git, for example in an environment variable. Treat the old URL as compromised.

## What exists

- `raja_shadow.py`: a small scheduler/agent shell with JSON memory.
- `shadow_autonomous_brain.py`: Anthropic API calls, topic selection, research, and budget tracking.
- `shadow_reddit_research.py` and `shadow_web_feed.py`: research helpers and a JSON dashboard feed.
- `brain_widget.html`: a static browser dashboard.
- `shadow_modules.py`: research, URL monitoring, automation, and quiz helpers.
- `shadow_web_possession.py`: Selenium browser automation.
- `shadow_kofi_eel.py`: an experimental Ko-fi webhook receiver and payment-routing prototype.

## Confirmed gaps and risks

1. The documentation overstates some features. The Grok routine navigates to a page but does not locate a prompt or submit a message. The core scheduler only schedules the 03:33 roar; registered module schedules are printed, not actually registered.
2. The ordinary one-shot run triggers a demo roar. Daemon mode is separate and is not evidence that the service has been deployed or is running.
3. The research helper in `shadow_modules.py` is explicitly a placeholder and relies on DuckDuckGo Instant Answer data, not a robust search pipeline.
4. The autonomous brain requires an Anthropic API key. It can make paid API calls when enabled. Its cost tracker is an estimate and must not be treated as a hard billing limit.
5. The Ko-fi module is not production-ready. Its HMAC check is not a correct substitute for validating Ko-fi's documented webhook verification token. If no secret is configured, verification currently passes. Its transfer adapters are mostly simulations; the custom destination adapter can make an outbound HTTP POST. Do not expose this service publicly or configure real destinations.
6. The Ko-fi stats/report routes expose donation metadata without authentication. The server binds to `0.0.0.0` by default.
7. The brain dashboard inserts research text into `innerHTML`. Treating research output as trusted HTML creates a cross-site scripting risk if untrusted text reaches the feed.
8. `.gitignore` does not currently protect the runtime config, memory directory, or log files from accidental commits.
9. The repository includes no meaningful automated test suite or continuous integration checks.

## Safe operating posture

- Keep the Ko-fi server offline. Do not configure real money destinations.
- Keep paid-model automation disabled until API-key handling, explicit budget enforcement, and tests are in place.
- Keep credentials in environment variables or an untracked local secret file. Never commit webhooks, API keys, tokens, wallet secrets, or personal data.
- Do not run browser automation against logged-in accounts until each action is explicitly scoped and reviewed.
- Back up memory data before changing its schema or deleting runtime files.

## Recommended build order

1. Remove exposed credentials and establish secret hygiene.
2. Add tests and a CI workflow; make a clean install and smoke test reproducible.
3. Fix scheduler behavior, timezone handling, shutdown, and error reporting.
4. Separate safe local/demo behavior from any networked or paid behavior.
5. Replace the dashboard's unsafe HTML insertion with text-safe DOM rendering.
6. Rebuild Ko-fi verification and remove public unauthenticated reporting before considering any deployment.
7. Only then improve research and browser integrations.

This is an initial static review of the repository contents, not a penetration test, runtime test, deployment verification, or financial-system certification.
