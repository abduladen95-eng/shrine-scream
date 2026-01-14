@echo off
echo ============================================
echo RAJA SHADOW - Discord Bot Launcher
echo ============================================
echo.
echo IMPORTANT: Edit this file first!
echo Replace YOUR_BOT_TOKEN_HERE with your Discord bot token
echo Replace YOUR_API_KEY_HERE with your Anthropic API key
echo.
echo Then save and run again.
echo.

REM Set API keys and configuration
REM EDIT THESE VALUES BEFORE RUNNING:
set DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
set ANTHROPIC_API_KEY=YOUR_API_KEY_HERE

REM Check if keys are still placeholders
if "%DISCORD_BOT_TOKEN%"=="YOUR_BOT_TOKEN_HERE" (
    echo ============================================
    echo ERROR: You need to edit this file first!
    echo ============================================
    echo.
    echo Open RUN_DISCORD_BOT.bat in Notepad
    echo Replace YOUR_BOT_TOKEN_HERE with your Discord bot token
    echo Replace YOUR_API_KEY_HERE with your Anthropic API key
    echo Save and run again
    echo.
    pause
    exit /b 1
)

echo Keys configured!
echo Starting RAJA Discord Bot...
echo.
echo You can now talk to RAJA in Discord!
echo Both-ways communication active!
echo.

python shadow_discord_bot.py

pause
