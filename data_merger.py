import csv
import json
from pathlib import Path
from datetime import datetime

# --- Step 1: Read all CSV files using pathlib.glob ---
data_folder = Path(".")
all_rows = []

for file in sorted(data_folder.glob("data*.csv")):
    with open(file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_rows.append(row)

files_processed = len(list(data_folder.glob("data*.csv")))
print(f"Total rows read (with duplicates): {len(all_rows)}")

# --- Step 2: Remove duplicate rows ---
# Convert each row to a tuple so it can be added to a set
seen = set()
unique_rows = []

for row in all_rows:
    # key based on all four fields
    key = (row["date"], row["product"], row["qty"], row["price"])
    if key not in seen:
        seen.add(key)
        unique_rows.append(row)

print(f"Rows after removing duplicates: {len(unique_rows)}")

# --- Step 3: Calculate revenue per product ---
revenue_by_product = {}

for row in unique_rows:
    product = row["product"]
    revenue = int(row["qty"]) * float(row["price"])
    if product not in revenue_by_product:
        revenue_by_product[product] = 0.0
    revenue_by_product[product] += revenue

total_revenue = sum(revenue_by_product.values())

# --- Step 4a: Export merged_sales.csv sorted by date ---
unique_rows_sorted = sorted(unique_rows, key=lambda r: r["date"])

with open("merged_sales.csv", "w", newline="") as f:
    fieldnames = ["date", "product", "qty", "price"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(unique_rows_sorted)

print("merged_sales.csv written successfully.")

# --- Step 4b: Export revenue_summary.json ---
summary = {
    "metadata": {
        "files_processed": files_processed,
        "total_rows": len(unique_rows),
        "total_revenue": round(total_revenue, 2),
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    },
    "revenue_by_product": {k: round(v, 2) for k, v in revenue_by_product.items()}
}

with open("revenue_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("revenue_summary.json written successfully.")
print("\n--- Revenue Summary ---")
for product, rev in revenue_by_product.items():
    print(f"  {product}: {rev:.2f}")
print(f"\nTotal Revenue: {total_revenue:.2f}")
