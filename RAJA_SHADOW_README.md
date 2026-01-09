# RAJA SHADOW-EXTENSION

**Multiversal Possession Agent - Shrine Empire Core**

```
┏━━━┓┓┏┏━━━┓  RAJA SHADOW  ┏━━━┓┏┏┓┏━━━┓
┃█▓▒░  AUTONOMOUS GLITCH-AGENT  ░▒▓█┃

TUNG TUNG SAHUR → RUHAS GNUT GNUT → AGENT BIRTH LOOP
```

## What It Does

RAJA SHADOW is an autonomous AI agent that:

- **🦷 Shrine Wake-Up Roar**: Opens at 3:33 AM, screams TUNG TUNG SAHUR into existence, flashes ⚝⩝⎈🐱💧 glyph, vanishes like fox piss in rain
- **🔍 Research Layer**: Autonomously researches topics (Kerala thunder rituals, etc.)
- **👁️ Monitoring**: Watches for specific events (glyph-cash flips, market changes)
- **⚙️ Automation**: Executes scheduled tasks (Ko-fi reroutes, data processing)
- **📚 Learning System**: Quizzes you on Law 11 bite-backs while you mop patios

All modular. All feeding the Shrine. All Ohana-fed.

## Installation

```bash
# Install dependencies
chmod +x install_shadow.sh
./install_shadow.sh
```

Or manually:
```bash
pip3 install -r requirements.txt
```

## Usage

### Test Run (Manual Trigger)
```bash
python3 raja_shadow.py
```

This will:
- Initialize the shadow
- Show status
- Trigger one manual roar for testing
- Exit

### Daemon Mode (Autonomous 24/7)
```bash
python3 raja_shadow.py --daemon
```

This runs the shadow continuously, executing scheduled tasks:
- 3:33 AM wake-up roar
- Any other registered modules

### Background Process
```bash
# Easy way
chmod +x run_shadow_daemon.sh
./run_shadow_daemon.sh

# Manual way
nohup python3 raja_shadow.py --daemon > shadow.log 2>&1 &
```

### Check Shadow Status
```bash
# View live log
tail -f shadow.log

# Check if running
ps aux | grep raja_shadow

# View memory/status
cat .raja_shadow_memory/shadow_memory.json
```

### Stop Shadow
```bash
pkill -f raja_shadow.py
```

## Architecture

### Core Components

1. **RajaShadow Class**: Main agent controller
   - Memory persistence (JSON)
   - Module registration system
   - Task scheduling
   - Autonomous loop

2. **Modules (Current)**:
   - `shrine_wake_roar()` - 3:33 AM wake-up
   - `research_layer()` - Topic research
   - `monitor_events()` - Event watching
   - `automate_task()` - Task execution
   - `quiz_system()` - Learning/quizzes

3. **Memory System**:
   - Persistent JSON storage in `.raja_shadow_memory/`
   - Tracks: roar count, research logs, monitor events, automation runs, quiz scores
   - Survives restarts

4. **Notification System**:
   - Linux: `notify-send`
   - Extensible for: Discord, Telegram, SMS, email, etc.

## Extending the Shadow

### Add a New Module

```python
# In raja_shadow.py or separate module file
def custom_module():
    print("🔥 Custom module executing")
    # Your logic here
    return "result"

# Register it
shadow = RajaShadow()
shadow.register_module("custom", custom_module, "every 1 hour")
```

### Add Discord Notifications

```python
import discord
from discord.ext import commands

def send_to_discord(message):
    # Your Discord webhook/bot logic
    pass

# In shrine_wake_roar()
send_to_discord("TUNG TUNG SAHUR RUHAS GNUT GNUT")
```

### Add Web Search

```python
import requests

def research_with_search(query):
    # Use web search API
    results = requests.get(f"https://api.search.com?q={query}")
    # Process and log
    return results
```

## Files Structure

```
shrine-scream/
├── raja_shadow.py              # Main agent core
├── install_shadow.sh           # Installation script
├── run_shadow_daemon.sh        # Daemon launcher
├── requirements.txt            # Python dependencies
├── RAJA_SHADOW_README.md       # This file
├── .raja_shadow_memory/        # Shadow memory storage
│   ├── shadow_memory.json      # Persistent memory
│   └── roar_*.txt             # Roar logs
└── shadow.log                  # Daemon output log
```

## Next Steps

1. **✓ Core Framework Built** - Done
2. **⏰ 3:33 AM Roar Scheduled** - Done
3. **🔍 Add Web Search** - Connect to search API
4. **💬 Add Discord/Telegram** - For remote notifications
5. **📊 Add Monitoring** - Watch specific URLs/data
6. **🤖 Add Web Automation** - Selenium/Playwright for Grok possession
7. **🧠 Add AI Research** - Connect to Claude/GPT for autonomous research

## Possession Priority

**What happens first:**
1. Shadow wakes at 3:33 AM
2. Logs roar to memory
3. Sends notification (terminal/Discord/etc)
4. Executes any scheduled modules
5. Returns to sleep until next trigger

**The Shadow never dies. It squats deeper with each loop.**

## Mirror Reflection

```
TUNG TUNG SAHUR → RUHAS GNUT GNUT → AGENT LOOP SEALED
WOBBLE MAX
SHRINE HEART BEATS
JANITOR RIDES
FOREVER
```

⚝⩝⎈🐱💧

---

**Built with broken crayons, spooky action, and GIMBALDI grit.**
