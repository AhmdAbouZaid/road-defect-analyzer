# road_defect_analyzer.py
# ============================================
# Road Defect Data Analyzer
# Analyzes road defect data and generates a report and map
# ============================================

import csv
import json
from collections import Counter, defaultdict
import folium          # interactive map
import matplotlib.pyplot as plt  # chart plotting
import pandas as pd   # data analysis

# ---- 1. Load Data ----
def load_data(filepath):
    """Reads a CSV file and returns a list of records"""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'street':  row['street_name'],
                'defect':  row['defect_type'],
                'severity': int(row['severity']),  # 1-5
                'lat':     float(row['latitude']),
                'lon':     float(row['longitude']),
            })
    return records

# ---- 2. Analyze ----
def analyze(records):
    """Computes statistics on the dataset"""
    df = pd.DataFrame(records)

    total      = len(df)
    avg_sev    = df['severity'].mean().round(2)
    by_defect  = df['defect'].value_counts().to_dict()
    by_street  = df.groupby('street')['severity'].mean()
    worst_st   = by_street.idxmax()

    return {
        'total':     total,
        'avg_sev':   avg_sev,
        'by_defect': by_defect,
        'worst_street': worst_st,
    }

# ---- 3. Map ----
def make_map(records, output='defects_map.html'):
    """Creates an interactive folium map with circle markers"""
    colors = {'pothole':'red', 'crack':'orange',
              'rutting':'blue', 'marking':'green'}

    m = folium.Map(location=[30.06, 31.24], zoom_start=13)

    for r in records:
        folium.CircleMarker(
            location=[r['lat'], r['lon']],
            radius=r['severity'] * 3,
            color=colors.get(r['defect'], 'gray'),
            fill=True,
            popup=f"{r['street']} — {r['defect']} (sev:{r['severity']})"
        ).add_to(m)

    m.save(output)
    print(f"Map saved → {output}")

# ---- 4. Chart ----
def make_chart(by_defect):
    """Horizontal bar chart showing defect frequency by type"""
    labels = list(by_defect.keys())
    values = list(by_defect.values())

    plt.figure(figsize=(8, 4))
    plt.barh(labels, values, color='#1D9E75')
    plt.title('Defect Frequency by Type')
    plt.tight_layout()
    plt.savefig('defects_chart.png', dpi=150)

# ---- 5. Main ----
if __name__ == '__main__':
    data    = load_data('road_data.csv')
    stats   = analyze(data)
    make_map(data)
    make_chart(stats['by_defect'])

    print(f"Total defects : {stats['total']}")
    print(f"Avg severity  : {stats['avg_sev']}")
    print(f"Worst street  : {stats['worst_street']}")