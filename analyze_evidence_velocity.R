#!/usr/bin/env Rscript
# NOTE: This R script processes only the first 100 of 501 reviews (legacy).
# The canonical full-dataset analysis is in run_mem_full_analysis.py (all 501 reviews).
# Output from this script: data/evidence_trajectories.csv (913 analyses from ~87 reviews)
# Canonical output: data/mem_velocity_full.csv (3,651 analyses from 415 reviews)

################################################################################
# MEM PHASE 1: EVIDENCE VELOCITY & EFFECT DECAY
# Reconstructing the history of 50,000 trials to model evidence trajectory
################################################################################

suppressPackageStartupMessages({
  library(data.table)
  library(dplyr)
  library(metafor)
})

rds_dir <- "data/cleaned_rds"
rds_files <- list.files(rds_dir, pattern = "\\.rds$", full.names = TRUE)

cat(sprintf("Found %d systematic review files. Analyzing timelines...\n", length(rds_files)))

# Analysis Function
analyze_trajectory <- function(file) {
  df <- tryCatch(readRDS(file), error = function(e) NULL)
  if (is.null(df)) return(NULL)
  
  # Standardize
  names(df) <- gsub("[^A-Za-z0-9]+", ".", names(df))
  if (!"Study.year" %in% names(df)) return(NULL)
  
  # Group by analysis
  analysis_num <- if ("Analysis.number" %in% names(df)) as.character(df$Analysis.number) else "1"
  subgroup_id <- if ("Subgroup.number" %in% names(df)) as.character(df$Subgroup.number) else "overall"
  df$analysis_id <- paste(analysis_num, subgroup_id, sep = "::")
  
  results <- list()
  for (id in unique(df$analysis_id)) {
    sub <- df[df$analysis_id == id, ]
    # Force year to numeric
    years <- as.numeric(as.character(sub$Study.year))
    sub <- sub[!is.na(years), ]
    years <- years[!is.na(years)]
    
    if (nrow(sub) < 5) next
    
    # Sort by year
    sub <- sub[order(years), ]
    years <- sort(years)
    
    # Calculate Evidence Velocity
    year_range <- max(years) - min(years)
    velocity <- nrow(sub) / max(1, year_range)
    
    results[[length(results)+1]] <- list(
      review = basename(file),
      analysis = id,
      k = nrow(sub),
      span_years = year_range,
      studies_per_year = velocity,
      start_year = min(years),
      end_year = max(years)
    )
  }
  return(rbindlist(results))
}

# Run on sample
cat("Mining temporal data (Batch 100)...\n")
results_raw <- lapply(rds_files[1:min(100, length(rds_files))], analyze_trajectory)
trajectories <- rbindlist(results_raw)

if (nrow(trajectories) == 0) {
  stop("No valid trajectories found. Check Study.year data in RDS files.")
}

cat("\n--- EVIDENCE VELOCITY ATLAS ---\n")
print(trajectories[, .(
  n_analyses = .N,
  avg_velocity = mean(studies_per_year, na.rm = TRUE),
  max_velocity = max(studies_per_year, na.rm = TRUE),
  median_span = median(span_years, na.rm = TRUE)
)])

fwrite(trajectories, "data/evidence_trajectories.csv")
cat("\nTemporal mining complete.\n")