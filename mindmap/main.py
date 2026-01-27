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
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


def export_to_xmind(mindmap: MindMap, output_path: str) -> None:
    """Export mind map as XMind file."""
    import xmind

    # Create new workbook
    workbook = xmind.load(output_path)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle(mindmap.title)

    # Get root topic
    root_topic = sheet.getRootTopic()
    root_topic.setTitle(mindmap.root.label)

    # Recursively add nodes
    def add_node_to_topic(node: MindMapNode, parent_topic):
        for child in node.children:
            child_topic = parent_topic.addSubTopic()
            child_topic.setTitle(child.label)
            # Recursively add children
            add_node_to_topic(child, child_topic)

    # Add all children to root
    add_node_to_topic(mindmap.root, root_topic)

    # Save
    xmind.save(workbook, output_path)
    logger.info(f"XMind mind map saved: {output_path}")


def generate_mindmap(
    content: str,
    output_path: str = "mindmap.xmind"
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

    # Export to XMind format
    export_to_xmind(mindmap, output_path)

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i")
    parser.add_argument("--output", "-o", default="mindmap.xmind")
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    if args.test:
        content = "Quantum computing uses qubits. Key concepts: superposition, entanglement, quantum gates. Applications: cryptography, drug discovery, optimization."
        result = generate_mindmap(content, "test_mindmap.xmind")
        print(f"Test mindmap: {result}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        result = generate_mindmap(content, args.output)
        print(f"Mind map: {result}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
