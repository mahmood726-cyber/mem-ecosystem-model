#!/usr/bin/env Rscript
# NOTE: This R script processes only the first 30 of 501 reviews (legacy).
# The canonical full-dataset analysis is in run_mem_full_analysis.py (all 501 reviews).
# Output from this script: data/evidence_decay.csv (204 analyses from ~26 reviews)
# Canonical output: data/mem_decay_full.csv (3,062 analyses from 381 reviews)

suppressPackageStartupMessages({
  library(data.table)
  library(metafor)
})

rds_dir <- "data/cleaned_rds"
rds_files <- list.files(rds_dir, pattern = "\\.rds$", full.names = TRUE)

analyze_decay <- function(file) {
  df <- tryCatch(readRDS(file), error = function(e) NULL)
  if (is.null(df)) return(NULL)
  names(df) <- gsub("[^A-Za-z0-9]+", ".", names(df))
  if (!"Study.year" %in% names(df)) return(NULL)
  
  analysis_num <- if ("Analysis.number" %in% names(df)) as.character(df$Analysis.number) else "1"
  subgroup_id <- if ("Subgroup.number" %in% names(df)) as.character(df$Subgroup.number) else "overall"
  df$analysis_id <- paste(analysis_num, subgroup_id, sep = "::")
  
  results <- list()
  for (id in unique(df$analysis_id)) {
    sub <- df[df$analysis_id == id, ]
    if (!all(c("Experimental.cases", "Experimental.N", "Control.cases", "Control.N") %in% names(sub))) next
    sub <- sub[!is.na(sub$Study.year) & sub$Experimental.N > 0 & sub$Control.N > 0, ]
    if (nrow(sub) < 8) next
    
    sub <- sub[order(as.numeric(as.character(sub$Study.year))), ]
    es <- tryCatch(escalc(measure="OR", ai=Experimental.cases, n1i=Experimental.N, 
                          ci=Control.cases, n2i=Control.N, data=sub, add=0.5, to="only0"),
                   error = function(e) NULL)
    if (is.null(es)) next
    
    cum_effects <- numeric(nrow(es))
    for (j in 3:nrow(es)) {
      fit <- tryCatch(rma(yi, vi, data = es[1:j, ], method = "FE"), error = function(e) NULL)
      if (!is.null(fit)) cum_effects[j] <- as.numeric(fit$beta)
    }
    
    es_early <- cum_effects[3]
    es_final <- cum_effects[nrow(es)]
    decay_ratio <- if (abs(es_early) > 0) abs(es_final) / abs(es_early) else NA
    
    results[[length(results)+1]] <- list(
      review = basename(file), k_total = nrow(es),
      early_effect = es_early, final_effect = es_final,
      decay_ratio = decay_ratio
    )
  }
  return(rbindlist(results))
}

cat("Modeling Evidence Decay (Fast Sample 30)...\n")
decay_data <- rbindlist(lapply(rds_files[1:min(30, length(rds_files))], function(f) {
  cat(".")
  analyze_decay(f)
}))

cat("\n--- THE LAW OF EVIDENCE DECAY ---\n")
print(decay_data[, .(
  n_analyses = .N,
  median_decay_ratio = median(decay_ratio, na.rm = TRUE),
  pct_shrinkage = (1 - mean(decay_ratio, na.rm = TRUE)) * 100
)])

fwrite(decay_data, "data/evidence_decay.csv")
cat("\nPhase 2 Complete.\n")