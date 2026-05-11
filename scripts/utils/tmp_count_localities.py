"""Count unique localities in the restaurant dataset."""
import pandas as pd
from pathlib import Path

csv_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "restaurants_clean.csv"
df = pd.read_csv(csv_path)
localities = df['locality'].dropna().astype(str).str.strip().unique()
print(f"Unique localities: {len(localities)}")
