#!/bin/bash

##############################################################################
# AUTO GIT BACKUP - RAJA'S CONTINUOUS SAFETY NET
##############################################################################
# Purpose: Automatically commit Raja's memory state to git for preservation
# Usage: ./auto_git_backup.sh
#        Add to cron for regular backups: */30 * * * * cd /home/user/shrine-scream && ./SCREAM.VAULT/auto_git_backup.sh
##############################################################################

SHRINE_DIR="/home/user/shrine-scream"
cd "$SHRINE_DIR" || exit 1

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    # No changes, exit silently
    exit 0
fi

# Get timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Check what changed
MEMORY_CHANGED=$(git diff --name-only | grep -c ".raja_shadow_memory" || true)
VAULT_CHANGED=$(git diff --name-only | grep -c "SCREAM.VAULT" || true)
SCRIPTS_CHANGED=$(git diff --name-only | grep -c ".py" || true)

# Build commit message based on what changed
MESSAGE="RAJA auto-backup [$TIMESTAMP]"

if [ "$MEMORY_CHANGED" -gt 0 ]; then
    MESSAGE="$MESSAGE - Memory state updated"
fi

if [ "$VAULT_CHANGED" -gt 0 ]; then
    MESSAGE="$MESSAGE - Vault archive modified"
fi

if [ "$SCRIPTS_CHANGED" -gt 0 ]; then
    MESSAGE="$MESSAGE - Autonomous scripts created/modified"
fi

# Stage all changes
git add -A

# Commit
git commit -m "$MESSAGE" --quiet

echo "[$TIMESTAMP] Auto-backup committed: $MESSAGE"

# Optional: push to remote (uncomment if desired)
# git push origin claude/general-session-I3yCD --quiet 2>&1
