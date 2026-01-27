# NotebookLM Skills Suite

A collection of Claude Code skills that replicate Google NotebookLM features for AI-powered research and content generation. Each skill is fully isolated and stateless, designed to work seamlessly with Claude Code.

## Features

Transform your research materials into various formats:

- **Audio Overview**: Multi-speaker podcast generation with customizable personas
- **Video Overview**: Narrated videos with visual slides and animations
- **Mind Map**: Interactive hierarchical concept visualizations
- **Reports**: Structured documents with professional formatting
- **Flashcards**: Study cards with Q&A pairs for learning
- **Quiz**: Generated quizzes with multiple question types
- **Infographic**: Visual data summaries with statistics and charts
- **Data Table**: Structured data extraction to CSV/Excel/JSON

## Quick Start

### Automatic Installation (Recommended)

Install all 8 skills with a single command:

```bash
git clone https://github.com/serenakeyitan/nblm-skills.git
cd nblm-skills
./install_all.sh
```

This automatically:
- ✅ Checks prerequisites (Python, FFmpeg)
- ✅ Installs all dependencies for 8 skills
- ✅ Creates .env templates
- ✅ Verifies installation

### Manual Installation

If you prefer to install skills individually:

```bash
cd audio-overview
bash scripts/install.sh
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

### Configuration

**Option 1: Environment Variables (Recommended for Cloud)**
```bash
export GEMINI_API_KEY="your_gemini_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
```

**Option 2: .env Files (Recommended for Local)**
```bash
cd audio-overview
cp .env.example .env
# Edit .env and add your API keys
```

### Usage with Claude Code

Each skill is registered with Claude Code. Simply invoke the skill name:

```bash
# Generate a podcast from your research
claude-code --skill audio-overview

# Create a mind map
claude-code --skill mindmap

# Generate flashcards for studying
claude-code --skill flashcards
```

Or use the skill name directly in Claude Code conversations.

## Skills Overview

### 1. Audio Overview
**Directory**: `audio-overview/`

Generate professional multi-speaker podcasts from your research materials.

**Features:**
- Customizable speaker personas (1-4 speakers)
- Adjustable episode length and tone
- Professional audio mixing
- Support for Google TTS and ElevenLabs

**Example:**
```python
from audio_overview import generate_podcast

podcast = generate_podcast(
    content="Your research materials...",
    speakers=2,
    duration="10 minutes",
    output_path="research_podcast.mp3"
)
```

**See**: [audio-overview/README.md](audio-overview/README.md)

---

### 2. Video Overview
**Directory**: `video-overview/`

Create narrated videos with visual slides from your content.

**Features:**
- Automatic storyboard generation
- Visual slide creation
- Voice narration
- MP4 export

**Example:**
```python
from video_overview import generate_video

video = generate_video(
    content="Your research materials...",
    style="professional",
    output_path="research_video.mp4"
)
```

**See**: [video-overview/README.md](video-overview/README.md)

---

### 3. Mind Map
**Directory**: `mindmap/`

Generate interactive mind maps from your research.

**Features:**
- Hierarchical concept extraction
- Relationship mapping
- Multiple export formats (HTML, PNG, Mermaid)
- Interactive visualization

**Example:**
```python
from mindmap import generate_mindmap

mindmap = generate_mindmap(
    content="Your research materials...",
    format="html",
    output_path="research_mindmap.html"
)
```

**See**: [mindmap/README.md](mindmap/README.md)

---

### 4. Reports
**Directory**: `reports/`

Create structured professional reports.

**Features:**
- Multiple report types (executive summary, research brief, analysis)
- Professional formatting
- Citation management
- Export to Markdown, PDF, DOCX

**Example:**
```python
from reports import generate_report

report = generate_report(
    content="Your research materials...",
    report_type="executive_summary",
    output_path="research_report.pdf"
)
```

**See**: [reports/README.md](reports/README.md)

---

### 5. Flashcards
**Directory**: `flashcards/`

Generate study flashcards from your materials.

**Features:**
- Question-answer pair extraction
- Difficulty categorization
- Anki/Quizlet export
- Interactive HTML viewer

**Example:**
```python
from flashcards import generate_flashcards

cards = generate_flashcards(
    content="Your research materials...",
    num_cards=20,
    output_path="flashcards.apkg"
)
```

**See**: [flashcards/README.md](flashcards/README.md)

---

### 6. Quiz
**Directory**: `quiz/`

Generate quizzes with multiple question types.

**Features:**
- Multiple choice, true/false, short answer
- Difficulty levels
- Answer keys with explanations
- Interactive HTML interface

**Example:**
```python
from quiz import generate_quiz

