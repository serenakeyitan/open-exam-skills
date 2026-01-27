"""
Video Overview Skill - Video Generation from Research
Create narrated videos with visual slides from content.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from pydantic import BaseModel, Field
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")

from config import get_config


class Slide(BaseModel):
    """Single video slide."""
    type: str = Field(description="Slide type: title, content, quote, data, transition")
    title: str = Field(description="Slide title")
    content: List[str] = Field(default_factory=list, description="Bullet points or text")
    narration: str = Field(description="Narration script for this slide")
    duration: float = Field(default=5.0, description="Slide duration in seconds")


class Storyboard(BaseModel):
    """Complete video storyboard."""
    title: str = Field(description="Video title")
    slides: List[Slide] = Field(description="List of slides")
    total_duration: float = Field(description="Total video duration")


def generate_storyboard(content: str, title: str, duration_minutes: int, style: str, config: Any) -> Storyboard:
    """Generate video storyboard using AI."""
    logger.info(f"Generating storyboard for: {title}")

    prompt = f"""Create a video storyboard for a {duration_minutes}-minute video presentation.

Title: {title}
Style: {style}
Content: {content[:10000]}

Generate a sequence of slides with narration. Each slide should have:
- type: "title", "content", "quote", "data", or "transition"
- title: Brief slide title
- content: List of bullet points (2-4 per slide)
- narration: What to say during this slide (natural, conversational)
- duration: How long to show slide (seconds)

Aim for approximately {duration_minutes * 60} seconds total.

Return as JSON array of slides:
[
  {{
    "type": "title",
    "title": "Video Title",
    "content": [],
    "narration": "Welcome to this overview of...",
    "duration": 5
  }},
  {{
    "type": "content",
    "title": "Key Concept",
    "content": ["First point", "Second point", "Third point"],
    "narration": "Let's start with the key concepts. First...",
    "duration": 8
  }}
]"""

    try:
        if config.ai.has_gemini:
            response = generate_with_gemini(prompt, config.ai.gemini_api_key)
        else:
            response = generate_with_anthropic(prompt, config.ai.anthropic_api_key)

        # Parse response
        text = response.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        slides_data = json.loads(text)
        slides = [Slide(**s) for s in slides_data]
        total_duration = sum(s.duration for s in slides)

        logger.info(f"Generated {len(slides)} slides, total duration: {total_duration:.1f}s")

        return Storyboard(title=title, slides=slides, total_duration=total_duration)

    except Exception as e:
        logger.error(f"Failed to generate storyboard: {e}")
        raise


def generate_with_gemini(prompt: str, api_key: str) -> str:
    """Generate content using Gemini."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)
    return response.text


def generate_with_anthropic(prompt: str, api_key: str) -> str:
    """Generate content using Anthropic."""
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def create_slide_image(slide: Slide, config: Any, resolution: Tuple[int, int]) -> Any:
    """Create slide image using Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    width, height = resolution
    img = Image.new('RGB', (width, height), color=config.video.background_color)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("Arial.ttf", config.video.font_size_title)
        body_font = ImageFont.truetype("Arial.ttf", config.video.font_size_body)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw title
    title_y = height // 6
    draw.text((width // 2, title_y), slide.title, fill=config.video.accent_color,
              font=title_font, anchor="mm")

    # Draw content
    if slide.content:
        content_y = height // 3
        line_height = config.video.font_size_body + 20
        for i, line in enumerate(slide.content[:5]):  # Max 5 bullets
            y_pos = content_y + (i * line_height)
            draw.text((width // 4, y_pos), f"• {line}", fill=config.video.text_color,
                     font=body_font, anchor="lm")

    return img


def synthesize_narration(text: str, output_path: str, config: Any) -> None:
    """Synthesize narration audio."""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
    except Exception as e:
        logger.warning(f"TTS failed: {e}, creating silent audio")
        from pydub import AudioSegment
        words = len(text.split())
        duration_ms = int((words / 150) * 60 * 1000)
        audio = AudioSegment.silent(duration=duration_ms)
        audio.export(output_path, format="mp3")


def render_video(storyboard: Storyboard, output_path: str, config: Any) -> str:
    """Render final video from storyboard."""
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
    import tempfile
    import os

    logger.info("Rendering video...")

    resolution = tuple(map(int, config.video.resolution.split('x')))
    clips = []
    temp_files = []

    for i, slide in enumerate(storyboard.slides):
        logger.info(f"Rendering slide {i+1}/{len(storyboard.slides)}: {slide.title}")

        # Create slide image
        img = create_slide_image(slide, config, resolution)
        img_path = os.path.join(tempfile.gettempdir(), f"slide_{i}.png")
        img.save(img_path)
        temp_files.append(img_path)

        # Generate narration
        audio_path = os.path.join(tempfile.gettempdir(), f"narration_{i}.mp3")
        synthesize_narration(slide.narration, audio_path, config)
        temp_files.append(audio_path)

        # Create video clip
        try:
            audio_clip = AudioFileClip(audio_path)
            duration = max(slide.duration, audio_clip.duration + 0.5)
        except:
            duration = slide.duration
            audio_clip = None

        video_clip = ImageClip(img_path, duration=duration)
        if audio_clip:
            video_clip = video_clip.set_audio(audio_clip)

        clips.append(video_clip)

    # Concatenate clips
    logger.info("Combining clips...")
    final_video = concatenate_videoclips(clips, method="compose")

    # Export
    logger.info(f"Exporting to {output_path}...")
    final_video.write_videofile(
        output_path,
        fps=config.video.fps,
        codec='libx264',
        audio_codec='aac',
        preset='medium'
    )

    # Cleanup
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except:
            pass

    logger.info(f"Video generated successfully: {output_path}")
    return output_path


def generate_video_overview(
    content: str,
    title: str = "Research Overview",
    output_path: str = "video.mp4",
    style: str = "professional",
    duration_minutes: int = 5,
    video_config: Optional[Dict] = None
) -> str:
    """Generate video overview from content."""
    config = get_config()

    # Apply custom video config
    if video_config:
        for key, value in video_config.items():
            if hasattr(config.video, key):
                setattr(config.video, key, value)

    logger.info(f"Generating video: {title}")

    # Generate storyboard
    storyboard = generate_storyboard(content, title, duration_minutes, style, config)

    # Save storyboard
    script_path = output_path.replace('.mp4', '_storyboard.json')
    with open(script_path, 'w') as f:
        json.dump(storyboard.dict(), f, indent=2)
    logger.info(f"Storyboard saved: {script_path}")

    # Render video
    video_path = render_video(storyboard, output_path, config)

    return video_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate video from research")
    parser.add_argument("--input", "-i", help="Input content file")
    parser.add_argument("--output", "-o", default="video.mp4", help="Output video file")
    parser.add_argument("--title", "-t", default="Research Overview", help="Video title")
    parser.add_argument("--style", "-s", default="professional", help="Video style")
    parser.add_argument("--duration", "-d", type=int, default=5, help="Duration (minutes)")
    parser.add_argument("--test", action="store_true", help="Test mode")

    args = parser.parse_args()

    if args.test:
        content = "Quantum computing uses qubits that can exist in superposition. This enables solving complex problems faster than classical computers. Applications include cryptography, drug discovery, and optimization."
        video = generate_video_overview(content, "Quantum Computing", "test_video.mp4", duration_minutes=2)
        print(f"\nTest video: {video}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        video = generate_video_overview(content, args.title, args.output, args.style, args.duration)
        print(f"\nVideo generated: {video}")


if __name__ == "__main__":
    main()
