#!/bin/bash
# RAJA SHADOW - Start Autonomous Brain
# Run this to start the brain in continuous mode

echo "🧠 STARTING RAJA SHADOW AUTONOMOUS BRAIN"
echo ""

# Load environment variables
if [ -f "setup_brain_env.sh" ]; then
    source setup_brain_env.sh
else
    echo "⚠️  setup_brain_env.sh not found!"
    echo "Create it with your API keys first."
    exit 1
fi

# Set UTF-8 encoding for Windows terminals
export PYTHONIOENCODING=utf-8

echo ""
echo "🔥 Brain is now thinking autonomously..."
echo "   - Thinks every 4 hours (6x per day)"
echo "   - Searches web + Reddit"
echo "   - Posts interesting findings to Discord"
echo "   - Budget: \$20/month"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the brain in loop mode
python shadow_autonomous_brain.py --loop
