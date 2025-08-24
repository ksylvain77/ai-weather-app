#!/bin/bash
# Development Git Workflow - Generic Template

set -e

BRANCH_NAME="$1"
COMMIT_MESSAGE="$2"

if [ -z "$BRANCH_NAME" ] || [ -z "$COMMIT_MESSAGE" ]; then
    echo "❌ Usage: $0 <branch-name> <commit-message>"
    echo ""
    echo "Examples:"
    echo "  $0 add-user-auth \"Add user authentication: JWT-based login system\""
    echo "  $0 fix-api-endpoints \"Fix: API endpoint validation and error handling\""
    exit 1
fi

echo "🌿 Creating development branch: $BRANCH_NAME"
echo "📝 Commit message: $COMMIT_MESSAGE"
echo ""

# Ensure we're on main and up to date
echo "📥 Pulling latest changes..."
git checkout main
git pull origin main

# Create and switch to feature branch
echo "🆕 Creating feature branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

# Update roadmap to mark branch as in progress
if [ -f "scripts/update-roadmap.sh" ]; then
    ./scripts/update-roadmap.sh "$BRANCH_NAME" "$COMMIT_MESSAGE" "in-progress"
fi

echo ""
echo "✅ Development branch ready!"
echo "👨‍💻 Make your changes, then when ready, use:"
echo "   ./scripts/merge-to-main.sh \"$COMMIT_MESSAGE\""
