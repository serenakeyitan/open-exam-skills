---
name: infographic
description: Create visual infographics from research data. This skill should be used when users want to generate professional visual summaries with statistics, charts, and key points.
---

# Infographic

Extract key statistics and generate professional visual infographics with data visualization from research materials.

## When to Use This Skill

Use this skill when:
- Creating visual summaries of research data
- Generating shareable infographics
- Visualizing key statistics and findings
- Producing data-driven visual content

## How to Use

### Quick Test

```bash
cd infographic
python main.py --test
```

### Generate Infographic

```bash
python main.py --input research.txt --output infographic.png --style modern
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output PNG filename
- `--style`: Visual style - modern, professional, minimal (default: modern)

### Python API

```python
from main import generate_infographic

image_path = generate_infographic(
    content="Your research...",
    style="professional",
    output_path="infographic.png"
)
```

## What Gets Generated

- **PNG**: Visual infographic image (1200x1600)
- **SVG**: Vector graphic (optional)

## How It Works

1. **Data Extraction** - Identifies key statistics and findings
2. **Layout Design** - Creates professional visual hierarchy
3. **Visualization** - Generates charts and graphics
4. **Rendering** - Exports high-quality image

## Configuration

Requires `.env` file with API keys (already configured).

## Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- **Pillow** - Image generation
- **matplotlib** - Charts and graphs
