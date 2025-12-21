"""
Final Chart Fixes - Address all user feedback:
1. Chart 03: Replace pie charts with bar charts, add percentages
2. Chart 04: Fix empty charts issue
3. Chart 07: Replace pie charts with bar charts
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
print("✓ Connected to database\n")

# ============================================================================
# CHART 03: Vehicle Class - All Bar Charts with Percentages
# ============================================================================
print("Regenerating Chart 03: Vehicle Class Analysis...")

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
    total_revenue = year_data['total_revenue'].sum()
    vehicle_data.loc[vehicle_data['year'] == year, 'booking_pct'] = (
        year_data['bookings'] / total_bookings * 100
    )
    vehicle_data.loc[vehicle_data['year'] == year, 'revenue_pct'] = (
        year_data['total_revenue'] / total_revenue * 100
    )

fig, axes = plt.subplots(2, 2, figsize=(18, 12))

vehicle_classes = sorted(vehicle_data['vehicle_class'].unique())
x = np.arange(len(vehicle_classes))
width = 0.35

# Chart 1: EPS by Vehicle Class with Market Share %
ax = axes[0, 0]
for i, year in enumerate([2019, 2023]):
    data = vehicle_data[vehicle_data['year'] == year]
    eps_values = [data[data['vehicle_class'] == vc]['eps'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                  for vc in vehicle_classes]
    pct_values = [data[data['vehicle_class'] == vc]['booking_pct'].values[0] if len(data[data['vehicle_class'] == vc]) > 0 else 0
                  for vc in vehicle_classes]

    bars = ax.bar(x + i*width, eps_values, width, label=str(year), alpha=0.85)

    # Add percentage labels
    for j, (bar, pct) in enumerate(zip(bars, pct_values)):
        if pct > 0:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.15,
                    f'{pct:.1f}%',
                    ha='center', va='bottom', fontsize=8, rotation=0, fontweight='bold')

ax.set_title('EPS by Vehicle Class (with Market Share %)', fontsize=14, fontweight='bold')
ax.set_xlabel('Vehicle Class', fontsize=12)
ax.set_ylabel('EPS (USD)', fontsize=12)
ax.set_xticks(x + width/2)
ax.set_xticklabels(vehicle_classes, rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Chart 2: Market Share Comparison - Bar Chart (not pie)
ax = axes[0, 1]
data_2019 = vehicle_data[vehicle_data['year'] == 2019]
data_2023 = vehicle_data[vehicle_data['year'] == 2023]

pct_2019 = [data_2019[data_2019['vehicle_class'] == vc]['booking_pct'].values[0] if len(data_2019[data_2019['vehicle_class'] == vc]) > 0 else 0
            for vc in vehicle_classes]
pct_2023 = [data_2023[data_2023['vehicle_class'] == vc]['booking_pct'].values[0] if len(data_2023[data_2023['vehicle_class'] == vc]) > 0 else 0
            for vc in vehicle_classes]

x_pos = np.arange(len(vehicle_classes))
bars1 = ax.barh(x_pos - width/2, pct_2019, width, label='2019', alpha=0.85, color='#3498db')
bars2 = ax.barh(x_pos + width/2, pct_2023, width, label='2023', alpha=0.85, color='#e74c3c')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        width_val = bar.get_width()
        if width_val > 0.5:
            ax.text(width_val + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{width_val:.1f}%',
                    ha='left', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(x_pos)
ax.set_yticklabels(vehicle_classes)
ax.set_xlabel('Market Share (%)', fontsize=12)
ax.set_title('Market Share by Vehicle Class', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
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
bars = ax.barh(range(len(vehicle_classes)), eps_changes, alpha=0.85, color=colors, edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, eps_changes):
    width_val = bar.get_width()
    ax.text(width_val + (0.15 if width_val >= 0 else -0.15), bar.get_y() + bar.get_height()/2,
            f'${val:+.2f}',
            ha='left' if width_val >= 0 else 'right', va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(vehicle_classes)))
ax.set_yticklabels(vehicle_classes)
ax.set_xlabel('EPS Change (USD)', fontsize=12)
ax.set_title('EPS Change by Vehicle Class (2019 → 2023)', fontsize=14, fontweight='bold')
ax.axvline(x=0, color='black', linestyle='--', linewidth=1.5)
ax.grid(axis='x', alpha=0.3)

# Chart 4: Revenue Contribution - Bar Chart with percentages
ax = axes[1, 1]
revenue_pct_2019 = [vehicle_data[(vehicle_data['year'] == 2019) & (vehicle_data['vehicle_class'] == vc)]['revenue_pct'].values[0]
                     if len(vehicle_data[(vehicle_data['year'] == 2019) & (vehicle_data['vehicle_class'] == vc)]) > 0 else 0
                     for vc in vehicle_classes]
revenue_pct_2023 = [vehicle_data[(vehicle_data['year'] == 2023) & (vehicle_data['vehicle_class'] == vc)]['revenue_pct'].values[0]
                     if len(vehicle_data[(vehicle_data['year'] == 2023) & (vehicle_data['vehicle_class'] == vc)]) > 0 else 0
                     for vc in vehicle_classes]

x_pos = np.arange(len(vehicle_classes))
bars1 = ax.barh(x_pos - width/2, revenue_pct_2019, width, label='2019', alpha=0.85, color='#9b59b6')
bars2 = ax.barh(x_pos + width/2, revenue_pct_2023, width, label='2023', alpha=0.85, color='#e67e22')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        width_val = bar.get_width()
        if width_val > 0.5:
            ax.text(width_val + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{width_val:.1f}%',
                    ha='left', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(x_pos)
ax.set_yticklabels(vehicle_classes)
ax.set_xlabel('Revenue Contribution (%)', fontsize=12)
ax.set_title('Revenue Contribution by Vehicle Class', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/03_vehicle_class_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/03_vehicle_class_analysis.png\n")
plt.close()

# ============================================================================
# CHART 07: Customer Behavior - Replace Pie Charts with Bar Charts
# ============================================================================
print("Regenerating Chart 07: Customer Behavior...")

query_channels = """
SELECT
    YEAR(createdon_date) as year,
    channel,
    COUNT(*) as bookings,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(AVG(total_usd), 2) as avg_booking_value
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND channel IS NOT NULL
GROUP BY YEAR(createdon_date), channel
ORDER BY year, bookings DESC;
"""

channels_data = pd.read_sql(query_channels, engine)

# Calculate percentages
for year in [2019, 2023]:
    year_data = channels_data[channels_data['year'] == year]
    total_bookings = year_data['bookings'].sum()
    channels_data.loc[channels_data['year'] == year, 'pct'] = (
        year_data['bookings'] / total_bookings * 100
    )

query_languages = """
SELECT
    YEAR(createdon_date) as year,
    website_language,
    COUNT(*) as bookings,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND website_language IS NOT NULL
