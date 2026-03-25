# Meta Ecosystem Model: a software tool for reviewer-auditable evidence synthesis

## Authors
- Mahmood Ahmad [1,2]
- Niraj Kumar [1]
- Bilaal Dar [3]
- Laiba Khan [1]
- Andrew Woo [4]
- Corresponding author: Andrew Woo (andy2709w@gmail.com)

## Affiliations
1. Royal Free Hospital
2. Tahir Heart Institute Rabwah
3. King's College Medical School
4. St George's Medical School

## Abstract
**Background:** Meta-analyses are often treated as static end points, even though their underlying evidence bases evolve over years and their pooled effects can shrink, reverse, or stabilize. Reviewers therefore need software that makes temporal evidence dynamics explicit rather than leaving them as narrative conjecture.

**Methods:** The Meta Ecosystem Model computes evidence velocity, cumulative-effect decay, trajectory stability, and a composite Future-Proof Index across Pairwise70 analyses. The local project couples R scripts, manuscript materials, and protocol notes for a dynamic view of meta-analytic durability.

**Results:** Repository artifacts include evidence-decay modelling scripts, manuscript drafts, protocol files, and local data products describing how effect trajectories evolve across hundreds of Cochrane review analyses.

**Conclusions:** The MEM software should be framed as a meta-research and surveillance tool for evidence durability, not as a substitute for clinical interpretation of individual meta-analyses.

## Keywords
living evidence; effect decay; evidence velocity; future-proof index; meta-research; software tool

## Introduction
The project makes a practical software contribution by turning ideas such as the Proteus phenomenon and evidence decay into reproducible metrics tied to concrete analysis trajectories. That supports reviewer requests for explicit examples and quantitative rather than purely rhetorical claims about evidence instability.

The appropriate comparison class includes cumulative meta-analysis, TSA-style sufficiency checks, and publication-bias assessment tools. MEM adds a temporal integration layer that these tools usually report separately.

The manuscript structure below is deliberately aligned to common open-software review requests: the rationale is stated explicitly, at least one runnable example path is named, local validation artifacts are listed, and conclusions are bounded to the functions and outputs documented in the repository.

## Methods
### Software architecture and workflow
The codebase includes scripts such as `analyze_evidence_velocity.R` and `model_evidence_decay.R`, manuscript drafts, protocol documentation, and derived data files used to compute velocity, decay, and future-proof components.

### Installation, runtime, and reviewer reruns
The local implementation is packaged under `C:\Models\Meta_Ecosystem_Model`. The manuscript identifies the local entry points, dependency manifest, fixed example input, and expected saved outputs so that reviewers can rerun the documented workflow without reconstructing it from scratch.

- Entry directory: `C:\Models\Meta_Ecosystem_Model`.
- Detected documentation entry points: `README.md`, `f1000_artifacts/tutorial_walkthrough.md`.
- Detected environment capture or packaging files: `requirements.txt`.
- Named worked-example paths in this draft: `MEM_Manuscript_PLOS_ONE.md` as the primary project narrative; `PROTOCOL_MEM.md` for the analysis blueprint; Derived data products in the project `data/` directory documenting trajectory outputs.
- Detected validation or regression artifacts: `f1000_artifacts/validation_summary.md`, `tests/verify_manuscript_numbers.py`, `tests/verify_deeper.R`, `tests/verify_hta.R`, `tests/_stale_r_tests/verify_manuscript_numbers.R`, `tests/analyze_outputs.R`, `tests/run_tests.R`, `tests/compute_cis.py`.
- Detected example or sample data files: `f1000_artifacts/example_dataset.csv`.

### Worked examples and validation materials
**Example or fixed demonstration paths**
- `MEM_Manuscript_PLOS_ONE.md` as the primary project narrative.
- `PROTOCOL_MEM.md` for the analysis blueprint.
- Derived data products in the project `data/` directory documenting trajectory outputs.

**Validation and reporting artifacts**
- `F1000_Submission_Checklist_RealReview.md` and local manuscript drafts for reporting alignment.
- Project scripts and saved outputs for velocity, decay, and FPI generation.
- Cross-linkage with MAFI-derived publication-bias information documented in the manuscript materials.

### Typical outputs and user-facing deliverables
- Evidence velocity and decay statistics at the analysis level.
- Future-Proof Index values for stability classification.
- Project-ready narrative outputs for guideline-surveillance discussions.

### Reviewer-informed safeguards
- Provides a named example workflow or fixed demonstration path.
- Documents local validation artifacts rather than relying on unsupported claims.
- Positions the software against existing tools without claiming blanket superiority.
- States limitations and interpretation boundaries in the manuscript itself.
- Requires explicit environment capture and public example accessibility in the released archive.

