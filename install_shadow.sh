#!/bin/bash
# RAJA SHADOW Installation Script
# Installs dependencies and sets up the autonomous agent

echo "🦷🩸 RAJA SHADOW INSTALLATION 🩸🦷"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✓ Dependencies installed"
echo ""
echo "🐱 RAJA SHADOW is ready to possess"
echo ""
echo "Usage:"
echo "  Manual test:     python3 raja_shadow.py"
echo "  Daemon mode:     python3 raja_shadow.py --daemon"
echo "  Background:      nohup python3 raja_shadow.py --daemon > shadow.log 2>&1 &"
echo ""
echo "TUNG TUNG SAHUR → RUHAS GNUT GNUT → WOBBLE MAX"
echo ""

chmod +x raja_shadow.py
