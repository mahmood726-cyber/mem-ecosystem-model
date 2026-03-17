#!/usr/bin/env python
"""
MEM Full Analysis Pipeline
===========================
Processes ALL 501 Cochrane reviews from Pairwise70 to compute:
1. Evidence Velocity (temporal accumulation rate)
2. Effect Decay (Proteus phenomenon: early vs final cumulative effect)
3. Merges with MAFI publication bias scores for integrated analysis

All results are saved to CSV for manuscript reporting.
Author: Mahmood Ul Hassan
"""

import os
import sys
import io
import csv
import math
import json
import warnings
from pathlib import Path
from collections import defaultdict

# UTF-8 output for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

try:
    import pyreadr
except ImportError:
    print("ERROR: pyreadr required. Install with: pip install pyreadr")
    sys.exit(1)

# ============================================================
# CONFIGURATION
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
RDS_DIR = SCRIPT_DIR / "data" / "cleaned_rds"
MAFI_CSV = SCRIPT_DIR / "data" / "MAFI_validated_results.csv"
OUTPUT_DIR = SCRIPT_DIR / "data"

MIN_STUDIES_VELOCITY = 5   # minimum k for velocity analysis
MIN_STUDIES_DECAY = 6      # minimum k for cumulative MA decay analysis
CONTINUITY_CORRECTION = 0.5  # for zero-cell correction in OR calculation
YEAR_MIN = 1900            # earliest plausible publication year
YEAR_MAX = 2025            # latest plausible publication year


def escalc_log_or(ai, n1i, ci, n2i):
    """Compute log OR and sampling variance from 2x2 table.
    Uses 0.5 continuity correction for zero cells (only0 method)."""
    # Apply continuity correction only if any cell is zero
    if ai == 0 or (n1i - ai) == 0 or ci == 0 or (n2i - ci) == 0:
        ai_c = ai + CONTINUITY_CORRECTION
        bi_c = (n1i - ai) + CONTINUITY_CORRECTION
        ci_c = ci + CONTINUITY_CORRECTION
        di_c = (n2i - ci) + CONTINUITY_CORRECTION
        n1i_c = n1i + 2 * CONTINUITY_CORRECTION
        n2i_c = n2i + 2 * CONTINUITY_CORRECTION
    else:
        ai_c, bi_c, ci_c, di_c = ai, n1i - ai, ci, n2i - ci

    if ai_c <= 0 or bi_c <= 0 or ci_c <= 0 or di_c <= 0:
        return None, None

    yi = math.log(ai_c * di_c / (bi_c * ci_c))
    vi = 1.0/ai_c + 1.0/bi_c + 1.0/ci_c + 1.0/di_c
    return yi, vi


def fixed_effect_ma(yi_list, vi_list):
    """Inverse-variance fixed-effect meta-analysis."""
    yi = np.array(yi_list, dtype=float)
    vi = np.array(vi_list, dtype=float)
    valid = np.isfinite(yi) & np.isfinite(vi) & (vi > 0)
    if valid.sum() < 2:
        return None, None, None
    yi, vi = yi[valid], vi[valid]
    wi = 1.0 / vi
    estimate = np.sum(wi * yi) / np.sum(wi)
    se = 1.0 / math.sqrt(np.sum(wi))
    return float(estimate), float(se), int(valid.sum())


