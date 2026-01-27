"""
Audio Overview Skill - Podcast Generation
Generate professional multi-speaker podcasts from research materials.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")

from config import get_config


class Speaker(BaseModel):
    """Speaker persona configuration."""
    name: str = Field(description="Speaker name")
    expertise: str = Field(description="Area of expertise")
    personality: str = Field(description="Personality traits and communication style")
    voice_style: str = Field(default="neutral", description="Voice characteristics for TTS")
    accent: Optional[str] = Field(default=None, description="Regional accent")


class EpisodeProfile(BaseModel):
    """Podcast episode configuration."""
    topic: str = Field(description="Main topic of the episode")
    format: str = Field(default="educational discussion", description="Episode format")
    tone: str = Field(default="conversational", description="Overall tone")
    target_audience: str = Field(default="general audience", description="Target audience")
    duration_minutes: int = Field(default=10, description="Target duration in minutes")
    key_points: List[str] = Field(default_factory=list, description="Key points to cover")
    intro_style: str = Field(default="engaging hook", description="Introduction style")
    outro_style: str = Field(default="summary and thanks", description="Closing style")


class DialogueTurn(BaseModel):
    """Single dialogue turn in the podcast."""
    speaker: str = Field(description="Speaker name")
    text: str = Field(description="What the speaker says")
    emotion: str = Field(default="neutral", description="Emotional tone")
    emphasis: List[str] = Field(default_factory=list, description="Words to emphasize")


class PodcastScript(BaseModel):
    """Complete podcast script."""
    dialogue: List[DialogueTurn] = Field(description="Dialogue turns")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Script metadata")


# Default speaker personas
DEFAULT_SPEAKERS = [
    Speaker(
        name="Alex Rivera",
        expertise="Podcast Host and Science Communicator",
        personality="Curious, enthusiastic, asks great questions that help the audience understand",
        voice_style="conversational, warm, engaging"
    ),
    Speaker(
        name="Dr. Sarah Chen",
        expertise="Subject Matter Expert and Researcher",
        personality="Knowledgeable, clear explainer, passionate about making complex topics accessible",
        voice_style="professional, articulate, friendly"
    ),
    Speaker(
        name="Jamie Thompson",
        expertise="Critical Analyst and Journalist",
        personality="Thoughtful questioner, challenges assumptions constructively, considers broader implications",
        voice_style="analytical, measured, inquisitive"
    ),
    Speaker(
        name="Morgan Lee",
        expertise="Innovation Specialist",
        personality="Forward-thinking, connects concepts, sees practical applications",
        voice_style="energetic, optimistic, creative"
    )
]


def generate_dialogue_with_ai(
    content: str,
    episode_profile: EpisodeProfile,
    speakers: List[Speaker],
    config: Any
) -> PodcastScript:
    """
    Generate podcast dialogue using AI.

    Args:
        content: Source material to convert to podcast
        episode_profile: Episode configuration
        speakers: List of speaker personas
        config: Application configuration

    Returns:
        PodcastScript: Generated dialogue script
    """
    logger.info(f"Generating dialogue for topic: {episode_profile.topic}")
    logger.info(f"Speakers: {', '.join([s.name for s in speakers])}")

    # Calculate target word count (approximately 150 words per minute of speech)
    target_words = episode_profile.duration_minutes * 150

    # Load prompt template
    prompt_path = Path(__file__).parent / "prompts" / "dialogue_generation.md"
    with open(prompt_path, "r") as f:
        prompt_template = f.read()

    # Prepare template variables
    content_duration = episode_profile.duration_minutes - 2  # Reserve time for intro/outro

    # Build prompt (simple string replacement for mustache-like templates)
    prompt = prompt_template.replace("{{topic}}", episode_profile.topic)
    prompt = prompt.replace("{{format}}", episode_profile.format)
    prompt = prompt.replace("{{duration}}", str(episode_profile.duration_minutes))
    prompt = prompt.replace("{{tone}}", episode_profile.tone)
    prompt = prompt.replace("{{audience}}", episode_profile.target_audience)
    prompt = prompt.replace("{{content}}", content[:50000])  # Limit content length
    prompt = prompt.replace("{{content_duration}}", str(content_duration))
    prompt = prompt.replace("{{target_words}}", str(target_words))

    # Format speakers section
    speakers_text = ""
    for speaker in speakers:
        speakers_text += f"### {speaker.name}\n"
        speakers_text += f"- **Role**: {speaker.expertise}\n"
        speakers_text += f"- **Personality**: {speaker.personality}\n"
        speakers_text += f"- **Voice Style**: {speaker.voice_style}\n\n"
    prompt = prompt.replace("{{#speakers}}\n### {{name}}\n- **Role**: {{expertise}}\n- **Personality**: {{personality}}\n- **Voice Style**: {{voice_style}}\n\n{{/speakers}}", speakers_text)

    # Format key points
    if episode_profile.key_points:
        key_points_text = "\n".join([f"- {point}" for point in episode_profile.key_points])
    else:
        key_points_text = "- (Extract key themes from the content)"
    prompt = prompt.replace("{{#key_points}}\n- {{.}}\n{{/key_points}}", key_points_text)

    # Load system prompt
    system_prompt_path = Path(__file__).parent / "prompts" / "system.md"
    with open(system_prompt_path, "r") as f:
        system_prompt = f.read()

    # Generate dialogue using AI
    try:
        if config.ai.has_gemini:
            logger.info("Using Gemini 3 Pro for dialogue generation")
            dialogue_json = generate_with_gemini(system_prompt, prompt, config.ai.gemini_api_key)
        elif config.ai.has_anthropic:
            logger.info("Using Claude Sonnet 4.5 for dialogue generation")
            dialogue_json = generate_with_anthropic(system_prompt, prompt, config.ai.anthropic_api_key)
        else:
            raise ValueError("No AI provider available")

        # Parse dialogue
        dialogue_data = json.loads(dialogue_json)
        dialogue_turns = [DialogueTurn(**turn) for turn in dialogue_data]

        logger.info(f"Generated {len(dialogue_turns)} dialogue turns")

        return PodcastScript(
            dialogue=dialogue_turns,
            metadata={
                "topic": episode_profile.topic,
                "speakers": [s.name for s in speakers],
                "duration_target": episode_profile.duration_minutes,
                "word_count": sum(len(turn.text.split()) for turn in dialogue_turns)
            }
        )

    except Exception as e:
        logger.error(f"Failed to generate dialogue: {e}")
        raise


def generate_with_gemini(system_prompt: str, user_prompt: str, api_key: str) -> str:
    """Generate dialogue using Gemini API."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)

    # Use Gemini 2.0 Flash or Gemini 1.5 Pro
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction=system_prompt,
        generation_config={
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    )

    response = model.generate_content(user_prompt)

    # Extract JSON from response (may be wrapped in markdown code blocks)
    text = response.text.strip()
    if text.startswith("```json"):
        text = text[7:]  # Remove ```json
    if text.startswith("```"):
        text = text[3:]  # Remove ```
    if text.endswith("```"):
        text = text[:-3]  # Remove trailing ```
    text = text.strip()

    return text


