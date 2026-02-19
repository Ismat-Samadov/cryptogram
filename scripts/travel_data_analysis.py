#!/usr/bin/env python
# coding: utf-8

# # 12Go Travel Data Analysis - EPS Investigation
# 
# **Objective:** Investigate EPS (Earn Per Seat) changes between 2019 and 2023
# 
# **Key Metrics:**
# - EPS = System Fee (USD) / Number of Seats
# - Comparing Q1-Q3 2019 vs Q1-Q3 2023


# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHARTS_DIR = PROJECT_ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

def display(obj):
    """Notebook-compatible display fallback for script execution."""
    print(obj)

print("✓ Libraries imported successfully")



# Load environment variables and create database connection
load_dotenv(PROJECT_ROOT / ".env")
DATABASE_URL = os.getenv('DATABASE_URL')

# Fix: Database is MySQL/MariaDB, not PostgreSQL
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'mysql+pymysql://')
    print("Note: Converted PostgreSQL URL to MySQL")

# Create engine
engine = create_engine(DATABASE_URL)

# Test connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT DATABASE(), @@version"))
    db_info = result.fetchone()
    print(f"✓ Connected to database: {db_info[0]}")
    print(f"✓ MySQL/MariaDB version: {db_info[1][:50]}...")


# ## 1. Data Exploration - Understanding the Schema


# Get table structure
query_columns = """
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'analytic_test_booking'
ORDER BY ordinal_position;
"""

columns_info = pd.read_sql(query_columns, engine)
print(f"Total columns: {len(columns_info)}")
print("\nKey columns:")
display(columns_info.head(15))



# Get sample data
query_sample = "SELECT * FROM analytic_test_booking LIMIT 3"
sample_data = pd.read_sql(query_sample, engine)

print("Sample record (transposed):")
display(sample_data.iloc[0].to_frame())


# ## 2. Overall EPS Analysis


# Calculate EPS for 2019 vs 2023
query_eps = """
SELECT
    YEAR(createdon_date) as year,
    COUNT(*) as total_bookings,
    SUM(seats) as total_seats,
    SUM(sysfee_usd) as total_sysfee,
    SUM(agfee_usd) as total_agfee,
    SUM(netprice_usd) as total_netprice,
    SUM(total_usd) as total_revenue,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(AVG(sysfee_usd), 2) as avg_sysfee_per_booking,
    COUNT(CASE WHEN refund_date IS NOT NULL THEN 1 END) as refunded_bookings,
    ROUND(COUNT(CASE WHEN refund_date IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as refund_rate_pct
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
GROUP BY YEAR(createdon_date)
ORDER BY year;
"""

eps_data = pd.read_sql(query_eps, engine)
print("EPS Comparison - Q1-Q3:")
display(eps_data)

if len(eps_data) == 2:
    eps_change = eps_data.iloc[1]['eps'] - eps_data.iloc[0]['eps']
    eps_pct_change = (eps_change / eps_data.iloc[0]['eps']) * 100
    print(f"\n📊 EPS Change: ${eps_change:.2f} ({eps_pct_change:+.2f}%)")
    print(f"📊 Booking Volume Change: {eps_data.iloc[1]['total_bookings'] - eps_data.iloc[0]['total_bookings']:+,}")
    print(f"📊 Refund Rate Change: {eps_data.iloc[1]['refund_rate_pct'] - eps_data.iloc[0]['refund_rate_pct']:+.2f}%")



