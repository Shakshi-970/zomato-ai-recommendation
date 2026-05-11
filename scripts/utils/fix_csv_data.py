"""Fix city/locality columns in the processed restaurant CSV."""
import pandas as pd
from pathlib import Path

csv_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "restaurants_clean.csv"
df = pd.read_csv(csv_path)

CITY_PATTERNS = {
    'bengaluru': 'Bengaluru', 'bangalore': 'Bengaluru',
    'delhi': 'Delhi', 'mumbai': 'Mumbai', 'chennai': 'Chennai',
    'kolkata': 'Kolkata', 'pune': 'Pune', 'hyderabad': 'Hyderabad',
    'ahmedabad': 'Ahmedabad',
}

def extract_city(locality_str):
    if pd.isna(locality_str):
        return 'Unknown'
    text = str(locality_str).lower()
    for pattern, city in CITY_PATTERNS.items():
        if pattern in text:
            return city
    return 'Bengaluru'

df['extracted_city'] = df['locality'].apply(extract_city)
df['new_locality'] = df['city']
df['city'] = df['extracted_city']
df['locality'] = df['new_locality']
df = df.drop(columns=['extracted_city', 'new_locality'])

df.to_csv(csv_path, index=False)
print(f"Updated CSV: {len(df)} rows")
print(f"Cities: {sorted(df['city'].unique())}")
print(f"Sample localities: {sorted(df['locality'].unique())[:10]}")
