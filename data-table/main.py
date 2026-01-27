"""
Data Table Skill - Extract structured data from research
"""

import json
import argparse
import os
from typing import List, Dict
from pydantic import BaseModel
from loguru import logger
import sys
import pandas as pd

logger.remove()
logger.add(sys.stderr, level="INFO")


class DataTable(BaseModel):
    """Structured data table."""
    name: str
    description: str
    columns: List[str]
    rows: List[List[str]]


def generate_with_ai(content: str, api_key: str, provider: str = "gemini") -> str:
    """Extract data table using AI."""
    prompt = f"""Extract structured data from this content into a table format.

Content: {content[:10000]}

Identify entities, attributes, and relationships. Create a table with:
- name: Table name
- description: What the table represents
- columns: Column headers
- rows: Data rows (each row is an array of values)

Return as JSON:
{{
  "name": "Quantum Systems",
  "description": "Comparison of quantum computing systems",
  "columns": ["System", "Qubits", "Technology", "Year"],
  "rows": [
    ["IBM Q", "127", "Superconducting", "2023"],
    ["Google Sycamore", "70", "Superconducting", "2021"]
  ]
}}

If multiple tables are appropriate, return an array of tables."""

    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
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


def export_to_csv(table: DataTable, output_path: str) -> None:
    """Export table to CSV."""
    df = pd.DataFrame(table.rows, columns=table.columns)
    df.to_csv(output_path, index=False)
    logger.info(f"CSV exported: {output_path}")


def export_to_excel(table: DataTable, output_path: str) -> None:
    """Export table to Excel."""
    df = pd.DataFrame(table.rows, columns=table.columns)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=table.name[:31], index=False)  # Excel sheet name limit

        # Auto-adjust column widths
        worksheet = writer.sheets[table.name[:31]]
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(str(col))
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

    logger.info(f"Excel exported: {output_path}")


def export_to_json(table: DataTable, output_path: str) -> None:
    """Export table to JSON."""
    data = {
        "name": table.name,
        "description": table.description,
        "columns": table.columns,
        "rows": table.rows,
        # Also include row objects for easier consumption
        "data": [
            dict(zip(table.columns, row))
            for row in table.rows
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    logger.info(f"JSON exported: {output_path}")


def extract_data_table(
    content: str,
    output_path: str = "data.xlsx"
) -> str:
    """Extract data table from content."""
    logger.info("Extracting structured data...")

    # Get API key
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    if gemini_key:
        response = generate_with_ai(content, gemini_key, "gemini")
    elif anthropic_key:
        response = generate_with_ai(content, anthropic_key, "anthropic")
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

    # Handle single table or multiple tables
    if isinstance(data, dict):
        table = DataTable(**data)
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        # Multiple tables - use first one
        table = DataTable(**data[0])
        logger.info(f"Multiple tables found, using: {table.name}")

    logger.info(f"Extracted table: {table.name} ({len(table.rows)} rows, {len(table.columns)} columns)")

    # Export based on format
    if output_path.endswith('.csv'):
        export_to_csv(table, output_path)
    elif output_path.endswith('.xlsx'):
        export_to_excel(table, output_path)
    elif output_path.endswith('.json'):
        export_to_json(table, output_path)
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        # Default to CSV
        csv_path = output_path + '.csv'
        export_to_csv(table, csv_path)
        output_path = csv_path

    return output_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="data.xlsx")
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    if args.test:
        content = """
        Quantum Computing Systems:
        IBM Q has 127 qubits using superconducting technology, released in 2023.
        Google Sycamore has 70 qubits, also superconducting, from 2021.
        IonQ uses 32 trapped ion qubits, released in 2022.
        """
        result = extract_data_table(content, "test_data.xlsx")
        print(f"Test data table: {result}")
    else:
        if not args.input:
            parser.error("--input is required when not in test mode")
        with open(args.input) as f:
            content = f.read()
        result = extract_data_table(content, args.output)
        print(f"Data table generated: {result}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
