---
name: quiz
description: Generate quizzes with multiple question types from research materials. This skill should be used when users want to create assessments with multiple choice, true/false, and short answer questions.
---

# Quiz

Create interactive quizzes with multiple question types, answer keys, and explanations from research materials.

## When to Use This Skill

Use this skill when:
- Creating assessments from research content
- Generating practice tests
- Building quiz-based learning materials
- Producing evaluation tools

## How to Use

### Quick Test

```bash
cd quiz
python main.py --test
```

### Generate Quiz

```bash
python main.py --input research.txt --output quiz.html --num 10 --difficulty medium
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output filename (.html or .json)
- `--num`: Number of questions (default: 10)
- `--difficulty`: Difficulty level - easy, medium, hard (default: medium)

### Python API

```python
from main import generate_quiz

quiz_path = generate_quiz(
    content="Your research...",
    num_questions=15,
    difficulty="medium",
    output_path="quiz.html"
)
```

## What Gets Generated

- **HTML**: Interactive quiz with answer checking
- **JSON**: Raw quiz data with answers and explanations

## How It Works

1. **Question Generation** - Creates multiple choice, true/false, and short answer questions
2. **Distractor Creation** - Generates plausible wrong answers
3. **Explanation Writing** - Provides detailed answer explanations
4. **Interface Building** - Creates interactive HTML quiz

## Configuration

Requires `.env` file with API keys (already configured).

## Dependencies

```bash
pip install -r requirements.txt
```
