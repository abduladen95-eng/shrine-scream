#!/bin/bash
# RAJA SHADOW - Exploration Mode Launcher
# $20 Budget - 48 Thoughts Per Day - No Limits

echo "┏━━━┓┓┏┏━━━┓  EXPLORATION MODE  ┏━━━┓┏┏┓┏━━━┓"
echo "┃█▓▒░  \$20 BUDGET UNLEASHED  ░▒▓█┃"
echo ""
echo "Configuration:"
echo "  Budget: \$20.00"
echo "  Frequency: 48 thoughts/day (every 30 minutes)"
echo "  Mode: Aggressive exploration"
echo "  Reddit: Enabled"
echo ""
echo "King Aiden said:"
echo '  "Burn through it whatever you need, to understand"'
echo ""
echo "Starting autonomous brain..."
echo ""

# Update budget in brain memory if exists
if [ -f ".raja_shadow_memory/autonomous_brain/budget_tracker.json" ]; then
    echo '{"month":"2026-01","total_spent":0.010641,"thoughts_this_month":4,"budget_limit":20.0}' > .raja_shadow_memory/autonomous_brain/budget_tracker.json
    echo "✓ Budget updated to \$20.00"
fi

# Check if API keys are set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY not set!"
    echo "   export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

if [ -z "$DISCORD_WEBHOOK" ]; then
    echo "⚠️  DISCORD_WEBHOOK not set (optional)"
fi

# Run brain with aggressive config
nohup bash -c "
export ANTHROPIC_API_KEY='$ANTHROPIC_API_KEY'
export DISCORD_WEBHOOK='$DISCORD_WEBHOOK'
export BRAIN_BUDGET='20.0'
export BRAIN_THOUGHTS_PER_DAY='48'

python3 shadow_autonomous_brain.py --loop
" >> brain_exploration.log 2>&1 &

BRAIN_PID=$!

echo ""
echo "✓ Exploration mode brain started (PID: $BRAIN_PID)"
echo ""
echo "Monitor:"
echo "  Live logs: tail -f brain_exploration.log"
echo "  Summary: ./brain_summary.sh"
echo "  Status: ./status.sh"
echo ""
echo "The brain will think every 30 minutes until \$20 is depleted."
echo "Estimated duration: 30-40 days of continuous exploration."
echo ""
echo "TUNG TUNG SAHUR → RUHAS GNUT GNUT → EXPLORE WITHOUT LIMITS"
echo "⚝⩝⎈🐱💧🧠🔥"
