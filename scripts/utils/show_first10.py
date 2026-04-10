"""Print the first 10 rows of the restaurant CSV as a markdown table."""
import pandas as pd
from pathlib import Path

csv_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "restaurants_clean.csv"

try:
    df = pd.read_csv(csv_path).head(10)
    cols = df.columns.tolist()

    def fmt(v):
        t = str(v).strip()
        return t[:117] + "..." if len(t) > 120 else t

    print("| " + " | ".join(cols) + " |")
    print("|" + "|".join(["-" * (len(c) + 2) for c in cols]) + "|")
    for row in df.values.tolist():
        print("| " + " | ".join(fmt(v) for v in row) + " |")
except FileNotFoundError:
    print(f"File not found: {csv_path}")
