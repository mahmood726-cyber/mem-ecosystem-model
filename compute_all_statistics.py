#!/usr/bin/env python
"""
Compute ALL manuscript statistics that are not produced by run_mem_full_analysis.py.

This script reads the CSV outputs from the main pipeline and computes:
1. Spearman rank correlations + p-values
2. Welch's t-test + Cohen's d for significance stratification
3. Meaningful reversal rate (both |logOR| > 0.2)
4. Cross-tabulation (Table 2) verification
5. FPI sensitivity analysis under alternative weights (S4 Table)
6. 55-analysis same-year count

Outputs:
- data/mem_sensitivity_weights.csv   (S4 Table)
- data/mem_crosstab.csv              (Table 2 verification)
- data/mem_extended_stats.json       (all computed statistics)

Author: Mahmood Ul Hassan
"""

import sys
import io
import json
import math
import csv
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
from scipy import stats

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"


def load_data():
    """Load all CSV outputs from the main pipeline."""
    velocity = pd.read_csv(DATA_DIR / "mem_velocity_full.csv")
    decay = pd.read_csv(DATA_DIR / "mem_decay_full.csv")
    integrated = pd.read_csv(DATA_DIR / "mem_integrated_full.csv")
    return velocity, decay, integrated


def compute_spearman_correlations(integrated):
    """Compute Spearman rank correlations reported in the manuscript."""
    # Filter to complete cases with decay_ratio <= 10
    df = integrated.copy()
    df['decay_ratio'] = pd.to_numeric(df['decay_ratio'], errors='coerce')
    df['trajectory_cv'] = pd.to_numeric(df['trajectory_cv'], errors='coerce')
    df['studies_per_year'] = pd.to_numeric(df['studies_per_year'], errors='coerce')
    df['mafi_score'] = pd.to_numeric(df['mafi_score'], errors='coerce')
    df['fpi_score'] = pd.to_numeric(df['fpi_score'], errors='coerce')

    complete = df.dropna(subset=['decay_ratio', 'trajectory_cv', 'studies_per_year', 'mafi_score'])
    complete = complete[complete['decay_ratio'] <= 10]
    n_complete = len(complete)

    results = {}
    results['n_complete_cases'] = n_complete

    # Spearman: velocity vs decay ratio
    rho, p = stats.spearmanr(complete['studies_per_year'], complete['decay_ratio'])
    results['spearman_velocity_decay'] = {'rho': round(rho, 3), 'p': round(p, 3)}

    # Spearman: velocity vs trajectory CV
    rho, p = stats.spearmanr(complete['studies_per_year'], complete['trajectory_cv'])
    results['spearman_velocity_cv'] = {'rho': round(rho, 3), 'p': round(p, 3)}

    # Spearman: MAFI vs decay ratio
    rho, p = stats.spearmanr(complete['mafi_score'], complete['decay_ratio'])
    results['spearman_mafi_decay'] = {'rho': round(rho, 3), 'p': round(p, 3)}

    # Pearson correlations (for verification)
    r, p = stats.pearsonr(complete['studies_per_year'], complete['decay_ratio'])
    results['pearson_velocity_decay'] = {'r': round(r, 3), 'p': round(p, 2)}

    r, p = stats.pearsonr(complete['studies_per_year'], complete['trajectory_cv'])
    results['pearson_velocity_cv'] = {'r': round(r, 3), 'p': round(p, 2)}

    r, p = stats.pearsonr(complete['mafi_score'], complete['decay_ratio'])
    results['pearson_mafi_decay'] = {'r': round(r, 3), 'p': round(p, 2)}

    # Part-whole correlations with FPI
    r, p = stats.pearsonr(complete['studies_per_year'], complete['fpi_score'])
    results['pearson_velocity_fpi'] = {'r': round(r, 3), 'p': round(p, 4)}

    r, p = stats.pearsonr(complete['mafi_score'], complete['fpi_score'])
    results['pearson_mafi_fpi'] = {'r': round(r, 3), 'p': round(p, 4)}

    r, p = stats.pearsonr(complete['decay_ratio'], complete['fpi_score'])
    results['pearson_decay_fpi'] = {'r': round(r, 3), 'p': round(p, 4)}

    return results


