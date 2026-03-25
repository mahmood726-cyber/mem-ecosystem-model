# Meta Ecosystem Model: reviewer rerun manifest

This manifest is the shortest reviewer-facing rerun path for the local software package. It lists the files that should be sufficient to recreate one worked example, inspect saved outputs, and verify that the manuscript claims remain bounded to what the repository actually demonstrates.

## Reviewer Entry Points
- Project directory: `C:\Models\Meta_Ecosystem_Model`.
- Preferred documentation start points: `README.md`, `f1000_artifacts/tutorial_walkthrough.md`.
- Detected public repository root: `https://github.com/mahmood726-cyber/mem-ecosystem-model`.
- Detected public source snapshot: Fixed public commit snapshot available at `https://github.com/mahmood726-cyber/mem-ecosystem-model/tree/0a039450cb85c062088a131678d8005b55c2f24d`.
- Detected public archive record: No project-specific DOI or Zenodo record URL was detected locally; archive registration pending.
- Environment capture files: `requirements.txt`.
- Validation/test artifacts: `f1000_artifacts/validation_summary.md`, `tests/verify_manuscript_numbers.py`, `tests/verify_deeper.R`, `tests/verify_hta.R`, `tests/_stale_r_tests/verify_manuscript_numbers.R`, `tests/analyze_outputs.R`, `tests/run_tests.R`, `tests/compute_cis.py`.

## Worked Example Inputs
- Manuscript-named example paths: `MEM_Manuscript_PLOS_ONE.md` as the primary project narrative; `PROTOCOL_MEM.md` for the analysis blueprint; Derived data products in the project `data/` directory documenting trajectory outputs; f1000_artifacts/example_dataset.csv.
- Auto-detected sample/example files: `f1000_artifacts/example_dataset.csv`.

## Expected Outputs To Inspect
- Evidence velocity and decay statistics at the analysis level.
- Future-Proof Index values for stability classification.
- Project-ready narrative outputs for guideline-surveillance discussions.

## Minimal Reviewer Rerun Sequence
- Start with the README/tutorial files listed below and keep the manuscript paths synchronized with the public archive.
- Create the local runtime from the detected environment capture files if available: `requirements.txt`.
- Run at least one named example path from the manuscript and confirm that the generated outputs match the saved validation materials.
- Quote one concrete numeric result from the local validation snippets below when preparing the final software paper.

## Local Numeric Evidence Available
- `f1000_artifacts/validation_summary.md` reports Example dataset used for walkthrough: data\cleaned_rds\CD000028_pub4_data.rds.
- `data/advanced_model_summary.txt` reports Spline strongly better (delta AIC <= -10): 0.006332454.
- `data/extended_summary_2005.txt` reports prop_abs_delta_i2_le_10 prop_delta_tau2_gt0 median_delta_i2 mean_delta_i2.
