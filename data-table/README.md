# Data Table Skill

Extract structured data tables from research materials using AI.

## Features

- Entity extraction
- Relationship mapping
- Multi-table support
- Export to CSV, JSON, Excel

## Installation

```bash
cd data-table
pip install -r requirements.txt
```

## Usage

```python
from main import extract_data_table

table = extract_data_table(
    content="Your research...",
    output_path="data.xlsx"
)
```

## Command Line

```bash
python main.py --input research.txt --output data.xlsx
```

## License

MIT
