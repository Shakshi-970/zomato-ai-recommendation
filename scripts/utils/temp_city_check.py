"""Quick city/locality count check on the restaurant dataset."""
import pandas as pd
from pathlib import Path

csv_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "restaurants_clean.csv"
df = pd.read_csv(csv_path, usecols=['city', 'locality'])

print('cities =', sorted(df['city'].dropna().unique()))
print('counts =', df['city'].value_counts().to_dict())
print('Mumbai rows =', len(df[df['city'] == 'Mumbai']))
print('Delhi rows  =', len(df[df['city'] == 'Delhi']))
print('Bengaluru sample localities =',
      sorted(df[df['city'] == 'Bengaluru']['locality'].dropna().unique())[:20])