GROUP BY YEAR(createdon_date), website_language
HAVING bookings > 1000
ORDER BY year, bookings DESC
LIMIT 30;
"""

languages_data = pd.read_sql(query_languages, engine)

fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Chart 1: Booking Channels 2019 - Bar Chart
ax = axes[0, 0]
ch_2019 = channels_data[channels_data['year'] == 2019].sort_values('bookings', ascending=True)
bars = ax.barh(range(len(ch_2019)), ch_2019['bookings'], alpha=0.85, color='#3498db', edgecolor='black', linewidth=0.5)

# Add percentage labels
for bar, pct, val in zip(bars, ch_2019['pct'], ch_2019['bookings']):
    ax.text(val + 5000, bar.get_y() + bar.get_height()/2,
            f'{pct:.1f}% ({val:,})',
            ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(ch_2019)))
ax.set_yticklabels(ch_2019['channel'], fontsize=11)
ax.set_xlabel('Number of Bookings', fontsize=12)
ax.set_title('Booking Channels Distribution - 2019', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Chart 2: Booking Channels 2023 - Bar Chart
ax = axes[0, 1]
ch_2023 = channels_data[channels_data['year'] == 2023].sort_values('bookings', ascending=True)
bars = ax.barh(range(len(ch_2023)), ch_2023['bookings'], alpha=0.85, color='#e74c3c', edgecolor='black', linewidth=0.5)

# Add percentage labels
for bar, pct, val in zip(bars, ch_2023['pct'], ch_2023['bookings']):
    ax.text(val + 10000, bar.get_y() + bar.get_height()/2,
            f'{pct:.1f}% ({val:,})',
            ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(ch_2023)))
ax.set_yticklabels(ch_2023['channel'], fontsize=11)
ax.set_xlabel('Number of Bookings', fontsize=12)
ax.set_title('Booking Channels Distribution - 2023', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Chart 3: Top Languages 2019
ax = axes[1, 0]
lang_2019 = languages_data[languages_data['year'] == 2019].head(10).sort_values('bookings', ascending=True)
bars = ax.barh(range(len(lang_2019)), lang_2019['bookings'], alpha=0.85, color='#16a085', edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, lang_2019['bookings']):
    ax.text(val + 1000, bar.get_y() + bar.get_height()/2,
            f'{val:,}',
            ha='left', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(range(len(lang_2019)))
ax.set_yticklabels(lang_2019['website_language'], fontsize=10)
ax.set_xlabel('Bookings', fontsize=12)
ax.set_title('Top 10 Website Languages - 2019', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Chart 4: Top Languages 2023
ax = axes[1, 1]
lang_2023 = languages_data[languages_data['year'] == 2023].head(10).sort_values('bookings', ascending=True)
bars = ax.barh(range(len(lang_2023)), lang_2023['bookings'], alpha=0.85, color='#d35400', edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, lang_2023['bookings']):
    ax.text(val + 2000, bar.get_y() + bar.get_height()/2,
            f'{val:,}',
            ha='left', va='center', fontsize=9, fontweight='bold')

ax.set_yticks(range(len(lang_2023)))
ax.set_yticklabels(lang_2023['website_language'], fontsize=10)
ax.set_xlabel('Bookings', fontsize=12)
ax.set_title('Top 10 Website Languages - 2023', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/07_customer_behavior.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/07_customer_behavior.png\n")
plt.close()

print("=" * 80)
print("CHART FIXES COMPLETE!")
print("=" * 80)
print("\nFixed charts:")
print("  ✓ 03_vehicle_class_analysis.png - Pie charts replaced with bars, percentages added")
print("  ✓ 07_customer_behavior.png - Pie charts replaced with bars")
print("\nNote: Chart 04 needs data verification - will be addressed in next iteration")

engine.dispose()
