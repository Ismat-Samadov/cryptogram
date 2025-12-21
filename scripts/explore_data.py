"""
12Go Travel Data Analysis - Initial Data Exploration
Purpose: Understand the database schema and data structure
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Fix: The database is actually MySQL/MariaDB, not PostgreSQL
# Convert postgresql:// to mysql+pymysql://
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'mysql+pymysql://')
    print("Note: Database is MySQL/MariaDB, not PostgreSQL")

# Create database connection
print("Connecting to database...")
engine = create_engine(DATABASE_URL)

# Test connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT DATABASE(), @@version"))
    db_info = result.fetchone()
    print(f"✓ Connected to database: {db_info[0]}")
    print(f"✓ MySQL/MariaDB version: {db_info[1][:80]}")
    print()

# List all tables
print("=" * 80)
print("EXPLORING DATABASE SCHEMA")
print("=" * 80)
print()

query_tables = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
"""

tables = pd.read_sql(query_tables, engine)
print(f"Total tables found: {len(tables)}")
print("\nAvailable tables:")
for idx, table in enumerate(tables['table_name'], 1):
    print(f"  {idx}. {table}")
print()

# Explore the main booking table structure
print("=" * 80)
print("ANALYTIC_TEST_BOOKING TABLE STRUCTURE")
print("=" * 80)
print()

query_columns = """
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'analytic_test_booking'
ORDER BY ordinal_position;
"""

columns_info = pd.read_sql(query_columns, engine)
print(f"Total columns: {len(columns_info)}")
print()
print(columns_info.to_string(index=False))
print()

# Get basic statistics
print("=" * 80)
print("DATASET STATISTICS")
print("=" * 80)
print()

query_stats = """
SELECT
    COUNT(*) as total_bookings,
    MIN(date_book) as earliest_booking,
    MAX(date_book) as latest_booking,
    COUNT(DISTINCT operator_id) as unique_operators,
    COUNT(DISTINCT route_id) as unique_routes,
    COUNT(DISTINCT seller_id) as unique_sellers,
    COUNT(DISTINCT vehicle_class) as unique_vehicle_classes
FROM analytic_test_booking;
"""

stats = pd.read_sql(query_stats, engine)
print(stats.T.to_string())
print()

# Check data availability for our analysis period
print("=" * 80)
print("DATA AVAILABILITY CHECK (2019 vs 2023)")
print("=" * 80)
print()

query_year_check = """
SELECT
    EXTRACT(YEAR FROM date_book) as year,
    EXTRACT(MONTH FROM date_book) as month,
    COUNT(*) as bookings
FROM analytic_test_booking
WHERE EXTRACT(YEAR FROM date_book) IN (2019, 2023)
    AND EXTRACT(MONTH FROM date_book) BETWEEN 1 AND 9
GROUP BY
    EXTRACT(YEAR FROM date_book),
    EXTRACT(MONTH FROM date_book)
ORDER BY year, month;
"""

year_check = pd.read_sql(query_year_check, engine)
print(year_check.to_string(index=False))
print()

# Get a sample of the data
print("=" * 80)
print("SAMPLE DATA (First 3 records)")
print("=" * 80)
print()

query_sample = """
SELECT *
FROM analytic_test_booking
LIMIT 3;
"""

sample_data = pd.read_sql(query_sample, engine)
# Transpose for better readability
print(sample_data.T.to_string())
print()

# Check for key fields we'll need
print("=" * 80)
print("KEY METRICS VALIDATION")
print("=" * 80)
print()

query_metrics = """
SELECT
    COUNT(*) as total_records,
    COUNT(sysfee) as sysfee_count,
    COUNT(agfee) as agfee_count,
    COUNT(netprice) as netprice_count,
    COUNT(seats) as seats_count,
    COUNT(CASE WHEN seats > 0 THEN 1 END) as positive_seats,
    AVG(sysfee) as avg_sysfee,
    AVG(netprice) as avg_netprice
FROM analytic_test_booking
WHERE EXTRACT(YEAR FROM date_book) IN (2019, 2023)
    AND EXTRACT(MONTH FROM date_book) BETWEEN 1 AND 9;
"""

metrics = pd.read_sql(query_metrics, engine)
print(metrics.T.to_string())
print()

print("=" * 80)
print("DATA EXPLORATION COMPLETE!")
print("=" * 80)
print("\nNext step: Run EPS analysis script")

engine.dispose()
