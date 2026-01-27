---
name: mindmap
description: Generate interactive mind maps from research materials. This skill should be used when users want to visualize hierarchical concepts and relationships between ideas in their research.
---

# Mind Map

Extract hierarchical concepts from research materials and generate interactive mind maps with visual relationship mapping.

## When to Use This Skill

Use this skill when:
- Visualizing complex research topics and their relationships
- Creating concept maps from documents
- Organizing ideas hierarchically
- Generating study aids or presentation materials

## How to Use

### Quick Test

```bash
cd mindmap
python main.py --test
```

### Generate Mind Map

```bash
python main.py --input research.txt --output mindmap.html
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output filename (default: mindmap.html)
- `--format`: Format type - html or mermaid (default: html)

### Python API

```python
from main import generate_mindmap

mindmap_path = generate_mindmap(
    content="Your research...",
    output_path="mindmap.html",
    format="html"  # or "mermaid"
)
```

## What Gets Generated

- **HTML**: Interactive mind map with clickable nodes
- **Mermaid**: Diagram markdown for documentation

## How It Works

1. **Concept Extraction** - AI identifies key concepts and themes
2. **Hierarchy Building** - Organizes concepts in parent-child relationships
3. **Relationship Mapping** - Connects related ideas
4. **Visualization** - Renders interactive or static output

## Configuration

Requires `.env` file with API keys (already configured).

## Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- **google-generativeai** - Concept extraction
- **graphviz** - Optional diagram generation
