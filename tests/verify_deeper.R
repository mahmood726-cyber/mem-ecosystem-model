library(data.table)
setwd("C:/Models/Meta_Ecosystem_Model")

fpa <- fread("output/future_proof_atlas.csv")
vel <- fread("data/evidence_trajectories.csv")
dec <- fread("data/evidence_decay.csv")

# CRITICAL CHECK 1: How many unique reviews are in FPI?
cat("=== CRITICAL: Unique reviews in FPI ===\n")
cat("Unique reviews:", length(unique(fpa$review)), "\n")
cat("Unique dataset_names:", length(unique(fpa$dataset_name)), "\n")
cat("Reviews:\n")
print(unique(fpa$review))
cat("\nDataset names:\n")
print(unique(fpa$dataset_name))

# CRITICAL CHECK 2: FPI has massive duplication
cat("\n=== CRITICAL: FPI row duplication ===\n")
cat("Total rows:", nrow(fpa), "\n")
cat("Unique (review + analysis_key + orig_estimate):", nrow(unique(fpa[, .(review, analysis_key, orig_estimate)])), "\n")
# The same analysis appears with different velocity values
cat("Unique (review + analysis_key):", nrow(unique(fpa[, .(review, analysis_key)])), "\n")
# Show the duplication pattern
cat("\nFirst review analysis key counts:\n")
print(fpa[, .N, by = .(review, analysis_key)][order(-N)][1:10])

# CRITICAL CHECK 3: Only 87 reviews in velocity, but manuscript claims 511
cat("\n=== CRITICAL: Review count discrepancy ===\n")
cat("Velocity script processes: rds_files[1:min(100, length(rds_files))]\n")
cat("So only first 100 RDS files are used!\n")
cat("Unique reviews in velocity:", length(unique(vel$review)), "\n")

# CRITICAL CHECK 4: IF >= 1.0 = 0% but manuscript says 8.6%
cat("\n=== CRITICAL: Information Fraction ===\n")
cat("IF >= 1.0:", sum(fpa$inf_frac >= 1.0), "out of", nrow(fpa), "\n")
cat("IF max:", max(fpa$inf_frac), "\n")
cat("Manuscript claims 8.6% achieved IF >= 1.0 -- DATA SAYS 0%!\n")

# CRITICAL CHECK 5: bias_detected rate
cat("\n=== Bias detection rate ===\n")
cat("bias_detected TRUE:", sum(fpa$bias_detected == TRUE), "out of", nrow(fpa), "\n")
cat("Percentage:", round(100 * sum(fpa$bias_detected == TRUE) / nrow(fpa), 1), "%\n")
cat("Manuscript claims 19.8%\n")

# CRITICAL CHECK 6: IQR mismatch
cat("\n=== IQR Check ===\n")
q <- quantile(vel$studies_per_year, c(0.25, 0.75))
cat("Actual IQR:", round(q[1], 2), "-", round(q[2], 2), "\n")
cat("Manuscript says: 0.38 - 1.25\n")

# CRITICAL CHECK 7: Median span mismatch
cat("\n=== Median span check ===\n")
cat("Actual median span:", median(vel$span_years), "\n")
cat("Manuscript says: 14\n")

# CHECK 8: decay mean vs median inconsistency
cat("\n=== Decay ratio statistics ===\n")
cat("Mean decay ratio:", round(mean(dec$decay_ratio, na.rm=TRUE), 2), "\n")
cat("Median decay ratio:", round(median(dec$decay_ratio, na.rm=TRUE), 2), "\n")
cat("The manuscript says 'mean shrinkage 43%' and 'median Decay Ratio 0.57'\n")
cat("But 1 - mean(decay_ratio) =", round(1 - mean(dec$decay_ratio, na.rm=TRUE), 2), "\n")
cat("And 1 - median(decay_ratio) =", round(1 - median(dec$decay_ratio, na.rm=TRUE), 2), "\n")
cat("43% shrinkage comes from median (0.57), NOT mean (9.18)\n")

# CHECK 9: OIS heterogeneity adjustment formula
cat("\n=== OIS adjusted check ===\n")
cat("het_penalty values:\n")
print(summary(fpa$het_penalty))
cat("\nManuscript says OIS_adj = OIS_base * (1/(1-I2))\n")
cat("But het_penalty column is separate from I2\n")
cat("I2 values:\n")
print(summary(fpa$I2))
# Check: does ois_adjusted = ois_base * het_penalty?
fpa[, check_ois := ois_base * het_penalty]
cat("ois_adjusted = ois_base * het_penalty?\n")
cat("Max difference:", max(abs(fpa$ois_adjusted - fpa$check_ois)), "\n")
# Check: does het_penalty = 1/(1-I2/100)?
fpa[, check_het := 1 / (1 - I2/100)]
cat("het_penalty = 1/(1-I2/100)?\n")
cat("First 5 rows:\n")
print(fpa[1:5, .(I2, het_penalty, check_het, ois_base, ois_adjusted)])

# CHECK 10: Velocity in FPI comes from which data?
cat("\n=== Cross-reference velocity in FPI vs trajectory ===\n")
# FPI has studies_per_year -- does it match velocity data?
# The FPI merge is: merge(hta_valid, velocity[, .(review, studies_per_year, span_years)])
# But if hta_valid has multiple analyses per review, and velocity also has multiple,
# this is a many-to-many merge!
cat("FPI rows per unique review:\n")
print(fpa[, .N, by = review])
cat("\nVelocity rows per review (first few):\n")
print(vel[, .N, by = review][order(-N)][1:10])
