"""
Part D — AI-Augmented Task
--------------------------
Prompt used with Claude AI:
"Write a Python script that reads a CSV file, automatically detects the delimiter
(comma, tab, semicolon, or pipe), and converts it into a properly formatted JSON file.
Use csv.Sniffer() if possible. Handle edge cases like missing values and header rows."

The script below is the AI-generated output (tested and verified by student).
"""

import csv
import json
import sys
from pathlib import Path


def csv_to_json(input_file, output_file=None):
    """
    Reads a CSV file, auto-detects delimiter, and saves as JSON.
    Handles comma, tab, semicolon, and pipe delimiters.
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: File '{input_file}' not found.")
        return

    # Set output filename if not given
    if output_file is None:
        output_file = input_path.stem + ".json"

    with open(input_path, "r", newline="", encoding="utf-8") as f:
        # Read a sample to detect delimiter
        sample = f.read(2048)
        f.seek(0)

        try:
            # csv.Sniffer tries to figure out the delimiter automatically
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
            delimiter = dialect.delimiter
        except csv.Error:
            # If Sniffer fails, fall back to comma
            print("Sniffer could not detect delimiter. Defaulting to comma.")
            delimiter = ","

        print(f"Detected delimiter: repr='{repr(delimiter)}'")

        reader = csv.DictReader(f, delimiter=delimiter)
        rows = []
        for row in reader:
            # Replace empty strings with None for clean JSON output
            cleaned = {k: (v if v != "" else None) for k, v in row.items()}
            rows.append(cleaned)

    # Write to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    print(f"Converted {len(rows)} rows to '{output_file}'")
    return rows


# --- Test with two different CSV files ---
if __name__ == "__main__":
    # Test 1: comma-delimited (standard CSV)
    test1 = "test_comma.csv"
    with open(test1, "w", newline="") as f:
        f.write("name,age,city\nAlice,25,Mumbai\nBob,30,Delhi\nCarla,,Pune\n")

    print("--- Test 1: Comma-delimited CSV ---")
    csv_to_json(test1, "test_comma.json")

    # Test 2: pipe-delimited
    test2 = "test_pipe.csv"
    with open(test2, "w", newline="") as f:
        f.write("id|product|price\n1|Laptop|45000\n2|Mouse|900\n3|Keyboard|1400\n")

    print("\n--- Test 2: Pipe-delimited CSV ---")
    csv_to_json(test2, "test_pipe.json")

    # Show output preview
    print("\n--- Preview of test_comma.json ---")
    with open("test_comma.json") as f:
        print(f.read())

    print("--- Preview of test_pipe.json ---")
    with open("test_pipe.json") as f:
        print(f.read())
