@echo off
echo ============================================
echo RAJA SHADOW - MSI Raider Launch Script
echo ============================================
echo.
echo IMPORTANT: Edit this file first!
echo Replace YOUR_API_KEY_HERE with your actual Anthropic API key
echo Replace YOUR_DISCORD_WEBHOOK_HERE with your Discord webhook URL
echo.
echo Then save and run again.
echo.

REM Set API keys and configuration
REM EDIT THESE VALUES BEFORE RUNNING:
set ANTHROPIC_API_KEY=YOUR_API_KEY_HERE
set DISCORD_WEBHOOK=YOUR_DISCORD_WEBHOOK_HERE
set BRAIN_BUDGET=20.0
set BRAIN_THOUGHTS_PER_DAY=96

REM Check if keys are still placeholders
if "%ANTHROPIC_API_KEY%"=="YOUR_API_KEY_HERE" (
    echo ============================================
    echo ERROR: You need to edit this file first!
    echo ============================================
    echo.
    echo Open RUN_ON_MSI_RAIDER.bat in Notepad
    echo Replace YOUR_API_KEY_HERE with your key
    echo Replace YOUR_DISCORD_WEBHOOK_HERE with your webhook
    echo Save and run again
    echo.
    pause
    exit /b 1
)

echo Keys configured!
echo Budget: $20
echo Thinking frequency: 96 thoughts/day (every 15 min)
echo.
echo Starting RAJA's autonomous brain...
echo.

python shadow_autonomous_brain.py --loop

pause
