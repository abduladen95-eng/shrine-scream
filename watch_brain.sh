#!/bin/bash
# Watch the Brain Think in Real-Time

echo "🧠 WATCHING RAJA SHADOW BRAIN THOUGHTS..."
echo "Press Ctrl+C to stop"
echo ""

# Follow brain log and highlight important parts
tail -f brain.log | grep --line-buffered -E "(DECISION:|Topic:|Reasoning:|ANALYSIS:|SELF-REFLECTION:)" --color=always
