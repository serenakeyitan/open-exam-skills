"""
Infographic Skill - Generate visual infographics
"""

import json
import argparse
import os
from typing import List, Dict
from pydantic import BaseModel
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")


class InfographicData(BaseModel):
    """Infographic data structure."""
    title: str
    subtitle: str
    statistics: List[Dict[str, str]]  # {label, value, description}
    key_points: List[str]


def generate_with_ai(content: str, api_key: str, provider: str = "gemini") -> str:
    """Generate infographic data using AI."""
    prompt = f"""Extract key data for an infographic from this content.

Content: {content[:10000]}

Create a visually-focused data structure with:
- title: Main title
- subtitle: Brief tagline
- statistics: Array of {{label, value, description}} objects (4-6 key stats)
- key_points: Array of bullet points (3-5 items)

Return as JSON:
{{
  "title": "Quantum Computing Revolution",
  "subtitle": "The Future of Computation",
  "statistics": [
    {{"label": "Processing Power", "value": "1000x", "description": "Faster than classical"}},
    {{"label": "Qubits", "value": "100+", "description": "Current systems"}}
  ],
  "key_points": [
    "Superposition enables parallel computation",
    "Quantum gates manipulate qubits"
  ]
}}"""

    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        return response.text
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


def create_infographic_image(data: InfographicData, output_path: str, style: str = "modern") -> None:
    """Create infographic image."""
    from PIL import Image, ImageDraw, ImageFont

    # Image dimensions
    width, height = 1200, 1600
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        title_font = ImageFont.truetype("Arial.ttf", 60)
        subtitle_font = ImageFont.truetype("Arial.ttf", 30)
        stat_value_font = ImageFont.truetype("Arial.ttf", 48)
        stat_label_font = ImageFont.truetype("Arial.ttf", 24)
        body_font = ImageFont.truetype("Arial.ttf", 22)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        stat_value_font = ImageFont.load_default()
        stat_label_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    y_pos = 80

    # Title
    draw.text((width // 2, y_pos), data.title, fill='#00adb5', font=title_font, anchor="mm")
    y_pos += 80

    # Subtitle
    draw.text((width // 2, y_pos), data.subtitle, fill='#eeeeee', font=subtitle_font, anchor="mm")
    y_pos += 100

    # Statistics (grid layout)
    stat_width = width // 2 - 60
    stat_height = 180
    x_start = 40
    y_start = y_pos

    for i, stat in enumerate(data.statistics[:4]):  # Max 4 stats
        row = i // 2
        col = i % 2
        x = x_start + col * (stat_width + 40)
        y = y_start + row * (stat_height + 20)

        # Stat box
        draw.rectangle([x, y, x + stat_width, y + stat_height], fill='#16213e', outline='#00adb5', width=2)

        # Value (large)
        draw.text((x + stat_width // 2, y + 60), stat['value'], fill='#00adb5', font=stat_value_font, anchor="mm")

        # Label
        draw.text((x + stat_width // 2, y + 110), stat['label'], fill='#eeeeee', font=stat_label_font, anchor="mm")

        # Description (small)
        desc_lines = stat['description'][:30]
        draw.text((x + stat_width // 2, y + 145), desc_lines, fill='#aaaaaa', font=ImageFont.load_default(), anchor="mm")

    y_pos = y_start + ((len(data.statistics) + 1) // 2) * (stat_height + 20) + 60

    # Key points
    for point in data.key_points:
        if y_pos > height - 100:
            break

        # Bullet point
        draw.ellipse([60, y_pos, 75, y_pos + 15], fill='#00adb5')

        # Text (wrap if too long)
        text_lines = []
        words = point.split()
        line = ""
        for word in words:
            test_line = line + " " + word if line else word
            if len(test_line) < 60:
                line = test_line
            else:
        if not args.input:
            parser.error("--input is required when not in test mode")
                text_lines.append(line)
                line = word
        if line:
            text_lines.append(line)

        for line in text_lines[:2]:  # Max 2 lines per point
            draw.text((100, y_pos), line, fill='#eeeeee', font=body_font)
            y_pos += 35

        y_pos += 20

    # Save
    img.save(output_path)
    logger.info(f"Infographic saved: {output_path}")


def generate_infographic(
    content: str,
    style: str = "modern",
    output_path: str = "infographic.png"
) -> str:
    """Generate infographic from content."""
    logger.info("Generating infographic...")

    # Get API key
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    if gemini_key:
        response = generate_with_ai(content, gemini_key, "gemini")
    elif anthropic_key:
        response = generate_with_ai(content, anthropic_key, "anthropic")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        raise ValueError("No API key found")

    # Parse response
    text = response.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    data = json.loads(text.strip())
    infographic_data = InfographicData(**data)

    # Create image
    create_infographic_image(infographic_data, output_path, style)

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="infographic.png")
    parser.add_argument("--style", "-s", default="modern")
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    if args.test:
        content = "Quantum computing: 1000x faster processing. Current systems have 100+ qubits. Superposition enables parallel computation. Applications in cryptography and drug discovery."
        result = generate_infographic(content, "modern", "test_infographic.png")
        print(f"Test infographic: {result}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        result = generate_infographic(content, args.style, args.output)
        print(f"Infographic generated: {result}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
