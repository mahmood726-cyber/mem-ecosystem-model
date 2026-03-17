# The meta-analysis ecosystem model: quantifying evidence velocity, effect decay, and a future-proof index across 501 Cochrane systematic reviews

**Authors:** Mahmood Ul Hassan [ORCID_PLACEHOLDER]

**Affiliation:** Independent Researcher, United Kingdom

**Corresponding Author:** Mahmood Ul Hassan ([CORRESPONDING_EMAIL_PLACEHOLDER])

---

## Abstract

**Background:** Meta-analyses are typically treated as static summaries, yet the underlying evidence evolves continuously. The Proteus phenomenon — where early inflated effects shrink or reverse — has been documented anecdotally but not systematically quantified at scale. This study aimed to develop a composite index quantifying the expected durability of meta-analytic conclusions and apply it across the Cochrane Library.

**Methods:** A total of 501 Cochrane systematic reviews comprising 3,651 analysis-level trajectories (k >= 5) were analyzed. For each, evidence velocity (studies per year) was computed, cumulative fixed-effect meta-analysis was performed to quantify effect decay (ratio of final to early pooled effect magnitude), and trajectory stability was assessed. These temporal metrics were integrated with publication bias scores from the Multi-Signal Aggregate Funnel Index (MAFI) into a composite Future-Proof Index (FPI; 0-100).

**Results:** Median evidence velocity was 0.82 studies per year (interquartile range [IQR] 0.50-1.52) over a median span of 16 years. Among 2,817 analyses with non-extreme decay ratios, the median was 0.66 (IQR 0.32-1.23), with 67.3% showing effect shrinkage. Sign reversals occurred in 25.1% of 3,062 analyses, though only 3.4% involved clinically meaningful effect magnitudes in both the early and final estimates. Velocity, decay, and publication bias showed negligible Pearson correlations (all |r| < 0.02). The mean FPI was 63.3 (standard deviation [SD] 14.1): 32.6% Stable (>= 70), 49.0% Moderate, 17.1% Volatile, 1.3% High Risk.

**Conclusions:** The Meta-Analysis Ecosystem Model provides the first systematic integration of evidence velocity, effect decay, and publication bias into a composite durability index across 501 Cochrane reviews. Two-thirds of meta-analytic effects shrink as evidence accumulates, underscoring the danger of treating early pooled results as definitive.

---

## Introduction

Evidence-based medicine depends on meta-analyses as the gold standard for synthesizing treatment effects [1]. However, meta-analyses are not static artifacts: the studies underpinning them accumulate over years or decades, and the pooled estimates they produce can shift substantially as new evidence emerges [2]. The *Proteus phenomenon*, first described by Ioannidis and Trikalinos [3], refers to the tendency for early extreme results to attenuate or reverse direction as additional studies are published. While cumulative meta-analysis has been used to illustrate this phenomenon in individual clinical questions [4], no systematic large-scale quantification exists across the breadth of clinical evidence.

Three related but distinct dynamics characterize the temporal evolution of a meta-analysis. First, the *rate of evidence accumulation* — how quickly new studies enter the evidence base — determines the information turnover within a clinical field. Second, the *stability of the pooled estimate* — whether early results persist or decay — reflects the reliability of initial conclusions. Third, *publication bias* — the selective reporting of results based on direction or significance — introduces systematic distortions that interact with both accumulation and stability [5,6].