def compute_welch_t_cohens_d(integrated):
    """Compute Welch's t-test and Cohen's d for significance stratification."""
    df = integrated.copy()
    df['significant'] = df['significant'].astype(str).str.upper()

    sig = df[df['significant'] == 'TRUE']['fpi_score'].dropna()
    nonsig = df[df['significant'] == 'FALSE']['fpi_score'].dropna()

    n_total = len(sig) + len(nonsig)
    n_missing = len(df) - n_total

    # Welch's t-test
    t_stat, p_val = stats.ttest_ind(sig, nonsig, equal_var=False)

    # Cohen's d (pooled SD)
    n1, n2 = len(sig), len(nonsig)
    s1, s2 = np.std(sig, ddof=0), np.std(nonsig, ddof=0)
    pooled_sd = math.sqrt(((n1 * s1**2) + (n2 * s2**2)) / (n1 + n2))
    d = (np.mean(sig) - np.mean(nonsig)) / pooled_sd

    return {
        'n_significant': int(n1),
        'n_nonsignificant': int(n2),
        'n_missing_significance': int(n_missing),
        'mean_fpi_significant': round(float(np.mean(sig)), 1),
        'mean_fpi_nonsignificant': round(float(np.mean(nonsig)), 1),
        'median_fpi_significant': round(float(np.median(sig)), 1),
        'median_fpi_nonsignificant': round(float(np.median(nonsig)), 1),
        'welch_t': round(float(t_stat), 1),
        'welch_p': float(p_val),
        'cohens_d': round(float(d), 2),
        'difference': round(float(np.mean(sig) - np.mean(nonsig)), 1),
    }


def compute_meaningful_reversals(decay):
    """Compute the clinically meaningful reversal rate."""
    df = decay.copy()
    df['early_effect'] = pd.to_numeric(df['early_effect'], errors='coerce')
    df['final_effect'] = pd.to_numeric(df['final_effect'], errors='coerce')

    n_total = len(df)
    n_any_reversal = df['direction_change'].sum()

    # Meaningful: both |early| > 0.2 and |final| > 0.2, and direction_change
    threshold = 0.2
    meaningful = df[
        df['direction_change'] &
        (df['early_effect'].abs() > threshold) &
        (df['final_effect'].abs() > threshold)
    ]
    n_meaningful = len(meaningful)

    return {
        'n_total_analyses': n_total,
        'n_any_reversal': int(n_any_reversal),
        'pct_any_reversal': round(100 * n_any_reversal / n_total, 1),
        'n_meaningful_reversal': n_meaningful,
        'pct_meaningful_reversal': round(100 * n_meaningful / n_total, 1),
        'threshold_log_or': threshold,
    }


def compute_crosstab(integrated):
    """Compute Table 2: MAFI class x FPI class cross-tabulation."""
    df = integrated.copy()

    mafi_order = ['Robust', 'Low Fragility', 'Moderate Fragility', 'High Fragility']
    fpi_order = ['Stable', 'Moderate', 'Volatile', 'High Risk']

    # Separate matched and unmatched
    matched = df[df['mafi_class'].isin(mafi_order)]
    unmatched = df[~df['mafi_class'].isin(mafi_order)]

    rows = []
    for mc in mafi_order:
        subset = matched[matched['mafi_class'] == mc]
        row = {'mafi_class': mc}
        for fc in fpi_order:
            row[fc] = int((subset['fpi_class'] == fc).sum())
        row['Total'] = len(subset)
        rows.append(row)

    # Unmatched row
    row = {'mafi_class': 'Unmatched'}
    for fc in fpi_order:
        row[fc] = int((unmatched['fpi_class'] == fc).sum())
    row['Total'] = len(unmatched)
    rows.append(row)

    # Save CSV
    csv_path = DATA_DIR / "mem_crosstab.csv"
    fieldnames = ['mafi_class'] + fpi_order + ['Total']
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Cross-tabulation saved to {csv_path.name}")
    return rows


def compute_sensitivity_analysis(integrated):
    """Compute FPI under alternative weight schemes (S4 Table)."""
    df = integrated.copy()

    # Get component values
    k_comp = df['fpi_k_component'].values
    bias_comp = df['fpi_bias_component'].values
    stab_comp = df['fpi_stability_component'].values
    decay_comp = df['fpi_decay_component'].values

    weight_schemes = {
        'Original (0.30, 0.25, 0.25, 0.20)': (0.30, 0.25, 0.25, 0.20),
        'Equal (0.25, 0.25, 0.25, 0.25)': (0.25, 0.25, 0.25, 0.25),
        'Stability-dominant (0.20, 0.20, 0.40, 0.20)': (0.20, 0.20, 0.40, 0.20),
        'Bias-dominant (0.20, 0.40, 0.20, 0.20)': (0.20, 0.40, 0.20, 0.20),
    }

    results = []
    for name, (wk, wb, ws, wd) in weight_schemes.items():
        fpi = np.clip((wk * k_comp + wb * bias_comp + ws * stab_comp + wd * decay_comp) * 100, 0, 100)

        classes = pd.cut(fpi, bins=[-0.1, 30, 50, 70, 100.1],
                        labels=['High Risk', 'Volatile', 'Moderate', 'Stable'])

        counts = classes.value_counts()
        n = len(fpi)

        results.append({
            'Weight scheme': name,
            'Mean FPI': round(float(np.mean(fpi)), 1),
            'SD FPI': round(float(np.std(fpi)), 1),
            'Stable (%)': round(100 * counts.get('Stable', 0) / n, 1),
            'Moderate (%)': round(100 * counts.get('Moderate', 0) / n, 1),
            'Volatile (%)': round(100 * counts.get('Volatile', 0) / n, 1),
            'High Risk (%)': round(100 * counts.get('High Risk', 0) / n, 1),
            'Stable (n)': int(counts.get('Stable', 0)),
            'Moderate (n)': int(counts.get('Moderate', 0)),
            'Volatile (n)': int(counts.get('Volatile', 0)),
            'High Risk (n)': int(counts.get('High Risk', 0)),
        })

    # Save S4 Table
    csv_path = DATA_DIR / "mem_sensitivity_weights.csv"
    fieldnames = list(results[0].keys())
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"  Sensitivity analysis saved to {csv_path.name}")
    return results


