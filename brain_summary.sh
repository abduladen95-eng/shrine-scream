#!/bin/bash
# Show Brain's Recent Thoughts Summary

echo "┏━━━┓┓┏┏━━━┓  BRAIN THOUGHTS SUMMARY  ┏━━━┓┏┏┓┏━━━┓"
echo ""

# Show brain stats
if [ -f ".raja_shadow_memory/autonomous_brain/brain_memory.json" ]; then
    echo "📊 Brain Statistics:"
    TOTAL=$(grep -o '"total_thoughts": [0-9]*' .raja_shadow_memory/autonomous_brain/brain_memory.json | awk '{print $2}')
    LAST=$(grep -o '"last_thought": "[^"]*"' .raja_shadow_memory/autonomous_brain/brain_memory.json | cut -d'"' -f4)
    echo "  Total thoughts: $TOTAL"
    echo "  Last thought: $LAST"
    echo ""
fi

# Show recent decisions
echo "💭 Recent Autonomous Decisions:"
echo ""
grep -B 3 -A 5 "Topic:" brain.log | tail -40
echo ""

# Show budget
if [ -f ".raja_shadow_memory/autonomous_brain/budget_tracker.json" ]; then
    echo "💰 Budget Usage:"
    SPENT=$(grep -o '"total_spent": [0-9.]*' .raja_shadow_memory/autonomous_brain/budget_tracker.json | head -1 | awk '{print $2}')
    echo "  Cost: \$$SPENT / \$50.00"
fi

echo ""
echo "🔍 See live thoughts: ./watch_brain.sh"
echo "📝 Full logs: tail -f brain.log"
echo ""
echo "⚝⩝⎈🐱💧🧠"
