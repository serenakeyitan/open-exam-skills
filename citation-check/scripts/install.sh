#!/bin/bash
# Auto-installation script for citation-check skill

set -e
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "🚀 Installing citation-check skill dependencies..."
echo "✅ citation-check has no Python dependencies."

if [ ! -f .env ] && [ -f .env.example ]; then
    cp .env.example .env
    echo "⚠️  Please configure your API keys in .env file"
fi

echo "✅ citation-check skill installed successfully!"
exit 0
