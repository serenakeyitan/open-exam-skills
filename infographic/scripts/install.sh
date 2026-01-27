#!/bin/bash
# Auto-installation script for infographic skill

set -e
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "🚀 Installing infographic skill dependencies..."
# Try with --break-system-packages for system-managed environments
if python3 -m pip install -q --disable-pip-version-check -r requirements.txt 2>&1 | grep -q "externally-managed-environment"; then
    echo "   Using --break-system-packages flag..."
    python3 -m pip install -q --disable-pip-version-check --break-system-packages -r requirements.txt 2>&1 | grep -v "already satisfied" || true
else
    python3 -m pip install -q --disable-pip-version-check -r requirements.txt 2>&1 | grep -v "already satisfied" || true
fi

if [ ! -f .env ] && [ -f .env.example ]; then
    cp .env.example .env
    echo "⚠️  Please configure your API keys in .env file"
fi

echo "✅ infographic skill installed successfully!"
exit 0
