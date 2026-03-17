setwd("C:/Models/Meta_Ecosystem_Model")
tryCatch(
  testthat::test_file("tests/testthat/test_mem_pipeline.R"),
  error = function(e) cat("ERROR:", conditionMessage(e), "\n")
)
