# How Claude Code Skills Work in the Cloud

This document explains how the NotebookLM Skills Suite ensures users get a fully working skill installation when they download and use it with Claude Code.

## Overview

When a user downloads these skills from GitHub/cloud and Claude Code loads them, everything "just works" because:

1. **Automatic Dependency Installation** via `scripts/install.sh`
2. **Smart Environment Detection** (handles system-managed Python)
3. **Template-Based Configuration** (`.env.example` → `.env`)
4. **Progressive Loading** (metadata → skill → resources)

---

## User Experience Flow

### What the User Does

```bash
# Step 1: Clone repository
git clone https://github.com/serenakeyitan/nblm-skills.git
cd nblm-skills

# Step 2: One-command installation
./install_all.sh

# Step 3: Configure API keys
export GEMINI_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"

# Done! Use with Claude Code
```

### What Happens Behind the Scenes

1. **Repository Clone**: User gets all 8 skills in isolated directories
2. **Master Installation**: `install_all.sh` runs each skill's `scripts/install.sh`
3. **Per-Skill Setup**:
   - Checks Python 3.8+ installed
   - Checks FFmpeg (for audio/video skills)
   - Installs Python packages from `requirements.txt`
   - Auto-detects externally-managed environments
   - Uses `--break-system-packages` if needed
   - Creates `.env` from `.env.example`
4. **Configuration**: User adds API keys (one time)
5. **Ready to Use**: Claude Code can invoke any skill

---

## How Claude Code Loads Skills

When Claude Code encounters a skill invocation:

### Phase 1: Discovery (Metadata Loading)

Claude reads `skill.yaml`:

```yaml
name: audio-overview
description: Generate professional multi-speaker podcasts...
version: 1.0.0
type: project
gitignored: true

# Installation hook
install_script: scripts/install.sh

# Dependencies
requires:
  - python3
  - ffmpeg

# Configuration
env_template: .env.example

# Entry point
main: main.py
```

**Claude knows:**
- Skill name and description
- What to install (`install_script`)
- System requirements (`requires`)
- How to configure (`.env.example`)
- How to run (`main.py`)

### Phase 2: Installation Check

If skill not yet installed:

```bash
# Claude automatically runs:
bash audio-overview/scripts/install.sh
```

This script:
1. Validates prerequisites (Python, FFmpeg)
2. Installs Python dependencies
3. Creates `.env` from template if missing
4. Reports success/failure

**Output:**
```
🚀 Installing audio-overview skill dependencies...
   ✅ Python 3.11.0 found
   ✅ FFmpeg found
📦 Installing Python packages...
   Using --break-system-packages flag...
⚙️  Creating .env from template...
⚠️  Please configure your API keys in .env file
✅ audio-overview skill installed successfully!
```

### Phase 3: Progressive Disclosure

Claude loads skill in stages:

**Stage 1: SKILL.md Frontmatter**
```yaml
---
name: audio-overview
description: Generate professional multi-speaker podcasts from research materials...
---
```

Claude understands when to use this skill.

**Stage 2: SKILL.md Content**
```markdown
# Audio Overview

Generate professional multi-speaker podcasts...

## When to Use This Skill
- Converting research materials into podcast format
- Creating educational audio content...

## How to Use
...
```

Claude learns skill capabilities and usage patterns.

**Stage 3: Reference Materials** (loaded only if needed)
```
references/
├── system.md              # Detailed podcast writing principles
└── dialogue_generation.md # AI dialogue generation template
```

Claude accesses deep technical details only when required.

### Phase 4: Execution

Claude invokes the skill:

**Method A: Direct Python Call**
```python
from audio_overview.main import generate_podcast

result = generate_podcast(
    content=user_content,
    num_speakers=2,
    duration_minutes=10,
    output_path="podcast.mp3"
)
```

**Method B: CLI Subprocess**
```bash
python audio-overview/main.py \
  --input research.txt \
  --output podcast.mp3 \
  --speakers 2 \
  --duration 10
```

### Phase 5: Output Delivery

Skill generates output:
- `podcast.mp3` - Audio file
- `podcast_script.json` - Transcript