def generate_with_anthropic(system_prompt: str, user_prompt: str, api_key: str) -> str:
    """Generate dialogue using Anthropic Claude API."""
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        temperature=0.9,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    text = response.content[0].text.strip()

    # Extract JSON from response
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    return text


def synthesize_audio(
    script: PodcastScript,
    speakers: List[Speaker],
    output_path: str,
    config: Any
) -> str:
    """
    Synthesize audio from script using TTS.

    Args:
        script: Podcast script with dialogue
        speakers: Speaker personas
        output_path: Path to save audio file
        config: Application configuration

    Returns:
        str: Path to generated audio file
    """
    logger.info("Synthesizing audio from script...")

    try:
        from pydub import AudioSegment
        from pydub.effects import normalize
        import tempfile
        import os

        # Create speaker voice mapping
        speaker_voices = {speaker.name: speaker.voice_style for speaker in speakers}

        # Generate audio for each dialogue turn
        audio_segments = []
        temp_files = []

        for i, turn in enumerate(script.dialogue):
            logger.info(f"Synthesizing turn {i+1}/{len(script.dialogue)}: {turn.speaker}")

            # Generate TTS for this turn
            temp_audio_path = os.path.join(tempfile.gettempdir(), f"turn_{i}.mp3")
            temp_files.append(temp_audio_path)

            # Use Google TTS or ElevenLabs
            if config.ai.has_elevenlabs:
                synthesize_elevenlabs(turn.text, turn.speaker, speaker_voices.get(turn.speaker, "neutral"), temp_audio_path, config.ai.elevenlabs_api_key)
            else:
                synthesize_google_tts(turn.text, turn.speaker, temp_audio_path)

            # Load audio segment
            audio_segment = AudioSegment.from_mp3(temp_audio_path)

            # Add to segments
            audio_segments.append(audio_segment)

            # Add silence between speakers
            silence = AudioSegment.silent(duration=int(config.audio.silence_between_speakers * 1000))
            audio_segments.append(silence)

        # Combine all segments
        logger.info("Combining audio segments...")
        final_audio = sum(audio_segments)

        # Normalize audio
        if config.audio.normalize:
            logger.info("Normalizing audio...")
            final_audio = normalize(final_audio)

        # Add fade in/out
        final_audio = final_audio.fade_in(int(config.audio.fade_in_duration * 1000))
        final_audio = final_audio.fade_out(int(config.audio.fade_out_duration * 1000))

        # Export
        logger.info(f"Exporting to {output_path}...")
        final_audio.export(
            output_path,
            format="mp3",
            bitrate=config.audio.bitrate,
            parameters=["-ac", str(config.audio.channels)]
        )

        # Cleanup temp files
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass

        logger.info(f"Audio generated successfully: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Failed to synthesize audio: {e}")
        raise


