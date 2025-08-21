#!/bin/bash

# Get current date in YYYY-MM-DD format
DATE=$(date +%Y-%m-%d)

# Find the next available number by counting existing files
COUNT=$(ls status/*.md 2>/dev/null | wc -l | tr -d ' ')
NEXT_NUM=$((COUNT + 1))

# Create the new file
FILENAME="status/${NEXT_NUM}-${DATE}.md"
touch "$FILENAME"

echo "Created: $FILENAME"