## Review-Driven Revisions
This draft has been tightened against recurring open peer-review objections taken from the supplied reviewer reports.
- Reproducibility: the draft names a reviewer rerun path and points readers to validation artifacts instead of assuming interface availability is proof of correctness.
- Validation: claims are anchored to local tests, validation summaries, simulations, or consistency checks rather than to unsupported assertions of performance.
- Comparators and niche: the manuscript now names the relevant comparison class and keeps the claimed niche bounded instead of implying universal superiority.
- Documentation and interpretation: the text expects a worked example, input transparency, and reviewer-verifiable outputs rather than a high-level feature list alone.
- Claims discipline: conclusions are moderated to the documented scope of Meta Ecosystem Model and paired with explicit limitations.

## Use Cases and Results
The software outputs should be described in terms of concrete reviewer-verifiable workflows: running the packaged example, inspecting the generated results, and checking that the reported interpretation matches the saved local artifacts. In this project, the most important result layer is the availability of a transparent execution path from input to analysis output.

Representative local result: `f1000_artifacts/validation_summary.md` reports Example dataset used for walkthrough: data\cleaned_rds\CD000028_pub4_data.rds.

### Concrete local quantitative evidence
- `f1000_artifacts/validation_summary.md` reports Example dataset used for walkthrough: data\cleaned_rds\CD000028_pub4_data.rds.
- `data/advanced_model_summary.txt` reports Spline strongly better (delta AIC <= -10): 0.006332454.
- `data/extended_summary_2005.txt` reports prop_abs_delta_i2_le_10 prop_delta_tau2_gt0 median_delta_i2 mean_delta_i2.

## Discussion
Representative local result: `f1000_artifacts/validation_summary.md` reports Example dataset used for walkthrough: data\cleaned_rds\CD000028_pub4_data.rds.

The paper stresses that MEM adds a temporal durability layer rather than attempting to replace conventional meta-analysis. Its main value is showing which evidence bases are stable, shrinking, or likely to require surveillance.

### Limitations
- Temporal metrics can be sensitive to sparse early data and arbitrary thresholds for meaningful reversals.
- The model is descriptive and surveillance-oriented rather than directly causal.
- Durability scores should not be interpreted as stand-alone clinical recommendations.

## Software Availability
- Local source package: `Meta_Ecosystem_Model` under `C:\Models`.
- Public repository: `https://github.com/mahmood726-cyber/mem-ecosystem-model`.
- Public source snapshot: Fixed public commit snapshot available at `https://github.com/mahmood726-cyber/mem-ecosystem-model/tree/0a039450cb85c062088a131678d8005b55c2f24d`.
- DOI/archive record: No project-specific DOI or Zenodo record URL was detected locally; archive registration pending.
- Environment capture detected locally: `requirements.txt`.
- Reviewer-facing documentation detected locally: `README.md`, `f1000_artifacts/tutorial_walkthrough.md`.
- Reproducibility walkthrough: `f1000_artifacts/tutorial_walkthrough.md` where present.
- Validation summary: `f1000_artifacts/validation_summary.md` where present.
- Reviewer rerun manifest: `F1000_Reviewer_Rerun_Manifest.md`.
- Multi-persona review memo: `F1000_MultiPersona_Review.md`.
- Concrete submission-fix note: `F1000_Concrete_Submission_Fixes.md`.
- License: see the local `LICENSE` file.

## Data Availability
All scripts and derived outputs used to compute velocity, decay, and FPI are stored locally. Source analyses are derived from public Pairwise70/Cochrane records.

## Reporting Checklist
Real-peer-review-aligned checklist: `F1000_Submission_Checklist_RealReview.md`.
Reviewer rerun companion: `F1000_Reviewer_Rerun_Manifest.md`.
Companion reviewer-response artifact: `F1000_MultiPersona_Review.md`.
Project-level concrete fix list: `F1000_Concrete_Submission_Fixes.md`.

## Declarations
### Competing interests
The authors declare that no competing interests were disclosed.

### Grant information
No specific grant was declared for this manuscript draft.

### Author contributions (CRediT)
| Author | CRediT roles |
|---|---|
| Mahmood Ahmad | Conceptualization; Software; Validation; Data curation; Writing - original draft; Writing - review and editing |
| Niraj Kumar | Conceptualization |
| Bilaal Dar | Conceptualization |
| Laiba Khan | Conceptualization |
| Andrew Woo | Conceptualization |

### Acknowledgements
The authors acknowledge contributors to open statistical methods, reproducible research software, and reviewer-led software quality improvement.

## References
1. DerSimonian R, Laird N. Meta-analysis in clinical trials. Controlled Clinical Trials. 1986;7(3):177-188.
2. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. Statistics in Medicine. 2002;21(11):1539-1558.
3. Viechtbauer W. Conducting meta-analyses in R with the metafor package. Journal of Statistical Software. 2010;36(3):1-48.
4. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71.
5. Fay C, Rochette S, Guyader V, Girard C. Engineering Production-Grade Shiny Apps. Chapman and Hall/CRC. 2022.
