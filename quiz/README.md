# Quiz Skill

Generate quizzes with multiple question types from research materials using AI.

## Features

- Multiple choice, true/false, short answer questions
- Difficulty levels
- Answer keys with explanations
- Interactive HTML interface

## Installation

```bash
cd quiz
pip install -r requirements.txt
```

## Usage

```python
from main import generate_quiz

quiz = generate_quiz(
    content="Your research...",
    num_questions=10,
    difficulty="medium",
    output_path="quiz.html"
)
```

## Command Line

```bash
python main.py --input research.txt --output quiz.html --num 10 --difficulty medium
```

## License

MIT
