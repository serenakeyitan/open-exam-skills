# Infographic Skill

Create visual infographics from research data using AI.

## Features

- Key statistics extraction
- Professional layouts
- Charts and visualizations
- PNG/SVG export

## Installation

```bash
cd infographic
pip install -r requirements.txt
```

## Usage

```python
from main import generate_infographic

infographic = generate_infographic(
    content="Your research...",
    style="modern",
    output_path="infographic.png"
)
```

## Command Line

```bash
python main.py --input research.txt --output infographic.png --style modern
```

## License

MIT
