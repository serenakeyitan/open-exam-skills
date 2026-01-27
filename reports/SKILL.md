---
name: reports
description: Generate structured professional reports from research materials. This skill should be used when users need formal documents like executive summaries, research briefs, or analytical reports.
---

# Reports

Create structured professional reports with multiple sections, proper formatting, and export to various formats.

## When to Use This Skill

Use this skill when:
- Creating executive summaries from research
- Generating formal research briefs
- Producing analytical reports
- Converting research into professional documents

## How to Use

### Quick Test

```bash
cd reports
python main.py --test
```

### Generate Report

```bash
python main.py --input research.txt --output report.pdf --type executive_summary
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output filename (.md, .pdf, or .docx)
- `--type`: Report type - executive_summary, research_brief, analysis (default: executive_summary)

### Python API

```python
from main import generate_report

report_path = generate_report(
    content="Your research...",
    report_type="executive_summary",
    output_path="report.pdf"
)
```

## What Gets Generated

- **Markdown**: Plain text formatted report
- **PDF**: Professional document with styling
- **DOCX**: Editable Word document

## How It Works

1. **Content Analysis** - Extracts key findings and insights
2. **Structure Generation** - Creates multi-section document
3. **Formatting** - Applies professional styling
4. **Export** - Renders to chosen format

## Configuration

Requires `.env` file with API keys (already configured).

## Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- **python-docx** - Word documents
- **weasyprint** - PDF generation
- **markdown2** - Markdown processing