def process_review(filepath):
    """Process a single RDS file: extract velocity and decay metrics."""
    try:
        result = pyreadr.read_r(str(filepath))
        if not result:
            return [], []
        df = list(result.values())[0]
    except Exception:
        return [], []

    # Standardize column names
    df.columns = [c.replace(' ', '.').replace('-', '.') for c in df.columns]

    if 'Study.year' not in df.columns:
        return [], []

    review_name = filepath.name

    # Check for binary outcome columns
    has_binary = all(c in df.columns for c in
                     ['Experimental.cases', 'Experimental.N', 'Control.cases', 'Control.N'])

    # Create analysis groups
    if 'Analysis.number' in df.columns:
        df['_analysis'] = df['Analysis.number'].astype(str)
    else:
        df['_analysis'] = '1'

    if 'Subgroup.number' in df.columns:
        df['_subgroup'] = df['Subgroup.number'].astype(str)
    else:
        df['_subgroup'] = 'overall'

    df['_group_id'] = df['_analysis'] + '::' + df['_subgroup']

    velocity_results = []
    decay_results = []

    for group_id, sub in df.groupby('_group_id'):
        # Convert year to numeric, filter implausible values
        years = pd.to_numeric(sub['Study.year'], errors='coerce')
        valid_year = years.notna() & (years >= YEAR_MIN) & (years <= YEAR_MAX)
        sub = sub[valid_year].copy()
        years = years[valid_year]

        if len(sub) < MIN_STUDIES_VELOCITY:
            continue

        # Sort by year
        sort_idx = years.argsort()
        sub = sub.iloc[sort_idx].reset_index(drop=True)
        years = years.iloc[sort_idx].reset_index(drop=True)

        k = len(sub)
        year_range = float(years.max() - years.min())
        velocity = k / max(1.0, year_range)

        velocity_results.append({
            'review': review_name,
            'analysis': group_id,
            'k': k,
            'span_years': year_range,
            'studies_per_year': round(velocity, 6),
            'start_year': int(years.min()),
            'end_year': int(years.max()),
        })

        # Decay analysis: requires binary data and k >= MIN_STUDIES_DECAY
        if not has_binary or k < MIN_STUDIES_DECAY:
            continue

        # Compute effect sizes
        yi_list = []
        vi_list = []
        valid_rows = []
        for _, row in sub.iterrows():
            try:
                ai = float(row['Experimental.cases'])
                n1 = float(row['Experimental.N'])
                ci = float(row['Control.cases'])
                n2 = float(row['Control.N'])
            except (ValueError, TypeError):
                yi_list.append(None)
                vi_list.append(None)
                valid_rows.append(False)
                continue

            if n1 <= 0 or n2 <= 0 or ai < 0 or ci < 0 or ai > n1 or ci > n2:
                yi_list.append(None)
                vi_list.append(None)
                valid_rows.append(False)
                continue

            yi, vi = escalc_log_or(ai, n1, ci, n2)
            yi_list.append(yi)
            vi_list.append(vi)
            valid_rows.append(yi is not None)

        # Need at least MIN_STUDIES_DECAY valid effect sizes
        n_valid = sum(1 for v in valid_rows if v)
        if n_valid < MIN_STUDIES_DECAY:
            continue

        # Cumulative fixed-effect meta-analysis
        cum_yi = [y for y, v in zip(yi_list, valid_rows) if v]
        cum_vi = [v for v, vr in zip(vi_list, valid_rows) if vr]
        cum_years_valid = [int(y) for y, v in zip(years, valid_rows) if v]

        # Compute cumulative effects at each step (from study 3 onward)
        cum_effects = []
        cum_ses = []
        cum_ks = []
        for j in range(2, len(cum_yi)):
            est, se, kk = fixed_effect_ma(cum_yi[:j+1], cum_vi[:j+1])
            if est is not None:
                cum_effects.append(est)
                cum_ses.append(se)
                cum_ks.append(kk)

        if len(cum_effects) < 2:
            continue

        early_effect = cum_effects[0]  # after 3 studies
        final_effect = cum_effects[-1]  # after all studies
        midpoint_effect = cum_effects[len(cum_effects)//2]

        # Decay ratio: |final| / |early|
        if abs(early_effect) > 1e-10:
            decay_ratio = abs(final_effect) / abs(early_effect)
        else:
            decay_ratio = None

        # Direction change: did the effect change sign?
        direction_change = (early_effect * final_effect) < 0 if (
            abs(early_effect) > 1e-10 and abs(final_effect) > 1e-10) else False

        # Effect trajectory stability: SD of cumulative effects / |mean|
        if len(cum_effects) >= 3 and abs(np.mean(cum_effects)) > 1e-10:
            trajectory_cv = float(np.std(cum_effects) / abs(np.mean(cum_effects)))
        else:
            trajectory_cv = None

        # Max absolute shift in cumulative effect
        max_shift = max(abs(cum_effects[i] - cum_effects[i-1])
                       for i in range(1, len(cum_effects)))

        decay_results.append({
            'review': review_name,
            'analysis': group_id,
            'k_total': n_valid,
            'early_effect': round(early_effect, 6),
            'midpoint_effect': round(midpoint_effect, 6),
            'final_effect': round(final_effect, 6),
            'decay_ratio': round(decay_ratio, 6) if decay_ratio is not None else '',
            'direction_change': direction_change,
            'trajectory_cv': round(trajectory_cv, 4) if trajectory_cv is not None else '',
            'max_cumulative_shift': round(max_shift, 6),
            'early_year': cum_years_valid[2] if len(cum_years_valid) > 2 else '',
            'final_year': cum_years_valid[-1] if cum_years_valid else '',
        })

    return velocity_results, decay_results


def load_mafi_scores():
    """Load MAFI validated results."""
    mafi = {}
    with open(MAFI_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['dataset'], row['analysis_id'])
            mafi[key] = {
                'MAFI': float(row['MAFI']) if row['MAFI'] else None,
                'MAFI_class': row['MAFI_class'],
                'k': int(row['k']) if row['k'] else None,
                'I2': float(row['I2']) if row['I2'] else None,
                'estimate': float(row['estimate']) if row['estimate'] else None,
                'significant': row['significant'] == 'TRUE',
                'direction_fragile': row['direction_fragile'] == 'TRUE',
                'composite_fragility': float(row['composite_fragility']) if row['composite_fragility'] else None,
            }
    return mafi


def main():
    rds_files = sorted(RDS_DIR.glob("*.rds"))
    print(f"Found {len(rds_files)} Cochrane review RDS files")

    all_velocity = []
    all_decay = []
    n_processed = 0
    n_errors = 0

    for i, filepath in enumerate(rds_files):
        if (i + 1) % 50 == 0:
            print(f"  Processing {i+1}/{len(rds_files)}...")

        try:
            vel, dec = process_review(filepath)
            all_velocity.extend(vel)
            all_decay.extend(dec)
            n_processed += 1
        except Exception as e:
            n_errors += 1
            if n_errors <= 5:
                print(f"  Warning: {filepath.name}: {e}")

    print(f"\nProcessed: {n_processed}/{len(rds_files)} reviews ({n_errors} errors)")

    # ============================================================
    # SAVE VELOCITY RESULTS
    # ============================================================
    vel_path = OUTPUT_DIR / "mem_velocity_full.csv"
    if all_velocity:
        fieldnames = list(all_velocity[0].keys())
        with open(vel_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_velocity)
        print(f"\nVelocity: {len(all_velocity)} analysis trajectories saved to {vel_path.name}")

        # Summary stats
        vels = [r['studies_per_year'] for r in all_velocity]
        spans = [r['span_years'] for r in all_velocity]
        ks = [r['k'] for r in all_velocity]
        print(f"  Mean velocity: {np.mean(vels):.3f} studies/year")
        print(f"  Median velocity: {np.median(vels):.3f} studies/year")
        print(f"  Mean span: {np.mean(spans):.1f} years")
        print(f"  Total analyses with k>={MIN_STUDIES_VELOCITY}: {len(all_velocity)}")
        print(f"  Unique reviews: {len(set(r['review'] for r in all_velocity))}")

    # ============================================================
    # SAVE DECAY RESULTS
    # ============================================================
    dec_path = OUTPUT_DIR / "mem_decay_full.csv"
    if all_decay:
        fieldnames = list(all_decay[0].keys())
        with open(dec_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_decay)
        print(f"\nDecay: {len(all_decay)} analysis trajectories saved to {dec_path.name}")

        valid_dr = [float(r['decay_ratio']) for r in all_decay
                     if r['decay_ratio'] != '' and float(r['decay_ratio']) < 10]
        dir_changes = sum(1 for r in all_decay if r['direction_change'])
        valid_cv = [float(r['trajectory_cv']) for r in all_decay
                     if r['trajectory_cv'] != '']

        print(f"  Median decay ratio: {np.median(valid_dr):.3f}" if valid_dr else "  No valid decay ratios")
        print(f"  Mean decay ratio: {np.mean(valid_dr):.3f}" if valid_dr else "")
        print(f"  Direction reversals: {dir_changes}/{len(all_decay)} ({100*dir_changes/len(all_decay):.1f}%)")
        print(f"  Median trajectory CV: {np.median(valid_cv):.3f}" if valid_cv else "")
        print(f"  Unique reviews: {len(set(r['review'] for r in all_decay))}")

    # ============================================================
    # MERGE WITH MAFI AND COMPUTE FPI
    # ============================================================
    print("\n--- MERGING WITH MAFI SCORES ---")
    mafi = load_mafi_scores()
    print(f"Loaded {len(mafi)} MAFI scores")

    # Create integrated dataset: merge decay results with MAFI
    integrated = []
    matched = 0
    for dr in all_decay:
        review = dr['review']
        # Parse analysis number from group_id
        analysis_parts = dr['analysis'].split('::')
        analysis_num = analysis_parts[0]

        # Try to match with MAFI
        mafi_key = (review.replace('.rds', ''), analysis_num)
        if mafi_key not in mafi:
            # Try with dataset suffix
            for mk in mafi:
                if mk[0].startswith(review.replace('.rds', '').replace('_data', '')) and mk[1] == analysis_num:
                    mafi_key = mk
                    break

        m = mafi.get(mafi_key, {})
        if m and m.get('MAFI') is not None:
            matched += 1

        # Compute FPI components
        mafi_score = m.get('MAFI', None)
        k_total = dr['k_total']
        decay_ratio_str = dr['decay_ratio']
        trajectory_cv_str = dr['trajectory_cv']

        # FPI: continuous score 0-100
        # Component 1: Sample size adequacy (0-1) - logistic function of k
        k_component = 1.0 / (1.0 + math.exp(-0.15 * (k_total - 15)))

        # Component 2: Bias risk (0-1) - inverse of MAFI score
        if mafi_score is not None:
            bias_component = max(0, 1.0 - mafi_score)
        else:
            bias_component = 0.5  # neutral if unknown

        # Component 3: Effect stability (0-1) - based on trajectory CV
        if trajectory_cv_str != '' and float(trajectory_cv_str) >= 0:
            cv = float(trajectory_cv_str)
            stability_component = max(0, 1.0 - min(cv, 2.0) / 2.0)
        else:
            stability_component = 0.5

        # Component 4: Decay magnitude (0-1)
        if decay_ratio_str != '':
            dr_val = float(decay_ratio_str)
            # decay_ratio near 1.0 = stable, far from 1.0 = unstable
            decay_component = max(0, 1.0 - min(abs(dr_val - 1.0), 2.0) / 2.0)
        else:
            decay_component = 0.5

        # Weighted FPI (0-100)
        fpi = (0.30 * k_component +
               0.25 * bias_component +
               0.25 * stability_component +
               0.20 * decay_component) * 100
        fpi = max(0, min(100, fpi))

        # Classification
        if fpi >= 70:
            fpi_class = "Stable"
        elif fpi >= 50:
            fpi_class = "Moderate"
        elif fpi >= 30:
            fpi_class = "Volatile"
        else:
            fpi_class = "High Risk"

        vel_match = None
        for vr in all_velocity:
            if vr['review'] == review and vr['analysis'] == dr['analysis']:
                vel_match = vr
                break

        integrated.append({
            'review': review,
            'analysis': dr['analysis'],
            'k': k_total,
            'early_effect': dr['early_effect'],
            'final_effect': dr['final_effect'],
            'decay_ratio': decay_ratio_str,
            'direction_change': dr['direction_change'],
            'trajectory_cv': trajectory_cv_str,
            'max_cumulative_shift': dr['max_cumulative_shift'],
            'studies_per_year': vel_match['studies_per_year'] if vel_match else '',
            'span_years': vel_match['span_years'] if vel_match else '',
            'mafi_score': round(mafi_score, 4) if mafi_score is not None else '',
            'mafi_class': m.get('MAFI_class', ''),
            'I2': round(m.get('I2', 0), 2) if m.get('I2') is not None else '',
            'estimate_re': round(m.get('estimate', 0), 6) if m.get('estimate') is not None else '',
            'significant': m.get('significant', ''),
            'fpi_k_component': round(k_component, 4),
            'fpi_bias_component': round(bias_component, 4),
            'fpi_stability_component': round(stability_component, 4),
            'fpi_decay_component': round(decay_component, 4),
            'fpi_score': round(fpi, 2),
            'fpi_class': fpi_class,
        })

    # Save integrated results
    int_path = OUTPUT_DIR / "mem_integrated_full.csv"
    if integrated:
        fieldnames = list(integrated[0].keys())
        with open(int_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(integrated)

        print(f"\nIntegrated: {len(integrated)} analyses saved to {int_path.name}")
        print(f"  MAFI-matched: {matched}/{len(integrated)} ({100*matched/len(integrated):.1f}%)")

        fpi_scores = [r['fpi_score'] for r in integrated]
        fpi_classes = defaultdict(int)
        for r in integrated:
            fpi_classes[r['fpi_class']] += 1

        print(f"\n--- FPI DISTRIBUTION ---")
        print(f"  Mean FPI: {np.mean(fpi_scores):.1f}")
        print(f"  Median FPI: {np.median(fpi_scores):.1f}")
        print(f"  SD FPI: {np.std(fpi_scores):.1f}")
        for cls in ["Stable", "Moderate", "Volatile", "High Risk"]:
            n = fpi_classes.get(cls, 0)
            print(f"  {cls}: {n} ({100*n/len(integrated):.1f}%)")

    # ============================================================
    # SUMMARY STATISTICS FOR MANUSCRIPT
    # ============================================================
    summary = {
        'n_reviews_processed': n_processed,
        'n_reviews_total': len(rds_files),
        'n_errors': n_errors,
        'velocity': {
            'n_analyses': len(all_velocity),
            'n_reviews': len(set(r['review'] for r in all_velocity)),
            'mean_velocity': round(np.mean([r['studies_per_year'] for r in all_velocity]), 3) if all_velocity else None,
            'median_velocity': round(np.median([r['studies_per_year'] for r in all_velocity]), 3) if all_velocity else None,
            'mean_span_years': round(np.mean([r['span_years'] for r in all_velocity]), 1) if all_velocity else None,
            'median_k': int(np.median([r['k'] for r in all_velocity])) if all_velocity else None,
        },
        'decay': {
            'n_analyses': len(all_decay),
            'n_reviews': len(set(r['review'] for r in all_decay)),
            'median_decay_ratio': round(np.median(valid_dr), 3) if valid_dr else None,
            'mean_decay_ratio': round(np.mean(valid_dr), 3) if valid_dr else None,
            'pct_direction_reversal': round(100 * dir_changes / len(all_decay), 1) if all_decay else None,
            'median_trajectory_cv': round(np.median(valid_cv), 3) if valid_cv else None,
        },
        'fpi': {
            'n_analyses': len(integrated),
            'n_mafi_matched': matched,
            'mean_fpi': round(np.mean(fpi_scores), 1) if fpi_scores else None,
            'median_fpi': round(np.median(fpi_scores), 1) if fpi_scores else None,
            'sd_fpi': round(np.std(fpi_scores), 1) if fpi_scores else None,
            'class_counts': dict(fpi_classes),
        }
    }

    summary_path = OUTPUT_DIR / "mem_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nSummary saved to {summary_path.name}")

    print("\n=== ANALYSIS COMPLETE ===")


if __name__ == '__main__':
    main()
