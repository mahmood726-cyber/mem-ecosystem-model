#!/usr/bin/env Rscript
# NOTE: This R script uses a different (multiplicative) FPI formula and stale data
# from a single review. The canonical FPI is computed in run_mem_full_analysis.py
# using the weighted additive formula described in the PLOS ONE manuscript.
# Canonical output: data/mem_integrated_full.csv (3,062 analyses, mean FPI 63.3)

################################################################################
# MEM PHASE 3: THE FUTURE-PROOF INDEX (FPI)
# Developing a composite engine for evidence stability forecasting
################################################################################

suppressPackageStartupMessages({
  library(data.table)
  library(dplyr)
})

# Load Components
velocity <- fread("data/evidence_trajectories.csv")
decay <- fread("C:/Models/Meta_Ecosystem_Model/data/evidence_decay.csv")
hta_valid <- fread("data/unified_hta_validation.csv")

# Merge
cat("Merging Evidence Ecosystem components...
")
hta_valid[, review := paste0(dataset_name, ".rds")]
final_dt <- merge(hta_valid, velocity[, .(review, studies_per_year, span_years)], by = "review", all.x = TRUE)

# CALCULATE FUTURE-PROOF INDEX (FPI)
# Higher = More stable
# Logic: 
# 1. High Information Fraction (inf_frac) increases FPI
# 2. High Publication Bias suspiction (bias_detected) decreases FPI
# 3. High Evidence Velocity (studies_per_year) decreases FPI (higher risk of rapid churn)

final_dt[, bias_prob := ifelse(bias_detected == TRUE, 0.6, 0.1)] # Simplified probability
final_dt[, velocity_penalty := scales::rescale(pmin(studies_per_year, 5), to = c(0, 0.5))] # Cap at 5 studies/yr

final_dt[, fpi_score := (inf_frac * (1 - bias_prob) * (1 - velocity_penalty)) * 100]
final_dt[, fpi_score := pmin(100, pmax(0, fpi_score))]

# Classification
final_dt[, stability_class := case_when(
  fpi_score >= 70 ~ "IMMUTABLE (Historical Anchor)",
  fpi_score >= 40 ~ "STABLE (Mature Evidence)",
  fpi_score >= 15 ~ "VOLATILE (Evolving)",
  TRUE ~ "HIGH RISK (Experimental/Ephemeral)"
)]

# Summary
cat("
--- FUTURE-PROOF INDEX (FPI) DISTRIBUTION ---
")
print(final_dt[, .N, by = stability_class])

# Save
fwrite(final_dt, "output/future_proof_atlas.csv")
cat("
MEM Engine Finalized. Project Ready for Reporting.
")
