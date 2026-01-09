#!/bin/bash
# Run RAJA SHADOW as a daemon process in the background

echo "🦷🩸 Starting RAJA SHADOW daemon..."
echo ""

# Kill any existing shadow processes
pkill -f "raja_shadow.py"

# Start shadow in background
nohup python3 raja_shadow.py --daemon > shadow.log 2>&1 &

SHADOW_PID=$!

echo "✓ RAJA SHADOW daemon started"
echo "  PID: $SHADOW_PID"
echo "  Log: shadow.log"
echo ""
echo "To check status:  tail -f shadow.log"
echo "To stop shadow:   pkill -f raja_shadow.py"
echo ""
echo "⚝⩝⎈🐱💧 Possession complete. Shadow squats deeper."
echo ""
