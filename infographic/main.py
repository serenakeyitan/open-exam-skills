"""
Infographic Skill - Generate visual infographics using Nano Banana Pro
"""

import json
import argparse
import os
from pydantic import BaseModel
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")


class InfographicStructure(BaseModel):
    """Structured infographic content."""
    title: str
    subtitle: str
    sections: list[dict]  # Each section has: title, content, visual_description


def analyze_content_with_ai(content: str, api_key: str) -> str:
    """Analyze content and extract structured infographic data using Gemini."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3-pro-preview")

    prompt = f"""Analyze this content and create a structured infographic outline.

Content: {content[:15000]}

Create a JSON structure with:
- title: Main title (concise, impactful)
- subtitle: Brief tagline describing the content
- sections: Array of 4-6 sections, each with:
  - title: Section heading
  - content: Key points, statistics, or facts (2-4 bullet points)
  - visual_description: Description of diagrams/illustrations to include

Format for HORIZONTAL layout with multiple sections arranged left-to-right.

Return ONLY valid JSON:
{{
  "title": "Main Title Here",
  "subtitle": "Descriptive subtitle",
  "sections": [
    {{
      "title": "Section 1 Name",
      "content": ["Point 1", "Point 2", "Point 3"],
      "visual_description": "Diagram showing..."
    }}
  ]
}}"""

    response = model.generate_content(prompt)
    return response.text


def generate_infographic_image(structure: InfographicStructure, content_summary: str, output_path: str, api_key: str) -> None:
    """Generate infographic image using Nano Banana Pro (Gemini 3 Pro Image)."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    # Build detailed prompt for horizontal infographic
    sections_text = "\n\n".join([
        f"SECTION: {section['title']}\n" +
        "\n".join(f"- {point}" for point in section['content']) +
        f"\nVisuals: {section['visual_description']}"
        for section in structure.sections
    ])

    image_prompt = f"""Create a professional horizontal infographic with this exact structure:

TITLE: {structure.title}
SUBTITLE: {structure.subtitle}

{sections_text}

DESIGN REQUIREMENTS:
- HORIZONTAL orientation (landscape, wide format like 1920x1080)
- Main title at the very top, large and bold
- Subtitle below title
- {len(structure.sections)} distinct sections arranged LEFT TO RIGHT across the page
- Each section should have:
  * Clear section heading
  * Professional illustrations/diagrams relevant to the content
  * Key bullet points or statistics
  * Color-coded or visually distinct boundaries
- Modern, clean design with professional color scheme
- Include relevant icons, diagrams, charts, and illustrations
- Text should be clearly readable
- Professional infographic style similar to scientific or educational materials
- Balance of text and visual elements
- Use boxes, arrows, and visual hierarchy to organize information

Style: Professional, educational, modern, clean layout with illustrations"""

    logger.info("Generating infographic with Nano Banana Pro...")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=image_prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
        )
    )

    # Extract and save image
    for part in response.parts:
        if image := part.as_image():
            image.save(output_path)
            logger.info(f"Infographic saved: {output_path}")
            return

    raise ValueError("No image generated in response")


def generate_infographic(
    content: str,
    output_path: str = "infographic.png"
) -> str:
    """Generate horizontal infographic from content using Nano Banana Pro."""
    logger.info("Analyzing content for infographic structure...")

    # Get API key
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in environment")

    # Step 1: Analyze content and extract structure
    response = analyze_content_with_ai(content, gemini_key)

    # Parse JSON response
    text = response.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    data = json.loads(text.strip())
    structure = InfographicStructure(**data)

    logger.info(f"Structure extracted: {structure.title}")
    logger.info(f"Sections: {len(structure.sections)}")

    # Step 2: Generate infographic image with Nano Banana Pro
    generate_infographic_image(structure, content[:500], output_path, gemini_key)

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate horizontal infographics using Nano Banana Pro")
    parser.add_argument("--input", "-i")
    parser.add_argument("--output", "-o", default="infographic.png")
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    if args.test:
        content = """Quantum Computing: The Next Revolution

        Quantum computers use qubits instead of classical bits. Key concepts include:
        - Superposition: qubits can be in multiple states simultaneously
        - Entanglement: qubits can be correlated in quantum ways
        - Quantum gates: operations that manipulate qubits

        Current systems have 100+ qubits and are 1000x faster for certain tasks.
        Applications include cryptography, drug discovery, optimization problems, and machine learning.

        Major players: IBM, Google, Microsoft, Amazon are all investing heavily.
        Challenges include error correction, maintaining coherence, and scaling up systems."""

        result = generate_infographic(content, "test_infographic.png")
        print(f"Test infographic: {result}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        result = generate_infographic(content, args.output)
        print(f"Infographic generated: {result}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
