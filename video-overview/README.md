# Video Overview Skill

Create narrated videos with visual slides from your research materials using AI. This skill transforms complex content into engaging video presentations with professional narration and visual elements.

## Features

- **Automatic Storyboard Generation**: AI extracts key points and creates visual flow
- **Visual Slide Creation**: Generate text slides with titles, bullet points, and key messages
- **Voice Narration**: Professional TTS narration synchronized with slides
- **Multiple Styles**: Educational, professional, entertaining, or documentary styles
- **Custom Branding**: Configurable colors, fonts, and visual themes
- **Export Formats**: MP4 video with configurable resolution and quality

## Installation

```bash
cd video-overview
pip install -r requirements.txt
```

### System Requirements

- **FFmpeg**: Required for video processing
  ```bash
  # macOS
  brew install ffmpeg

  # Ubuntu/Debian
  sudo apt-get install ffmpeg

  # Windows
  # Download from https://ffmpeg.org/download.html
  ```

## Configuration

Create a `.env` file in this directory:

```bash
# Required: Primary AI for content generation
GEMINI_API_KEY=your_gemini_api_key

# Optional: Fallback AI
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional: Enhanced voice quality
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Usage

### As a Claude Code Skill

```
User: Create a video overview of this research paper on climate change
```

### As a Python Module

```python
from main import generate_video_overview

# Basic usage
video_path = generate_video_overview(
    content="Your research materials...",
    output_path="overview.mp4"
)

# Advanced usage
video_path = generate_video_overview(
    content="Your research materials...",
    title="Climate Change: Key Findings",
    style="professional",
    duration_minutes=5,
    video_config={
        "resolution": "1920x1080",
        "fps": 30,
        "background_color": "#1a1a2e",
        "text_color": "#ffffff",
        "accent_color": "#00adb5"
    },
    narration_config={
        "voice": "professional female",
        "speed": 1.0,
        "pause_between_slides": 1.0
    },
    output_path="climate_video.mp4"
)

print(f"Video generated: {video_path}")
```

### Command Line

```bash
python main.py \
  --input research.txt \
  --output video.mp4 \
  --title "Research Overview" \
  --style professional \
  --duration 5
```

## Video Styles

### Educational
- Clear, structured presentation
- Emphasis on key concepts
- Step-by-step explanation
- Visual hierarchy with bullet points

### Professional
- Corporate-style aesthetics
- Clean and minimal design
- Professional color schemes
- Business-appropriate tone

### Entertaining
- Dynamic visuals
- Engaging transitions
- Vibrant colors
- Conversational narration

### Documentary
- Cinematic aesthetic
- Narrative storytelling
- Dramatic pacing
- Rich visual elements

## Slide Types

The skill automatically generates different slide types:

1. **Title Slide**: Introduction with main topic
2. **Key Points**: Bullet-point summaries
3. **Quote Slides**: Important statements or findings
4. **Data Slides**: Statistics and numbers
5. **Transition Slides**: Section breaks
6. **Conclusion Slide**: Closing summary

## How It Works

1. **Content Analysis**: AI analyzes your materials and extracts key themes
2. **Storyboard Creation**: Generates sequence of slides with narration script
3. **Slide Generation**: Creates visual slides with text and design
4. **Narration Synthesis**: Converts script to speech with TTS
5. **Video Assembly**: Combines slides and audio into synchronized video
6. **Export**: Renders final MP4 video

## Examples

### Example 1: Research Paper Summary

```python
video = generate_video_overview(
    content=open("paper.pdf").read(),
    title="Quantum Computing: A New Era",
    style="educational",
    duration_minutes=5,
    output_path="quantum_video.mp4"
)
```

### Example 2: Multi-Source Compilation

```python
# Combine multiple sources
sources = [
    open("article1.txt").read(),
    open("article2.txt").read(),
    open("notes.md").read()
]
content = "\n\n---\n\n".join(sources)

