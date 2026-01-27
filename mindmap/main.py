"""
Mind Map Skill - Generate mind maps from research
"""

import json
import argparse
import os
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")


class MindMapNode(BaseModel):
    """A node in the mind map."""
    id: str
    label: str
    children: List['MindMapNode'] = Field(default_factory=list)
    level: int = 0


class MindMap(BaseModel):
    """Complete mind map structure."""
    root: MindMapNode
    title: str


def generate_with_ai(content: str, api_key: str, provider: str = "gemini") -> str:
    """Generate mind map structure using AI."""
    prompt = f"""Analyze this content and create a hierarchical mind map structure.

Content: {content[:10000]}

Create a JSON mind map with this structure:
{{
  "root": {{
    "id": "0",
    "label": "Main Topic",
    "level": 0,
    "children": [
      {{
        "id": "1",
        "label": "Subtopic 1",
        "level": 1,
        "children": [
          {{"id": "1.1", "label": "Detail", "level": 2, "children": []}}
        ]
      }}
    ]
  }},
  "title": "Mind Map Title"
}}

Return only valid JSON."""

    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3-pro-preview")
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


def export_to_html(mindmap: MindMap, output_path: str) -> None:
    """Export mind map as interactive HTML."""
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .mindmap {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .node {{
            margin: 10px 0 10px 20px;
            padding: 8px 12px;
            background: #e3f2fd;
            border-left: 3px solid #2196f3;
            border-radius: 4px;
            cursor: pointer;
        }}
        .node.level-0 {{
            background: #1976d2;
            color: white;
            font-size: 24px;
            font-weight: bold;
            border: none;
        }}
        .node.level-1 {{
            background: #42a5f5;
            color: white;
            font-size: 18px;
        }}
        .node.level-2 {{
            background: #90caf9;
            font-size: 16px;
        }}
        .children {{
            margin-left: 30px;
        }}
    </style>
</head>
<body>
    <div class="mindmap">
        <h1>{title}</h1>
        {content}
    </div>
</body>
</html>
"""

    def render_node(node: MindMapNode) -> str:
        html = f'<div class="node level-{node.level}">{node.label}</div>'
        if node.children:
            html += '<div class="children">'
            for child in node.children:
                html += render_node(child)
            html += '</div>'
        return html

    content_html = render_node(mindmap.root)
    final_html = html_template.format(title=mindmap.title, content=content_html)

    with open(output_path, 'w') as f:
        f.write(final_html)

    logger.info(f"HTML mind map saved: {output_path}")


def export_to_mermaid(mindmap: MindMap, output_path: str) -> None:
    """Export mind map as Mermaid diagram."""
    lines = ["```mermaid", "graph TD"]

    def add_node(node: MindMapNode, parent_id: Optional[str] = None):
        node_def = f'    {node.id}["{node.label}"]'
        lines.append(node_def)
        if parent_id:
            lines.append(f'    {parent_id} --> {node.id}')
        for child in node.children:
            add_node(child, node.id)

    add_node(mindmap.root)
    lines.append("```")

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    logger.info(f"Mermaid diagram saved: {output_path}")


def generate_mindmap(
    content: str,
    output_path: str = "mindmap.html",
    format: str = "html"
) -> str:
    """Generate mind map from content."""
    logger.info("Generating mind map...")

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
    mindmap = MindMap(**data)

    # Export
    if format == "html":
        export_to_html(mindmap, output_path)
    elif format == "mermaid":
        export_to_mermaid(mindmap, output_path)
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        raise ValueError(f"Unknown format: {format}")

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i")
    parser.add_argument("--output", "-o", default="mindmap.html")
    parser.add_argument("--format", "-f", default="html", choices=["html", "mermaid"])
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    if args.test:
        content = "Quantum computing uses qubits. Key concepts: superposition, entanglement, quantum gates. Applications: cryptography, drug discovery, optimization."
        result = generate_mindmap(content, "test_mindmap.html", "html")
        print(f"Test mindmap: {result}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        result = generate_mindmap(content, args.output, args.format)
        print(f"Mind map: {result}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
