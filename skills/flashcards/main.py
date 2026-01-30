"""
Flashcards Skill - Convert JSON flashcards to interactive HTML
Pure frontend - AI generates JSON, this converts to interactive UI
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


def generate_notebooklm_html(flashcards: list, output_path: str, title: str = "Flashcards") -> None:
    """Generate interactive flashcard HTML."""

    logger.info(f"Generating HTML for {len(flashcards)} flashcards...")
    
    # Load and encode background images as base64
    script_dir = Path(__file__).parent
    confetti_black_path = script_dir / "Confetti_black.png"
    confetti_white_path = script_dir / "Confetti_white.png"
    
    confetti_black_b64 = ""
    confetti_white_b64 = ""
    
    if confetti_black_path.exists():
        with open(confetti_black_path, 'rb') as f:
            confetti_black_b64 = base64.b64encode(f.read()).decode('utf-8')
        logger.info("✓ Loaded Confetti_black.png")
    else:
        logger.warning(f"⚠ Confetti_black.png not found at {confetti_black_path}")
    
    if confetti_white_path.exists():
        with open(confetti_white_path, 'rb') as f:
            confetti_white_b64 = base64.b64encode(f.read()).decode('utf-8')
        logger.info("✓ Loaded Confetti_white.png")
    else:
        logger.warning(f"⚠ Confetti_white.png not found at {confetti_white_path}")

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #1b1b1b;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            position: relative;
        }}

        body::before,
        body::after {{
            content: "";
            position: fixed;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: rgba(120, 210, 255, 0.15);
            filter: blur(25px);
            pointer-events: none;
            z-index: 0;
        }}

        body::before {{
            top: 10%;
            left: 10%;
        }}

        body::after {{
            bottom: 10%;
            right: 10%;
        }}

        body > * {{
            position: relative;
            z-index: 1;
        }}

        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
            width: 100%;
            max-width: 600px;
        }}

        .header h1 {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .header .source {{
            font-size: 14px;
            opacity: 0.9;
        }}

        .instructions {{
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .card-container {{
            position: relative;
            width: 100%;
            max-width: 360px;
            height: 520px;
            perspective: 1000px;
        }}

        .card {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
            cursor: pointer;
        }}

        .card.flipped {{
            transform: rotateY(180deg);
        }}

        .card-face {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 16px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        }}

        .card-front {{
            background: #0f0f0f url('data:image/png;base64,{confetti_black_b64}') center / cover no-repeat;
            color: white;
        }}

        .card-back {{
            background: #ffffff url('data:image/png;base64,{confetti_white_b64}') center / cover no-repeat;
            color: #2d2d2d;
            transform: rotateY(180deg);
        }}

        .card-content {{
            font-size: 22px;
            line-height: 1.6;
            text-align: center;
            max-width: 100%;
            word-wrap: break-word;
        }}

        .card-back .card-content {{
            font-size: 20px;
            text-align: left;
            padding-left: 20px;
            padding-right: 20px;
        }}

        .card-back .card-content ul,
        .card-back .card-content ol {{
            text-align: left;
            margin: 16px 0;
            padding-left: 30px;
            list-style-position: outside;
        }}

        .card-back .card-content ul {{
            list-style-type: disc;
        }}

        .card-back .card-content ol {{
            list-style-type: decimal;
        }}

        .card-back .card-content li {{
            margin: 10px 0;
            line-height: 1.7;
            padding-left: 8px;
        }}

        .card-back .card-content .formatted-answer {{
            text-align: left;
            white-space: pre-line;
        }}

        .card-front .card-action {{
            position: absolute;
            bottom: 30px;
            color: rgba(255, 255, 255, 0.6);
            font-size: 14px;
        }}

        .card-back .card-action {{
            position: absolute;
            bottom: 30px;
            display: flex;
            gap: 12px;
        }}

        .explain-btn {{
            background: none;
            border: 1px solid #dadce0;
            color: #5f6368;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}

        .explain-btn:hover {{
            background: #f8f9fa;
            border-color: #5f6368;
        }}

        .navigation {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-top: 30px;
        }}

        .nav-btn {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: white;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        .nav-btn:hover:not(:disabled) {{
            background: #f8f9fa;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        .nav-btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
        }}

        .nav-btn svg {{
            width: 20px;
            height: 20px;
            stroke: #5f6368;
            stroke-width: 2;
            fill: none;
        }}

        .controls {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin-top: 20px;
        }}

        .progress {{
            color: white;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .control-btn {{
            background: none;
            border: none;
            cursor: pointer;
            padding: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: opacity 0.2s;
        }}

        .control-btn:hover {{
            opacity: 0.7;
        }}

        .control-btn svg {{
            width: 20px;
            height: 20px;
            stroke: white;
            stroke-width: 2;
            fill: none;
        }}

        .download-icon {{
            fill: white;
            stroke: none;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="source">Based on 1 source</div>
    </div>

    <div class="instructions">
        Press "Space" to flip, "← / →" to navigate
    </div>

    <div class="card-container">
        <div class="card" id="card">
            <div class="card-face card-front">
                <div class="card-content" id="question"></div>
                <div class="card-action">See answer</div>
            </div>
            <div class="card-face card-back">
                <div class="card-content" id="answer"></div>
            </div>
        </div>
    </div>

    <div class="navigation">
        <button class="nav-btn" id="prev-btn" onclick="previousCard()">
            <svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <button class="nav-btn" id="next-btn" onclick="nextCard()">
            <svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
        </button>
    </div>

    <div class="controls">
        <button class="control-btn" onclick="resetCards()" title="Reset">
            <svg viewBox="0 0 24 24">
                <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                <path d="M21 3v5h-5"/>
                <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                <path d="M3 21v-5h5"/>
            </svg>
        </button>
        <div class="progress">
            <span id="current">1</span> / <span id="total">{total}</span> cards
        </div>
        <button class="control-btn" onclick="downloadCSV()" title="Download CSV">
            <svg viewBox="0 0 24 24" class="download-icon">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
        </button>
    </div>

    <script>
        const flashcards = {flashcards_json};
        let currentIndex = 0;
        let isFlipped = false;

        function formatAnswerForExam(text) {{
            if (!text) return '';
            
            // Convert to string and escape HTML
            let formatted = String(text)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;');
            
            // Split by lines first
            const lines = formatted.split(/\\n|\\r\\n|\\r/);
            const items = [];
            let inList = false;
            
            for (let i = 0; i < lines.length; i++) {{
                const line = lines[i].trim();
                if (!line) continue;
                
                // Check for bullet points: •, -, *, ◦, ▪, or Unicode bullets
                const bulletMatch = line.match(/^[•\-\*◦▪▪▫]\s+(.+)$/);
                if (bulletMatch) {{
                    items.push({{type: 'bullet', content: bulletMatch[1]}});
                    inList = true;
                    continue;
                }}
                
                // Check for numbered lists: 1., 2., 3., etc. or 1), 2), 3), etc.
                const numberMatch = line.match(/^(\d+)[\.\)]\s+(.+)$/);
                if (numberMatch) {{
                    items.push({{type: 'number', content: numberMatch[2]}});
                    inList = true;
                    continue;
                }}
                
                // Check for lettered lists: a., b., c., etc. or a), b), c), etc.
                const letterMatch = line.match(/^([a-zA-Z])[\.\)]\s+(.+)$/);
                if (letterMatch) {{
                    items.push({{type: 'letter', content: letterMatch[2]}});
                    inList = true;
                    continue;
                }}
                
                // Regular text line
                items.push({{type: 'text', content: line}});
            }}
            
            // Build HTML output
            let html = '';
            let currentList = null;
            let listType = null;
            
            for (let i = 0; i < items.length; i++) {{
                const item = items[i];
                
                if (item.type === 'bullet' || item.type === 'number' || item.type === 'letter') {{
                    // Start a new list if needed
                    if (!currentList || listType !== item.type) {{
                        if (currentList) {{
                            html += '</ul>';
                        }}
                        currentList = [];
                        listType = item.type;
                        html += '<ul>';
                    }}
                    html += '<li>' + item.content + '</li>';
                }} else {{
                    // Close current list if open
                    if (currentList) {{
                        html += '</ul>';
                        currentList = null;
                        listType = null;
                    }}
                    // Add text with line break
                    html += '<div class="formatted-answer">' + item.content + '</div>';
                }}
            }}
            
            // Close any open list
            if (currentList) {{
                html += '</ul>';
            }}
            
            // If no lists were found, return as formatted text
            if (!html.includes('<ul>')) {{
                html = '<div class="formatted-answer">' + formatted.replace(/\\n/g, '<br>') + '</div>';
            }}
            
            return html;
        }}

        function updateCard() {{
            const card = document.getElementById('card');
            const question = document.getElementById('question');
            const answer = document.getElementById('answer');
            const current = document.getElementById('current');
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');

            // Update content
            question.textContent = flashcards[currentIndex].question;
            // Format answer for exam mode with proper line breaks
            answer.innerHTML = formatAnswerForExam(flashcards[currentIndex].answer);
            current.textContent = currentIndex + 1;

            // Reset flip
            if (isFlipped) {{
                card.classList.remove('flipped');
                isFlipped = false;
            }}

            // Update navigation buttons
            prevBtn.disabled = currentIndex === 0;
            nextBtn.disabled = currentIndex === flashcards.length - 1;
        }}

        function flipCard() {{
            const card = document.getElementById('card');
            card.classList.toggle('flipped');
            isFlipped = !isFlipped;
        }}

        function nextCard() {{
            if (currentIndex < flashcards.length - 1) {{
                currentIndex++;
                updateCard();
            }}
        }}

        function previousCard() {{
            if (currentIndex > 0) {{
                currentIndex--;
                updateCard();
            }}
        }}

        function resetCards() {{
            currentIndex = 0;
            updateCard();
        }}

        function downloadCSV() {{
            let csv = 'question,answer\\n';
            flashcards.forEach(card => {{
                const q = '"' + card.question.replace(/"/g, '""') + '"';
                const a = '"' + card.answer.replace(/"/g, '""') + '"';
                csv += q + ',' + a + '\\n';
            }});

            const blob = new Blob([csv], {{ type: 'text/csv' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '{title}_flashcards.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'Space') {{
                e.preventDefault();
                flipCard();
            }} else if (e.code === 'ArrowLeft') {{
                e.preventDefault();
                previousCard();
            }} else if (e.code === 'ArrowRight') {{
                e.preventDefault();
                nextCard();
            }}
        }});

        // Click to flip
        document.getElementById('card').addEventListener('click', flipCard);

        // Initialize
        updateCard();
    </script>
</body>
</html>"""

    # Generate HTML
    flashcards_json = json.dumps(flashcards)
    html = html_template.format(
        title=title,
        total=len(flashcards),
        flashcards_json=flashcards_json,
        confetti_black_b64=confetti_black_b64,
        confetti_white_b64=confetti_white_b64
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    logger.info(f"✓ Flashcards saved: {output_path}")


def convert_json_to_flashcards(json_path: str, output_path: str) -> str:
    """Convert JSON flashcards to interactive HTML."""

    logger.info("=" * 60)
    logger.info("FLASHCARDS CONVERSION STARTED")
    logger.info("=" * 60)

    # Verify input file exists
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Input file not found: {json_path}")

    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validate structure
    if isinstance(data, dict) and 'flashcards' in data:
        flashcards = data['flashcards']
        title = data.get('title', 'Flashcards')
    elif isinstance(data, list):
        flashcards = data
        title = "Flashcards"
    else:
        raise ValueError("Invalid JSON format. Expected array or {flashcards: [], title: ''}")

    if not flashcards:
        raise ValueError("No flashcards found in JSON")

    # Validate each flashcard has question and answer
    for i, card in enumerate(flashcards):
        if 'question' not in card or 'answer' not in card:
            raise ValueError(f"Card {i+1} missing 'question' or 'answer' field")

    logger.info(f"Loaded {len(flashcards)} flashcards")
    logger.info(f"Title: {title}")

    # Generate HTML
    generate_notebooklm_html(flashcards, output_path, title)

    file_size = os.path.getsize(output_path) / 1024

    logger.info("=" * 60)
    logger.info(f"✓ CONVERSION COMPLETED")
    logger.info(f"✓ Interactive flashcards saved: {output_path} ({file_size:.1f} KB)")
    logger.info("=" * 60)

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert JSON flashcards to interactive HTML"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input JSON file path"
    )
    parser.add_argument(
        "--output", "-o",
        default="flashcards.html",
        help="Output HTML file path (default: flashcards.html)"
    )

    args = parser.parse_args()

    try:
        result = convert_json_to_flashcards(args.input, args.output)

        if os.path.exists(result):
            size = os.path.getsize(result) / 1024
            print(f"✓ Flashcards created: {result} ({size:.1f} KB)")
            print(f"✓ Open in browser: file://{os.path.abspath(result)}")
            print()
            print("Features:")
            print("  • Click card to flip")
            print("  • Press Space to flip")
            print("  • Press ← → to navigate")
            print("  • Click download icon for CSV export")
        else:
            print(f"✗ Error: File not created at {result}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n✗ Conversion cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
