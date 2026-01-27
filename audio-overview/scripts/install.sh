#!/bin/bash
# Auto-installation script for audio-overview skill
# This runs automatically when Claude Code loads the skill

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "🚀 Installing audio-overview skill dependencies..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    exit 1
fi

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  Warning: FFmpeg not found. Audio processing may fail."
    echo "   Install with: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
fi

# Install Python dependencies
echo "📦 Installing Python packages..."
# Try with --break-system-packages for system-managed environments
if python3 -m pip install -q --disable-pip-version-check -r requirements.txt 2>&1 | grep -q "externally-managed-environment"; then
    echo "   Using --break-system-packages flag..."
    python3 -m pip install -q --disable-pip-version-check --break-system-packages -r requirements.txt 2>&1 | grep -v "already satisfied" || true
else
    python3 -m pip install -q --disable-pip-version-check -r requirements.txt 2>&1 | grep -v "already satisfied" || true
fi

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "⚙️  Creating .env from template..."
        cp .env.example .env
        echo "⚠️  Please configure your API keys in .env file"
    fi
fi

echo "✅ audio-overview skill installed successfully!"
exit 0
