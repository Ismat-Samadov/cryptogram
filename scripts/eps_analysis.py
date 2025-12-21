"""
12Go Travel Data Analysis - EPS Root Cause Analysis
Investigating EPS (Earn Per Seat) decrease between 2019 and 2023

Key Metrics:
- EPS = sysfee_usd / seats (company's earn per seat)
- Comparing Q1-Q3 2019 vs Q1-Q3 2023
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Fix: Database is MySQL/MariaDB
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'mysql+pymysql://')

# Create database connection
print("Connecting to database...")
engine = create_engine(DATABASE_URL)
print("✓ Connected to 12Go database")
print()

# Create charts directory
os.makedirs('/Users/ismatsamadov/travel_data_analyse/charts', exist_ok=True)

# ============================================================================
# 1. OVERALL EPS COMPARISON
# ============================================================================
print("=" * 80)
print("1. OVERALL EPS ANALYSIS - 2019 vs 2023")
print("=" * 80)

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
print("\nEPS Comparison - Q1-Q3:")
print(eps_data.to_string(index=False))

if len(eps_data) == 2:
    eps_change = eps_data.iloc[1]['eps'] - eps_data.iloc[0]['eps']
    eps_pct_change = (eps_change / eps_data.iloc[0]['eps']) * 100
    print(f"\n📊 EPS Change: ${eps_change:.2f} ({eps_pct_change:+.2f}%)")
    print(f"📊 Booking Volume Change: {eps_data.iloc[1]['total_bookings'] - eps_data.iloc[0]['total_bookings']:+,}")
    print(f"📊 Refund Rate Change: {eps_data.iloc[1]['refund_rate_pct'] - eps_data.iloc[0]['refund_rate_pct']:+.2f}%")

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Chart 1: EPS Comparison
ax = axes[0, 0]
colors = ['#2ecc71' if v > eps_data.iloc[0]['eps'] else '#e74c3c' for v in eps_data['eps']]
bars = ax.bar(eps_data['year'].astype(str), eps_data['eps'], color=colors, alpha=0.8, edgecolor='black', linewidth=2)
ax.set_title('EPS (Earn Per Seat) - 2019 vs 2023', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('EPS (USD)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
for i, (v, y) in enumerate(zip(eps_data['eps'], eps_data['year'])):
    ax.text(i, v + 0.02, f'${v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Chart 2: Total Bookings
ax = axes[0, 1]
ax.bar(eps_data['year'].astype(str), eps_data['total_bookings'], color=['#3498db', '#9b59b6'], alpha=0.8, edgecolor='black', linewidth=2)
ax.set_title('Total Bookings - 2019 vs 2023', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Bookings', fontsize=12)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(eps_data['total_bookings']):
    ax.text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Chart 3: Average Revenue Breakdown
ax = axes[1, 0]
x = np.arange(len(eps_data))
width = 0.25
ax.bar(x - width, eps_data['total_sysfee'] / eps_data['total_bookings'], width, label='Avg Sysfee', alpha=0.8)
ax.bar(x, eps_data['total_agfee'] / eps_data['total_bookings'], width, label='Avg Agfee', alpha=0.8)
ax.bar(x + width, eps_data['total_netprice'] / eps_data['total_bookings'], width, label='Avg Netprice', alpha=0.8)
ax.set_title('Average Revenue Components per Booking', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('USD', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(eps_data['year'].astype(str))
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Chart 4: Refund Rate
ax = axes[1, 1]
ax.bar(eps_data['year'].astype(str), eps_data['refund_rate_pct'], color=['#e67e22', '#e74c3c'], alpha=0.8, edgecolor='black', linewidth=2)
ax.set_title('Refund Rate - 2019 vs 2023', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Refund Rate (%)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(eps_data['refund_rate_pct']):
    ax.text(i, v, f'{v:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/01_eps_overview.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: charts/01_eps_overview.png")
plt.close()

# ============================================================================
# 2. MONTHLY TRENDS
# ============================================================================
print("\n" + "=" * 80)
print("2. MONTHLY EPS TRENDS")
print("=" * 80)

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

monthly_data = pd.read_sql(query_monthly, engine)
print("\nMonthly breakdown:")
print(monthly_data.to_string(index=False))

# Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Monthly EPS Trends
ax = axes[0]
for year in [2019, 2023]:
    data = monthly_data[monthly_data['year'] == year]
    ax.plot(data['month'], data['eps'], marker='o', linewidth=2.5, label=f'{year}', markersize=8)

ax.set_title('Monthly EPS Trends - 2019 vs 2023 (Q1-Q3)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('EPS (USD)', fontsize=12)
ax.set_xticks(range(1, 10))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'])
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

# Monthly Booking Volume
ax = axes[1]
for year in [2019, 2023]:
    data = monthly_data[monthly_data['year'] == year]
    ax.plot(data['month'], data['bookings'], marker='s', linewidth=2.5, label=f'{year}', markersize=8)

ax.set_title('Monthly Booking Volume - 2019 vs 2023 (Q1-Q3)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Bookings', fontsize=12)
ax.set_xticks(range(1, 10))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'])
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/02_monthly_trends.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: charts/02_monthly_trends.png")
plt.close()

# ============================================================================
# 3. VEHICLE CLASS ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("3. VEHICLE CLASS ANALYSIS")
print("=" * 80)

query_vehicle = """
SELECT
    YEAR(createdon_date) as year,
    vehclass_id as vehicle_class,
    COUNT(*) as bookings,
    SUM(seats) as seats,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(SUM(total_usd), 2) as total_revenue,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY YEAR(createdon_date)), 2) as pct_of_bookings
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND vehclass_id IS NOT NULL
GROUP BY YEAR(createdon_date), vehclass_id
ORDER BY year, bookings DESC;
"""

vehicle_data = pd.read_sql(query_vehicle, engine)
print("\nVehicle Class Performance:")
print(vehicle_data.to_string(index=False))

# Get top vehicle classes
vehicle_classes = sorted(vehicle_data['vehicle_class'].unique())

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Chart 1: EPS by Vehicle Class
ax = axes[0, 0]
x = np.arange(len(vehicle_classes))
width = 0.35

for i, year in enumerate([2019, 2023]):
    data = vehicle_data[vehicle_data['year'] == year]
    eps_values = [data[data['vehicle_class'] == vc]['eps'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                  for vc in vehicle_classes]
    ax.bar(x + i*width, eps_values, width, label=str(year), alpha=0.8)

ax.set_title('EPS by Vehicle Class - 2019 vs 2023', fontsize=14, fontweight='bold')
ax.set_xlabel('Vehicle Class', fontsize=12)
ax.set_ylabel('EPS (USD)', fontsize=12)
ax.set_xticks(x + width/2)
ax.set_xticklabels(vehicle_classes, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Chart 2: Booking Volume by Vehicle Class
ax = axes[0, 1]
for i, year in enumerate([2019, 2023]):
    data = vehicle_data[vehicle_data['year'] == year]
    booking_values = [data[data['vehicle_class'] == vc]['bookings'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                      for vc in vehicle_classes]
    ax.bar(x + i*width, booking_values, width, label=str(year), alpha=0.8)

ax.set_title('Booking Volume by Vehicle Class - 2019 vs 2023', fontsize=14, fontweight='bold')
ax.set_xlabel('Vehicle Class', fontsize=12)
ax.set_ylabel('Number of Bookings', fontsize=12)
ax.set_xticks(x + width/2)
ax.set_xticklabels(vehicle_classes, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Chart 3: Market Share by Vehicle Class (2019)
ax = axes[1, 0]
data_2019 = vehicle_data[vehicle_data['year'] == 2019]
ax.pie(data_2019['bookings'], labels=data_2019['vehicle_class'], autopct='%1.1f%%', startangle=90)
ax.set_title('2019 - Market Share by Vehicle Class', fontsize=14, fontweight='bold')

# Chart 4: Market Share by Vehicle Class (2023)
ax = axes[1, 1]
data_2023 = vehicle_data[vehicle_data['year'] == 2023]
ax.pie(data_2023['bookings'], labels=data_2023['vehicle_class'], autopct='%1.1f%%', startangle=90)
ax.set_title('2023 - Market Share by Vehicle Class', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/03_vehicle_class_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: charts/03_vehicle_class_analysis.png")
plt.close()

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nCharts saved in: /charts directory")
print("\nNext: Review charts and continue with deeper analysis")

engine.dispose()
