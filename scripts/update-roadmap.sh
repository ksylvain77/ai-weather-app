#!/bin/bash

# Update roadmap files with current project status
# Usage: ./scripts/update-roadmap.sh [branch-name] [description] [status]

ROADMAP_FILE="ROADMAP.md"
GOALS_FILE="PROJECT_GOALS.md"

if [ ! -f "$ROADMAP_FILE" ]; then
    echo "❌ ROADMAP.md not found. Run this from project root."
    exit 1
fi

BRANCH_NAME="${1:-$(git branch --show-current)}"
DESCRIPTION="${2:-Updated roadmap}"
STATUS="${3:-in-progress}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Function to update completion status in roadmap
update_roadmap_status() {
    local branch="$1"
    local status="$2"
    
    if [ "$status" = "completed" ]; then
        # Mark branch as completed
        sed -i "s/- \[ \] \*\*${branch}\*\*/- [x] **${branch}**/" "$ROADMAP_FILE"
        echo "✅ Marked $branch as completed in roadmap"
    elif [ "$status" = "in-progress" ]; then
        # Ensure branch is in progress (unchecked)
        sed -i "s/- \[x\] \*\*${branch}\*\*/- [ ] **${branch}**/" "$ROADMAP_FILE"
        echo "🔄 Marked $branch as in-progress in roadmap"
    fi
}

# Function to add implementation notes
add_implementation_note() {
    local note="$1"
    
    # Add note to implementation notes section
    awk -v note="- **$(date '+%Y-%m-%d')**: $note" '
    /^### Completed Features/ { 
        found=1
        print
        print note
        next
    }
    { print }
    ' "$ROADMAP_FILE" > "${ROADMAP_FILE}.tmp" && mv "${ROADMAP_FILE}.tmp" "$ROADMAP_FILE"
    
    echo "📝 Added implementation note to roadmap"
}

# Function to update last updated timestamp
update_timestamp() {
    sed -i "s/- \*\*Last Updated\*\*:.*/- **Last Updated**: $TIMESTAMP/" "$ROADMAP_FILE"
    echo "⏰ Updated timestamp in roadmap"
}

# Main execution
case "$STATUS" in
    "completed")
        update_roadmap_status "$BRANCH_NAME" "completed"
        add_implementation_note "Completed: $DESCRIPTION"
        ;;
    "in-progress")
        update_roadmap_status "$BRANCH_NAME" "in-progress"
        add_implementation_note "Started: $DESCRIPTION"
        ;;
    "note")
        add_implementation_note "$DESCRIPTION"
        ;;
    *)
        echo "Usage: $0 [branch-name] [description] [completed|in-progress|note]"
        exit 1
        ;;
esac

update_timestamp

echo "🎯 Roadmap updated successfully!"
echo "📄 View: cat $ROADMAP_FILE"
