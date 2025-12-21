"""
Quick data exploration to understand column names and data structure
"""

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Fix: The database is MySQL/MariaDB
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'mysql+pymysql://')

# Create database connection
print("Connecting to database...")
engine = create_engine(DATABASE_URL)

print("✓ Connected!")
print()

# Get a small sample to see the data structure
print("=" * 80)
print("SAMPLE DATA (5 records)")
print("=" * 80)

query = "SELECT * FROM analytic_test_booking LIMIT 5"
sample = pd.read_sql(query, engine)

print(f"\nTotal columns: {len(sample.columns)}")
print(f"Column names:")
for i, col in enumerate(sample.columns, 1):
    print(f"  {i:2d}. {col}")

print("\n" + "=" * 80)
print("First record (transposed for readability):")
print("=" * 80)
print(sample.iloc[0].to_string())

print("\n" + "=" * 80)
print("Date columns check:")
print("=" * 80)

# Check which date column to use
date_cols = ['godate', 'paidon', 'createdon', 'createdon_date', 'stamp']
for col in date_cols:
    if col in sample.columns:
        print(f"\n{col}:")
        print(sample[col].head())

print("\n" + "=" * 80)
print("Key metric columns check:")
print("=" * 80)

# Check available metric columns
metric_cols = ['sysfee_usd', 'netprice_usd', 'agfee_usd', 'total_usd', 'seats', 'refund_date', 'refund_usd']
for col in metric_cols:
    if col in sample.columns:
        print(f"\n{col}: {sample[col].head().tolist()}")

engine.dispose()
print("\n✓ Done!")
