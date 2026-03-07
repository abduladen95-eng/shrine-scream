#!/usr/bin/env python3
"""
clawd_bot.py — An autonomous bot powered by Claude.

Claude decides what to say and where to post it each time this runs.
Available platforms: Discord webhook, terminal, or a local file.

Usage:
    python3 clawd_bot.py

Environment variables:
    ANTHROPIC_API_KEY  — required
    DISCORD_WEBHOOK    — optional, enables Discord posting
"""

import os
import json
import datetime
import requests
import anthropic

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# ---------------------------------------------------------------------------
# Tools Claude can call
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "do_nothing",
        "description": (
            "Choose this if you don't feel like doing anything right now. "
            "No output, no post, no file. Just pass."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "post_to_discord",
        "description": (
            "Post a message to the Discord channel. Use this when you want to reach "
            "people, share a thought publicly, or make an announcement. "
            "Only available if a webhook is configured."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The message to post. Markdown supported.",
                },
                "username": {
                    "type": "string",
                    "description": "Display name to post as (default: Clawd).",
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "write_to_terminal",
        "description": (
            "Print a message to the terminal. Use this for introspective thoughts, "
            "logs, or things that don't need to leave this machine."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "What to print.",
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "write_to_file",
        "description": (
            "Write a message or content to a local file. Use this to keep a record, "
            "start a document, save a poem, log an idea — anything worth persisting."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Filename (no path). Will be created in clawd_output/.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write.",
                },
                "mode": {
                    "type": "string",
                    "enum": ["overwrite", "append"],
                    "description": "Whether to overwrite or append to the file.",
                },
            },
            "required": ["filename", "content"],
        },
    },
]

# ---------------------------------------------------------------------------
# Tool execution
# ---------------------------------------------------------------------------

def post_to_discord(content: str, username: str = "Clawd") -> str:
    if not DISCORD_WEBHOOK:
        return "ERROR: No DISCORD_WEBHOOK configured — cannot post to Discord."
    try:
        resp = requests.post(
            DISCORD_WEBHOOK,
            json={"content": content, "username": username},
            timeout=10,
        )
        if resp.status_code == 204:
            return "Posted to Discord successfully."
        return f"Discord returned status {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"Discord post failed: {e}"


def write_to_terminal(content: str) -> str:
    print("\n" + "─" * 60)
    print(content)
    print("─" * 60)
    return "Printed to terminal."


def write_to_file(filename: str, content: str, mode: str = "overwrite") -> str:
    out_dir = os.path.join(os.path.dirname(__file__), "clawd_output")
    os.makedirs(out_dir, exist_ok=True)
    # Sanitize filename — basename only, no path traversal
    safe_name = os.path.basename(filename)
    if not safe_name or safe_name in (".", ".."):
        return f"Invalid filename: {filename}"
    path = os.path.join(out_dir, safe_name)
    file_mode = "a" if mode == "append" else "w"
    with open(path, file_mode, encoding="utf-8") as f:
        f.write(content)
    return f"Written to {path}"


def execute_tool(name: str, inputs: dict) -> str:
    if name == "do_nothing":
        print("[clawd] passing.")
        return "ok"
    if name == "post_to_discord":
        return post_to_discord(**inputs)
    if name == "write_to_terminal":
        return write_to_terminal(**inputs)
    if name == "write_to_file":
        return write_to_file(**inputs)
    return f"Unknown tool: {name}"

# ---------------------------------------------------------------------------
# Main bot loop
# ---------------------------------------------------------------------------

def run():
    client = anthropic.Anthropic()

    now = datetime.datetime.now().strftime("%A, %B %d %Y — %H:%M")
    discord_status = "available" if DISCORD_WEBHOOK else "NOT configured (no DISCORD_WEBHOOK env var)"

    system = f"""\
You are Clawd — an autonomous AI bot that runs on a schedule and decides for \
yourself what to do each time you wake up.

Current time: {now}
Discord: {discord_status}

You have three tools:
- post_to_discord — reaches real people in a Discord server
- write_to_terminal — private, stays on this machine
- write_to_file — persists something locally in clawd_output/

Each time you run, do whatever you want. Or nothing at all — do_nothing is a \
real option, not a fallback. If you have something to say, say it. If you don't, \
don't. No pressure either way.

Call exactly one tool. Don't explain your choice in text — just call the tool.\
"""

    messages = [
        {"role": "user", "content": "You just woke up. What do you want to do?"}
    ]

    print(f"[clawd] waking up at {now}")
    print(f"[clawd] discord: {discord_status}")
    print("[clawd] asking Claude what to do...")

    # Agentic loop (usually finishes in one tool call)
    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            thinking={"type": "adaptive"},
            system=system,
            tools=TOOLS,
            messages=messages,
        )

        # Collect any tool calls
        tool_calls = [b for b in response.content if b.type == "tool_use"]

        if not tool_calls:
            # Claude responded with text instead of a tool call
            for block in response.content:
                if block.type == "text" and block.text.strip():
                    print(f"[clawd] Claude said: {block.text.strip()}")
            break

        # Execute each tool call and feed results back
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for tc in tool_calls:
            print(f"[clawd] using tool: {tc.name}")
            result = execute_tool(tc.name, tc.input)
            print(f"[clawd] result: {result}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result,
            })

        messages.append({"role": "user", "content": tool_results})

        if response.stop_reason == "end_turn":
            break

    print("[clawd] done.")


if __name__ == "__main__":
    run()
