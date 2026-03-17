"""
Verify ALL manuscript claims against actual data files.

Data sources:
  - mem_summary.json          (top-level counts)
  - mem_velocity_full.csv     (velocity analyses)
  - mem_decay_full.csv        (decay analyses)
  - mem_integrated_full.csv   (integrated FPI data)
  - mem_extended_stats.json   (Spearman, t-test, reversals, sensitivity)

Each claim prints PASS or FAIL with actual vs claimed values.
Floating-point tolerance: 0.05 (absolute).
"""

import json
import csv
import sys
import math
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TOL = 0.05  # absolute tolerance for float comparisons

pass_count = 0
fail_count = 0


def safe_float(val, default=None):
    """Convert string to float, returning default if empty/invalid."""
    if val is None or str(val).strip() == "":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def check(label, actual, claimed, tol=TOL):
    """Compare actual vs claimed. Print PASS/FAIL."""
    global pass_count, fail_count
    if isinstance(claimed, float):
        ok = abs(actual - claimed) <= tol
    elif isinstance(claimed, int):
        ok = actual == claimed
    else:
        ok = actual == claimed

    status = "PASS" if ok else "FAIL"
    if status == "PASS":
        pass_count += 1
    else:
        fail_count += 1
    print(f"  [{status}] {label}: actual={actual}, claimed={claimed}")


def median(vals):
    s = sorted(vals)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def percentile(vals, p):
    """Linear interpolation percentile (numpy default / R type 7)."""
    s = sorted(vals)
    n = len(s)
    idx = (p / 100.0) * (n - 1)
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return s[lo]
    frac = idx - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def mean(vals):
    return sum(vals) / len(vals)


def sd_pop(vals):
    """Population standard deviation (ddof=0), consistent with manuscript."""
    m = mean(vals)
    return math.sqrt(sum((x - m) ** 2 for x in vals) / len(vals))


def pearson_r(x, y):
    """Pearson correlation coefficient."""
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / n
    sx = math.sqrt(sum((xi - mx) ** 2 for xi in x) / n)
    sy = math.sqrt(sum((yi - my) ** 2 for yi in y) / n)
    if sx == 0 or sy == 0:
        return 0.0
    return cov / (sx * sy)