def compute_same_year_count(velocity):
    """Count analyses where all studies share the same publication year."""
    n_same_year = (velocity['span_years'] == 0).sum()
    return {
        'n_same_year': int(n_same_year),
        'pct_same_year': round(100 * n_same_year / len(velocity), 1),
    }


def main():
    print("=== Computing extended manuscript statistics ===\n")

    velocity, decay, integrated = load_data()
    print(f"Loaded: {len(velocity)} velocity, {len(decay)} decay, {len(integrated)} integrated\n")

    all_stats = {}

    # 1. Spearman correlations
    print("1. Spearman correlations...")
    spearman = compute_spearman_correlations(integrated)
    all_stats['correlations'] = spearman
    print(f"  n={spearman['n_complete_cases']} complete cases")
    print(f"  Velocity vs decay: rho={spearman['spearman_velocity_decay']['rho']}, p={spearman['spearman_velocity_decay']['p']}")
    print(f"  Velocity vs CV:    rho={spearman['spearman_velocity_cv']['rho']}, p={spearman['spearman_velocity_cv']['p']}")
    print(f"  MAFI vs decay:     rho={spearman['spearman_mafi_decay']['rho']}, p={spearman['spearman_mafi_decay']['p']}")

    # 2. Welch's t-test + Cohen's d
    print("\n2. Welch's t-test (significant vs non-significant)...")
    ttest = compute_welch_t_cohens_d(integrated)
    all_stats['significance_comparison'] = ttest
    print(f"  n_sig={ttest['n_significant']}, n_nonsig={ttest['n_nonsignificant']}, missing={ttest['n_missing_significance']}")
    print(f"  FPI sig: {ttest['mean_fpi_significant']} vs nonsig: {ttest['mean_fpi_nonsignificant']}")
    print(f"  Welch t={ttest['welch_t']}, p={ttest['welch_p']:.2e}, Cohen's d={ttest['cohens_d']}")

    # 3. Meaningful reversals
    print("\n3. Meaningful reversal rate...")
    reversals = compute_meaningful_reversals(decay)
    all_stats['reversals'] = reversals
    print(f"  Any reversal: {reversals['n_any_reversal']}/{reversals['n_total_analyses']} ({reversals['pct_any_reversal']}%)")
    print(f"  Meaningful (|logOR|>0.2): {reversals['n_meaningful_reversal']}/{reversals['n_total_analyses']} ({reversals['pct_meaningful_reversal']}%)")

    # 4. Cross-tabulation
    print("\n4. Cross-tabulation (Table 2)...")
    crosstab = compute_crosstab(integrated)
    all_stats['crosstab'] = crosstab
    for row in crosstab:
        print(f"  {row['mafi_class']:20s}: S={row['Stable']:4d} M={row['Moderate']:4d} V={row['Volatile']:4d} HR={row['High Risk']:3d} Total={row['Total']}")

    # 5. Sensitivity analysis (S4 Table)
    print("\n5. FPI sensitivity analysis...")
    sensitivity = compute_sensitivity_analysis(integrated)
    all_stats['sensitivity'] = sensitivity
    for row in sensitivity:
        print(f"  {row['Weight scheme']:42s}: Stable={row['Stable (%)']:5.1f}% Moderate={row['Moderate (%)']:5.1f}% Volatile={row['Volatile (%)']:5.1f}% HR={row['High Risk (%)']:4.1f}%")

    # 6. Same-year count
    print("\n6. Same-year analysis count...")
    same_year = compute_same_year_count(velocity)
    all_stats['same_year'] = same_year
    print(f"  {same_year['n_same_year']} analyses with span=0 ({same_year['pct_same_year']}%)")

    # Save all stats
    stats_path = DATA_DIR / "mem_extended_stats.json"
    with open(stats_path, 'w') as f:
        json.dump(all_stats, f, indent=2, default=str)
    print(f"\nAll statistics saved to {stats_path.name}")

    print("\n=== EXTENDED STATISTICS COMPLETE ===")


if __name__ == '__main__':
    main()
