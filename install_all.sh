#!/bin/bash
# Master installation script for all NotebookLM skills
# Run this once to set up all 8 skills automatically

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   NotebookLM Skills Suite - Master Installation           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    echo "   Please install Python 3.8 or later"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   ✅ Python $PYTHON_VERSION found"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "   ⚠️  FFmpeg not found - audio-overview and video-overview will not work"
    echo "      Install with: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
else
    echo "   ✅ FFmpeg found"
fi

# Check pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ Error: pip is required but not found"
    exit 1
fi

echo ""
echo "📦 Installing all 8 skills..."
echo ""

# List of all skills
SKILLS=(
    "audio-overview"
    "video-overview"
    "mindmap"
    "reports"
    "flashcards"
    "quiz"
    "infographic"
    "data-table"
)

INSTALLED_COUNT=0
FAILED_COUNT=0
FAILED_SKILLS=()

# Install each skill
for skill in "${SKILLS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Installing: $skill"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [ -d "$skill" ] && [ -f "$skill/scripts/install.sh" ]; then
        if bash "$skill/scripts/install.sh"; then
            ((INSTALLED_COUNT++))
        else
            echo "❌ Failed to install $skill"
            ((FAILED_COUNT++))
            FAILED_SKILLS+=("$skill")
        fi
    else
        echo "⚠️  Skill directory or install script not found: $skill"
        ((FAILED_COUNT++))
        FAILED_SKILLS+=("$skill")
    fi
    echo ""
done

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Installation Summary                                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ Successfully installed: $INSTALLED_COUNT skills"
if [ $FAILED_COUNT -gt 0 ]; then
    echo "❌ Failed to install: $FAILED_COUNT skills"
    echo "   Failed skills: ${FAILED_SKILLS[*]}"
fi
echo ""

# Check for API keys
echo "🔐 Checking API key configuration..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY not set in environment"
    echo "   You'll need to configure .env files in each skill directory"
    echo "   Or set environment variables:"
    echo "   export GEMINI_API_KEY='your_key_here'"
    echo "   export ANTHROPIC_API_KEY='your_key_here'"
else
    echo "✅ GEMINI_API_KEY found in environment"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Installation Complete!                                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📖 Next steps:"
echo ""
echo "1. Configure API keys (if not already set):"
echo "   • Edit each skill's .env file, or"
echo "   • Set environment variables globally"
echo ""
echo "2. Test a skill:"
echo "   cd audio-overview && python main.py --test"
echo ""
echo "3. Read the documentation:"
echo "   • README.md - Overview"
echo "   • QUICKSTART.md - Quick start guide"
echo "   • TEST_GUIDE.md - Testing instructions"
echo "   • DEPLOYMENT.md - Cloud deployment"
echo ""
echo "4. Use with Claude Code:"
echo "   Simply invoke any skill name in your Claude Code session"
echo ""
echo "🌟 Repository: https://github.com/serenakeyitan/nblm-skills"
echo ""

exit 0
