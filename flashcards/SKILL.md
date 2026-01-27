---
name: flashcards
description: Generate study flashcards from research materials. This skill should be used when users want to create question-answer pairs for learning and spaced repetition.
---

# Flashcards

Extract question-answer pairs from research materials and generate interactive flashcards with difficulty categorization.

## When to Use This Skill

Use this skill when:
- Creating study materials from research
- Generating Q&A pairs for learning
- Producing flashcard decks for spaced repetition
- Building quiz prep materials

## How to Use

### Quick Test

```bash
cd flashcards
python main.py --test
```

### Generate Flashcards

```bash
python main.py --input research.txt --output flashcards.html --num 20
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output filename (.html, .apkg, or .json)
- `--num`: Number of flashcards (default: 20)

### Python API

```python
from main import generate_flashcards

cards_path = generate_flashcards(
    content="Your research...",
    num_cards=30,
    output_path="flashcards.apkg"  # Anki format
)
```

## What Gets Generated

- **HTML**: Interactive web-based flashcards
- **Anki (.apkg)**: Import directly into Anki app
- **JSON**: Raw flashcard data

## How It Works

1. **Q&A Extraction** - Identifies key concepts and creates questions
2. **Difficulty Assignment** - Categorizes as easy, medium, or hard
3. **Tag Organization** - Groups by topic
4. **Export** - Formats for chosen platform

## Configuration

Requires `.env` file with API keys (already configured).

## Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- **genanki** - Anki deck export
- **google-generativeai** - Q&A generation
