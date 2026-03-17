#!/usr/bin/env python3
"""Generate all figures for the MEM PLOS ONE manuscript."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data — column names from actual CSVs:
# integrated: fpi_score, fpi_class, decay_ratio, studies_per_year, mafi_score, mafi_class, significant
# velocity: studies_per_year, k, span_years
# decay: decay_ratio, trajectory_cv, direction_change
integrated = pd.read_csv(os.path.join(DATA_DIR, 'mem_integrated_full.csv'))
velocity = pd.read_csv(os.path.join(DATA_DIR, 'mem_velocity_full.csv'))
decay = pd.read_csv(os.path.join(DATA_DIR, 'mem_decay_full.csv'))

print(f"Loaded: integrated={len(integrated)}, velocity={len(velocity)}, decay={len(decay)}")

# ============================================================================
# Fig 1: FPI Distribution Histogram
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 5))
fpi = integrated['fpi_score'].dropna()
ax.hist(fpi, bins=40, color='#4472C4', edgecolor='white', alpha=0.85)
# Tier boundaries
for threshold, label, color in [(30, 'High Risk/Volatile', '#E74C3C'),
                                  (50, 'Volatile/Moderate', '#F39C12'),
                                  (70, 'Moderate/Stable', '#27AE60')]:
    ax.axvline(threshold, color=color, linestyle='--', linewidth=1.5, alpha=0.8)
    ax.text(threshold + 0.5, ax.get_ylim()[1] * 0.92, f'FPI={threshold}',
            color=color, fontsize=9, rotation=90, va='top')

ax.set_xlabel('Future-Proof Index (FPI)')
ax.set_ylabel('Number of Analyses')
ax.set_title('Distribution of FPI Scores Across 3,062 Cochrane Meta-Analyses')
ax.set_xlim(0, 100)
fig.savefig(os.path.join(OUT_DIR, 'Fig1_FPI_distribution.tiff'), format='tiff')
fig.savefig(os.path.join(OUT_DIR, 'Fig1_FPI_distribution.png'), format='png')
plt.close(fig)
print("Fig 1 saved: FPI distribution histogram")

# ============================================================================
# Fig 2: Velocity vs Decay Ratio scatter
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 6))

merged = integrated.copy()
mask = merged['decay_ratio'].notna() & (merged['decay_ratio'] <= 10) & merged['studies_per_year'].notna()
plot_data = merged[mask]

ax.scatter(plot_data['studies_per_year'], plot_data['decay_ratio'],
           alpha=0.15, s=8, color='#4472C4', rasterized=True)
ax.axhline(1.0, color='#E74C3C', linestyle='--', linewidth=1, alpha=0.6, label='No change (DR=1)')
ax.set_xlabel('Evidence Velocity (studies per year)')
ax.set_ylabel('Effect Decay Ratio')
ax.set_title(f'Velocity vs Decay Ratio (n={len(plot_data):,}, r=-0.002)')
ax.set_xlim(0, min(20, plot_data['studies_per_year'].quantile(0.99) * 1.1))
ax.set_ylim(0, min(5, plot_data['decay_ratio'].quantile(0.99) * 1.1))
ax.legend(loc='upper right', fontsize=9)
fig.savefig(os.path.join(OUT_DIR, 'Fig2_velocity_vs_decay.tiff'), format='tiff')
fig.savefig(os.path.join(OUT_DIR, 'Fig2_velocity_vs_decay.png'), format='png')
plt.close(fig)
print("Fig 2 saved: Velocity vs Decay scatter")

# ============================================================================
# Fig 3: MAFI x FPI cross-tabulation heatmap
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 5))

mafi_order = ['Robust', 'Low Fragility', 'Moderate Fragility', 'High Fragility']
fpi_order = ['Stable', 'Moderate', 'Volatile', 'High Risk']

# Use existing fpi_class and mafi_class columns from the data
ct = pd.crosstab(integrated['mafi_class'].fillna('Unmatched'), integrated['fpi_class'])

# Reindex to ensure order (exclude Unmatched for the heatmap)
for c in fpi_order:
    if c not in ct.columns:
        ct[c] = 0
for r in mafi_order:
    if r not in ct.index:
        ct.loc[r] = 0
ct = ct.reindex(index=mafi_order, columns=fpi_order, fill_value=0)

im = ax.imshow(ct.values, cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(len(fpi_order)))
ax.set_xticklabels(fpi_order, fontsize=10)
ax.set_yticks(range(len(mafi_order)))
ax.set_yticklabels(mafi_order, fontsize=10)
ax.set_xlabel('FPI Stability Class')
ax.set_ylabel('MAFI Publication Bias Class')
ax.set_title('Cross-Tabulation: Publication Bias vs Evidence Stability')

for i in range(len(mafi_order)):
    for j in range(len(fpi_order)):
        val = ct.values[i, j]
        color = 'white' if val > ct.values.max() * 0.6 else 'black'
        ax.text(j, i, f'{val}', ha='center', va='center', color=color, fontsize=10)

fig.colorbar(im, ax=ax, label='Count', shrink=0.8)
fig.savefig(os.path.join(OUT_DIR, 'Fig3_mafi_fpi_heatmap.tiff'), format='tiff')
fig.savefig(os.path.join(OUT_DIR, 'Fig3_mafi_fpi_heatmap.png'), format='png')
plt.close(fig)
print("Fig 3 saved: MAFI x FPI heatmap")

# ============================================================================
# S1 Fig: Velocity histogram (log-scaled x-axis)
# ============================================================================
fig, ax = plt.subplots(figsize=(7, 4.5))
vel_data = velocity['studies_per_year'].dropna()
vel_data = vel_data[vel_data > 0]
ax.hist(vel_data, bins=np.logspace(np.log10(vel_data.min()), np.log10(vel_data.max()), 50),
        color='#2E86C1', edgecolor='white', alpha=0.85)
ax.set_xscale('log')
ax.set_xlabel('Evidence Velocity (studies per year, log scale)')
ax.set_ylabel('Number of Analyses')
ax.set_title(f'Distribution of Evidence Velocity (n={len(vel_data):,})')
fig.savefig(os.path.join(OUT_DIR, 'S1_Fig_velocity_histogram.tiff'), format='tiff')
fig.savefig(os.path.join(OUT_DIR, 'S1_Fig_velocity_histogram.png'), format='png')
plt.close(fig)
print("S1 Fig saved: Velocity histogram")

# ============================================================================
# S2 Fig: Decay ratio histogram
# ============================================================================
fig, ax = plt.subplots(figsize=(7, 4.5))
dr = decay['decay_ratio'].dropna()
dr_plot = dr[dr <= 5]  # Cap for visualization
ax.hist(dr_plot, bins=50, color='#E67E22', edgecolor='white', alpha=0.85)
ax.axvline(1.0, color='#E74C3C', linestyle='--', linewidth=1.5, label='No change (DR=1)')
ax.set_xlabel('Decay Ratio (|final effect| / |early effect|)')
ax.set_ylabel('Number of Analyses')
ax.set_title(f'Distribution of Decay Ratios (n={len(dr_plot):,}, capped at 5)')
ax.legend(fontsize=9)
fig.savefig(os.path.join(OUT_DIR, 'S2_Fig_decay_histogram.tiff'), format='tiff')
fig.savefig(os.path.join(OUT_DIR, 'S2_Fig_decay_histogram.png'), format='png')
plt.close(fig)
print("S2 Fig saved: Decay ratio histogram")

# ============================================================================
# S3 Fig: FPI by significance status
# ============================================================================
fig, ax = plt.subplots(figsize=(7, 4.5))
sig = integrated[integrated['significant'] == True]['fpi_score'].dropna()
nonsig = integrated[integrated['significant'] == False]['fpi_score'].dropna()

bins = np.linspace(0, 100, 41)
ax.hist(sig, bins=bins, alpha=0.6, color='#27AE60', label=f'Significant (n={len(sig):,})', edgecolor='white')
ax.hist(nonsig, bins=bins, alpha=0.6, color='#95A5A6', label=f'Non-significant (n={len(nonsig):,})', edgecolor='white')
ax.set_xlabel('Future-Proof Index (FPI)')
ax.set_ylabel('Number of Analyses')
ax.set_title('FPI Distribution by Statistical Significance')
ax.legend(fontsize=9)
fig.savefig(os.path.join(OUT_DIR, 'S3_Fig_fpi_by_significance.tiff'), format='tiff')
fig.savefig(os.path.join(OUT_DIR, 'S3_Fig_fpi_by_significance.png'), format='png')
plt.close(fig)
print("S3 Fig saved: FPI by significance")

print(f"\nAll figures generated in: {OUT_DIR}")
print("Done!")
