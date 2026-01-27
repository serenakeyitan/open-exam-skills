# Quick Start Guide

Get started with NotebookLM Skills Suite in minutes.

## Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd nblm-skills
```

### 2. Choose a Skill

Navigate to any skill directory:

```bash
cd audio-overview  # or video-overview, mindmap, etc.
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the skill directory:

```bash
# Copy example and edit
cp .env.example .env

# Edit with your API keys
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note**: Replace the placeholder values with your actual API keys.

### 5. Test the Skill

Run in test mode:

```bash
python main.py --test
```

This will generate sample output to verify everything works.

## Usage Examples

### Audio Overview (Podcast Generation)

```bash
# Create a podcast from your research
python main.py --input research.txt --output podcast.mp3 --speakers 2 --duration 10

# Or with Python
from main import generate_podcast
podcast = generate_podcast(
    content=open("research.txt").read(),
    num_speakers=2,
    duration_minutes=10,
    output_path="podcast.mp3"
)
```

**Output**: `podcast.mp3` + `podcast_script.json`

---

### Video Overview

```bash
cd ../video-overview

# Generate narrated video with slides
python main.py --input research.txt --output video.mp4 --title "Research Overview"

# Or with Python
from main import generate_video_overview
video = generate_video_overview(
    content=open("research.txt").read(),
    title="My Research",
    style="professional",
    output_path="video.mp4"
)
```

**Output**: `video.mp4` + `video_storyboard.json`

**Requirements**: FFmpeg must be installed
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`

---

### Mind Map

```bash
cd ../mindmap

# Generate interactive mind map
python main.py --input research.txt --output mindmap.html

# Or Mermaid diagram
python main.py --input research.txt --output mindmap.md --format mermaid
```

**Output**: Interactive HTML or Mermaid markdown

---

### Reports

```bash
cd ../reports

# Generate professional report
python main.py --input research.txt --output report.pdf --type executive_summary

# Formats: .md, .pdf, .docx
python main.py --input research.txt --output report.docx
```

**Output**: Structured report in specified format

---

### Flashcards

```bash
cd ../flashcards

# Generate study flashcards
python main.py --input research.txt --output flashcards.html --num 20

# Or Anki deck
python main.py --input research.txt --output flashcards.apkg --num 30
```

**Output**: Interactive HTML or Anki deck (.apkg)

---

### Quiz

```bash
cd ../quiz

# Generate interactive quiz
python main.py --input research.txt --output quiz.html --num 10 --difficulty medium

# Difficulty levels: easy, medium, hard
```

**Output**: Interactive HTML quiz with answer checking

---

### Infographic

```bash
cd ../infographic

# Generate visual infographic
python main.py --input research.txt --output infographic.png --style modern

# Styles: modern, professional, minimal
```

**Output**: PNG image (1200x1600)

---

### Data Table

```bash
cd ../data-table

# Extract structured data
python main.py --input research.txt --output data.xlsx

# Formats: .csv, .xlsx, .json
python main.py --input research.txt --output data.csv
```

**Output**: Structured data table

---

## Using with Claude Code

All skills are registered with Claude Code. Invoke them in your Claude Code conversations:

```
User: Generate a podcast from this research paper about quantum computing
Claude Code: [Invokes audio-overview skill]

User: Create a mind map of the key concepts
Claude Code: [Invokes mindmap skill]

User: Make flashcards for studying
Claude Code: [Invokes flashcards skill]
```

## Tips

### 1. Content Sources

Skills accept text content from:
- Plain text files (.txt, .md)
- Copied text
- Multiple files (concatenate with `\n\n---\n\n`)

### 2. Quality Input = Quality Output

- Well-structured content produces better results
- Include clear sections and headings
- Remove irrelevant information

### 3. Optimal Lengths

- **Podcasts**: 10-20 minutes (best engagement)
- **Videos**: 5-7 minutes (optimal attention span)
- **Flashcards**: 20-30 cards per topic
- **Quizzes**: 10-15 questions

### 4. API Keys

The provided API keys are pre-configured:
- **Gemini 3 Pro**: Primary for content generation
- **Claude Sonnet 4.5**: Fallback

No additional setup needed!

### 5. Output Formats

Choose formats based on use case:
- **HTML**: Interactive, shareable, no software required
- **PDF**: Professional, printable
- **JSON**: Programmatic access, further processing
- **Anki (.apkg)**: Direct import to Anki app

### 6. Batch Processing

Process multiple files:

```bash
# Process all files in a directory
for file in inputs/*.txt; do
    python main.py --input "$file" --output "outputs/$(basename $file .txt).mp3"
done
```

### 7. Customization

Each skill supports customization:

```python
# Audio Overview - Custom speakers
from main import generate_podcast
podcast = generate_podcast(
    content=content,
    speakers=[
        {"name": "Dr. Smith", "expertise": "Physicist", "personality": "Clear explainer"},
        {"name": "Jane", "expertise": "Science journalist", "personality": "Curious"}
    ],
    output_path="custom_podcast.mp3"
)

# Video Overview - Custom branding
from main import generate_video_overview
video = generate_video_overview(
    content=content,
    video_config={
        "background_color": "#000000",
        "accent_color": "#ff0000"
    },
    output_path="branded_video.mp4"
)
```

## Troubleshooting

### Issue: "No API key found"

**Solution**: Ensure `.env` file exists in the skill directory with correct keys

```bash
cd your-skill
cat .env  # Check file exists
```

### Issue: "FFmpeg not found" (video-overview)

**Solution**: Install FFmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows - Download from https://ffmpeg.org/
```

### Issue: "Module not found"

**Solution**: Install requirements

```bash
pip install -r requirements.txt
```

### Issue: Output quality is poor

**Solutions**:
1. Improve input content (add structure, clarity)
2. Adjust parameters (increase duration, number of items)
3. Try different difficulty/style settings

### Issue: Generation is slow

**Expected**:
- Podcasts: 2-5 minutes
- Videos: 3-7 minutes
- Other skills: 30-120 seconds

**Tips**:
- Reduce output length
- Use shorter input content
- Check internet connection (API calls)

## Next Steps

1. **Explore Each Skill**: Try test mode for each skill
2. **Process Real Content**: Use your own research materials
3. **Customize**: Experiment with parameters and styles
4. **Integrate**: Use skills in your workflow
5. **Combine**: Use multiple skills on the same content

## Examples

### Complete Workflow Example

```bash
# Start with research paper
INPUT="quantum_computing_paper.txt"

# 1. Generate overview podcast
cd audio-overview
python main.py -i ../$INPUT -o podcast.mp3 -d 15

# 2. Create visual video
cd ../video-overview
python main.py -i ../$INPUT -o video.mp4

# 3. Make mind map
cd ../mindmap
python main.py -i ../$INPUT -o mindmap.html

# 4. Generate study materials
cd ../flashcards
python main.py -i ../$INPUT -o flashcards.html -n 30

cd ../quiz
python main.py -i ../$INPUT -o quiz.html -n 15

# 5. Create report
cd ../reports
python main.py -i ../$INPUT -o report.pdf

# 6. Extract data
cd ../data-table
python main.py -i ../$INPUT -o data.xlsx

# 7. Make infographic
cd ../infographic
python main.py -i ../$INPUT -o infographic.png
```

Now you have a complete content package!

## Support

For issues or questions:
1. Check skill README in each directory
2. Review error messages carefully
3. Open GitHub issue with details

## License

MIT License - See LICENSE file