quiz = generate_quiz(
    content="Your research materials...",
    num_questions=10,
    difficulty="medium",
    output_path="quiz.html"
)
```

**See**: [quiz/README.md](quiz/README.md)

---

### 7. Infographic
**Directory**: `infographic/`

Create visual infographics from your data.

**Features:**
- Key statistics extraction
- Professional layouts
- Charts and icons
- PNG/SVG export

**Example:**
```python
from infographic import generate_infographic

infographic = generate_infographic(
    content="Your research materials...",
    style="modern",
    output_path="infographic.png"
)
```

**See**: [infographic/README.md](infographic/README.md)

---

### 8. Data Table
**Directory**: `data-table/`

Extract structured data into tables.

**Features:**
- Entity extraction
- Relationship mapping
- Multi-table support
- Export to CSV, JSON, Excel

**Example:**
```python
from data_table import extract_data_table

table = extract_data_table(
    content="Your research materials...",
    output_path="data.xlsx"
)
```

**See**: [data-table/README.md](data-table/README.md)

---

## Architecture

### Design Principles

1. **Fully Isolated**: Each skill is completely independent with no shared code
2. **Stateless**: No databases or persistent storage required
3. **AI-Powered**: Powered by Gemini 3 Pro (primary) and Claude Sonnet 4.5 (fallback)
4. **Professional Quality**: Based on patterns from the excellent [Open Notebook](https://github.com/lfnovo/open-notebook) project

### Project Structure

```
nblm-skills/
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── audio-overview/          # Podcast generation skill
│   ├── README.md
│   ├── skill.yaml
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   └── prompts/
├── video-overview/          # Video generation skill
│   └── ...
├── mindmap/                 # Mind map generation skill
│   └── ...
├── reports/                 # Report generation skill
│   └── ...
├── flashcards/              # Flashcard generation skill
│   └── ...
├── quiz/                    # Quiz generation skill
│   └── ...
├── infographic/             # Infographic generation skill
│   └── ...
└── data-table/              # Data extraction skill
    └── ...
```

### Technology Stack

- **Language**: Python 3.10+
- **AI Models**:
  - Gemini 3 Pro (primary for generation)
  - Claude Sonnet 4.5 (fallback)
- **Audio**: Google TTS, ElevenLabs
- **Video**: FFmpeg, MoviePy, Pillow
- **Data**: Pandas, OpenPyXL
- **Validation**: Pydantic

## Cloud Deployment

This skills suite is designed for easy deployment in cloud environments and integration with Claude Code.

### Deployment Options

1. **GitHub Repository** (Recommended for Claude Code)
   - Clone and install with `./install_all.sh`
   - Skills load automatically when Claude invokes them
   - Easy updates with `git pull`

2. **Docker Container**
   - Build: `docker build -t nblm-skills:latest .`
   - Run: `docker run -e GEMINI_API_KEY=xxx nblm-skills:latest`

3. **Cloud VM** (AWS, GCP, Azure)
   - Deploy on Ubuntu/Debian instance
   - Install FFmpeg: `sudo apt-get install ffmpeg`
   - Run `./install_all.sh`

4. **Serverless** (AWS Lambda, Cloud Functions)
   - Deploy individual skills as functions
   - See DEPLOYMENT.md for detailed instructions

### For Claude Code Users

When you download and use these skills:

1. **Automatic Installation**: Each skill has `scripts/install.sh` that runs automatically
2. **Dependency Management**: All Python packages install on first use
3. **Configuration**: Uses `.env.example` as template
4. **Isolation**: Each skill is completely independent

**See**: [DEPLOYMENT.md](DEPLOYMENT.md) for complete cloud deployment guide, Docker configurations, and production best practices.

---

## Configuration

Each skill uses environment variables for API keys. Create a `.env` file in each skill directory:

```bash
# Primary AI provider
GEMINI_API_KEY=your_gemini_api_key

# Fallback AI provider
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional: For audio features
ELEVENLABS_API_KEY=your_elevenlabs_key
```

**Security Note**: Never commit `.env` files to version control. API keys are already in `.gitignore`.

## Development

### Adding a New Skill

1. Create a new directory for your skill
2. Copy the template structure:
   ```bash
   mkdir my-skill
   cd my-skill
   touch README.md skill.yaml requirements.txt main.py config.py
   mkdir prompts
   ```
3. Implement your skill following the isolation rules:
   - No imports from other skills
   - No shared configuration files
   - Self-contained dependencies in `requirements.txt`

### Testing

Each skill includes usage examples in its README. Test individually:

```bash
cd audio-overview
python main.py --test
```

## Credits

Inspired by:
- [Open Notebook](https://github.com/lfnovo/open-notebook) - Excellent open-source NotebookLM alternative
- Google NotebookLM - Original inspiration for features

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Maintain skill isolation (no shared code)
2. Include comprehensive tests and examples
3. Update documentation
4. Follow existing code style

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
