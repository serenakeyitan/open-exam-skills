"""
Configuration management for video-overview skill.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
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


class VideoConfig(BaseModel):
    """Video generation configuration."""
    resolution: str = "1920x1080"
    fps: int = 30
    background_color: str = "#1a1a2e"
    text_color: str = "#ffffff"
    accent_color: str = "#00adb5"
    font_family: str = "Arial"
    font_size_title: int = 72
    font_size_body: int = 36
    slide_duration: float = 5.0  # Default seconds per slide


class Config(BaseModel):
    """Main configuration class."""
    ai: AIConfig = Field(default_factory=AIConfig)
    video: VideoConfig = Field(default_factory=VideoConfig)


def load_config() -> Config:
    """Load configuration from environment variables."""
    ai_config = AIConfig(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", "")
    )

    if not ai_config.has_gemini and not ai_config.has_anthropic:
        logger.error("No AI provider API key found")
        raise ValueError("At least one AI provider API key is required")

    config = Config(ai=ai_config)
    logger.info("Configuration loaded successfully")
    return config


_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global configuration instance."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
