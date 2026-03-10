import csv
from pathlib import Path


# -------------------------------------------------------
# Q2 - find_large_files function
# -------------------------------------------------------

def find_large_files(directory, size_mb):
    """
    Recursively finds files larger than size_mb megabytes.
    Returns a list of (filename, size_in_mb) sorted by size descending.
    """
    results = []
    dir_path = Path(directory)

    # rglob searches recursively through all subdirectories
    for file in dir_path.rglob("*"):
        if file.is_file():
            size_in_mb = file.stat().st_size / (1024 * 1024)
            if size_in_mb > size_mb:
                results.append((file.name, round(size_in_mb, 4)))

    # Sort by file size in descending order
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# -------------------------------------------------------
# Q3 - Fixed merge_csv_files function
# -------------------------------------------------------

# Bug Fix 1: Added missing import (was missing at top of original code)
# Bug Fix 2: Added newline='' to both open() calls to avoid blank rows on Windows
# Bug Fix 3: Skip header row for all files after the first one to avoid duplicate headers

def merge_csv_files(file_list):
    all_data = []
    header_saved = False

    for filename in file_list:
        # Bug Fix 2: Added newline='' to prevent blank rows on Windows
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                # Bug Fix 3: Only include header from first file
                if i == 0:
                    if not header_saved:
                        all_data.append(row)
                        header_saved = True
                    # skip header rows from other files
                else:
                    all_data.append(row)

    # Bug Fix 2: Added newline='' here too
    with open("merged.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)

    return len(all_data)


# -------------------------------------------------------
# Quick test
# -------------------------------------------------------
if __name__ == "__main__":
    # Test find_large_files (using current directory as example)
    print("--- Testing find_large_files ---")
    large = find_large_files(".", 0.0001)  # low threshold just to show output
    if large:
        for name, size in large:
            print(f"  {name}: {size} MB")
    else:
        print("  No files found above threshold.")

    # Test merge_csv_files
    print("\n--- Testing merge_csv_files ---")
    files = ["data1.csv", "data2.csv", "data3.csv"]
    count = merge_csv_files(files)
    print(f"  Total rows written to merged.csv: {count}")