Existing frameworks address these dimensions in isolation. Trial Sequential Analysis (TSA) evaluates whether cumulative evidence has reached a sufficient information size [7]. Heterogeneity statistics (I-squared, tau-squared) quantify between-study variability at a single time point [8]. Publication bias tests (funnel plots, Egger's test, trim-and-fill) assess reporting distortions [5]. The Multi-Signal Aggregate Funnel Index (MAFI) combines eight publication bias signals into a calibrated composite score [9]. However, none of these tools integrates the temporal trajectory of evidence with its current methodological quality.

This paper proposes the *Meta-Analysis Ecosystem Model* (MEM), a framework that treats evidence as a dynamic system with measurable properties: evidence velocity (temporal accumulation rate), effect decay (magnitude attenuation over the evidence lifecycle), and trajectory stability (consistency of cumulative estimates). By integrating these temporal metrics with publication bias assessment, a composite *Future-Proof Index* (FPI) is derived — a score (0-100) that quantifies the expected durability of a meta-analytic conclusion. MEM is applied to 501 Cochrane systematic reviews encompassing 3,651 analysis-level trajectories, providing the first systematic integration of these temporal metrics with publication bias assessment into a composite durability index across the Cochrane Library.

## Materials and methods

### Data source

The Pairwise70 benchmark dataset [10] was used, which contains cleaned study-level data from 501 Cochrane systematic reviews of interventions. Each review was stored as a structured data file containing, for each included study: author, publication year, analysis group identifier, and binary outcome data (number of events and total participants in experimental and control arms). The dataset spans healthcare topics across the Cochrane Library, representing a diverse cross-section of clinical evidence.

### Evidence velocity

For each analysis within a review (defined by the combination of analysis number and subgroup), evidence velocity was computed as the number of included studies divided by the time span from the earliest to the most recent study publication year:

*Velocity = k / (year_max - year_min)*

where *k* is the number of studies with valid publication years (filtered to the plausible range 1900-2025) and the denominator is bounded below by 1.0 to avoid division by zero (affecting 55 analyses [1.5%] where all studies shared the same publication year). A minimum of five studies per analysis was required for velocity computation. This metric captures how rapidly a clinical question accumulates evidence.

### Cumulative meta-analysis and effect decay

For analyses with binary outcome data and at least six studies with valid 2x2 tables (to ensure a minimum of four cumulative estimates starting from the third study), cumulative fixed-effect meta-analysis was performed using the inverse-variance method. Studies were ordered chronologically by publication year. For each study *i*, the log odds ratio was computed:

*ln(OR_i) = ln[(a_i * d_i) / (b_i * c_i)]*

with sampling variance *v_i = 1/a_i + 1/b_i + 1/c_i + 1/d_i*, where a, b, c, d represent the four cells of the 2x2 table (after any continuity correction). When any cell contained zero, a 0.5 continuity correction was added to all four cells, with each row marginal total increased by 1.0 to maintain consistency [11]. While Sweeting et al. [11] discuss alternative correction strategies, the standard 0.5 correction was used for consistency with widely used meta-analytic software (RevMan, metafor).

The cumulative pooled estimate after *j* studies was computed using inverse-variance fixed-effect weights:

*theta_j = sum(w_i * y_i) / sum(w_i)*

where *w_i = 1/v_i*. Cumulative estimates were computed starting from the third study onward. The "early" estimate (after three studies), "midpoint" estimate, and "final" estimate (after all studies) were recorded for each analysis.

Effect decay was quantified as the decay ratio:

*Decay Ratio = |theta_final| / |theta_early|*

Values below 1.0 indicate that the effect magnitude shrank as evidence accumulated (consistent with the Proteus phenomenon); values above 1.0 indicate that the effect grew. A direction reversal was recorded when the early and final estimates had opposite signs (both exceeding a minimum magnitude of 1e-10 to avoid spurious sign changes near zero). To distinguish genuine clinical contradictions from minor fluctuations around the null, a "clinically meaningful reversal" was defined as one where both the early and final estimates exceeded |log OR| > 0.2 (corresponding to OR outside 0.82-1.22). This threshold is conservative; alternative thresholds are considered in the Discussion.

Trajectory stability was computed as the coefficient of variation (CV) of the sequence of cumulative estimates using population standard deviation (dividing by *n* rather than *n - 1*, as the sequence represents the complete set of cumulative estimates, not a sample from a larger population):

*Trajectory CV = SD_pop(theta_3, theta_4, ..., theta_k) / |mean(theta_3, ..., theta_k)|*

Higher CV indicates greater instability in the cumulative evidence trajectory.

### Multi-signal aggregate funnel index (MAFI)

Pre-computed MAFI scores from a validated analysis of the same 501 Cochrane reviews [9] were used. MAFI integrates eight statistical signals of publication bias — including funnel asymmetry, small-study effects, excess significance, and fragility — into a calibrated composite score (0 to 1, where higher values indicate greater bias risk). MAFI scores were available for 4,424 individual meta-analyses across the dataset. MAFI scores were matched to decay analyses using review name and analysis number, achieving a 93.9% match rate (2,874 of 3,062 analyses). The 188 unmatched analyses (6.1%) reflect cases where the MAFI key could not be linked, distinct from the 86 analyses (2.8%) missing significance data used in subgroup comparisons.

### Future-proof index (FPI)

The FPI is a weighted composite of four continuous components, each scaled to [0, 1]:

1. **Sample size adequacy** (weight 0.30): A logistic function of the number of studies, *k_component = 1 / (1 + exp(-0.15 * (k - 15)))*, reflecting the diminishing marginal information gain as studies accumulate. This component is partially correlated with both stability and decay (larger k tends to yield more stable trajectories), a redundancy acknowledged in Limitation 2.

2. **Bias risk** (weight 0.25): *bias_component = 1 - MAFI*, where lower MAFI (less bias) yields higher component scores.

3. **Trajectory stability** (weight 0.25): *stability_component = 1 - min(CV, 2) / 2*, where lower CV (more stable trajectory) yields higher scores, capped at CV = 2 to prevent extreme outliers from dominating.

4. **Decay magnitude** (weight 0.20): *decay_component = 1 - min(|DR - 1|, 2) / 2*, where decay ratios closer to 1.0 (stable magnitude) yield higher scores. Note that this formulation treats shrinkage and growth asymmetrically on the ratio scale (see Limitation 8).

The composite FPI (0-100) is:

*FPI = 100 * (0.30 * k_component + 0.25 * bias_component + 0.25 * stability_component + 0.20 * decay_component)*

FPI was computed for all 3,062 decay analyses, including the 245 with extreme decay ratios (> 10), for which the min-capping in the decay component yields a score of 0. FPI scores were classified as: Stable (>= 70), Moderate (50-69), Volatile (30-49), or High Risk (< 30). When MAFI scores were unavailable (6.1% of analyses), a neutral value of 0.5 was assigned to the bias component.

### Statistical analysis

Descriptive statistics are reported as means with population standard deviations (SD) and medians with interquartile ranges (IQR). Population SD (dividing by *n*) was used throughout because the analyses represent the complete set of eligible Cochrane trajectories in the Pairwise70 dataset, not a sample from a larger target population. Both Pearson and Spearman rank correlation coefficients were computed to assess relationships between velocity, decay, publication bias, and FPI, with p-values from two-sided tests. Cross-tabulations were used to examine the joint distribution of MAFI classes and FPI classes (Table 2, Fig 3). Subgroup comparisons (statistically significant vs non-significant meta-analyses) used Welch's t-test with Cohen's d effect size. Analyses with missing significance data from MAFI (n = 86, 2.8%) were excluded from significance-stratified comparisons; this is a subset of the 188 analyses (6.1%) with unmatched MAFI scores. All analyses were performed in Python 3.13 using NumPy 2.2 [12] and SciPy 1.15 [13] for statistical tests. Data were read from R data files using pyreadr 0.5 and pandas 2.2. The analysis pipeline and all data are publicly available (see Data Availability). This study was not preregistered.

## Results

### Dataset characteristics

All 501 Cochrane review files were successfully processed (no processing errors). After applying the minimum study count threshold (k >= 5) and filtering implausible publication years (outside 1900-2025), 3,651 analysis-level trajectories from 415 reviews were eligible for velocity analysis (S1 Table). Of these, 3,062 trajectories from 381 reviews had sufficient binary outcome data (k >= 6 with valid 2x2 tables) for cumulative meta-analysis (S2 Table). The median number of studies per analysis was 11 (IQR 7-20; range 5-478).

### Evidence velocity

Across 3,651 eligible analyses, the median evidence velocity was 0.82 studies per year (IQR 0.50-1.52; mean 1.50, SD 2.20). The median time span from earliest to most recent study was 16.0 years (IQR 10.0-24.0; mean 17.9, SD 11.3). The distribution of velocities was right-skewed (S1 Fig), with the fastest-accumulating analyses exceeding 40 studies per year, reflecting highly active clinical fields (Table 1).

### Effect decay and the Proteus phenomenon

Among 3,062 analyses with cumulative meta-analysis results, 2,817 had non-extreme decay ratios (excluding 245 with ratios > 10 arising from near-zero early effects). The median decay ratio was 0.66 (IQR 0.32-1.23), indicating that the typical final pooled effect was approximately two-thirds the magnitude of the early estimate (S2 Fig). Of these, 67.3% exhibited shrinkage (decay ratio < 1.0) and 39.0% showed major shrinkage (ratio < 0.5, corresponding to more than halving of the initial effect). Sign reversals — where the final pooled estimate had the opposite sign to the early estimate — occurred in 25.1% of all 3,062 analyses (769 analyses). However, when restricted to analyses where both early and final estimates exceeded a clinically meaningful magnitude (|log OR| > 0.2, corresponding to OR outside 0.82-1.22), the meaningful reversal rate was 3.4% (105 of 3,062). The remaining sign changes predominantly involved small fluctuations around the null, where the near-zero early or final estimate crossed the null without either reaching a clinically relevant magnitude.

The median trajectory CV was 0.50 (IQR 0.25-1.14; mean 2.19, SD 13.2), indicating that cumulative estimates typically varied by approximately half a standard deviation around their mean over the evidence lifecycle. The right-skewed distribution of CV values reflects a subset of analyses with highly unstable trajectories (Table 1).

### Correlations between evidence dimensions

Among 2,650 analyses with complete data for all variables (Fig 2), Pearson correlations between evidence velocity, decay ratio, and MAFI were negligible: velocity vs decay ratio r = -0.002 (p = 0.91), velocity vs trajectory CV r = 0.014 (p = 0.47), and MAFI vs decay ratio r = 0.001 (p = 0.98). Spearman rank correlations, which are more appropriate for these right-skewed distributions, were also small in magnitude though some reached statistical significance with n = 2,650: velocity vs decay ratio rho = -0.047 (p = 0.015), velocity vs trajectory CV rho = 0.055 (p = 0.005), and MAFI vs decay ratio rho = 0.077 (p < 0.001). These results indicate that the three dimensions are largely uncorrelated, with only weak monotonic associations, supporting their combination in a composite index.

Each dimension showed the expected moderate correlation with the composite FPI: velocity with FPI r = 0.236 (p < 0.001), MAFI with FPI r = -0.510 (p < 0.001), and decay ratio with FPI r = -0.267 (p < 0.001). The strongest correlation was between MAFI and FPI; however, this is partly tautological because MAFI enters FPI directly as the bias component (weight 0.25). Part-whole correlations of this nature are expected by construction.

### Future-proof index distribution

The mean FPI score was 63.3 (SD 14.1; median 64.4, IQR 54.0-72.5; range 19.3-97.0). The distribution of FPI classes was: Stable 998 (32.6%), Moderate 1,500 (49.0%), Volatile 524 (17.1%), and High Risk 40 (1.3%) (Fig 1). The four FPI components contributed as follows (Table 3): sample size adequacy (mean 0.50, SD 0.28), bias risk (mean 0.81, SD 0.15), trajectory stability (mean 0.62, SD 0.33), and decay magnitude (mean 0.62, SD 0.29). The complete integrated dataset with all component values is provided in S3 Table, and the machine-readable summary statistics in S5 Table.

### FPI and statistical significance

Among 2,976 analyses with available significance data (86 unmatched), meta-analyses with statistically significant pooled results had higher FPI scores (mean 70.8, median 71.2; n = 887) compared to non-significant results (mean 60.6, median 61.9; n = 2,089; S3 Fig), a difference of 10.2 points (Welch's t = 20.4, p < 0.001, Cohen's d = 0.77, indicating a large effect by conventional thresholds). This is consistent with the expectation that significant results tend to arise from larger evidence bases with more stable trajectories.

### Cross-tabulation of publication bias and FPI

Table 2 shows the joint distribution of MAFI publication bias classes and FPI stability classes (Fig 3). Among analyses classified as "Robust" by MAFI (low publication bias), 53.0% (728 of 1,373) were also classified as Stable by FPI, while only 0.1% (1 of 1,373) were High Risk. Conversely, among analyses with "High Fragility" (high publication bias per MAFI), none were Stable, and 47.2% were Volatile or High Risk. This demonstrates that low publication bias is a necessary but not sufficient condition for evidence stability: even among Robust analyses, 47.0% were classified as Moderate or worse by FPI, reflecting the additional information captured by the temporal decay and velocity components.

## Discussion

### Principal findings

This study provides the first systematic integration of evidence velocity, effect decay, and publication bias into a composite durability index applied across the Cochrane Library. Three principal findings emerge. First, effect shrinkage is pervasive: two-thirds of meta-analyses exhibit shrinkage of the initial pooled effect over their evidence lifecycle. Sign reversals occur in 25.1% of analyses, though the rate of clinically meaningful reversals (both early and final |log OR| > 0.2) is substantially lower at 3.4%, indicating that most reversals involve small fluctuations around the null. Second, temporal dynamics (velocity and decay) are largely uncorrelated with publication bias (all Pearson |r| < 0.02; Spearman |rho| < 0.08), supporting the rationale for combining these dimensions in a composite index. Third, the FPI classifies approximately half of Cochrane meta-analyses as having only "Moderate" future stability, with an additional 18% classified as Volatile or High Risk.

### Comparison with existing literature

The finding that the median decay ratio is 0.66 is consistent with prior individual-level observations of the Proteus phenomenon. Ioannidis and Trikalinos [3] described effect attenuation in early genetic association studies, and Pereira and Ioannidis [14] documented the "winner's curse" whereby initial studies overestimate effects. The 25.1% sign reversal rate (or 3.4% when restricted to clinically meaningful magnitudes) provides a more nuanced picture than prior estimates of how often research findings are contradicted [15]. The present analysis extends these observations from selected examples to 3,062 systematically analyzed evidence trajectories, revealing that many apparent "reversals" are in fact small fluctuations around the null rather than genuine contradictions of meaningful effects.

The near-zero correlations between velocity, decay, and MAFI scores support the theoretical rationale for combining these dimensions into a composite index. Previous work on Trial Sequential Analysis [7] and information size calculations [16] has addressed the sample size dimension of evidence sufficiency, while MAFI [9] addresses publication bias. The FPI integrates both of these with temporal stability metrics that neither approach captures alone.

### Implications for evidence synthesis and guideline development

The predominance of the Moderate FPI class (49.0%) suggests that nearly half of current Cochrane meta-analyses occupy an intermediate zone where conclusions are neither clearly durable nor clearly unstable. For guideline developers, this intermediate zone presents the greatest challenge: these analyses have accumulated meaningful evidence but show sufficient trajectory instability to warrant ongoing surveillance. The FPI could serve as a triage tool for prioritizing which systematic reviews to update, complementing existing approaches based on study volume and time since last search [17]. As a preliminary framework, analyses with FPI below 50 (Volatile or High Risk, representing 18.4% of the dataset) could be flagged for priority updating, while those above 70 (Stable, 32.6%) could be monitored with standard review cycles. Analyses in the Moderate zone (50-69) would benefit from reassessment when new studies emerge in the field. These thresholds should be validated prospectively before adoption.

The finding that statistically significant meta-analyses have higher FPI scores (mean 70.8 vs 60.6) has a nuanced interpretation. On one hand, this is expected: larger, more stable evidence bases are more likely to detect true effects. On the other hand, it cautions against equating statistical significance with evidence durability — even among significant results, the mean FPI of 70.8 places the average analysis only marginally within the "Stable" zone.

### Limitations

Several limitations should be considered. First, fixed-effect meta-analysis was used for cumulative estimates, which does not account for between-study heterogeneity. Fixed-effect cumulative analysis assigns weight proportional to 1/variance, which favors larger studies that typically appear later in the evidence timeline. This means that apparent effect "decay" may partly reflect the transition from imprecise small-study estimates to more precise large-study estimates — a precision-driven reweighting effect — rather than a true change in the underlying treatment effect. Disentangling genuine Proteus-type decay from precision reweighting would require random-effects cumulative analysis or simulation-based calibration, which is an important direction for future work. This choice was made for computational tractability across 3,062 analyses; random-effects cumulative analysis may yield different decay patterns, particularly for heterogeneous evidence bases [8].

Second, the FPI component weights (0.30, 0.25, 0.25, 0.20) were chosen based on conceptual reasoning rather than empirical optimization. The sample size component (weight 0.30) is partially correlated with both the stability and decay components, as larger evidence bases tend to produce more stable cumulative trajectories. A sensitivity analysis under alternative weighting schemes showed moderate robustness: under equal weights (0.25 each), the Stable class increased from 32.6% to 36.1% while Volatile decreased from 17.1% to 16.0%; under stability-dominant weights (0.20, 0.20, 0.40, 0.20), Stable increased to 41.9% but Volatile also increased to 19.6%; under bias-dominant weights (0.20, 0.40, 0.20, 0.20), Stable rose to 45.2% with Volatile dropping to 9.7% (S4 Table). The relative ordering of analyses was largely preserved across schemes, but absolute class assignments shifted, indicating that weight selection meaningfully affects classification. Future work could use supervised learning approaches to optimize weights against known outcomes of evidence stability.

Third, the Pairwise70 dataset is limited to binary outcomes analyzed as odds ratios. Evidence dynamics for continuous outcomes (mean differences, standardized mean differences) or other effect measures (risk ratios, hazard ratios) may differ and were not assessed.

Fourth, the velocity metric treats all studies within an analysis equally regardless of sample size. A weighted velocity measure incorporating participant counts could better capture the information accumulation rate, analogous to the information fraction in TSA [7].

Fifth, MAFI scores were unavailable for 6.1% of decay analyses, where neutral bias estimates were substituted. This may slightly underestimate the variance of FPI scores but is unlikely to substantially affect overall conclusions.

Sixth, MAFI scores were matched at the analysis level, meaning that subgroups within the same analysis share identical MAFI values. Approximately 487 rows from 172 multi-subgroup analyses are affected, introducing non-independence in MAFI-related statistics. The effective sample size for correlations involving MAFI may therefore be somewhat lower than reported.

Seventh, FPI was not validated prospectively — that is, it was not tested whether analyses classified as Volatile or High Risk were indeed more likely to shift in subsequent updates of Cochrane reviews. Prospective validation against actual Cochrane review updates is an important direction for future research.

Eighth, the decay component treats shrinkage and growth asymmetrically on the ratio scale: a decay ratio of 0.5 (effect halved) yields |0.5 - 1| = 0.5 and a component score of 0.75, while a decay ratio of 2.0 (effect doubled) yields |2.0 - 1| = 1.0 and a score of 0.50, despite these being symmetric multiplicative changes (each is the reciprocal of the other). This asymmetry means that all reported FPI scores slightly favor analyses with shrinking effects over those with growing effects. A log-transformed decay ratio, *decay_component = 1 - min(|ln(DR)|, ln(10)) / ln(10)*, would address this asymmetry and should be considered in future refinements. Because the majority of analyses (67.3%) show shrinkage (DR < 1), the net effect of this asymmetry is to slightly inflate FPI scores relative to a symmetric formulation.

Ninth, the |log OR| > 0.2 threshold for "clinically meaningful" reversals is a single illustrative cut-point, not a validated clinical standard. The meaningful reversal rate would differ under alternative thresholds (e.g., |log OR| > 0.1 or > 0.5), and the 3.4% figure should be interpreted as specific to this definition.

### Conclusions

The Meta-Analysis Ecosystem Model reveals that clinical evidence is substantially more dynamic than static synthesis snapshots suggest. Two-thirds of Cochrane meta-analytic effects shrink as evidence accumulates, and while sign reversals occur in one-quarter of analyses, clinically meaningful reversals are less common (3.4%). Temporal dynamics are largely uncorrelated with publication bias, supporting the value of a composite approach. The Future-Proof Index provides a data-driven signal for identifying evidence bases most likely to shift, offering a tool for evidence surveillance and guideline update prioritization.

---

## Tables

### Table 1. Summary statistics of evidence dynamics across 501 Cochrane systematic reviews

| Metric | N | Mean (SD) | Median (IQR) |
|--------|---|-----------|---------------|
| **Evidence velocity** | | | |
| Studies per year | 3,651 | 1.50 (2.20) | 0.82 (0.50-1.52) |
| Time span (years) | 3,651 | 17.9 (11.3) | 16.0 (10.0-24.0) |
| Number of studies (k) | 3,651 | 20.0 (33.3) | 11.0 (7-20) |
| **Effect decay** | | | |
| Decay ratio^a^ | 2,817 | 1.17 (1.54) | 0.66 (0.32-1.23) |
| Trajectory CV | 3,062 | 2.19 (13.2) | 0.50 (0.25-1.14) |
| Sign reversal rate | 3,062 | 25.1% | -- |
| Meaningful reversal rate^b^ | 3,062 | 3.4% | -- |
| **Future-proof index** | | | |
| FPI score (0-100) | 3,062 | 63.3 (14.1) | 64.4 (54.0-72.5) |

^a^ Excluding 245 analyses with extreme decay ratios (> 10) arising from near-zero early effects. ^b^ Both early and final |log OR| > 0.2.

### Table 2. Cross-tabulation of MAFI publication bias class and FPI stability class

| MAFI Class | Stable | Moderate | Volatile | High Risk | Total |
|------------|--------|----------|----------|-----------|-------|
| Robust | 728 | 553 | 91 | 1 | 1,373 |
| Low Fragility | 231 | 607 | 226 | 15 | 1,079 |
| Moderate Fragility | 8 | 221 | 125 | 15 | 369 |
| High Fragility | 0 | 28 | 24 | 1 | 53 |
| *Unmatched* | 31 | 91 | 58 | 8 | 188 |
| **Total** | **998** | **1,500** | **524** | **40** | **3,062** |

### Table 3. FPI component contributions

| Component | Weight | Mean (SD) | Median (IQR) |
|-----------|--------|-----------|---------------|
| Sample size adequacy | 0.30 | 0.50 (0.28) | 0.39 (0.26-0.74) |
| Bias risk (1-MAFI) | 0.25 | 0.81 (0.15) | 0.83 (0.74-0.94) |
| Trajectory stability | 0.25 | 0.62 (0.33) | 0.75 (0.43-0.87) |
| Decay magnitude | 0.20 | 0.62 (0.29) | 0.67 (0.52-0.83) |

---

## Figures

**Fig 1.** Distribution of Future-Proof Index (FPI) scores across 3,062 Cochrane meta-analyses. Vertical dashed lines indicate classification thresholds: Stable (>= 70), Moderate (50-69), Volatile (30-49), High Risk (< 30).

**Fig 2.** Scatter plot of evidence velocity (studies per year) versus effect decay ratio for 2,650 analyses with complete data. The negligible Pearson correlation (r = -0.002, p = 0.91) indicates that evidence accumulation rate and effect attenuation are largely uncorrelated.

**Fig 3.** Cross-tabulation heatmap of MAFI publication bias class versus FPI stability class. Cell intensity represents the count of analyses in each combination. Low publication bias (Robust) is necessary but not sufficient for evidence stability.

---

## Supporting information

**S1 Table.** Full velocity statistics for all 3,651 analysis trajectories. (CSV)

**S2 Table.** Full decay statistics for all 3,062 analysis trajectories. (CSV)

**S3 Table.** Integrated dataset with FPI scores and all component values for 3,062 analyses. (CSV)

**S4 Table.** FPI sensitivity analysis: class distributions under alternative component weight schemes. (CSV)

**S5 Table.** Summary statistics in machine-readable format. (JSON)

**S1 Fig.** Histogram of evidence velocity (studies per year) with log-scaled x-axis showing the right-skewed distribution.

**S2 Fig.** Histogram of decay ratios showing the predominance of values below 1.0 (effect shrinkage).

**S3 Fig.** FPI score distributions stratified by statistical significance of the pooled result.

---

## Acknowledgments

The author thanks the Cochrane Collaboration for maintaining the systematic review infrastructure from which the Pairwise70 dataset is derived, and the developers of the open-source tools used in this analysis (NumPy, SciPy, pandas, pyreadr, matplotlib).

## Author contributions

**Conceptualization:** Mahmood Ul Hassan. **Data curation:** Mahmood Ul Hassan. **Formal analysis:** Mahmood Ul Hassan. **Investigation:** Mahmood Ul Hassan. **Methodology:** Mahmood Ul Hassan. **Software:** Mahmood Ul Hassan. **Validation:** Mahmood Ul Hassan. **Visualization:** Mahmood Ul Hassan. **Writing - original draft:** Mahmood Ul Hassan. **Writing - review & editing:** Mahmood Ul Hassan.

## Funding

The author(s) received no specific funding for this work.

## Competing interests

The author has declared that no competing interests exist.

## Data availability

All analysis scripts, intermediate data files, and the complete computational pipeline are available at [ZENODO_DOI_PLACEHOLDER]. The Pairwise70 benchmark dataset is derived from publicly available Cochrane systematic reviews [10]. The MAFI package is available as described in [9].

## Ethics statement

This study analyzed aggregate published data from Cochrane systematic reviews. No individual participant data were accessed. No ethical approval was required.

---

## References

1. Higgins JPT, Thomas J, Chandler J, Cumpston M, Li T, Page MJ, et al., editors. Cochrane Handbook for Systematic Reviews of Interventions version 6.4. Cochrane; 2023. Available from: https://training.cochrane.org/handbook.

2. Elliott JH, Synnot A, Turner T, Simmonds M, Akl EA, McDonald S, et al. Living systematic review: 1. Introduction-the why, what, when, and how. J Clin Epidemiol. 2017;91:23-30. https://doi.org/10.1016/j.jclinepi.2017.08.010

3. Ioannidis JPA, Trikalinos TA. Early extreme contradictory estimates may appear in published research: the Proteus phenomenon in molecular genetics research and randomized trials. J Clin Epidemiol. 2005;58(6):543-549. https://doi.org/10.1016/j.jclinepi.2004.10.019

4. Lau J, Antman EM, Jimenez-Silva J, Kupelnick B, Mosteller F, Chalmers TC. Cumulative meta-analysis of therapeutic trials for myocardial infarction. N Engl J Med. 1992;327(4):248-254. https://doi.org/10.1056/NEJM199207233270406

5. Sterne JAC, Sutton AJ, Ioannidis JPA, Terrin N, Jones DR, Lau J, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. BMJ. 2011;343:d4002. https://doi.org/10.1136/bmj.d4002

6. Rothstein HR, Sutton AJ, Borenstein M. Publication Bias in Meta-Analysis: Prevention, Assessment and Adjustments. Chichester: John Wiley & Sons; 2005. ISBN: 978-0-470-87014-3.

7. Wetterslev J, Thorlund K, Brok J, Gluud C. Trial sequential analysis may establish when firm evidence is reached in cumulative meta-analysis. J Clin Epidemiol. 2008;61(1):64-75. https://doi.org/10.1016/j.jclinepi.2007.03.013

8. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. Stat Med. 2002;21(11):1539-1558. https://doi.org/10.1002/sim.1186

9. Hassan MU. MAFI: A Multi-Signal Aggregate Funnel Index for publication bias detection in meta-analysis. [In preparation]. [MAFI_DOI_PLACEHOLDER]

10. Hassan MU. Pairwise70: Study-level data from 501 Cochrane systematic reviews of interventions. R data package, version 2.0.0. [ZENODO_DOI_PLACEHOLDER]

11. Sweeting MJ, Sutton AJ, Lambert PC. What to add to nothing? Use and avoidance of continuity corrections in meta-analysis of sparse data. Stat Med. 2004;23(9):1351-1375. https://doi.org/10.1002/sim.1761

12. Harris CR, Millman KJ, van der Walt SJ, Gommers R, Virtanen P, Cournapeau D, et al. Array programming with NumPy. Nature. 2020;585(7825):357-362. https://doi.org/10.1038/s41586-020-2649-2

13. Virtanen P, Gommers R, Oliphant TE, Haberland M, Reddy T, Cournapeau D, et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. Nat Methods. 2020;17(3):261-272. https://doi.org/10.1038/s41592-019-0686-2

14. Pereira TV, Ioannidis JPA. Statistically significant meta-analyses of clinical trials have modest credibility and inflated effects. J Clin Epidemiol. 2011;64(10):1060-1069. https://doi.org/10.1016/j.jclinepi.2010.12.012

15. Ioannidis JPA. Why most published research findings are false. PLoS Med. 2005;2(8):e124. https://doi.org/10.1371/journal.pmed.0020124

16. Thorlund K, Engstrom J, Wetterslev J, Brok J, Imberger G, Gluud C. User manual for Trial Sequential Analysis (TSA). Copenhagen Trial Unit, Centre for Clinical Intervention Research; 2011. p. 1-115. Available from: https://ctu.dk/tsa/.

17. Garner P, Hopewell S, Chandler J, MacLehose H, Schunemann HJ, Akl EA, et al. When and how to update systematic reviews: consensus and checklist. BMJ. 2016;354:i3507. https://doi.org/10.1136/bmj.i3507
