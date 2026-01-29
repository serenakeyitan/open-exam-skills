---
name: audio-overview
description: Generate professional multi-speaker podcasts from research materials. This skill should be used when users want to create engaging audio content, educational podcasts, or conversational overviews from their research documents.
---

# Audio Overview

Generate professional multi-speaker podcasts from research materials using AI-powered dialogue generation and text-to-speech synthesis.

## When to Use This Skill

Use this skill when:
- Converting research materials into podcast format
- Creating educational audio content from documents
- Generating multi-speaker conversations about complex topics
- Producing engaging audio overviews for learning or sharing

## How to Use

### Quick Test

Run the test mode to verify functionality:

```bash
cd audio-overview
python main.py --test
```

### Generate a Podcast

#### Command Line

```bash
python main.py --input research.txt --output podcast.mp3 --speakers 2 --duration 10
```

Parameters:
- `--input`: Path to research materials (text file)
- `--output`: Output MP3 filename (default: podcast.mp3)
- `--speakers`: Number of speakers 1-4 (default: 2)
- `--duration`: Target length in minutes (default: 10)
- `--tone`: Podcast tone - conversational, educational, professional (default: conversational)

#### Python API

```python
from main import generate_podcast

podcast_path = generate_podcast(
    content="Your research text here...",
    num_speakers=2,
    duration_minutes=10,
    output_path="podcast.mp3"
)
```

### Advanced Customization

Customize speaker personas and episode format:

```python
podcast_path = generate_podcast(
    content="Your research...",
    speakers=[
        {
            "name": "Dr. Sarah Chen",
            "expertise": "Quantum Physics Professor",
            "personality": "Clear and enthusiastic explainer",
            "voice_style": "professional female"
        },
        {
            "name": "Alex Rivera",
            "expertise": "Tech Journalist",
            "personality": "Curious and asks insightful questions",
            "voice_style": "conversational male"
        }
    ],
    episode_profile={
        "topic": "Quantum Computing Fundamentals",
        "format": "educational discussion",
        "target_audience": "tech enthusiasts",
        "key_points": ["superposition", "entanglement", "applications"]
    },
    duration_minutes=15,
    output_path="quantum_podcast.mp3"
)
```

## What Gets Generated

The skill produces two output files:

1. **MP3 Audio File** - Complete podcast with multi-speaker dialogue and professional audio mixing
2. **JSON Script File** - Full transcript with speaker assignments, emotions, and emphasized words

## How It Works

1. **Content Analysis** - AI extracts key themes and concepts from research materials
2. **Dialogue Generation** - Gemini 3 Pro creates natural conversation between speakers
3. **Script Structuring** - Organizes dialogue into proper turn-taking with engagement optimization
4. **Audio Synthesis** - Text-to-speech converts each speaker's lines to audio
5. **Audio Mixing** - Combines tracks with normalization, fade effects, and proper timing

## Configuration

The skill requires API keys configured in the `.env` file (already set up):

```bash
GEMINI_API_KEY=your_gemini_key          # Primary AI for dialogue
ANTHROPIC_API_KEY=your_anthropic_key    # Fallback AI
ELEVENLABS_API_KEY=your_elevenlabs_key  # Optional: Premium voices
```

## Reference Materials

Detailed system prompts and dialogue generation templates are available in `references/`:

- `references/system.md` - Core podcast writing principles and best practices
- `references/dialogue_generation.md` - Template for AI dialogue generation

To review these prompts or customize dialogue style, read and modify the reference files.

## Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Key dependencies:
- **google-generativeai** - Gemini API for dialogue generation
- **anthropic** - Claude API (fallback)
- **pydub** - Audio processing and mixing
- **gTTS** - Text-to-speech synthesis
- **elevenlabs** - Optional premium TTS
- **FFmpeg** - Required system dependency for audio processing

## Performance and Limitations

**Generation Time**: 2-5 minutes for a 10-minute podcast

**Content Limit**: Up to 100,000 tokens of input

**Output Length**: Configurable from 5-60 minutes

**Audio Quality**: 192 kbps MP3, 44.1kHz stereo, normalized

**Limitations**:
- TTS voices may sound synthetic without ElevenLabs upgrade
- Technical jargon may be mispronounced
- No background music (add in post-production if needed)
- Pre-scripted dialogue only (not real-time conversation)

## Tips for Best Results

- Provide well-structured, clear source material
- Define specific episode goals and target audience
- Use 2-3 speakers for optimal engagement (4+ can feel crowded)
- Target 10-20 minutes for best listener engagement
- Give speakers distinct personalities and expertise areas
- Review the JSON script before final audio generation if needed

## Example Use Cases

**Research Paper Summary**: Convert academic papers into accessible podcast discussions

**Educational Content**: Transform course materials into engaging audio lectures

**Meeting Summaries**: Turn meeting notes into podcast-style recaps

**Book Reviews**: Create conversational book summaries and analysis

**Industry Updates**: Generate news-style podcasts from industry reports
