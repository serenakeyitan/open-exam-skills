# Reports Skill

Generate structured professional reports from research materials using AI.

## Features

- Multiple report types (executive summary, research brief, analysis)
- Professional formatting
- Export to Markdown, PDF, DOCX
- Citation management

## Installation

```bash
cd reports
pip install -r requirements.txt
```

## Configuration

```bash
GEMINI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## Usage

```python
from main import generate_report

report = generate_report(
    content="Your research...",
    report_type="executive_summary",
    output_path="report.pdf"
)
```

## Command Line

```bash
python main.py --input research.txt --output report.pdf --type executive_summary
```

## License

MIT
