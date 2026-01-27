# Audio Overview Skill

Generate professional multi-speaker podcasts from your research materials using AI. This skill creates engaging conversational content with customizable speaker personas, professional audio quality, and natural dialogue flow.

## Features

- **Multi-Speaker Support**: 1-4 customizable speakers with unique personalities
- **Persona Customization**: Define expertise, personality traits, and speaking styles
- **Episode Configuration**: Control length, tone, format, and target audience
- **Professional Quality**: Natural dialogue with proper turn-taking and engagement
- **Multiple TTS Providers**: Google TTS (default) and ElevenLabs support
- **Audio Mixing**: Professional audio post-processing and normalization

## Installation

```bash
cd audio-overview
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in this directory:

```bash
# Required: Primary AI for dialogue generation
GEMINI_API_KEY=your_gemini_api_key

# Optional: Fallback AI
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional: Enhanced voice quality
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Usage

### As a Claude Code Skill

Simply invoke the skill in your Claude Code conversation:

```
User: Generate a podcast from this research paper about quantum computing
```

### As a Python Module

```python
from main import generate_podcast

# Basic usage
podcast_path = generate_podcast(
    content="Your research materials here...",
    output_path="my_podcast.mp3"
)

# Advanced usage with customization
podcast_path = generate_podcast(
    content="Your research materials here...",
    num_speakers=3,
    duration_minutes=15,
    tone="conversational",
    episode_profile={
        "topic": "Quantum Computing Breakthroughs",
        "format": "educational discussion",
        "target_audience": "tech enthusiasts",
        "key_points": ["superposition", "entanglement", "applications"]
    },
    speakers=[
        {
            "name": "Dr. Sarah Chen",
            "expertise": "Quantum Physics Professor",
            "personality": "Enthusiastic and clear explainer",
            "voice_style": "professional female"
        },
        {
            "name": "Alex Martinez",
            "expertise": "Tech Journalist",
            "personality": "Curious and asks great questions",
            "voice_style": "conversational male"
        }
    ],
    output_path="quantum_podcast.mp3"
)

print(f"Podcast generated: {podcast_path}")
```

### Command Line

```bash
python main.py \
  --input research.txt \
  --output podcast.mp3 \
  --speakers 2 \
  --duration 10 \
  --tone conversational
```

## Speaker Personas

### Default Speakers

The skill includes professional default personas:

1. **Host (Primary)**: Experienced facilitator who guides the conversation
2. **Expert**: Deep knowledge specialist who explains concepts
3. **Questioner** (optional): Asks clarifying questions for the audience
4. **Analyst** (optional): Provides critical analysis and alternative perspectives

### Custom Speakers

Define custom speakers with:

```python
speaker = {
    "name": "Speaker Name",
    "expertise": "Their field of knowledge",
    "personality": "Communication style and traits",
    "voice_style": "Voice characteristics for TTS",
    "accent": "Optional: regional accent"
}
```

## Episode Profiles

Control the podcast format:

```python
episode_profile = {
    "topic": "Main subject of discussion",
    "format": "interview | panel | educational | storytelling",
    "tone": "casual | professional | academic | entertaining",
    "target_audience": "Who is this for?",
    "duration": "Target length (will be approximate)",
    "key_points": ["List", "of", "main", "topics"],
    "intro_style": "How to open the episode",
    "outro_style": "How to close the episode"
}
```

## Output Formats

- **MP3**: Compressed audio (default, recommended)
- **WAV**: Uncompressed high-quality audio
- **Script**: Text transcript of the dialogue (JSON)

## Examples

### Example 1: Research Paper Summary

```python
podcast = generate_podcast(
    content=open("paper.pdf").read(),
    num_speakers=2,
    duration_minutes=10,
    tone="educational",
    output_path="paper_summary.mp3"
)
```

### Example 2: Multi-Source Deep Dive