Claude presents results to user.

---

## Automatic Installation Technical Details

### Installation Script Architecture

Every skill has `scripts/install.sh`:

```bash
#!/bin/bash
set -e  # Exit on error

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "🚀 Installing {skill-name} dependencies..."

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    exit 1
fi

# 2. Check FFmpeg (audio/video skills only)
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  Warning: FFmpeg not found"
fi

# 3. Install Python packages (handles externally-managed environments)
if python3 -m pip install -q -r requirements.txt 2>&1 | grep -q "externally-managed"; then
    python3 -m pip install -q --break-system-packages -r requirements.txt
else
    python3 -m pip install -q -r requirements.txt
fi

# 4. Create .env from template
if [ ! -f .env ] && [ -f .env.example ]; then
    cp .env.example .env
    echo "⚠️  Please configure your API keys in .env file"
fi

echo "✅ {skill-name} skill installed successfully!"
exit 0
```

### Handling Different Python Environments

**Problem**: Modern Python (3.11+) uses "externally-managed" environments

**Solution**: Auto-detect and use `--break-system-packages`:

```bash
# Try normal install first
if python3 -m pip install -r requirements.txt 2>&1 | grep -q "externally-managed"; then
    # Fallback to --break-system-packages
    python3 -m pip install --break-system-packages -r requirements.txt
fi
```

**Alternatives** (for stricter environments):
```bash
# Option 1: Virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: User install
pip install --user -r requirements.txt
```

### Master Installation Script

`install_all.sh` orchestrates installation of all 8 skills:

```bash
#!/bin/bash

# 1. Check prerequisites globally
echo "🔍 Checking prerequisites..."
- Python 3.8+? ✅
- FFmpeg? ⚠️ (optional but recommended)

# 2. Install each skill
for skill in audio-overview video-overview mindmap reports flashcards quiz infographic data-table; do
    echo "Installing: $skill"
    bash "$skill/scripts/install.sh"
done

# 3. Report results
echo "✅ Successfully installed: 8 skills"
echo "⚠️  Remember to configure API keys"
```

---

## Configuration Management

### Three-Tier Configuration Priority

Skills load configuration in this order:

**1. Environment Variables** (Highest Priority)
```bash
export GEMINI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Use Case**: Cloud deployments, CI/CD, containers

**2. .env File** (Middle Priority)
```bash
# audio-overview/.env
GEMINI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

**Use Case**: Local development, per-skill configuration

**3. .env.example Template** (Lowest Priority, Fallback)
```bash
# audio-overview/.env.example
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Use Case**: First-time setup, documentation

### Code Implementation

```python
# config.py in each skill
import os
from dotenv import load_dotenv

# Load .env file if exists
load_dotenv()

# Get API keys (environment variables take precedence)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not configured")
```

---

## Skill Isolation Architecture

### Why Isolation Matters

Each skill is **completely independent**:

```
nblm-skills/
├── audio-overview/       ← Isolated
│   ├── main.py          ← No imports from other skills
│   ├── config.py        ← Duplicated utilities
│   ├── requirements.txt ← Independent dependencies
│   └── .env             ← Separate configuration
├── video-overview/       ← Isolated
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env
...
```

**Benefits:**
- ✅ Skills can be used independently
- ✅ No dependency conflicts between skills
- ✅ Easy to add/remove individual skills
- ✅ Parallel development possible
- ✅ Failure in one skill doesn't affect others

**Tradeoff:**
- ❌ Some code duplication (AI provider functions)
- ✅ But: Easier to maintain, test, and deploy

### How Isolation is Maintained

**1. No Shared Code**
```python
# ❌ Bad: Shared utility
from ../utils import call_gemini_api

# ✅ Good: Duplicated in each skill
def call_gemini_api():
    # Implementation in this skill only
```

**2. Independent Dependencies**
```txt
# audio-overview/requirements.txt
google-generativeai==0.8.3
pydub==0.25.1

