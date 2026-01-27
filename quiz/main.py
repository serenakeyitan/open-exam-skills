"""
Quiz Skill - Generate quizzes from research
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


class QuizQuestion(BaseModel):
    """A quiz question."""
    type: str  # multiple_choice, true_false, short_answer
    question: str
    options: List[str] = []  # For multiple choice
    correct_answer: str
    explanation: str
    difficulty: str = "medium"


def generate_with_ai(content: str, num_questions: int, difficulty: str, api_key: str, provider: str = "gemini") -> str:
    """Generate quiz using AI."""
    prompt = f"""Create a {difficulty} quiz with {num_questions} questions from this content.

Content: {content[:10000]}

Generate a mix of question types:
- multiple_choice: Question with 4 options
- true_false: Yes/no questions
- short_answer: Brief answer questions

Return as JSON array:
[
  {{
    "type": "multiple_choice",
    "question": "What is quantum superposition?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option B",
    "explanation": "Superposition means...",
    "difficulty": "{difficulty}"
  }},
  {{
    "type": "true_false",
    "question": "Qubits can only be 0 or 1",
    "options": ["True", "False"],
    "correct_answer": "False",
    "explanation": "Qubits can be in superposition...",
    "difficulty": "{difficulty}"
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


def export_to_html(questions: List[QuizQuestion], output_path: str) -> None:
    """Export quiz as interactive HTML."""
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Quiz</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            background: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
        }}
        .question {{
            background: white;
            padding: 30px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .question-text {{
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .options {{
            margin: 15px 0;
        }}
        .option {{
            padding: 12px;
            margin: 8px 0;
            background: #ecf0f1;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .option:hover {{
            background: #d5dbdb;
        }}
        .option.selected {{
            background: #3498db;
            color: white;
        }}
        .option.correct {{
            background: #2ecc71;
            color: white;
        }}
        .option.incorrect {{
            background: #e74c3c;
            color: white;
        }}
        .explanation {{
            margin-top: 15px;
            padding: 15px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
            display: none;
        }}
        .explanation.show {{
            display: block;
        }}
        button {{
            padding: 12px 24px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }}
        button:hover {{
            background: #2980b9;
        }}
        .score {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            display: none;
        }}
    </style>
    <script>
        let answers = {{}};

        function selectOption(questionId, option) {{
            answers[questionId] = option;

            // Update UI
            const questionDiv = document.getElementById('q' + questionId);
            const options = questionDiv.querySelectorAll('.option');
            options.forEach(opt => {{
                opt.classList.remove('selected');
                if (opt.textContent.includes(option)) {{
                    opt.classList.add('selected');
                }}
            }});
        }}

        function checkAnswer(questionId, correctAnswer) {{
            const userAnswer = answers[questionId];
            const questionDiv = document.getElementById('q' + questionId);
            const options = questionDiv.querySelectorAll('.option');
            const explanation = questionDiv.querySelector('.explanation');

            options.forEach(opt => {{
                opt.style.pointerEvents = 'none';
                const optText = opt.textContent.trim();
                if (optText.includes(correctAnswer)) {{
                    opt.classList.add('correct');
                }}
                if (userAnswer && optText.includes(userAnswer) && userAnswer !== correctAnswer) {{
                    opt.classList.add('incorrect');
                }}
            }});

            explanation.classList.add('show');
        }}

        function submitQuiz() {{
            const totalQuestions = {num_questions};
            let correct = 0;

            // Check all answers
            const buttons = document.querySelectorAll('button');
            buttons.forEach(button => {{
                if (button.textContent === 'Check Answer') {{
                    button.click();
                }}
            }});

            // Calculate score (would need more sophisticated tracking)
            document.getElementById('score').style.display = 'block';
            document.getElementById('score').innerHTML = 'Quiz Complete! Review your answers above.';
        }}
    </script>
</head>
<body>
    <h1>Quiz</h1>
    <p style="text-align: center; color: #7f8c8d;">Test your knowledge</p>

    {questions_html}

    <div style="text-align: center; margin: 30px 0;">
        <button onclick="submitQuiz()" style="font-size: 18px;">Submit Quiz</button>
    </div>

    <div id="score" class="score"></div>
</body>
</html>
"""

    questions_html = ""
    for i, q in enumerate(questions, 1):
        questions_html += f'<div class="question" id="q{i}">\n'
        questions_html += f'    <div class="question-text">{i}. {q.question}</div>\n'

        if q.type in ["multiple_choice", "true_false"]:
            questions_html += '    <div class="options">\n'
            for opt in q.options:
                questions_html += f'        <div class="option" onclick="selectOption({i}, \'{opt}\')">{opt}</div>\n'
            questions_html += '    </div>\n'
            questions_html += f'    <button onclick="checkAnswer({i}, \'{q.correct_answer}\')">Check Answer</button>\n'
        else:
            questions_html += f'    <p style="color: #7f8c8d;">Answer: {q.correct_answer}</p>\n'

        questions_html += f'    <div class="explanation"><strong>Explanation:</strong> {q.explanation}</div>\n'
        questions_html += '</div>\n'

    final_html = html_template.format(
        questions_html=questions_html,
        num_questions=len(questions)
    )

    with open(output_path, 'w') as f:
        f.write(final_html)

    logger.info(f"HTML quiz saved: {output_path}")


def generate_quiz(
    content: str,
    num_questions: int = 10,
    difficulty: str = "medium",
    output_path: str = "quiz.html"
) -> str:
    """Generate quiz from content."""
    logger.info(f"Generating quiz with {num_questions} questions ({difficulty})...")

    # Get API key
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    if gemini_key:
        response = generate_with_ai(content, num_questions, difficulty, gemini_key, "gemini")
    elif anthropic_key:
        response = generate_with_ai(content, num_questions, difficulty, anthropic_key, "anthropic")
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
    questions = [QuizQuestion(**q) for q in data]

    logger.info(f"Generated {len(questions)} questions")

    # Export
    if output_path.endswith('.html'):
        export_to_html(questions, output_path)
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        # JSON export
        with open(output_path, 'w') as f:
            json.dump([q.dict() for q in questions], f, indent=2)
        logger.info(f"JSON quiz saved: {output_path}")

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="quiz.html")
    parser.add_argument("--num", "-n", type=int, default=10)
    parser.add_argument("--difficulty", "-d", default="medium", choices=["easy", "medium", "hard"])
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    if args.test:
        content = "Quantum computing uses qubits. Superposition allows multiple states simultaneously. Entanglement creates quantum correlation. Quantum gates perform operations."
        result = generate_quiz(content, 5, "easy", "test_quiz.html")
        print(f"Test quiz: {result}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        result = generate_quiz(content, args.num, args.difficulty, args.output)
        print(f"Quiz generated: {result}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