video = generate_video_overview(
    content=content,
    title="AI Safety: A Comprehensive Overview",
    style="professional",
    duration_minutes=10,
    output_path="ai_safety_video.mp4"
)
```

### Example 3: Custom Branding

```python
video = generate_video_overview(
    content="Your research...",
    title="Company Research Briefing",
    style="professional",
    video_config={
        "resolution": "1920x1080",
        "background_color": "#0a0a0a",
        "text_color": "#e0e0e0",
        "accent_color": "#ff6b6b",
        "font_family": "Arial",
        "logo_path": "company_logo.png"  # Optional branding
    },
    output_path="briefing.mp4"
)
```

## Configuration Options

### Video Configuration

```python
video_config = {
    "resolution": "1920x1080" | "1280x720" | "3840x2160",
    "fps": 24 | 30 | 60,
    "background_color": "#hex_color",
    "text_color": "#hex_color",
    "accent_color": "#hex_color",
    "font_family": "font_name",
    "font_size_title": 72,
    "font_size_body": 36,
    "logo_path": "optional_logo.png",
    "slide_duration": 5.0  # seconds per slide (adjusted by narration)
}
```

### Narration Configuration

```python
narration_config = {
    "voice": "professional female" | "conversational male" | "authoritative",
    "speed": 0.8 - 1.2,  # Speech rate
    "pause_between_slides": 0.5 - 2.0,  # seconds
    "emphasis_words": ["list", "of", "words", "to", "emphasize"]
}
```

## Output Formats

- **MP4** (default): H.264 codec, optimized for web and playback
- **Resolution**: 1080p (default), 720p, or 4K
- **Audio**: AAC codec, 192 kbps

## Technical Details

### AI Models Used
- **Content Analysis**: Gemini 3 Pro or Claude Sonnet 4.5
- **Narration**: Google TTS, ElevenLabs, or gTTS

### Video Processing
- **Library**: MoviePy with FFmpeg backend
- **Image Generation**: Pillow (PIL)
- **Rendering**: CPU-based (GPU acceleration not required)

### Performance
- Typical generation time: 3-7 minutes for a 5-minute video
- Content limit: Up to 50,000 tokens
- Recommended duration: 3-10 minutes

## Limitations

- No animated graphics (static slides only)
- No background music (can be added in post-production)
- No video clips or stock footage (text slides only)
- Narration may sound synthetic with basic TTS

## Tips for Best Results

1. **Content Quality**: Well-structured input produces better videos
2. **Duration**: 5-7 minutes is optimal for engagement
3. **Style**: Choose style that matches your audience
4. **Resolution**: Use 1080p for general purposes
5. **Voice**: ElevenLabs provides most natural narration
6. **Review**: Check storyboard before final rendering

## Troubleshooting

**Issue**: FFmpeg not found
- **Solution**: Install FFmpeg (see System Requirements)

**Issue**: Video rendering is slow
- **Solution**: Reduce resolution or frame rate

**Issue**: Text too small or cut off
- **Solution**: Adjust font sizes in video_config

**Issue**: Narration too fast/slow
- **Solution**: Adjust speed in narration_config

## Advanced Features

### Custom Slide Templates

```python
# Define custom slide template
template = {
    "background": "#1a1a2e",
    "title_font": "Helvetica Bold",
    "body_font": "Helvetica",
    "layout": "centered" | "left-aligned" | "grid"
}

video = generate_video_overview(
    content="...",
    slide_template=template
)
```

### Storyboard Preview

```python
# Generate storyboard without rendering video
storyboard = generate_storyboard_only(
    content="...",
    output_path="storyboard.json"
)

# Review and edit storyboard, then render
video = render_from_storyboard(
    storyboard_path="storyboard.json",
    output_path="video.mp4"
)
```

## Credits

Inspired by Google NotebookLM's Video Overview feature.

## License

MIT License