def main():
    # ---------------------------------------------------------------
    # 1. Load data
    # ---------------------------------------------------------------
    with open(DATA_DIR / "mem_summary.json", "r") as f:
        summary = json.load(f)

    velocity_rows = []
    with open(DATA_DIR / "mem_velocity_full.csv", "r", newline="") as f:
        for row in csv.DictReader(f):
            velocity_rows.append(row)

    decay_rows = []
    with open(DATA_DIR / "mem_decay_full.csv", "r", newline="") as f:
        for row in csv.DictReader(f):
            decay_rows.append(row)

    integrated_rows = []
    with open(DATA_DIR / "mem_integrated_full.csv", "r", newline="") as f:
        for row in csv.DictReader(f):
            integrated_rows.append(row)

    # Load extended stats (Spearman, t-test, etc.)
    ext_path = DATA_DIR / "mem_extended_stats.json"
    if ext_path.exists():
        with open(ext_path, "r") as f:
            extended = json.load(f)
    else:
        extended = None
        print("  [WARN] mem_extended_stats.json not found — run compute_all_statistics.py first")

    # ---------------------------------------------------------------
    # SECTION 1: Top-level counts (mem_summary.json)
    # ---------------------------------------------------------------
    print("=" * 70)
    print("SECTION 1: Top-level counts (mem_summary.json)")
    print("=" * 70)

    check("Reviews processed", summary["n_reviews_processed"], 501)
    check("Errors", summary["n_errors"], 0)
    check("Velocity analyses (json)", summary["velocity"]["n_analyses"], 3651)
    check("Velocity reviews (json)", summary["velocity"]["n_reviews"], 415)
    check("Decay analyses (json)", summary["decay"]["n_analyses"], 3062)
    check("Decay reviews (json)", summary["decay"]["n_reviews"], 381)

    # ---------------------------------------------------------------
    # SECTION 2: CSV row counts
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 2: CSV row counts")
    print("=" * 70)

    check("Velocity CSV rows", len(velocity_rows), 3651)
    check("Decay CSV rows", len(decay_rows), 3062)
    check("Integrated CSV rows", len(integrated_rows), 3062)

    vel_reviews = set(r["review"] for r in velocity_rows)
    decay_reviews = set(r["review"] for r in decay_rows)
    check("Velocity unique reviews", len(vel_reviews), 415)
    check("Decay unique reviews", len(decay_reviews), 381)

    # ---------------------------------------------------------------
    # SECTION 3: Velocity statistics
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 3: Velocity statistics")
    print("=" * 70)

    velocities = [float(r["studies_per_year"]) for r in velocity_rows]
    spans = [float(r["span_years"]) for r in velocity_rows]
    ks_vel = [int(r["k"]) for r in velocity_rows]

    check("Median velocity", round(median(velocities), 2), 0.82)
    check("Velocity Q1", round(percentile(velocities, 25), 2), 0.50)
    check("Velocity Q3", round(percentile(velocities, 75), 2), 1.52)
    check("Mean velocity", round(mean(velocities), 2), 1.50)
    check("SD velocity", round(sd_pop(velocities), 2), 2.20)

    check("Median span years", round(median(spans), 1), 16.0)
    check("Span Q1", round(percentile(spans, 25), 1), 10.0)
    check("Span Q3", round(percentile(spans, 75), 1), 24.0)
    check("Mean span years", round(mean(spans), 1), 17.9)
    check("SD span years", round(sd_pop(spans), 1), 11.3)

    check("Median k", round(median(ks_vel), 0), 11)
    check("k Q1", round(percentile(ks_vel, 25), 0), 7)
    check("k Q3", round(percentile(ks_vel, 75), 0), 20)

    # Same-year count (manuscript: 55 analyses [1.5%])
    n_same_year = sum(1 for s in spans if s == 0)
    check("Same-year analyses (span=0)", n_same_year, 55)

    # ---------------------------------------------------------------
    # SECTION 4: Decay statistics
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 4: Decay statistics")
    print("=" * 70)

    decay_ratios_all = [safe_float(r["decay_ratio"]) for r in decay_rows]
    decay_ratios = [v for v in decay_ratios_all if v is not None]
    n_valid_decay = len(decay_ratios)
    n_empty_decay = len(decay_rows) - n_valid_decay
    print(f"  [INFO] {n_valid_decay} valid decay ratios, {n_empty_decay} empty (early_effect=0)")

    direction_changes = [r["direction_change"] for r in decay_rows]

    trajectory_cvs_all = [safe_float(r["trajectory_cv"]) for r in decay_rows]
    trajectory_cvs = [v for v in trajectory_cvs_all if v is not None]
    n_valid_cv = len(trajectory_cvs)
    n_empty_cv = len(decay_rows) - n_valid_cv
    print(f"  [INFO] {n_valid_cv} valid trajectory CVs, {n_empty_cv} empty")

    non_extreme = [r for r in decay_ratios if r <= 10.0]
    n_non_extreme = len(non_extreme)

    check("Median decay ratio", round(median(non_extreme), 2), 0.66)
    check("Decay ratio Q1", round(percentile(non_extreme, 25), 2), 0.32)
    check("Decay ratio Q3", round(percentile(non_extreme, 75), 2), 1.23)

    check("Non-extreme count (n)", n_non_extreme, 2817)
    shrinkage_count = sum(1 for r in non_extreme if r < 1.0)
    pct_shrinkage = round(100.0 * shrinkage_count / n_non_extreme, 1)
    check("Shrinkage % (ratio < 1.0)", pct_shrinkage, 67.3)

    major_shrinkage_count = sum(1 for r in non_extreme if r < 0.5)
    pct_major = round(100.0 * major_shrinkage_count / n_non_extreme, 1)
    check("Major shrinkage % (ratio < 0.5)", pct_major, 39.0)

    n_reversals = sum(1 for d in direction_changes if d.strip().lower() == "true")
    check("Direction reversals count", n_reversals, 769)
    pct_reversals = round(100.0 * n_reversals / len(decay_rows), 1)
    check("Direction reversals %", pct_reversals, 25.1)

    check("Median trajectory CV", round(median(trajectory_cvs), 2), 0.50)
    check("Trajectory CV Q1", round(percentile(trajectory_cvs, 25), 2), 0.25)
    check("Trajectory CV Q3", round(percentile(trajectory_cvs, 75), 2), 1.14)
    check("Mean trajectory CV", round(mean(trajectory_cvs), 2), 2.19)
    check("SD trajectory CV", round(sd_pop(trajectory_cvs), 1), 13.2)

    # ---------------------------------------------------------------
    # SECTION 5: Meaningful reversals (NEW)
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 5: Meaningful reversals")
    print("=" * 70)

    threshold = 0.2
    n_meaningful = 0
    for r in decay_rows:
        if r["direction_change"].strip().lower() != "true":
            continue
        early = safe_float(r["early_effect"])
        final = safe_float(r["final_effect"])
        if early is not None and final is not None:
            if abs(early) > threshold and abs(final) > threshold:
                n_meaningful += 1

    check("Meaningful reversals (|logOR|>0.2)", n_meaningful, 105)
    pct_meaningful = round(100.0 * n_meaningful / len(decay_rows), 1)
    check("Meaningful reversal %", pct_meaningful, 3.4)

    # ---------------------------------------------------------------
    # SECTION 6: Correlations (Pearson + Spearman from extended stats)
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 6: Correlations")
    print("=" * 70)

    corr_vel = []
    corr_decay = []
    corr_cv = []
    corr_mafi = []

    for r in integrated_rows:
        vel = safe_float(r["studies_per_year"])
        dec = safe_float(r["decay_ratio"])
        cv_val = safe_float(r["trajectory_cv"])
        mafi_val = safe_float(r["mafi_score"])
        if all(x is not None for x in [vel, dec, cv_val, mafi_val]) and dec <= 10.0:
            corr_vel.append(vel)
            corr_decay.append(dec)
            corr_cv.append(cv_val)
            corr_mafi.append(mafi_val)

    n_complete = len(corr_vel)
    print(f"  [INFO] {n_complete} complete cases")
    check("Complete cases for correlations", n_complete, 2650)

    r_vel_decay = round(pearson_r(corr_vel, corr_decay), 3)
    check("Pearson velocity-decay", r_vel_decay, -0.002, tol=0.005)

    r_vel_cv = round(pearson_r(corr_vel, corr_cv), 3)
    check("Pearson velocity-CV", r_vel_cv, 0.014, tol=0.005)

    r_mafi_decay = round(pearson_r(corr_mafi, corr_decay), 3)
    check("Pearson MAFI-decay", r_mafi_decay, 0.001, tol=0.005)

    # Spearman from extended stats
    if extended and 'correlations' in extended:
        corr = extended['correlations']
        check("Spearman velocity-decay rho", corr['spearman_velocity_decay']['rho'], -0.047, tol=0.005)
        check("Spearman velocity-CV rho", corr['spearman_velocity_cv']['rho'], 0.055, tol=0.005)
        check("Spearman MAFI-decay rho", corr['spearman_mafi_decay']['rho'], 0.077, tol=0.005)
    else:
        print("  [SKIP] Spearman correlations — run compute_all_statistics.py")

    # ---------------------------------------------------------------
    # SECTION 7: FPI statistics
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 7: FPI statistics")
    print("=" * 70)

    fpi_scores = [float(r["fpi_score"]) for r in integrated_rows]

    check("Mean FPI", round(mean(fpi_scores), 1), 63.3)
    check("SD FPI", round(sd_pop(fpi_scores), 1), 14.1)
    check("Median FPI", round(median(fpi_scores), 1), 64.4)
    check("FPI Q1", round(percentile(fpi_scores, 25), 1), 54.0)
    check("FPI Q3", round(percentile(fpi_scores, 75), 1), 72.5)
    check("FPI min", round(min(fpi_scores), 1), 19.3)
    check("FPI max", round(max(fpi_scores), 1), 97.0)

    fpi_classes = [r["fpi_class"] for r in integrated_rows]
    class_counts = {}
    for c in fpi_classes:
        class_counts[c] = class_counts.get(c, 0) + 1

    n_total = len(fpi_classes)
    check("Stable count", class_counts.get("Stable", 0), 998)
    check("Moderate count", class_counts.get("Moderate", 0), 1500)
    check("Volatile count", class_counts.get("Volatile", 0), 524)
    check("High Risk count", class_counts.get("High Risk", 0), 40)

    check("Stable %", round(100.0 * class_counts.get("Stable", 0) / n_total, 1), 32.6)
    check("Moderate %", round(100.0 * class_counts.get("Moderate", 0) / n_total, 1), 49.0)
    check("Volatile %", round(100.0 * class_counts.get("Volatile", 0) / n_total, 1), 17.1)
    check("High Risk %", round(100.0 * class_counts.get("High Risk", 0) / n_total, 1), 1.3)

    # ---------------------------------------------------------------
    # SECTION 8: FPI component means + SDs (Table 3)
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 8: FPI component statistics (Table 3)")
    print("=" * 70)

    k_comp = [float(r["fpi_k_component"]) for r in integrated_rows]
    bias_comp = [float(r["fpi_bias_component"]) for r in integrated_rows]
    stab_comp = [float(r["fpi_stability_component"]) for r in integrated_rows]
    decay_comp = [float(r["fpi_decay_component"]) for r in integrated_rows]

    check("Mean k component", round(mean(k_comp), 2), 0.50)
    check("SD k component", round(sd_pop(k_comp), 2), 0.28)
    check("Median k component", round(median(k_comp), 2), 0.39)

    check("Mean bias component", round(mean(bias_comp), 2), 0.81)
    check("SD bias component", round(sd_pop(bias_comp), 2), 0.15)
    check("Median bias component", round(median(bias_comp), 2), 0.83)

    check("Mean stability component", round(mean(stab_comp), 2), 0.62)
    check("SD stability component", round(sd_pop(stab_comp), 2), 0.33)
    check("Median stability component", round(median(stab_comp), 2), 0.75)

    check("Mean decay component", round(mean(decay_comp), 2), 0.62)
    check("SD decay component", round(sd_pop(decay_comp), 2), 0.29)
    check("Median decay component", round(median(decay_comp), 2), 0.67)

    # ---------------------------------------------------------------
    # SECTION 9: MAFI match rate
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 9: MAFI match rate")
    print("=" * 70)

    mafi_vals = [safe_float(r["mafi_score"]) for r in integrated_rows]
    n_mafi_matched = sum(1 for m in mafi_vals if m is not None and m >= 0)
    check("MAFI matched count", n_mafi_matched, 2874)
    pct_mafi = round(100.0 * n_mafi_matched / len(integrated_rows), 1)
    check("MAFI match %", pct_mafi, 93.9)

    # ---------------------------------------------------------------
    # SECTION 10: Significance comparison (Welch's t, Cohen's d)
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 10: Significant vs non-significant FPI")
    print("=" * 70)

    sig_fpi = [float(r["fpi_score"]) for r in integrated_rows
               if r["significant"].strip().lower() == "true"]
    nonsig_fpi = [float(r["fpi_score"]) for r in integrated_rows
                  if r["significant"].strip().lower() == "false"]

    n_sig = len(sig_fpi)
    n_nonsig = len(nonsig_fpi)
    n_empty_sig = len(integrated_rows) - n_sig - n_nonsig
    print(f"  [INFO] {n_sig} significant, {n_nonsig} non-significant, {n_empty_sig} missing")

    check("n significant", n_sig, 887)
    check("n non-significant", n_nonsig, 2089)
    check("n missing significance", n_empty_sig, 86)
    check("Significant mean FPI", round(mean(sig_fpi), 1), 70.8)
    check("Non-significant mean FPI", round(mean(nonsig_fpi), 1), 60.6)

    if extended and 'significance_comparison' in extended:
        sc = extended['significance_comparison']
        check("Welch t-statistic", sc['welch_t'], 20.4, tol=0.5)
        check("Cohen's d", sc['cohens_d'], 0.77, tol=0.05)
    else:
        print("  [SKIP] Welch t and Cohen's d — run compute_all_statistics.py")

    # ---------------------------------------------------------------
    # SECTION 11: Cross-tabulation (Table 2)
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 11: Cross-tabulation (Table 2)")
    print("=" * 70)

    mafi_classes = {}
    for r in integrated_rows:
        mc = r.get("mafi_class", "").strip()
        fc = r.get("fpi_class", "").strip()
        if not mc:
            mc = "Unmatched"
        key = (mc, fc)
        mafi_classes[key] = mafi_classes.get(key, 0) + 1

    # Expected from Table 2
    expected = {
        ("Robust", "Stable"): 728, ("Robust", "Moderate"): 553,
        ("Robust", "Volatile"): 91, ("Robust", "High Risk"): 1,
        ("Low Fragility", "Stable"): 231, ("Low Fragility", "Moderate"): 607,
        ("Low Fragility", "Volatile"): 226, ("Low Fragility", "High Risk"): 15,
        ("Moderate Fragility", "Stable"): 8, ("Moderate Fragility", "Moderate"): 221,
        ("Moderate Fragility", "Volatile"): 125, ("Moderate Fragility", "High Risk"): 15,
        ("High Fragility", "Stable"): 0, ("High Fragility", "Moderate"): 28,
        ("High Fragility", "Volatile"): 24, ("High Fragility", "High Risk"): 1,
        ("Unmatched", "Stable"): 31, ("Unmatched", "Moderate"): 91,
        ("Unmatched", "Volatile"): 58, ("Unmatched", "High Risk"): 8,
    }

    for key, exp_val in expected.items():
        actual_val = mafi_classes.get(key, 0)
        check(f"Table2 {key[0]}-{key[1]}", actual_val, exp_val)

    # ---------------------------------------------------------------
    # SECTION 12: Sensitivity analysis (S4 Table)
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    print("SECTION 12: Sensitivity analysis")
    print("=" * 70)

    if extended and 'sensitivity' in extended:
        sens = extended['sensitivity']
        # Equal weights
        eq = sens[1]
        check("Equal weights Stable %", eq['Stable (%)'], 36.1, tol=0.5)
        check("Equal weights Volatile %", eq['Volatile (%)'], 16.0, tol=0.5)

        # Stability-dominant
        sd_w = sens[2]
        check("Stability-dominant Stable %", sd_w['Stable (%)'], 41.9, tol=0.5)
        check("Stability-dominant Volatile %", sd_w['Volatile (%)'], 19.6, tol=0.5)

        # Bias-dominant
        bd = sens[3]
        check("Bias-dominant Stable %", bd['Stable (%)'], 45.2, tol=0.5)
        check("Bias-dominant Volatile %", bd['Volatile (%)'], 9.7, tol=0.5)
    else:
        print("  [SKIP] Sensitivity analysis — run compute_all_statistics.py")

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print()
    print("=" * 70)
    total = pass_count + fail_count
    print(f"SUMMARY: {pass_count}/{total} PASS, {fail_count}/{total} FAIL")
    if fail_count == 0:
        print("ALL MANUSCRIPT NUMBERS VERIFIED SUCCESSFULLY")
    else:
        print(f"WARNING: {fail_count} claim(s) did not match the data")
    print("=" * 70)

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
