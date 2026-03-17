"""Compute confidence intervals and p-values for manuscript claims."""
import numpy as np
import pandas as pd
from scipy import stats

from pathlib import Path
DATA_DIR = str(Path(__file__).resolve().parent.parent / "data")

integrated = pd.read_csv(f"{DATA_DIR}/mem_integrated_full.csv")
velocity = pd.read_csv(f"{DATA_DIR}/mem_velocity_full.csv")

print("=== CIs for Key Manuscript Claims ===\n")

# 1. FPI difference: significant vs non-significant
sig = integrated[integrated['significant'] == True]['fpi_score'].dropna()
nonsig = integrated[integrated['significant'] == False]['fpi_score'].dropna()
print(f"Significant FPI: n={len(sig)}, mean={sig.mean():.1f}, SD={sig.std():.1f}")
print(f"Non-significant FPI: n={len(nonsig)}, mean={nonsig.mean():.1f}, SD={nonsig.std():.1f}")
diff = sig.mean() - nonsig.mean()
# Welch's t-test
t_stat, p_val = stats.ttest_ind(sig, nonsig, equal_var=False)
# CI for difference
se_diff = np.sqrt(sig.var()/len(sig) + nonsig.var()/len(nonsig))
df_welch = (sig.var()/len(sig) + nonsig.var()/len(nonsig))**2 / \
           ((sig.var()/len(sig))**2/(len(sig)-1) + (nonsig.var()/len(nonsig))**2/(len(nonsig)-1))
t_crit = stats.t.ppf(0.975, df_welch)
ci_lo = diff - t_crit * se_diff
ci_hi = diff + t_crit * se_diff
print(f"Difference: {diff:.1f} (95% CI: {ci_lo:.1f} to {ci_hi:.1f})")
print(f"Welch's t={t_stat:.2f}, df={df_welch:.0f}, p={p_val:.2e}\n")

# 2. Correlations with CIs (Fisher z-transform)
def corr_ci(x, y, label):
    mask = x.notna() & y.notna()
    x_clean, y_clean = x[mask].values, y[mask].values
    n = len(x_clean)
    r, p = stats.pearsonr(x_clean, y_clean)
    z = np.arctanh(r)
    se_z = 1 / np.sqrt(n - 3)
    z_lo, z_hi = z - 1.96*se_z, z + 1.96*se_z
    r_lo, r_hi = np.tanh(z_lo), np.tanh(z_hi)
    print(f"{label}: r={r:.3f} (95% CI: {r_lo:.3f} to {r_hi:.3f}), n={n}, p={p:.2e}")

# Filter to non-extreme decay
mask_complete = (integrated['decay_ratio'].notna() &
                 (integrated['decay_ratio'] <= 10) &
                 integrated['studies_per_year'].notna() &
                 integrated['mafi_score'].notna() &
                 integrated['trajectory_cv'].notna())
complete = integrated[mask_complete]
print(f"Complete cases for correlations: n={len(complete)}")

corr_ci(complete['studies_per_year'], complete['decay_ratio'], "Velocity-Decay")
corr_ci(complete['studies_per_year'], complete['trajectory_cv'], "Velocity-CV")
corr_ci(complete['mafi_score'], complete['decay_ratio'], "MAFI-Decay")
corr_ci(complete['studies_per_year'], complete['fpi_score'], "Velocity-FPI")
corr_ci(complete['mafi_score'], complete['fpi_score'], "MAFI-FPI")
corr_ci(complete['decay_ratio'], complete['fpi_score'], "Decay-FPI")

# 3. Decay ratio CI
decay_non_extreme = integrated['decay_ratio'].dropna()
decay_non_extreme = decay_non_extreme[decay_non_extreme <= 10]
n_dr = len(decay_non_extreme)
print(f"\nDecay ratio (non-extreme, n={n_dr}):")
print(f"  Median: {decay_non_extreme.median():.2f}")
print(f"  IQR: {decay_non_extreme.quantile(0.25):.2f} - {decay_non_extreme.quantile(0.75):.2f}")

# Bootstrap CI for median decay ratio
np.random.seed(42)
boot_medians = [np.median(np.random.choice(decay_non_extreme.values, size=n_dr, replace=True))
                for _ in range(10000)]
print(f"  Bootstrap 95% CI for median: {np.percentile(boot_medians, 2.5):.2f} to {np.percentile(boot_medians, 97.5):.2f}")

# 4. Direction reversal CI (proportion)
n_total = 3062
n_reversal = 769
p_rev = n_reversal / n_total
se_rev = np.sqrt(p_rev * (1-p_rev) / n_total)
ci_lo_rev = p_rev - 1.96*se_rev
ci_hi_rev = p_rev + 1.96*se_rev
print(f"\nDirection reversal: {n_reversal}/{n_total} = {100*p_rev:.1f}% (95% CI: {100*ci_lo_rev:.1f}% to {100*ci_hi_rev:.1f}%)")

print("\nDone!")
