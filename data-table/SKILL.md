---
name: data-table
description: Extract structured data tables from research materials. This skill should be used when users want to organize information into tabular format with entities, attributes, and relationships.
---

# Data Table

Extract entities and relationships from research materials and generate structured data tables in multiple formats.

## When to Use This Skill

Use this skill when:
- Extracting structured data from unstructured text
- Creating comparison tables
- Organizing research findings into tables
- Generating datasets for analysis

## How to Use

### Quick Test

```bash
cd data-table
python main.py --test
```

### Extract Data Table

```bash
python main.py --input research.txt --output data.xlsx
```

Parameters:
- `--input`: Path to research materials
- `--output`: Output filename (.xlsx, .csv, or .json)

### Python API

```python
from main import extract_data_table

table_path = extract_data_table(
    content="Your research...",
    output_path="data.xlsx"
)
```

## What Gets Generated

- **Excel (.xlsx)**: Formatted spreadsheet with styling
- **CSV**: Plain text comma-separated values
- **JSON**: Structured data with metadata

## How It Works

1. **Entity Extraction** - Identifies key entities and attributes
2. **Relationship Mapping** - Determines how entities relate
3. **Schema Generation** - Creates table structure
4. **Data Population** - Fills table with extracted information
5. **Export** - Formats for chosen output type

## Configuration

Requires `.env` file with API keys (already configured).

## Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- **pandas** - Data manipulation
- **openpyxl** - Excel file handling
