"""
Fix and improve charts based on feedback
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'mysql+pymysql://')

engine = create_engine(DATABASE_URL)
print("✓ Connected")

# ============================================================================
# FIX 1: Vehicle Class Analysis - Cleaner with Percentages
# ============================================================================
print("\nFixing vehicle class analysis chart...")

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
ORDER BY year, bookings DESC;
"""

vehicle_data = pd.read_sql(query_vehicle, engine)

# Calculate percentages
for year in [2019, 2023]:
    year_data = vehicle_data[vehicle_data['year'] == year]
    total_bookings = year_data['bookings'].sum()
    vehicle_data.loc[vehicle_data['year'] == year, 'pct'] = (
        year_data['bookings'] / total_bookings * 100
    )

fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Chart 1: EPS by Vehicle Class with Percentage Labels
ax = axes[0, 0]
vehicle_classes = sorted(vehicle_data['vehicle_class'].unique())
x = np.arange(len(vehicle_classes))
width = 0.35

for i, year in enumerate([2019, 2023]):
    data = vehicle_data[vehicle_data['year'] == year]
    eps_values = [data[data['vehicle_class'] == vc]['eps'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                  for vc in vehicle_classes]
    pct_values = [data[data['vehicle_class'] == vc]['pct'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                  for vc in vehicle_classes]

    bars = ax.bar(x + i*width, eps_values, width, label=str(year), alpha=0.85)

    # Add percentage labels on bars
    for j, (bar, pct) in enumerate(zip(bars, pct_values)):
        if pct > 0:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{pct:.1f}%',
                    ha='center', va='bottom', fontsize=8, rotation=90)

ax.set_title('EPS by Vehicle Class with Market Share %', fontsize=14, fontweight='bold')
ax.set_xlabel('Vehicle Class', fontsize=12)
ax.set_ylabel('EPS (USD)', fontsize=12)
ax.set_xticks(x + width/2)
ax.set_xticklabels(vehicle_classes, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Chart 2: Market Share Comparison
ax = axes[0, 1]
data_2019 = vehicle_data[vehicle_data['year'] == 2019].sort_values('pct', ascending=False)
data_2023 = vehicle_data[vehicle_data['year'] == 2023].sort_values('pct', ascending=False)

x_pos = np.arange(len(vehicle_classes))
pct_2019 = [data_2019[data_2019['vehicle_class'] == vc]['pct'].values[0] if len(data_2019[data_2019['vehicle_class'] == vc]) > 0 else 0
            for vc in vehicle_classes]
pct_2023 = [data_2023[data_2023['vehicle_class'] == vc]['pct'].values[0] if len(data_2023[data_2023['vehicle_class'] == vc]) > 0 else 0
            for vc in vehicle_classes]

bars1 = ax.barh(x_pos - width/2, pct_2019, width, label='2019', alpha=0.85, color='#3498db')
bars2 = ax.barh(x_pos + width/2, pct_2023, width, label='2023', alpha=0.85, color='#e74c3c')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        width_val = bar.get_width()
        if width_val > 0.5:
            ax.text(width_val, bar.get_y() + bar.get_height()/2,
                    f'{width_val:.1f}%',
                    ha='left', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(x_pos)
ax.set_yticklabels(vehicle_classes)
ax.set_xlabel('Market Share (%)', fontsize=12)
ax.set_title('Market Share Distribution by Vehicle Class', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='x', alpha=0.3)

# Chart 3: EPS Change 2019 → 2023
ax = axes[1, 0]
eps_changes = []
for vc in vehicle_classes:
    eps_2019 = vehicle_data[(vehicle_data['year'] == 2019) & (vehicle_data['vehicle_class'] == vc)]['eps'].values
    eps_2023 = vehicle_data[(vehicle_data['year'] == 2023) & (vehicle_data['vehicle_class'] == vc)]['eps'].values

    if len(eps_2019) > 0 and len(eps_2023) > 0:
        change = eps_2023[0] - eps_2019[0]
    elif len(eps_2023) > 0:
        change = eps_2023[0]
    else:
        change = 0
    eps_changes.append(change)

colors = ['#27ae60' if x >= 0 else '#e74c3c' for x in eps_changes]
bars = ax.barh(range(len(vehicle_classes)), eps_changes, alpha=0.85, color=colors)

# Add value labels
for bar, val in zip(bars, eps_changes):
    width_val = bar.get_width()
    ax.text(width_val + (0.1 if width_val >= 0 else -0.1), bar.get_y() + bar.get_height()/2,
            f'${val:+.2f}',
            ha='left' if width_val >= 0 else 'right', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(range(len(vehicle_classes)))
ax.set_yticklabels(vehicle_classes)
ax.set_xlabel('EPS Change (USD)', fontsize=12)
ax.set_title('EPS Change by Vehicle Class (2019 → 2023)', fontsize=14, fontweight='bold')
ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax.grid(axis='x', alpha=0.3)

# Chart 4: Revenue Contribution
ax = axes[1, 1]
revenue_2019 = [vehicle_data[(vehicle_data['year'] == 2019) & (vehicle_data['vehicle_class'] == vc)]['total_revenue'].values[0]
                if len(vehicle_data[(vehicle_data['year'] == 2019) & (vehicle_data['vehicle_class'] == vc)]) > 0 else 0
                for vc in vehicle_classes]
revenue_2023 = [vehicle_data[(vehicle_data['year'] == 2023) & (vehicle_data['vehicle_class'] == vc)]['total_revenue'].values[0]
                if len(vehicle_data[(vehicle_data['year'] == 2023) & (vehicle_data['vehicle_class'] == vc)]) > 0 else 0
                for vc in vehicle_classes]

total_rev_2019 = sum(revenue_2019)
total_rev_2023 = sum(revenue_2023)
rev_pct_2019 = [r/total_rev_2019*100 if total_rev_2019 > 0 else 0 for r in revenue_2019]
rev_pct_2023 = [r/total_rev_2023*100 if total_rev_2023 > 0 else 0 for r in revenue_2023]

x_pos = np.arange(len(vehicle_classes))
ax.barh(x_pos - width/2, rev_pct_2019, width, label='2019', alpha=0.85, color='#9b59b6')
ax.barh(x_pos + width/2, rev_pct_2023, width, label='2023', alpha=0.85, color='#e67e22')

ax.set_yticks(x_pos)
ax.set_yticklabels(vehicle_classes)
ax.set_xlabel('Revenue Contribution (%)', fontsize=12)
ax.set_title('Revenue Contribution by Vehicle Class', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/03_vehicle_class_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Fixed: charts/03_vehicle_class_analysis.png")
plt.close()

# ============================================================================
# FIX 2: Route Analysis - Better visualization
# ============================================================================
print("\nFixing route analysis chart...")

query_routes = """
SELECT
    YEAR(createdon_date) as year,
    from_station_name,
    to_station_name,
    COUNT(*) as bookings,
    SUM(seats) as total_seats,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(SUM(total_usd), 2) as total_revenue
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND from_station_name IS NOT NULL
    AND to_station_name IS NOT NULL
GROUP BY YEAR(createdon_date), from_station_name, to_station_name
HAVING bookings > 500
ORDER BY year, bookings DESC;
"""

routes_data = pd.read_sql(query_routes, engine)

# Create route labels
routes_data['route'] = routes_data['from_station_name'].str[:20] + ' → ' + routes_data['to_station_name'].str[:20]

fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Chart 1: Top 12 Routes by Volume 2019
ax = axes[0, 0]
top_12_2019 = routes_data[routes_data['year'] == 2019].head(12)
y_pos = np.arange(len(top_12_2019))
bars = ax.barh(y_pos, top_12_2019['bookings'], alpha=0.85, color='#3498db', edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, top_12_2019['bookings']):
    ax.text(val + 100, bar.get_y() + bar.get_height()/2, f'{val:,}',
            ha='left', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(top_12_2019['route'], fontsize=9)
ax.set_xlabel('Number of Bookings', fontsize=12)
ax.set_title('Top 12 Routes by Booking Volume - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 2: Top 12 Routes by Volume 2023
ax = axes[0, 1]
top_12_2023 = routes_data[routes_data['year'] == 2023].head(12)
y_pos = np.arange(len(top_12_2023))
bars = ax.barh(y_pos, top_12_2023['bookings'], alpha=0.85, color='#e74c3c', edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, top_12_2023['bookings']):
    ax.text(val + 200, bar.get_y() + bar.get_height()/2, f'{val:,}',
            ha='left', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(top_12_2023['route'], fontsize=9)
ax.set_xlabel('Number of Bookings', fontsize=12)
ax.set_title('Top 12 Routes by Booking Volume - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 3: Top 12 Routes by EPS 2019
ax = axes[1, 0]
top_eps_2019 = routes_data[routes_data['year'] == 2019].nlargest(12, 'eps')
y_pos = np.arange(len(top_eps_2019))
colors = ['#27ae60' if x > 3 else '#f39c12' if x > 1.5 else '#95a5a6' for x in top_eps_2019['eps']]
bars = ax.barh(y_pos, top_eps_2019['eps'], alpha=0.85, color=colors, edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val, bookings in zip(bars, top_eps_2019['eps'], top_eps_2019['bookings']):
    ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
            f'${val:.2f} ({bookings:,} bookings)',
            ha='left', va='center', fontsize=8, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(top_eps_2019['route'], fontsize=9)
ax.set_xlabel('EPS (USD)', fontsize=12)
ax.set_title('Top 12 Routes by EPS - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 4: Top 12 Routes by EPS 2023
ax = axes[1, 1]
top_eps_2023 = routes_data[routes_data['year'] == 2023].nlargest(12, 'eps')
y_pos = np.arange(len(top_eps_2023))
colors = ['#27ae60' if x > 3 else '#f39c12' if x > 1.5 else '#95a5a6' for x in top_eps_2023['eps']]
bars = ax.barh(y_pos, top_eps_2023['eps'], alpha=0.85, color=colors, edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val, bookings in zip(bars, top_eps_2023['eps'], top_eps_2023['bookings']):
    ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
            f'${val:.2f} ({bookings:,} bookings)',
            ha='left', va='center', fontsize=8, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(top_eps_2023['route'], fontsize=9)
ax.set_xlabel('EPS (USD)', fontsize=12)
ax.set_title('Top 12 Routes by EPS - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/04_route_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Fixed: charts/04_route_analysis.png")
plt.close()

print("\n✓ Charts fixed successfully!")
engine.dispose()