# Visualize EPS comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: EPS Comparison
colors = ['#3498db', '#e74c3c']
axes[0].bar(eps_data['year'].astype(str), eps_data['eps'], color=colors, alpha=0.8, edgecolor='black', linewidth=2)
axes[0].set_title('EPS (Earn Per Seat) - 2019 vs 2023', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('EPS (USD)')
axes[0].grid(axis='y', alpha=0.3)
for i, v in enumerate(eps_data['eps']):
    axes[0].text(i, v, f'${v:.2f}', ha='center', va='bottom', fontweight='bold')

# Chart 2: Total Bookings
axes[1].bar(eps_data['year'].astype(str), eps_data['total_bookings'], color=colors, alpha=0.8, edgecolor='black', linewidth=2)
axes[1].set_title('Total Bookings - 2019 vs 2023', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Number of Bookings')
axes[1].grid(axis='y', alpha=0.3)
for i, v in enumerate(eps_data['total_bookings']):
    axes[1].text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()


# ## 3. Monthly Trends Analysis


# Monthly EPS trends
query_monthly = """
SELECT
    YEAR(createdon_date) as year,
    MONTH(createdon_date) as month,
    COUNT(*) as bookings,
    SUM(seats) as seats,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(AVG(total_usd), 2) as avg_booking_value
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
GROUP BY YEAR(createdon_date), MONTH(createdon_date)
ORDER BY year, month;
"""

monthly_trends = pd.read_sql(query_monthly, engine)
print("Monthly EPS Trends:")
display(monthly_trends)

# Plot
fig, ax = plt.subplots(figsize=(14, 6))

for year in [2019, 2023]:
    data = monthly_trends[monthly_trends['year'] == year]
    ax.plot(data['month'], data['eps'], marker='o', linewidth=2.5, label=f'{year}', markersize=8)

ax.set_title('Monthly EPS Trends - 2019 vs 2023 (Q1-Q3)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('EPS (USD)')
ax.set_xticks(range(1, 10))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'])
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# ## 4. Vehicle Class Analysis


# EPS by vehicle class
query_vehicle = """
SELECT
    YEAR(createdon_date) as year,
    vehclass_id as vehicle_class,
    COUNT(*) as bookings,
    SUM(seats) as seats,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(SUM(total_usd), 2) as total_revenue
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND vehclass_id IS NOT NULL
GROUP BY YEAR(createdon_date), vehclass_id
ORDER BY year, eps DESC;
"""

vehicle_analysis = pd.read_sql(query_vehicle, engine)

# Calculate market share percentages
for year in [2019, 2023]:
    year_data = vehicle_analysis[vehicle_analysis['year'] == year]
    total = year_data['bookings'].sum()
    vehicle_analysis.loc[vehicle_analysis['year'] == year, 'market_share_pct'] = (
        year_data['bookings'] / total * 100
    )

print("EPS by Vehicle Class:")
display(vehicle_analysis.round(2))



# Visualize vehicle class comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

vehicle_classes = sorted(vehicle_analysis['vehicle_class'].unique())
x = np.arange(len(vehicle_classes))
width = 0.35

# Chart 1: EPS by vehicle class
for i, year in enumerate([2019, 2023]):
    data = vehicle_analysis[vehicle_analysis['year'] == year]
    eps_values = [data[data['vehicle_class'] == vc]['eps'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                  for vc in vehicle_classes]
    axes[0].bar(x + i*width, eps_values, width, label=str(year), alpha=0.8)

axes[0].set_title('EPS by Vehicle Class - 2019 vs 2023', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Vehicle Class')
axes[0].set_ylabel('EPS (USD)')
axes[0].set_xticks(x + width/2)
axes[0].set_xticklabels(vehicle_classes, rotation=45, ha='right')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Chart 2: Market share
for i, year in enumerate([2019, 2023]):
    data = vehicle_analysis[vehicle_analysis['year'] == year]
    mkt_share = [data[data['vehicle_class'] == vc]['market_share_pct'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                 for vc in vehicle_classes]
    axes[1].bar(x + i*width, mkt_share, width, label=str(year), alpha=0.8)

axes[1].set_title('Market Share by Vehicle Class', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Vehicle Class')
axes[1].set_ylabel('Market Share (%)')
axes[1].set_xticks(x + width/2)
axes[1].set_xticklabels(vehicle_classes, rotation=45, ha='right')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()


# ## 5. Geographic Analysis


# Top customer origin countries
query_countries = """
SELECT
    YEAR(createdon_date) as year,
    user_origin_country_id as country,
    COUNT(*) as bookings,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND user_origin_country_id IS NOT NULL
GROUP BY YEAR(createdon_date), user_origin_country_id
HAVING bookings > 1000
ORDER BY year, bookings DESC
LIMIT 30;
"""

country_data = pd.read_sql(query_countries, engine)
print("Top Customer Origin Countries:")
display(country_data.head(20))


# ## 6. Summary Statistics


# Generate summary
print("="*80)
print(" " * 25 + "EPS ANALYSIS SUMMARY")
print("="*80)
print()
print("PERIOD: Q1-Q3 2019 vs Q1-Q3 2023")
print()
print("KEY FINDINGS:")
print("-" * 80)

if len(eps_data) == 2:
    for _, row in eps_data.iterrows():
        print(f"\n{int(row['year'])}:")
        print(f"  Total Bookings: {row['total_bookings']:,}")
        print(f"  Total Seats: {row['total_seats']:,.0f}")
        print(f"  Total Revenue: ${row['total_revenue']:,.2f}")
        print(f"  EPS: ${row['eps']:.2f}")
        print(f"  Refund Rate: {row['refund_rate_pct']:.2f}%")

    eps_delta = eps_data.iloc[1]['eps'] - eps_data.iloc[0]['eps']
    eps_pct = (eps_delta / eps_data.iloc[0]['eps']) * 100
    
    print("\n" + "="*80)
    print(f"\n🎯 EPS CHANGE: ${eps_delta:.2f} ({eps_pct:+.2f}%)")
    
    if eps_pct > 0:
        print("\n✅ POSITIVE FINDING: EPS INCREASED despite massive growth!")
    else:
        print("\n⚠️ ATTENTION: EPS DECREASED - Investigation needed")
    
    booking_growth = ((eps_data.iloc[1]['total_bookings'] - eps_data.iloc[0]['total_bookings']) / 
                     eps_data.iloc[0]['total_bookings'] * 100)
    print(f"📈 BOOKING GROWTH: +{booking_growth:.1f}%")
    
    refund_change = eps_data.iloc[1]['refund_rate_pct'] - eps_data.iloc[0]['refund_rate_pct']
    print(f"{'✅' if refund_change < 0 else '⚠️'} REFUND RATE CHANGE: {refund_change:+.2f}%")

print("\n" + "="*80)
print("\nAnalysis complete! Check README.md for full presentation.")
print(f"Charts available in {CHARTS_DIR}")



# Close connection
engine.dispose()
print("\n✓ Database connection closed")
