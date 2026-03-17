# Analyze MEM output data for manuscript numbers

library(data.table)

# 1. Future-Proof Atlas
fpa <- fread("C:/Models/Meta_Ecosystem_Model/output/future_proof_atlas.csv")
cat("=== FUTURE-PROOF ATLAS ===\n")
cat("Total entries:", nrow(fpa), "\n")
cat("Columns:", paste(names(fpa), collapse=", "), "\n")
if ("stability_class" %in% names(fpa)) {
  cat("Stability classes:\n")
  print(table(fpa$stability_class))
  cat("Pct distribution:\n")
  for (cl in unique(fpa$stability_class)) {
    cat(sprintf("  %s: %.1f%%\n", cl, 100*mean(fpa$stability_class == cl)))
  }
}
if ("fpi_score" %in% names(fpa)) {
  cat("FPI score stats:\n")
  cat("  Mean:", mean(fpa$fpi_score, na.rm=TRUE), "\n")
  cat("  Median:", median(fpa$fpi_score, na.rm=TRUE), "\n")
  cat("  SD:", sd(fpa$fpi_score, na.rm=TRUE), "\n")
  cat("  Range:", range(fpa$fpi_score, na.rm=TRUE), "\n")
}

# 2. Evidence trajectories
vel_path <- "C:/Models/Meta_Ecosystem_Model/data/evidence_trajectories.csv"
if (file.exists(vel_path)) {
  vel <- fread(vel_path)
  cat("\n=== EVIDENCE VELOCITY ===\n")
  cat("Total velocity entries:", nrow(vel), "\n")
  cat("Columns:", paste(names(vel), collapse=", "), "\n")
  if ("studies_per_year" %in% names(vel)) {
    cat("Velocity stats:\n")
    cat("  Mean:", mean(vel$studies_per_year, na.rm=TRUE), "\n")
    cat("  Median:", median(vel$studies_per_year, na.rm=TRUE), "\n")
  }
  if ("k" %in% names(vel)) {
    cat("Studies per analysis:\n")
    cat("  Mean k:", mean(vel$k, na.rm=TRUE), "\n")
    cat("  Median k:", median(vel$k, na.rm=TRUE), "\n")
    cat("  Total analyses:", nrow(vel), "\n")
  }
}

# 3. Evidence decay
decay_path <- "C:/Models/Meta_Ecosystem_Model/data/evidence_decay.csv"
if (file.exists(decay_path)) {
  dec <- fread(decay_path)
  cat("\n=== EVIDENCE DECAY ===\n")
  cat("Total decay entries:", nrow(dec), "\n")
  cat("Columns:", paste(names(dec), collapse=", "), "\n")
  if ("decay_ratio" %in% names(dec)) {
    cat("Decay ratio stats:\n")
    cat("  Mean:", mean(dec$decay_ratio, na.rm=TRUE), "\n")
    cat("  Median:", median(dec$decay_ratio, na.rm=TRUE), "\n")
    fin <- dec[is.finite(decay_ratio)]
    cat("  Finite entries:", nrow(fin), "\n")
    cat("  Mean (finite):", mean(fin$decay_ratio), "\n")
  }
}

# 4. MAFI results
mafi_path <- "C:/Models/Meta_Ecosystem_Model/data/MAFI_validated_results.csv"
if (file.exists(mafi_path)) {
  mafi <- fread(mafi_path)
  cat("\n=== MAFI RESULTS ===\n")
  cat("Total MAFI entries:", nrow(mafi), "\n")
  cat("Columns:", paste(names(mafi)[1:min(15,ncol(mafi))], collapse=", "), "\n")
}

# 5. Full analysis results
ar_path <- "C:/Models/Meta_Ecosystem_Model/data/analysis_results.csv"
if (file.exists(ar_path)) {
  ar <- fread(ar_path, nrows=5)
  cat("\n=== ANALYSIS RESULTS (first 5 rows) ===\n")
  cat("Columns:", paste(names(ar), collapse=", "), "\n")
  ar_full <- fread(ar_path)
  cat("Total rows:", nrow(ar_full), "\n")
  cat("Unique reviews:", length(unique(ar_full$review)), "\n")
}
