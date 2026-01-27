"""
Infographic Skill - Generate visual infographics using Nano Banana Pro
"""

import json
import argparse
import os
import time
from pydantic import BaseModel
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")

# API timeout settings
ANALYZE_TIMEOUT = 60  # seconds for content analysis
GENERATE_TIMEOUT = 120  # seconds for image generation
MAX_RETRIES = 2  # number of retries for API calls


class InfographicStructure(BaseModel):
    """Structured infographic content."""
    title: str
    subtitle: str
    sections: list[dict]  # Each section has: title, content, visual_description


def analyze_content_with_ai(content: str, api_key: str) -> str:
    """Analyze content and extract structured infographic data using Gemini."""
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig

    logger.info("Step 1/2: Analyzing content structure...")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3-pro-preview")

    prompt = f"""Analyze this content and create a structured infographic outline.

Content: {content[:15000]}

Create a JSON structure with:
- title: Main title (short, impactful, max 6 words)
- subtitle: Brief tagline (max 10 words)
- sections: Array of 4-5 sections, each with:
  - title: Section heading (max 3 words)
  - content: MINIMAL key points (1-2 SHORT bullet points max, each under 8 words)
  - visual_description: Description of diagrams/illustrations to include

CRITICAL: Keep text MINIMAL. Professional infographics are 70% visual, 30% text.
Focus on single key statistics, short phrases, not full sentences.

Format for HORIZONTAL layout with multiple sections arranged left-to-right.

Return ONLY valid JSON:
{{
  "title": "Main Title",
  "subtitle": "Brief tagline",
  "sections": [
    {{
      "title": "Section Name",
      "content": ["Short point 1", "Key stat 2"],
      "visual_description": "Diagram showing..."
    }}
  ]
}}"""

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            if attempt > 0:
                logger.info(f"Retry attempt {attempt + 1}/{MAX_RETRIES}...")

            start_time = time.time()
            response = model.generate_content(
                prompt,
                generation_config=GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                ),
                request_options={"timeout": ANALYZE_TIMEOUT}
            )

            elapsed = time.time() - start_time
            logger.info(f"Content analysis completed in {elapsed:.1f}s")

            if not response.text:
                raise ValueError("Empty response from Gemini API")

            return response.text

        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {type(e).__name__}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                wait_time = (attempt + 1) * 2  # 2, 4 seconds
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

    # All retries failed
    logger.error(f"Content analysis failed after {MAX_RETRIES} attempts: {type(last_error).__name__}: {str(last_error)}")
    raise RuntimeError(f"Failed to analyze content after {MAX_RETRIES} attempts: {str(last_error)}")


