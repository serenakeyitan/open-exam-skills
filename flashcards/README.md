# Flashcards Skill

Generate study flashcards from research materials using AI.

## Features

- Question-answer pair generation
- Difficulty categorization
- Anki/Quizlet export
- Interactive HTML viewer

## Installation

```bash
cd flashcards
pip install -r requirements.txt
```

## Usage

```python
from main import generate_flashcards

cards = generate_flashcards(
    content="Your research...",
    num_cards=20,
    output_path="flashcards.json"
)
```

## Command Line

```bash
python main.py --input research.txt --output flashcards.json --num 20
```

## License

MIT