# video-overview/requirements.txt
google-generativeai==0.8.3
moviepy==1.0.3
```

**3. Separate Configuration**
```bash
# Each skill has its own .env
audio-overview/.env
video-overview/.env
...
```

---

## Cloud Deployment Scenarios

### Scenario 1: GitHub Repository → Claude Code

**Flow:**
1. User clones repository
2. Runs `./install_all.sh`
3. Configures API keys
4. Claude Code loads skills on demand

**Advantages:**
- Simple setup
- Easy updates via `git pull`
- No server management

### Scenario 2: Docker Container

**Flow:**
1. Build image with all skills:
   ```dockerfile
   FROM python:3.11-slim
   RUN apt-get install -y ffmpeg
   COPY . /app
   RUN ./install_all.sh
   ```

2. Run container:
   ```bash
   docker run -e GEMINI_API_KEY=xxx nblm-skills:latest
   ```

**Advantages:**
- Reproducible environment
- Portable across systems
- Easy scaling

### Scenario 3: Cloud VM (AWS/GCP/Azure)

**Flow:**
1. Launch Ubuntu VM
2. Install prerequisites:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip ffmpeg git
   ```

3. Clone and install:
   ```bash
   git clone https://github.com/serenakeyitan/nblm-skills.git
   cd nblm-skills
   ./install_all.sh
   ```

4. Configure environment:
   ```bash
   export GEMINI_API_KEY="..."
   export ANTHROPIC_API_KEY="..."
   ```

**Advantages:**
- Full control
- Persistent storage
- Easy debugging

### Scenario 4: Serverless (Lambda/Cloud Functions)

**Flow:**
1. Package individual skill:
   ```bash
   cd audio-overview
   pip install -r requirements.txt -t package/
   cp main.py config.py package/
   cd package && zip -r ../lambda.zip .
   ```

2. Deploy as Lambda function
3. Invoke via API

**Advantages:**
- Pay per use
- Auto-scaling
- No server management

---

## FAQ: How It Works

### Q: How does Claude know to run install.sh?

**A:** Claude reads `skill.yaml` which specifies `install_script: scripts/install.sh`. On first load, Claude checks if dependencies are installed and runs the script if needed.

### Q: What if a user doesn't run install_all.sh?

**A:** Each skill's `install.sh` can be run independently:
```bash
bash audio-overview/scripts/install.sh
```

Or dependencies install automatically when skill is first invoked by Claude.

### Q: How are API keys managed securely?

**A:**
- `.env` files are gitignored (never committed)
- Environment variables used in production
- `.env.example` provides template without secrets
- Users must add their own keys

### Q: What if FFmpeg is missing?

**A:**
- Installation script warns but continues
- Audio/video skills will fail gracefully
- Other skills work fine
- User can install FFmpeg later: `brew install ffmpeg`

### Q: Can skills work without internet?

**A:** No, all skills require:
- Internet for API calls (Gemini, Claude)
- Gemini 3 Pro for content generation
- Claude Sonnet 4.5 as fallback

### Q: How are dependency conflicts handled?

**A:** Each skill is isolated:
- Independent `requirements.txt`
- No shared dependencies
- Version conflicts only affect individual skills
- Other skills continue working

### Q: Can I use only one skill?

**A:** Yes! Each skill is completely independent:
```bash
cd audio-overview
bash scripts/install.sh
python main.py --test
```

### Q: How do updates work?

**A:**
```bash
git pull origin main
./install_all.sh  # Reinstall with new dependencies
```

Each skill maintains backward compatibility.

---

## Summary

### For Users

**Download skills → Run install_all.sh → Add API keys → Use with Claude**

Everything else is automatic.

### For Claude Code

**Read skill.yaml → Run install.sh → Load SKILL.md → Execute main.py → Return results**

Progressive disclosure ensures efficient loading.

### For Deployment

**Clone repo → Run install script → Configure environment → Deploy (GitHub/Docker/VM/Serverless)**

Flexible deployment options for any infrastructure.

---

## Next Steps

- **Try it**: Clone the repository and run `./install_all.sh`
- **Test**: Run `./test_all_skills.sh` to verify installation
- **Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- **Develop**: See [QUICKSTART.md](QUICKSTART.md) for usage examples

**Repository**: https://github.com/serenakeyitan/nblm-skills
