"""
Flashcards Skill - Generate study flashcards
"""

import json
import argparse
import os
from typing import List
from pydantic import BaseModel
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")


class Flashcard(BaseModel):
    """A flashcard."""
    question: str
    answer: str
    difficulty: str = "medium"  # easy, medium, hard
    tags: List[str] = []


def generate_with_ai(content: str, num_cards: int, api_key: str, provider: str = "gemini") -> str:
    """Generate flashcards using AI."""
    prompt = f"""Create {num_cards} flashcards from this content.

Content: {content[:10000]}

Generate question-answer pairs for studying. Include:
- question: Clear, specific question
- answer: Concise, accurate answer
- difficulty: "easy", "medium", or "hard"
- tags: Relevant topic tags

Return as JSON array:
[
  {{
    "question": "What is quantum superposition?",
    "answer": "A quantum state where a qubit exists in multiple states simultaneously until measured.",
    "difficulty": "medium",
    "tags": ["quantum", "fundamentals"]
  }}
]"""

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
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


def export_to_anki(flashcards: List[Flashcard], output_path: str, deck_name: str = "Study Deck") -> None:
    """Export flashcards as Anki deck."""
    import genanki
    import random

    # Create model
    model_id = random.randrange(1 << 30, 1 << 31)
    model = genanki.Model(
        model_id,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    # Create deck
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, deck_name)

    # Add cards
    for card in flashcards:
        note = genanki.Note(
            model=model,
            fields=[card.question, card.answer],
            tags=card.tags
        )
        deck.add_note(note)

    # Export
    genanki.Package(deck).write_to_file(output_path)
    logger.info(f"Anki deck saved: {output_path}")


def export_to_html(flashcards: List[Flashcard], output_path: str) -> None:
    """Export flashcards as interactive HTML."""
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Flashcards</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            background: #f0f0f0;
        }}
        .flashcard {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.3s;
        }}
        .flashcard:hover {{
            transform: scale(1.02);
        }}
        .question {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        }}
        .answer {{
            font-size: 18px;
            color: #34495e;
            display: none;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #3498db;
        }}
        .flashcard.flipped .answer {{
            display: block;
        }}
        .difficulty {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 14px;
            margin-top: 10px;
        }}
        .difficulty.easy {{ background: #2ecc71; color: white; }}
        .difficulty.medium {{ background: #f39c12; color: white; }}
        .difficulty.hard {{ background: #e74c3c; color: white; }}
        .tags {{
            margin-top: 10px;
            font-size: 14px;
            color: #7f8c8d;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
        }}
    </style>
    <script>
        function flipCard(element) {{
            element.classList.toggle('flipped');
        }}
    </script>
</head>
<body>
    <h1>Study Flashcards</h1>
    <p style="text-align: center; color: #7f8c8d;">Click cards to reveal answers</p>
    {cards_html}
</body>
</html>
"""

    cards_html = ""
    for i, card in enumerate(flashcards, 1):
        tags_str = ", ".join(card.tags) if card.tags else ""
        cards_html += f"""
    <div class="flashcard" onclick="flipCard(this)">
        <div class="question">{i}. {card.question}</div>
        <div class="difficulty {card.difficulty}">{card.difficulty.upper()}</div>
        <div class="tags">{tags_str}</div>
        <div class="answer">{card.answer}</div>
    </div>
"""

    final_html = html_template.format(cards_html=cards_html)

    with open(output_path, 'w') as f:
        f.write(final_html)

    logger.info(f"HTML flashcards saved: {output_path}")


def generate_flashcards(
    content: str,
    num_cards: int = 20,
    output_path: str = "flashcards.json"
) -> str:
    """Generate flashcards from content."""
    logger.info(f"Generating {num_cards} flashcards...")

    # Get API key
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    if gemini_key:
        response = generate_with_ai(content, num_cards, gemini_key, "gemini")
    elif anthropic_key:
        response = generate_with_ai(content, num_cards, anthropic_key, "anthropic")
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
    flashcards = [Flashcard(**card) for card in data]

    logger.info(f"Generated {len(flashcards)} flashcards")

    # Export based on format
    if output_path.endswith('.apkg'):
        export_to_anki(flashcards, output_path)
    elif output_path.endswith('.html'):
        export_to_html(flashcards, output_path)
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        # JSON export
        with open(output_path, 'w') as f:
            json.dump([card.dict() for card in flashcards], f, indent=2)
        logger.info(f"JSON flashcards saved: {output_path}")

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="flashcards.json")
    parser.add_argument("--num", "-n", type=int, default=20)
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    if args.test:
        content = "Quantum computing uses qubits. Superposition allows multiple states. Entanglement creates quantum correlation. Quantum gates manipulate qubits."
        result = generate_flashcards(content, 5, "test_flashcards.html")
        print(f"Test flashcards: {result}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        result = generate_flashcards(content, args.num, args.output)
        print(f"Flashcards generated: {result}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
