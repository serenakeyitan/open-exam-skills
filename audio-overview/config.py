"""
Configuration management for audio-overview skill.
Handles API keys and application settings.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class AIConfig(BaseModel):
    """AI provider configuration."""
    gemini_api_key: str = Field(default="")
    anthropic_api_key: str = Field(default="")
    elevenlabs_api_key: str = Field(default="")

    @property
    def has_gemini(self) -> bool:
        return bool(self.gemini_api_key)

    @property
    def has_anthropic(self) -> bool:
        return bool(self.anthropic_api_key)

    @property
    def has_elevenlabs(self) -> bool:
        return bool(self.elevenlabs_api_key)


class AudioConfig(BaseModel):
    """Audio generation configuration."""
    sample_rate: int = 44100
    bit_depth: int = 16
    channels: int = 2
    format: str = "mp3"
    bitrate: str = "192k"
    normalize: bool = True
    fade_in_duration: float = 0.5  # seconds
    fade_out_duration: float = 1.0  # seconds
    silence_between_speakers: float = 0.3  # seconds


class PodcastConfig(BaseModel):
    """Default podcast generation settings."""
    default_duration_minutes: int = 10
    default_tone: str = "conversational"
    default_format: str = "educational discussion"
    max_content_tokens: int = 100000
    min_speakers: int = 1
    max_speakers: int = 4


class Config(BaseModel):
    """Main configuration class."""
    ai: AIConfig = Field(default_factory=AIConfig)
    audio: AudioConfig = Field(default_factory=AudioConfig)
    podcast: PodcastConfig = Field(default_factory=PodcastConfig)


def load_config() -> Config:
    """
    Load configuration from environment variables.

    Returns:
        Config: Application configuration

    Raises:
        ValueError: If required API keys are missing
    """
    ai_config = AIConfig(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", "")
    )

    # Validate that we have at least one AI provider
    if not ai_config.has_gemini and not ai_config.has_anthropic:
        logger.error("No AI provider API key found. Please set GEMINI_API_KEY or ANTHROPIC_API_KEY")
        raise ValueError("At least one AI provider API key is required (GEMINI_API_KEY or ANTHROPIC_API_KEY)")

    if not ai_config.has_gemini:
        logger.warning("GEMINI_API_KEY not found, falling back to Anthropic")

    config = Config(ai=ai_config)

    logger.info("Configuration loaded successfully")
    logger.info(f"AI Providers: Gemini={ai_config.has_gemini}, Anthropic={ai_config.has_anthropic}, ElevenLabs={ai_config.has_elevenlabs}")

    return config


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global configuration instance."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
