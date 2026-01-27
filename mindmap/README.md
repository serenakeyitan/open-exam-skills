# Mind Map Skill

Generate interactive mind maps from research materials using AI. Extract hierarchical concepts and visualize relationships between ideas.

## Features

- Hierarchical concept extraction
- Relationship mapping between ideas
- Multiple export formats (HTML, Mermaid, PNG)
- Interactive visualization
- Customizable styling

## Installation

```bash
cd mindmap
pip install -r requirements.txt
```

## Configuration

Create `.env`:
```bash
GEMINI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## Usage

```python
from main import generate_mindmap

mindmap = generate_mindmap(
    content="Your research...",
    output_path="mindmap.html",
    format="html"  # or "mermaid", "png"
)
```

## Command Line

```bash
python main.py --input research.txt --output mindmap.html
```

## License

MIT
