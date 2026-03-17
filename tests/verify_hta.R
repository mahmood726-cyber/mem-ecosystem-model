library(data.table)
setwd("C:/Models/Meta_Ecosystem_Model")

hta <- fread("data/unified_hta_validation.csv")
cat("=== HTA Validation Data ===\n")
cat("N rows:", nrow(hta), "\n")
cat("Unique dataset_names:", length(unique(hta$dataset_name)), "\n")
cat("Unique analysis_keys:", length(unique(hta$analysis_key)), "\n")
cat("Dataset names:\n")
print(unique(hta$dataset_name))

# The FPI script does:
# hta_valid[, review := paste0(dataset_name, ".rds")]
# final_dt <- merge(hta_valid, velocity[, .(review, studies_per_year, span_years)], by = "review", all.x = TRUE)
# This is a MANY-TO-MANY merge because:
# - hta_valid has 50 rows for CD000028_pub4_data.rds
# - velocity has 12 rows for CD000028_pub4_data.rds
# Result: 50 * 12 = 600 rows!

vel <- fread("data/evidence_trajectories.csv")
cat("\nVelocity rows for CD000028:", sum(vel$review == "CD000028_pub4_data.rds"), "\n")
cat("HTA rows: 50 x Velocity rows: 12 =", 50 * 12, "(matches FPI N=600!)\n")

# Check het_penalty -- manuscript says OIS_adj = OIS_base / (1-I2)
# But data shows het_penalty = 20 for ALL rows regardless of I2
cat("\n=== het_penalty analysis ===\n")
cat("All het_penalty values:", unique(hta$het_penalty), "\n")
cat("I2 range:", range(hta$I2), "\n")
cat("When I2=0, 1/(1-I2)=1, but het_penalty=20\n")
cat("When I2=98.4, 1/(1-I2/100)=62.5, but het_penalty=20\n")
cat("het_penalty is HARDCODED to 20, not computed from I2!\n")

# Check IF: inf_frac = total_n / ois_adjusted
cat("\n=== Information Fraction check ===\n")
hta[, check_if := total_n / ois_adjusted]
cat("Max IF difference:", max(abs(hta$inf_frac - hta$check_if)), "\n")
cat("IF range:", range(hta$inf_frac), "\n")
cat("Max IF:", max(hta$inf_frac), "\n")
cat("All IF < 1:", all(hta$inf_frac < 1), "\n")
