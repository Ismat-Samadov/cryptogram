"""
12Go Travel Data - Deep Dive Analysis
Comprehensive root cause analysis with multiple dimensions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore')

# Setup
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'mysql+pymysql://')

engine = create_engine(DATABASE_URL)
print("✓ Connected to database")

os.makedirs('/Users/ismatsamadov/travel_data_analyse/charts', exist_ok=True)

# ============================================================================
# 4. TOP ROUTES ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("4. TOP ROUTES ANALYSIS")
print("=" * 80)

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
HAVING bookings > 100
ORDER BY year, bookings DESC
LIMIT 40;
"""

routes_data = pd.read_sql(query_routes, engine)
print(f"\nTop routes loaded: {len(routes_data)} records")

# Get top 10 routes per year
top_routes_2019 = routes_data[routes_data['year'] == 2019].head(10)
top_routes_2023 = routes_data[routes_data['year'] == 2023].head(10)

fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Chart 1: Top 10 Routes by Bookings 2019
ax = axes[0, 0]
route_labels_2019 = [f"{row['from_station_name'][:15]}→{row['to_station_name'][:15]}"
                     for _, row in top_routes_2019.iterrows()]
y_pos = np.arange(len(route_labels_2019))
ax.barh(y_pos, top_routes_2019['bookings'], alpha=0.8, color='#3498db')
ax.set_yticks(y_pos)
ax.set_yticklabels(route_labels_2019, fontsize=9)
ax.set_xlabel('Number of Bookings', fontsize=11)
ax.set_title('Top 10 Routes by Volume - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 2: Top 10 Routes by Bookings 2023
ax = axes[0, 1]
route_labels_2023 = [f"{row['from_station_name'][:15]}→{row['to_station_name'][:15]}"
                     for _, row in top_routes_2023.iterrows()]
y_pos = np.arange(len(route_labels_2023))
ax.barh(y_pos, top_routes_2023['bookings'], alpha=0.8, color='#e74c3c')
ax.set_yticks(y_pos)
ax.set_yticklabels(route_labels_2023, fontsize=9)
ax.set_xlabel('Number of Bookings', fontsize=11)
ax.set_title('Top 10 Routes by Volume - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 3: Top Routes by EPS 2019
ax = axes[1, 0]
top_eps_2019 = routes_data[routes_data['year'] == 2019].nlargest(10, 'eps')
route_labels_eps_2019 = [f"{row['from_station_name'][:15]}→{row['to_station_name'][:15]}"
                         for _, row in top_eps_2019.iterrows()]
y_pos = np.arange(len(route_labels_eps_2019))
colors_2019 = ['#27ae60' if x > 2 else '#f39c12' for x in top_eps_2019['eps']]
ax.barh(y_pos, top_eps_2019['eps'], alpha=0.8, color=colors_2019)
ax.set_yticks(y_pos)
ax.set_yticklabels(route_labels_eps_2019, fontsize=9)
ax.set_xlabel('EPS (USD)', fontsize=11)
ax.set_title('Top 10 Routes by EPS - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 4: Top Routes by EPS 2023
ax = axes[1, 1]
top_eps_2023 = routes_data[routes_data['year'] == 2023].nlargest(10, 'eps')
route_labels_eps_2023 = [f"{row['from_station_name'][:15]}→{row['to_station_name'][:15]}"
                         for _, row in top_eps_2023.iterrows()]
y_pos = np.arange(len(route_labels_eps_2023))
colors_2023 = ['#27ae60' if x > 2 else '#f39c12' for x in top_eps_2023['eps']]
ax.barh(y_pos, top_eps_2023['eps'], alpha=0.8, color=colors_2023)
ax.set_yticks(y_pos)
ax.set_yticklabels(route_labels_eps_2023, fontsize=9)
ax.set_xlabel('EPS (USD)', fontsize=11)
ax.set_title('Top 10 Routes by EPS - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/04_route_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/04_route_analysis.png")
plt.close()

# ============================================================================
# 5. GEOGRAPHIC ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("5. GEOGRAPHIC ANALYSIS")
print("=" * 80)

query_geography = """
SELECT
    YEAR(createdon_date) as year,
    from_country_id,
    to_country_id,
    COUNT(*) as bookings,
    SUM(seats) as total_seats,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(SUM(total_usd), 2) as total_revenue
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND from_country_id IS NOT NULL
    AND to_country_id IS NOT NULL
GROUP BY YEAR(createdon_date), from_country_id, to_country_id
ORDER BY year, bookings DESC;
"""

geo_data = pd.read_sql(query_geography, engine)
print(f"\nGeographic data loaded: {len(geo_data)} country pairs")

# Top country pairs
fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Chart 1: Top Country Pairs 2019
ax = axes[0, 0]
top_geo_2019 = geo_data[geo_data['year'] == 2019].head(15)
geo_labels_2019 = [f"{row['from_country_id']} → {row['to_country_id']}"
                   for _, row in top_geo_2019.iterrows()]
ax.barh(range(len(geo_labels_2019)), top_geo_2019['bookings'], alpha=0.8)
ax.set_yticks(range(len(geo_labels_2019)))
ax.set_yticklabels(geo_labels_2019, fontsize=9)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 15 Country Routes - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 2: Top Country Pairs 2023
ax = axes[0, 1]
top_geo_2023 = geo_data[geo_data['year'] == 2023].head(15)
geo_labels_2023 = [f"{row['from_country_id']} → {row['to_country_id']}"
                   for _, row in top_geo_2023.iterrows()]
ax.barh(range(len(geo_labels_2023)), top_geo_2023['bookings'], alpha=0.8)
ax.set_yticks(range(len(geo_labels_2023)))
ax.set_yticklabels(geo_labels_2023, fontsize=9)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 15 Country Routes - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 3: Customer Origin Countries 2019
ax = axes[1, 0]
query_origin = """
SELECT
    YEAR(createdon_date) as year,
    user_origin_country_id,
    COUNT(*) as bookings,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps
FROM analytic_test_booking
WHERE YEAR(createdon_date) = 2019
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND user_origin_country_id IS NOT NULL
GROUP BY YEAR(createdon_date), user_origin_country_id
ORDER BY bookings DESC
LIMIT 15;
"""
origin_2019 = pd.read_sql(query_origin, engine)
ax.barh(range(len(origin_2019)), origin_2019['bookings'], alpha=0.8, color='#9b59b6')
ax.set_yticks(range(len(origin_2019)))
ax.set_yticklabels(origin_2019['user_origin_country_id'], fontsize=9)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 15 Customer Origin Countries - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 4: Customer Origin Countries 2023
ax = axes[1, 1]
query_origin_2023 = query_origin.replace("2019", "2023")
origin_2023 = pd.read_sql(query_origin_2023, engine)
ax.barh(range(len(origin_2023)), origin_2023['bookings'], alpha=0.8, color='#e67e22')
ax.set_yticks(range(len(origin_2023)))
ax.set_yticklabels(origin_2023['user_origin_country_id'], fontsize=9)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 15 Customer Origin Countries - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/05_geographic_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/05_geographic_analysis.png")
plt.close()

# ============================================================================
# 6. OPERATOR PERFORMANCE
# ============================================================================
print("\n" + "=" * 80)
print("6. OPERATOR PERFORMANCE ANALYSIS")
print("=" * 80)

query_operators = """
SELECT
    YEAR(createdon_date) as year,
    operator_id,
    COUNT(*) as bookings,
    SUM(seats) as total_seats,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps,
    ROUND(SUM(total_usd), 2) as total_revenue,
    COUNT(CASE WHEN refund_date IS NOT NULL THEN 1 END) as refunds,
    ROUND(COUNT(CASE WHEN refund_date IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as refund_rate
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND operator_id IS NOT NULL
GROUP BY YEAR(createdon_date), operator_id
HAVING bookings > 500
ORDER BY year, bookings DESC;
"""

operators_data = pd.read_sql(query_operators, engine)
print(f"\nOperators analyzed: {len(operators_data)} operator-year combinations")

fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Chart 1: Top 15 Operators by Volume 2019
ax = axes[0, 0]
top_ops_2019 = operators_data[operators_data['year'] == 2019].head(15)
ax.barh(range(len(top_ops_2019)), top_ops_2019['bookings'], alpha=0.8, color='#3498db')
ax.set_yticks(range(len(top_ops_2019)))
ax.set_yticklabels([f"Operator {int(x)}" for x in top_ops_2019['operator_id']], fontsize=9)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 15 Operators by Volume - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 2: Top 15 Operators by Volume 2023
ax = axes[0, 1]
top_ops_2023 = operators_data[operators_data['year'] == 2023].head(15)
ax.barh(range(len(top_ops_2023)), top_ops_2023['bookings'], alpha=0.8, color='#e74c3c')
ax.set_yticks(range(len(top_ops_2023)))
ax.set_yticklabels([f"Operator {int(x)}" for x in top_ops_2023['operator_id']], fontsize=9)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 15 Operators by Volume - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 3: EPS vs Refund Rate scatter (2019)
ax = axes[1, 0]
ops_2019 = operators_data[operators_data['year'] == 2019]
scatter = ax.scatter(ops_2019['refund_rate'], ops_2019['eps'],
                     s=ops_2019['bookings']/50, alpha=0.6, c=ops_2019['total_revenue'],
                     cmap='viridis')
ax.set_xlabel('Refund Rate (%)', fontsize=11)
ax.set_ylabel('EPS (USD)', fontsize=11)
ax.set_title('Operator Performance: EPS vs Refund Rate - 2019\n(bubble size = volume)',
             fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax, label='Total Revenue')

# Chart 4: EPS vs Refund Rate scatter (2023)
ax = axes[1, 1]
ops_2023 = operators_data[operators_data['year'] == 2023]
scatter = ax.scatter(ops_2023['refund_rate'], ops_2023['eps'],
                     s=ops_2023['bookings']/50, alpha=0.6, c=ops_2023['total_revenue'],
                     cmap='viridis')
ax.set_xlabel('Refund Rate (%)', fontsize=11)
ax.set_ylabel('EPS (USD)', fontsize=11)
ax.set_title('Operator Performance: EPS vs Refund Rate - 2023\n(bubble size = volume)',
             fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax, label='Total Revenue')

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/06_operator_performance.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/06_operator_performance.png")
plt.close()

# ============================================================================
# 7. CUSTOMER BEHAVIOR ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("7. CUSTOMER BEHAVIOR ANALYSIS")
print("=" * 80)

# Payment channels
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
print(f"\nChannels analyzed: {len(channels_data)} channel-year combinations")

# Website languages
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

# Chart 1: Booking Channels 2019
ax = axes[0, 0]
ch_2019 = channels_data[channels_data['year'] == 2019]
ax.pie(ch_2019['bookings'], labels=ch_2019['channel'], autopct='%1.1f%%', startangle=90)
ax.set_title('Booking Channels Distribution - 2019', fontsize=13, fontweight='bold')

# Chart 2: Booking Channels 2023
ax = axes[0, 1]
ch_2023 = channels_data[channels_data['year'] == 2023]
ax.pie(ch_2023['bookings'], labels=ch_2023['channel'], autopct='%1.1f%%', startangle=90)
ax.set_title('Booking Channels Distribution - 2023', fontsize=13, fontweight='bold')

# Chart 3: Top Languages 2019
ax = axes[1, 0]
lang_2019 = languages_data[languages_data['year'] == 2019].head(10)
ax.barh(range(len(lang_2019)), lang_2019['bookings'], alpha=0.8, color='#16a085')
ax.set_yticks(range(len(lang_2019)))
ax.set_yticklabels(lang_2019['website_language'], fontsize=10)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 10 Website Languages - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

# Chart 4: Top Languages 2023
ax = axes[1, 1]
lang_2023 = languages_data[languages_data['year'] == 2023].head(10)
ax.barh(range(len(lang_2023)), lang_2023['bookings'], alpha=0.8, color='#d35400')
ax.set_yticks(range(len(lang_2023)))
ax.set_yticklabels(lang_2023['website_language'], fontsize=10)
ax.set_xlabel('Bookings', fontsize=11)
ax.set_title('Top 10 Website Languages - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/07_customer_behavior.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/07_customer_behavior.png")
plt.close()

# ============================================================================
# 8. BOOKING VALUE AND SEATS ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("8. BOOKING VALUE & SEATS ANALYSIS")
print("=" * 80)

query_seats = """
SELECT
    YEAR(createdon_date) as year,
    seats,
    COUNT(*) as bookings,
    ROUND(AVG(sysfee_usd), 2) as avg_sysfee,
    ROUND(AVG(total_usd), 2) as avg_total
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
    AND seats BETWEEN 1 AND 10
GROUP BY YEAR(createdon_date), seats
ORDER BY year, seats;
"""

seats_data = pd.read_sql(query_seats, engine)

# Booking value distribution
query_value_dist = """
SELECT
    YEAR(createdon_date) as year,
    CASE
        WHEN total_usd < 20 THEN '< $20'
        WHEN total_usd < 50 THEN '$20-50'
        WHEN total_usd < 100 THEN '$50-100'
        WHEN total_usd < 200 THEN '$100-200'
        WHEN total_usd < 500 THEN '$200-500'
        ELSE '$500+'
    END as value_range,
    COUNT(*) as bookings,
    ROUND(SUM(sysfee_usd) / SUM(seats), 2) as eps
FROM analytic_test_booking
WHERE YEAR(createdon_date) IN (2019, 2023)
    AND MONTH(createdon_date) BETWEEN 1 AND 9
GROUP BY YEAR(createdon_date), value_range
ORDER BY year,
    CASE value_range
        WHEN '< $20' THEN 1
        WHEN '$20-50' THEN 2
        WHEN '$50-100' THEN 3
        WHEN '$100-200' THEN 4
        WHEN '$200-500' THEN 5
        WHEN '$500+' THEN 6
    END;
"""

value_dist_data = pd.read_sql(query_value_dist, engine)

fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Chart 1: Seats per Booking Distribution 2019 vs 2023
ax = axes[0, 0]
seats_2019 = seats_data[seats_data['year'] == 2019]
seats_2023 = seats_data[seats_data['year'] == 2023]
width = 0.35
x = np.arange(len(seats_2019))
ax.bar(x - width/2, seats_2019['bookings'], width, label='2019', alpha=0.8)
ax.bar(x + width/2, seats_2023['bookings'], width, label='2023', alpha=0.8)
ax.set_xlabel('Number of Seats', fontsize=11)
ax.set_ylabel('Number of Bookings', fontsize=11)
ax.set_title('Seats per Booking Distribution', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(seats_2019['seats'])
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Chart 2: Average Booking Value by Seats
ax = axes[0, 1]
ax.plot(seats_2019['seats'], seats_2019['avg_total'], marker='o', linewidth=2.5,
        markersize=8, label='2019')
ax.plot(seats_2023['seats'], seats_2023['avg_total'], marker='s', linewidth=2.5,
        markersize=8, label='2023')
ax.set_xlabel('Number of Seats', fontsize=11)
ax.set_ylabel('Average Booking Value (USD)', fontsize=11)
ax.set_title('Average Booking Value by Seats Booked', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# Chart 3: Booking Value Distribution 2019
ax = axes[1, 0]
val_2019 = value_dist_data[value_dist_data['year'] == 2019]
colors = plt.cm.viridis(np.linspace(0, 1, len(val_2019)))
ax.bar(range(len(val_2019)), val_2019['bookings'], alpha=0.8, color=colors)
ax.set_xticks(range(len(val_2019)))
ax.set_xticklabels(val_2019['value_range'], rotation=45, ha='right')
ax.set_ylabel('Number of Bookings', fontsize=11)
ax.set_title('Booking Value Distribution - 2019', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Chart 4: Booking Value Distribution 2023
ax = axes[1, 1]
val_2023 = value_dist_data[value_dist_data['year'] == 2023]
colors = plt.cm.plasma(np.linspace(0, 1, len(val_2023)))
ax.bar(range(len(val_2023)), val_2023['bookings'], alpha=0.8, color=colors)
ax.set_xticks(range(len(val_2023)))
ax.set_xticklabels(val_2023['value_range'], rotation=45, ha='right')
ax.set_ylabel('Number of Bookings', fontsize=11)
ax.set_title('Booking Value Distribution - 2023', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/ismatsamadov/travel_data_analyse/charts/08_booking_value_seats.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/08_booking_value_seats.png")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("DEEP DIVE ANALYSIS COMPLETE!")
print("=" * 80)
print("\nGenerated 5 additional comprehensive chart sets:")
print("  - 04_route_analysis.png")
print("  - 05_geographic_analysis.png")
print("  - 06_operator_performance.png")
print("  - 07_customer_behavior.png")
print("  - 08_booking_value_seats.png")
print("\nTotal: 8 chart files in /charts directory")

engine.dispose()