```python
# Combine multiple sources
content = "\n\n---\n\n".join([
    open("article1.txt").read(),
    open("article2.txt").read(),
    open("notes.md").read()
])

podcast = generate_podcast(
    content=content,
    num_speakers=3,
    duration_minutes=20,
    episode_profile={
        "topic": "AI Safety Research Overview",
        "format": "panel discussion",
        "target_audience": "ML researchers"
    },
    output_path="ai_safety_overview.mp3"
)
```

### Example 3: Interview Style

```python
podcast = generate_podcast(
    content="Biography and accomplishments...",
    speakers=[
        {
            "name": "Jamie Lee",
            "expertise": "Podcast Host",
            "personality": "Warm and insightful interviewer"
        },
        {
            "name": "Dr. Maria Rodriguez",
            "expertise": "Climate Scientist",
            "personality": "Passionate about communication"
        }
    ],
    episode_profile={
        "format": "interview",
        "tone": "conversational",
        "intro_style": "Brief host introduction then straight into questions"
    },
    output_path="climate_interview.mp3"
)
```

## How It Works

1. **Content Analysis**: AI analyzes your research materials to extract key themes
2. **Script Generation**: Creates natural dialogue between speakers using Gemini 3 Pro
3. **Speaker Assignment**: Distributes content across speakers with proper turn-taking
4. **TTS Synthesis**: Converts each speaker's lines to audio
5. **Audio Mixing**: Combines tracks with proper timing and audio levels
6. **Export**: Saves final podcast as MP3

## Technical Details

### AI Models Used

- **Dialogue Generation**: Gemini 3 Pro (primary) or Claude Sonnet 4.5 (fallback)
- **Text-to-Speech**: Google TTS (default) or ElevenLabs (premium)

### Audio Processing

- Sample rate: 44.1kHz
- Bit depth: 16-bit
- Format: Stereo MP3 (192 kbps)
- Processing: Normalization, silence removal, fade in/out

### Performance

- Typical generation time: 2-5 minutes for a 10-minute podcast
- Content limit: Up to 100,000 tokens of input
- Output length: Configurable from 5-60 minutes

## Limitations

- TTS voices may sound synthetic (ElevenLabs recommended for best quality)
- Very technical jargon may be mispronounced
- Background music not included (can be added in post-production)
- No real-time conversation; pre-scripted dialogue

## Tips for Best Results

1. **Quality Input**: Provide well-written, clear source material
2. **Specificity**: Define clear episode goals and target audience
3. **Speaker Count**: 2-3 speakers work best; 4+ can feel crowded
4. **Duration**: 10-20 minutes is optimal for engagement
5. **Personas**: Give speakers distinct personalities and expertise
6. **Review**: Always review the script before final audio generation

## Troubleshooting

**Issue**: Audio sounds robotic
- **Solution**: Try ElevenLabs API for more natural voices

**Issue**: Speakers sound too similar
- **Solution**: Provide more distinct personality descriptions

**Issue**: Content is too long
- **Solution**: Reduce duration or split into multiple episodes

**Issue**: Missing key points
- **Solution**: Explicitly list key_points in episode_profile

## Advanced Features

### Script-Only Mode

Generate just the dialogue script without audio:

```python
script = generate_script_only(
    content="Your content...",
    output_path="script.json"
)
```

### Custom Audio Mixing

Control audio parameters:

```python
podcast = generate_podcast(
    content="Your content...",
    audio_config={
        "sample_rate": 48000,
        "bit_depth": 24,
        "normalization": True,
        "add_silence_between_speakers": 0.3  # seconds
    }
)
```

### Multi-Language Support

Generate podcasts in different languages:

```python
podcast = generate_podcast(
    content="Your content...",
    language="es",  # Spanish
    speakers=[
        {
            "name": "María García",
            "voice_style": "es-ES-Standard-A"
        }
    ]
)
```

## Credits

Inspired by Google NotebookLM's Audio Overview feature and Open Notebook's podcast generation system.

## License

MIT License
