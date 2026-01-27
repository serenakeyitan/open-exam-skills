# Testing Guide

Complete guide to testing all skills in the nblm-skills repository.

## Prerequisites

1. **Install System Dependencies**
```bash
# Install FFmpeg (required for audio/video skills)
brew install ffmpeg
```

2. **Configure API Keys**

Each skill needs API keys. You have two options:

**Option A: Set Environment Variables Globally**
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
```

**Option B: Create .env File in Each Skill**
```bash
# For each skill directory
cd audio-overview
cp .env.example .env
# Edit .env and add your API keys
```

## Test All Skills at Once

Run the automated test script:

```bash
cd /Users/keyitan/nblm-skills
chmod +x test_all_skills.sh
./test_all_skills.sh
```

## Test Individual Skills

### 1. Audio Overview (Podcast Generation)

```bash
cd audio-overview
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_podcast.mp3` (4-5 MB, ~2 minutes)
- `test_podcast_script.json` (dialogue transcript)

**Time**: ~2-3 minutes

---

### 2. Video Overview (Narrated Video)

```bash
cd video-overview
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_video.mp4` (10-15 MB, ~2 minutes)
- `test_video_storyboard.json` (slide sequence)

**Time**: ~3-5 minutes

---

### 3. Mind Map (Concept Visualization)

```bash
cd mindmap
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_mindmap.html` (interactive mind map)

**Time**: ~30 seconds

---

### 4. Reports (Professional Documents)

```bash
cd reports
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_report.md` (formatted report)

**Time**: ~30 seconds

---

### 5. Flashcards (Study Cards)

```bash
cd flashcards
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_flashcards.html` (interactive flashcards)

**Time**: ~30 seconds

---

### 6. Quiz (Interactive Assessment)

```bash
cd quiz
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_quiz.html` (interactive quiz)

**Time**: ~30 seconds

---

### 7. Infographic (Visual Summary)

```bash
cd infographic
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_infographic.png` (visual infographic)

**Time**: ~1 minute

---

### 8. Data Table (Structured Data)

```bash
cd data-table
pip install -r requirements.txt
python main.py --test
```

**Expected Output:**
- `test_data.xlsx` (Excel spreadsheet)

**Time**: ~30 seconds

---

## Test with Your Own Content

Each skill accepts custom input:

```bash
# Audio Overview - Generate podcast from research paper
cd audio-overview
python main.py --input your_research.txt --output my_podcast.mp3 --duration 15

# Video Overview - Create video from document
cd video-overview
python main.py --input your_doc.txt --output my_video.mp4 --duration 7

# Mind Map - Visualize concepts
cd mindmap
python main.py --input your_notes.txt --output mindmap.html

# Reports - Generate professional report
cd reports
python main.py --input research.txt --output report.pdf --type executive_summary

# Flashcards - Create study materials
cd flashcards
python main.py --input textbook.txt --output cards.apkg --num 50

# Quiz - Generate assessment
cd quiz
python main.py --input study_material.txt --output quiz.html --num 20 --difficulty hard

# Infographic - Visual summary
cd infographic
python main.py --input data.txt --output infographic.png --style modern

# Data Table - Extract structured data
cd data-table
python main.py --input research.txt --output data.xlsx
```

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```bash
# Install dependencies
pip install -r requirements.txt

# If permission errors, use:
python3 -m pip install --break-system-packages -r requirements.txt
```

**2. FFmpeg Not Found**
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Windows
# Download from: https://ffmpeg.org/download.html
```

**3. API Key Errors**
```bash
# Check if keys are set
echo $GEMINI_API_KEY
echo $ANTHROPIC_API_KEY

# Or check .env file exists
ls -la .env
cat .env
```

**4. Permission Denied on Scripts**
```bash
chmod +x test_all_skills.sh
```

**5. MoviePy Version Issues**
```bash
# Downgrade to compatible version
pip install moviepy==1.0.3
```

## Performance Expectations

| Skill | Test Time | Output Size |
|-------|-----------|-------------|
| audio-overview | 2-3 min | 4-5 MB |
| video-overview | 3-5 min | 10-15 MB |
| mindmap | 30 sec | 50-100 KB |
| reports | 30 sec | 10-20 KB |
| flashcards | 30 sec | 50-100 KB |
| quiz | 30 sec | 50-100 KB |
| infographic | 1 min | 500 KB - 2 MB |
| data-table | 30 sec | 10-50 KB |

**Total Test Time**: ~10-15 minutes for all skills

## Verification

After testing, verify outputs:

```bash
# List all generated test files
find . -name "test_*" -type f

# Check audio file
open audio-overview/test_podcast.mp3

# Check video file
open video-overview/test_video.mp4

# Check HTML outputs
open mindmap/test_mindmap.html
open flashcards/test_flashcards.html
open quiz/test_quiz.html

# Check data files
open data-table/test_data.xlsx

# Check images
open infographic/test_infographic.png
```

## Clean Up Test Files

```bash
# Remove all test outputs
find . -name "test_*" -delete

# Or remove from specific skill
cd audio-overview
rm test_*
```

## CI/CD Integration

Add to your CI pipeline:

```yaml
# .github/workflows/test.yml
name: Test Skills
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install FFmpeg
        run: sudo apt-get install -y ffmpeg
      - name: Test All Skills
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: ./test_all_skills.sh
```

## Next Steps

- Test with your own research materials
- Customize output formats and styles
- Integrate skills into your workflow
- Report issues on GitHub
