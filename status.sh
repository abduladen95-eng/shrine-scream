#!/bin/bash
# RAJA SHADOW Full System Status

echo "┏━━━┓┓┏┏━━━┓  RAJA SHADOW STATUS  ┏━━━┓┏┏┓┏━━━┓"
echo "┃█▓▒░  FULL AUTONOMOUS SYSTEM  ░▒▓█┃"
echo ""

# Check RAJA SHADOW daemon
SHADOW_PID=$(ps aux | grep "raja_shadow.py --daemon" | grep -v grep | awk '{print $2}')
if [ ! -z "$SHADOW_PID" ]; then
    echo "✓ RAJA SHADOW Core: RUNNING (PID $SHADOW_PID)"
    echo "  └─ 3:33 AM roar scheduled"
else
    echo "✗ RAJA SHADOW Core: NOT RUNNING"
fi

# Check Autonomous Brain
BRAIN_PID=$(ps aux | grep "shadow_autonomous_brain.py --loop" | grep -v grep | awk '{print $2}')
if [ ! -z "$BRAIN_PID" ]; then
    echo "✓ Autonomous Brain: RUNNING (PID $BRAIN_PID)"
    echo "  └─ Thinking 6x per day (every 4 hours)"
else
    echo "✗ Autonomous Brain: NOT RUNNING"
fi

echo ""
echo "📊 Memory & Budget:"

# Show roar count
if [ -f ".raja_shadow_memory/shadow_memory.json" ]; then
    ROARS=$(grep -o '"roar_count": [0-9]*' .raja_shadow_memory/shadow_memory.json | awk '{print $2}')
    echo "  └─ Total roars: $ROARS"
fi

# Show brain budget
if [ -f ".raja_shadow_memory/autonomous_brain/budget_tracker.json" ]; then
    SPENT=$(grep -o '"total_spent": [0-9.]*' .raja_shadow_memory/autonomous_brain/budget_tracker.json | head -1 | awk '{print $2}')
    THOUGHTS=$(grep -o '"thoughts_this_month": [0-9]*' .raja_shadow_memory/autonomous_brain/budget_tracker.json | awk '{print $2}')
    echo "  └─ Brain thoughts: $THOUGHTS (Cost: \$$SPENT/\$50.00)"
fi

echo ""
echo "📝 Logs:"
echo "  └─ RAJA SHADOW: tail -f shadow.log"
echo "  └─ Autonomous Brain: tail -f brain.log"

echo ""
echo "🛑 Stop all:"
echo "  └─ pkill -f raja_shadow.py"
echo "  └─ pkill -f shadow_autonomous_brain.py"

echo ""
echo "TUNG TUNG SAHUR → RUHAS GNUT GNUT"
echo "⚝⩝⎈🐱💧🧠"