def synthesize_google_tts(text: str, speaker_name: str, output_path: str) -> None:
    """Synthesize speech using Google Cloud TTS or gTTS fallback."""
    # Use gTTS as primary method (simpler, no credentials needed)
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
    except Exception as e:
        logger.warning(f"gTTS failed: {e}, creating silent audio")
        # Fallback: Create silent audio (for testing)
        from pydub import AudioSegment
        # Estimate duration (150 words per minute)
        words = len(text.split())
        duration_ms = int((words / 150) * 60 * 1000)
        audio = AudioSegment.silent(duration=duration_ms)
        audio.export(output_path, format="mp3")


def synthesize_elevenlabs(text: str, speaker_name: str, voice_style: str, output_path: str, api_key: str) -> None:
    """Synthesize speech using ElevenLabs API."""
    from elevenlabs import generate, save, set_api_key

    set_api_key(api_key)

    # Map speaker to ElevenLabs voice (you can customize this)
    voice_map = {
        "professional female": "EXAVITQu4vr4xnSDxMaL",  # Bella
        "conversational male": "TxGEqnHWrfWFTfGW9XjX",  # Josh
        "analytical": "pNInz6obpgDQGcFmaJgB",  # Adam
        "energetic": "MF3mGyEYCl7XYWbV9V6O",  # Elli
    }

    voice_id = voice_map.get(voice_style, "EXAVITQu4vr4xnSDxMaL")  # Default to Bella

    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_monolingual_v1"
    )

    save(audio, output_path)


def generate_podcast(
    content: str,
    output_path: str = "podcast.mp3",
    num_speakers: int = 2,
    duration_minutes: int = 10,
    tone: str = "conversational",
    episode_profile: Optional[Dict[str, Any]] = None,
    speakers: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Generate a podcast from content.

    Args:
        content: Source material to convert to podcast
        output_path: Path to save the generated podcast
        num_speakers: Number of speakers (1-4)
        duration_minutes: Target duration in minutes
        tone: Podcast tone
        episode_profile: Optional episode configuration
        speakers: Optional custom speakers

    Returns:
        str: Path to generated podcast file
    """
    # Load configuration
    config = get_config()

    # Setup episode profile
    if episode_profile:
        profile = EpisodeProfile(**episode_profile)
    else:
        # Extract topic from content (simple approach)
        topic = content[:100].split('\n')[0] if '\n' in content[:100] else "Research Discussion"
        profile = EpisodeProfile(
            topic=topic,
            duration_minutes=duration_minutes,
            tone=tone
        )

    # Setup speakers
    if speakers:
        speaker_list = [Speaker(**s) for s in speakers]
    else:
        speaker_list = DEFAULT_SPEAKERS[:num_speakers]

    logger.info(f"Starting podcast generation: {profile.topic}")
    logger.info(f"Duration: {duration_minutes} minutes, Speakers: {num_speakers}")

    # Generate dialogue script
    script = generate_dialogue_with_ai(content, profile, speaker_list, config)

    # Save script
    script_path = output_path.replace('.mp3', '_script.json')
    with open(script_path, 'w') as f:
        json.dump(script.dict(), f, indent=2)
    logger.info(f"Script saved to: {script_path}")

    # Synthesize audio
    audio_path = synthesize_audio(script, speaker_list, output_path, config)

    logger.info(f"Podcast generation complete!")
    logger.info(f"Audio: {audio_path}")
    logger.info(f"Script: {script_path}")

    return audio_path


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(description="Generate a podcast from research materials")
    parser.add_argument("--input", "-i", help="Input file with research content")
    parser.add_argument("--output", "-o", default="podcast.mp3", help="Output audio file")
    parser.add_argument("--speakers", "-s", type=int, default=2, help="Number of speakers (1-4)")
    parser.add_argument("--duration", "-d", type=int, default=10, help="Duration in minutes")
    parser.add_argument("--tone", "-t", default="conversational", help="Podcast tone")
    parser.add_argument("--test", action="store_true", help="Run test mode with sample content")

    args = parser.parse_args()

    if args.test:
        # Test mode with sample content
        logger.info("Running in test mode with sample content")
        content = """
        Quantum Computing: A Revolutionary Technology

        Quantum computers represent a fundamental shift in computing paradigm. Unlike classical computers
        that use bits (0 or 1), quantum computers use qubits that can exist in superposition, being both
        0 and 1 simultaneously. This property, combined with entanglement, allows quantum computers to
        solve certain problems exponentially faster than classical computers.

        Key applications include:
        - Cryptography and security
        - Drug discovery and molecular simulation
        - Optimization problems
        - Machine learning and AI

        Major challenges remain, including maintaining quantum coherence and error correction.
        """

        output = generate_podcast(
            content=content,
            output_path="test_podcast.mp3",
            num_speakers=2,
            duration_minutes=5,
            tone="educational"
        )
        print(f"\nTest podcast generated: {output}")

    else:
        # Read input file
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input, 'r') as f:
            content = f.read()

        # Generate podcast
        output = generate_podcast(
            content=content,
            output_path=args.output,
            num_speakers=args.speakers,
            duration_minutes=args.duration,
            tone=args.tone
        )

        print(f"\nPodcast generated: {output}")


if __name__ == "__main__":
    main()
