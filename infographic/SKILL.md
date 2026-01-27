---
name: infographic
description: Create professional horizontal infographics from research data using Nano Banana Pro (Gemini 3 Pro Image). Generates landscape-oriented visual summaries with sections arranged left-to-right, featuring diagrams, illustrations, and minimal text for maximum visual impact.
---

# Infographic

Generate professional horizontal infographics using AI-powered image generation (Nano Banana Pro). Creates educational-style visual summaries with clear sections, professional diagrams, and concise information presentation.

## When to Use This Skill

Use this skill when:
- Creating visual summaries of research data
- Generating shareable educational infographics
- Visualizing key concepts with diagrams and illustrations
- Producing professional presentation materials
- Creating study aids and reference materials

## How to Use

### Quick Test

```bash
cd infographic
python main.py --test
```

### Generate Infographic

```bash
python main.py --input research.txt --output infographic.png
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output PNG filename (default: infographic.png)

### Python API

```python
from main import generate_infographic

image_path = generate_infographic(
    content="Your research...",
    output_path="infographic.png"
)
```

## What Gets Generated

- **Horizontal Layout PNG**: Professional landscape-oriented infographic (typically 1920x1080 or similar)
- **Multiple Sections**: 4-6 distinct sections arranged left-to-right
- **Visual Elements**: Diagrams, illustrations, charts, and icons
- **Professional Design**: Color-coded sections with clear visual hierarchy
- **Minimal Text**: Concise bullet points and key statistics only

## Design Philosophy

Professional infographic design principles:
- **Less is More**: Minimal text, maximum visual impact
- **Clear Sections**: Each section focuses on one key concept
- **Visual Storytelling**: Diagrams and illustrations convey information
- **Horizontal Flow**: Information flows naturally left-to-right
- **Professional Color Scheme**: Clean, color-coded sections for easy navigation

## How It Works

1. **Content Analysis** (Gemini 3 Pro) - Analyzes content and extracts structured infographic outline with 4-6 sections
2. **Image Generation** (Nano Banana Pro) - Generates professional horizontal infographic with:
   - Clear title and subtitle at top
   - Multiple sections arranged left-to-right
   - Professional diagrams and illustrations
   - Minimal, impactful text
   - Color-coded visual hierarchy

## Technical Details

- **Model**: `gemini-3-pro-image-preview` (Nano Banana Pro)
- **Text Analysis**: `gemini-3-pro-preview`
- **Output Format**: PNG (landscape orientation)
- **Generation Time**: ~30-60 seconds per infographic

## Configuration

Requires `.env` file with:
```
GEMINI_API_KEY=your_key_here
```

## Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- **google-genai** - Nano Banana Pro image generation API
- **google-generativeai** - Gemini text analysis
- **pydantic** - Data validation