def generate_infographic_image(structure: InfographicStructure, content_summary: str, output_path: str, api_key: str) -> None:
    """Generate infographic image using Nano Banana Pro (Gemini 3 Pro Image)."""
    from google import genai
    from google.genai import types

    logger.info("Step 2/2: Generating infographic image with Nano Banana Pro...")

    client = genai.Client(api_key=api_key)

    # Build detailed prompt for horizontal infographic
    sections_text = "\n\n".join([
        f"SECTION: {section['title']}\n" +
        "\n".join(f"- {point}" for point in section['content']) +
        f"\nVisuals: {section['visual_description']}"
        for section in structure.sections
    ])

    image_prompt = f"""Create a professional horizontal infographic with minimal text and maximum visual impact:

TITLE: {structure.title}
SUBTITLE: {structure.subtitle}

{sections_text}

CRITICAL DESIGN REQUIREMENTS (Professional Infographic Standards):

LAYOUT:
- HORIZONTAL orientation (landscape, wide format like 1920x1080)
- Main title at top (LARGE, BOLD)
- Subtitle below (smaller, concise)
- {len(structure.sections)} distinct sections arranged LEFT TO RIGHT

TEXT RULES (MINIMAL TEXT - CRITICAL):
- Use VERY FEW words - only essential information
- Large, bold section headings
- 1-2 SHORT bullet points per section maximum
- Statistics/numbers should be LARGE and prominent
- More white space, less crowding
- 70% VISUALS, 30% TEXT

VISUAL ELEMENTS (PRIMARY FOCUS):
- LARGE professional diagrams and illustrations dominate each section
- Icons, charts, visual metaphors
- Color-coded sections with clear visual boundaries
- Use arrows, flowcharts, process diagrams
- Professional scientific/educational illustration style
- Each section should be primarily visual with minimal supporting text

STYLE:
- Clean, modern, professional
- Educational/scientific aesthetic
- Strong visual hierarchy
- Generous spacing between elements
- Bold color scheme for section distinction

Remember: A professional infographic maker prioritizes visual storytelling over text. The visuals should convey the message; text only supports."""

    logger.info(f"Requesting image generation (this may take 30-120 seconds)...")

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            if attempt > 0:
                logger.info(f"Retry attempt {attempt + 1}/{MAX_RETRIES}...")

            start_time = time.time()

            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=image_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE'],
                )
            )

            elapsed = time.time() - start_time
            logger.info(f"Image generation completed in {elapsed:.1f}s")

            # Extract and save image
            image_saved = False
            for part in response.parts:
                if image := part.as_image():
                    image.save(output_path)
                    file_size = os.path.getsize(output_path) / 1024  # KB
                    logger.info(f"Infographic saved: {output_path} ({file_size:.1f} KB)")
                    image_saved = True
                    return

            if not image_saved:
                raise ValueError("No image generated in API response")

        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {type(e).__name__}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                wait_time = (attempt + 1) * 3  # 3, 6 seconds
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

    # All retries failed
    logger.error(f"Image generation failed after {MAX_RETRIES} attempts: {type(last_error).__name__}: {str(last_error)}")
    raise RuntimeError(f"Failed to generate infographic image after {MAX_RETRIES} attempts: {str(last_error)}")


def generate_infographic(
    content: str,
    output_path: str = "infographic.png"
) -> str:
    """Generate horizontal infographic from content using Nano Banana Pro."""
    total_start = time.time()

    try:
        logger.info("=" * 60)
        logger.info("INFOGRAPHIC GENERATION STARTED")
        logger.info("=" * 60)

        # Get API key
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        logger.info(f"Content length: {len(content)} characters")
        logger.info(f"Output path: {output_path}")

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

        try:
            data = json.loads(text.strip())
            structure = InfographicStructure(**data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {text[:500]}...")
            raise RuntimeError(f"Invalid JSON response from content analysis")

        logger.info(f"✓ Structure extracted: '{structure.title}'")
        logger.info(f"✓ Sections: {len(structure.sections)}")

        # Step 2: Generate infographic image with Nano Banana Pro
        generate_infographic_image(structure, content[:500], output_path, gemini_key)

        total_elapsed = time.time() - total_start
        logger.info("=" * 60)
        logger.info(f"✓ INFOGRAPHIC GENERATION COMPLETED in {total_elapsed:.1f}s")
        logger.info("=" * 60)

        return output_path

    except Exception as e:
        total_elapsed = time.time() - total_start
        logger.error("=" * 60)
        logger.error(f"✗ INFOGRAPHIC GENERATION FAILED after {total_elapsed:.1f}s")
        logger.error(f"Error: {type(e).__name__}: {str(e)}")
        logger.error("=" * 60)
        raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate horizontal infographics using Nano Banana Pro")
    parser.add_argument("--input", "-i")
    parser.add_argument("--output", "-o", default="infographic.png")
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    try:
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

            # Verify file was created
            if os.path.exists(result):
                size = os.path.getsize(result) / 1024
                print(f"✓ Test infographic created: {result} ({size:.1f} KB)")
            else:
                print(f"✗ Error: File not created at {result}")
                sys.exit(1)
        else:
            if not args.input:
                parser.error("--input is required when not in test mode")

            if not os.path.exists(args.input):
                print(f"✗ Error: Input file not found: {args.input}")
                sys.exit(1)

            with open(args.input) as f:
                content = f.read()

            if not content.strip():
                print(f"✗ Error: Input file is empty: {args.input}")
                sys.exit(1)

            result = generate_infographic(content, args.output)

            # Verify file was created
            if os.path.exists(result):
                size = os.path.getsize(result) / 1024
                print(f"✓ Infographic created: {result} ({size:.1f} KB)")
            else:
                print(f"✗ Error: File not created at {result}")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n✗ Generation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
