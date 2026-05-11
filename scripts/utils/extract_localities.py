"""Extract unique cities/localities from the processed restaurant dataset."""
import json
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
csv_path = ROOT / "data" / "processed" / "restaurants_clean.csv"

df = pd.read_csv(csv_path)
cities = sorted(df['city'].dropna().unique())

print(f"Total unique cities: {len(cities)}\n")
for i, loc in enumerate(cities, 1):
    print(f"{i:2d}. {loc}")

out = ROOT / "data" / "localities.json"
out.write_text(json.dumps({"total": len(cities), "localities": list(cities)}, indent=2))
print(f"\n✅ Saved {len(cities)} cities to {out}")
