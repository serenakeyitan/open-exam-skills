---
name: video-overview
description: Create narrated videos with visual slides from research materials. This skill should be used when users want to transform documents into engaging video presentations with professional narration and synchronized visuals.
---

# Video Overview

Generate narrated videos with visual slides from research materials using AI-powered storyboard generation, slide design, and text-to-speech narration.

## When to Use This Skill

Use this skill when:
- Creating video presentations from research documents
- Producing educational video content
- Generating visual overviews for presentations or sharing
- Converting written content into engaging video format

## How to Use

### Quick Test

```bash
cd video-overview
python main.py --test
```

### Generate a Video

```bash
python main.py --input research.txt --output video.mp4 --title "Research Overview" --duration 5
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output MP4 filename (default: video.mp4)
- `--title`: Video title (default: "Research Overview")
- `--style`: Visual style - professional, educational, modern (default: professional)
- `--duration`: Target length in minutes (default: 5)

### Python API

```python
from main import generate_video_overview

video_path = generate_video_overview(
    content="Your research...",
    title="Climate Change Analysis",
    style="professional",
    duration_minutes=7,
    video_config={
        "resolution": "1920x1080",
        "fps": 30,
        "background_color": "#1a1a2e",
        "text_color": "#ffffff",
        "accent_color": "#00adb5"
    },
    output_path="climate_video.mp4"
)
```

## What Gets Generated

1. **MP4 Video File** - Complete video with synchronized narration and visual slides
2. **JSON Storyboard** - Slide sequence with narration and timing

## How It Works

1. **Storyboard Generation** - AI creates slide sequence from content
2. **Slide Design** - Generates visual slides with typography and layout
3. **Narration Synthesis** - TTS converts narration script to audio
4. **Video Assembly** - Combines slides and audio with proper timing
5. **Export** - Renders final MP4 video with H.264 codec

## Configuration

Requires `.env` file with API keys (already configured):

```bash
GEMINI_API_KEY=your_key          # Primary AI
ANTHROPIC_API_KEY=your_key       # Fallback
ELEVENLABS_API_KEY=your_key      # Optional premium TTS
```

## Dependencies

Install requirements:

```bash
pip install -r requirements.txt
```

**System Requirements**:
- FFmpeg (required for video processing)
- Install: `brew install ffmpeg` (macOS) or `apt-get install ffmpeg` (Linux)

Key dependencies:
- **moviepy==1.0.3** - Video processing
- **Pillow** - Image/slide generation
- **google-generativeai** - Gemini API
- **gTTS** - Text-to-speech

## Performance

- Generation time: 3-7 minutes for 5-minute video
- Content limit: 50,000 tokens
- Recommended duration: 3-10 minutes
- Output: 1080p MP4, H.264, AAC audio

## Limitations

- Static slides only (no animations)
- No background music included
- No video clips or stock footage
- Basic TTS narration (upgrade to ElevenLabs for quality)
