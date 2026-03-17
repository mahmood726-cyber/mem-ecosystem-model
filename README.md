# Meta-Analysis Ecosystem Model (MEM)

## Installation
Use the dependency files in this directory (for example `requirements.txt`, `environment.yml`, `DESCRIPTION`, or equivalent project-specific files) to create a clean local environment before running analyses.
Document any package-version mismatch encountered during first run.

A framework for quantifying the temporal dynamics and durability of meta-analytic evidence, applied to 501 Cochrane systematic reviews.

## Overview

The Meta-Analysis Ecosystem Model treats evidence as a dynamic system with three measurable properties:

1. **Evidence Velocity** — how rapidly new studies accumulate (studies per year)
2. **Effect Decay** — whether early pooled effects shrink or reverse as evidence grows (Proteus phenomenon)
3. **Future-Proof Index (FPI)** — a composite score (0-100) integrating velocity, decay, trajectory stability, and publication bias (MAFI)

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Run main analysis (requires Pairwise70 RDS files in data/cleaned_rds/)
python run_mem_full_analysis.py

# Step 2: Compute extended statistics (Spearman, t-tests, sensitivity analysis)
python compute_all_statistics.py

# Step 3: Generate figures
python paper/generate_figures.py

# Step 4: Verify all manuscript numbers
python tests/verify_manuscript_numbers.py
```

## Data

The analysis requires the Pairwise70 benchmark dataset — 501 Cochrane systematic review RDS files placed in `data/cleaned_rds/`. The Pairwise70 R package is available from [ZENODO_DOI_PLACEHOLDER].

Pre-computed MAFI publication bias scores are included in `data/MAFI_validated_results.csv`.

## Pipeline outputs

| File | Description |
|------|-------------|
| `data/mem_velocity_full.csv` | 3,651 analysis-level velocity metrics |
| `data/mem_decay_full.csv` | 3,062 analysis-level decay metrics |
| `data/mem_integrated_full.csv` | Integrated dataset with FPI scores |
| `data/mem_summary.json` | Summary statistics |
| `data/mem_extended_stats.json` | Spearman correlations, t-tests, sensitivity analysis |
| `data/mem_sensitivity_weights.csv` | S4 Table: FPI under alternative weight schemes |
| `data/mem_crosstab.csv` | Table 2: MAFI class x FPI class |

## Verification

The verification script checks 100+ manuscript claims against the actual data:

```bash
python tests/verify_manuscript_numbers.py
# Expected: ALL PASS (currently 100+/100+ PASS, 0 FAIL)
```

## Key results

- 501 Cochrane reviews, 3,651 analysis trajectories, 3,062 with cumulative meta-analysis
- Median decay ratio: 0.66 (67.3% show effect shrinkage)
- Sign reversals: 25.1% (3.4% clinically meaningful)
- Mean FPI: 63.3 (SD 14.1); 32.6% Stable, 49.0% Moderate, 17.1% Volatile, 1.3% High Risk

## Requirements

- Python >= 3.10
- numpy >= 2.0, pandas >= 2.0, scipy >= 1.11, pyreadr >= 0.5, matplotlib >= 3.7

## Manuscript

Hassan MU. The meta-analysis ecosystem model: quantifying evidence velocity, effect decay, and a future-proof index across 501 Cochrane systematic reviews. [Manuscript in preparation for PLOS ONE].

## License

MIT
