# SSCI Reanalysis Audit Report

## 1. Critical issues found
1. `item_sensitivity_proxy` is not independent of the outcome. It was constructed as the negative information-type mean of the same item-specific consent outcome used in the heterogeneity model. Final answer: INVALID FOR CONFIRMATORY ANALYSIS.
2. The core `Management Trust x Risk Perception` result is reproducible across no-control, demographic-control, z-standardized, and factor-score outcome specifications. Final answer: the risk-conditioned trust claim is supported, but the added explanatory power is substantively modest.
3. The 3-item policy-acceptance measurement check supports high internal consistency, but a 3-indicator single-factor model is just-identified; do not claim excellent global CFA fit from that model.
4. Citizen-practitioner structural comparisons should not be used because core management-trust and 3-item policy-acceptance measures are not fully comparable.

## 2. Information-sensitivity proxy audit
The proxy was generated from citizen item-specific consent variables `q29_1` to `q29_15`. Each item is coded 1-5, where higher values indicate stronger consent to government collection of that information type.
Formula used in the previous script:
`item_sensitivity_proxy_j = -mean(consent_ij)`; `item_sensitivity_proxy_c = item_sensitivity_proxy_j - mean(item_sensitivity_proxy_j)`.
There was reverse coding by multiplying the item mean by `-1`, no z-standardization, and mean-centering before interaction modeling.

| Information type | Original variable | Mean consent | Final centered sensitivity score |
|---|---:|---:|---:|
| Financial account | q29_8 | 1.933 | 0.852 |
| Credit information | q29_9 | 2.041 | 0.744 |
| Habits/preferences | q29_15 | 2.284 | 0.501 |
| Photograph | q29_10 | 2.335 | 0.450 |
| Family information | q29_11 | 2.424 | 0.361 |
| Communication records | q29_14 | 2.431 | 0.354 |
| Medical information | q29_12 | 2.718 | 0.067 |
| Affiliation | q29_7 | 2.753 | 0.032 |
| Home address | q29_5 | 2.793 | -0.008 |
| Location information | q29_13 | 2.932 | -0.147 |
| Email address | q29_6 | 3.163 | -0.377 |
| Phone number | q29_3 | 3.264 | -0.479 |
| Date of birth | q29_4 | 3.305 | -0.520 |
| Name | q29_1 | 3.622 | -0.837 |
| Gender | q29_2 | 3.780 | -0.994 |

Circularity judgment: because the predictor is a deterministic transformation of the outcome's information-type means, the sensitivity interaction has outcome-derived predictor bias. It can describe the empirical ordering of item difficulty/consent, but it cannot serve as confirmatory evidence that exogenous information sensitivity moderates trust.
Final verdict: INVALID FOR CONFIRMATORY ANALYSIS. Remove `Information Sensitivity x Management Trust` and `Information Sensitivity x Risk` from main empirical claims.
A label scan of the SAV metadata found respondent-level leakage/misuse/risk items and disaster-type severity items, but no independent 15-category information-type sensitivity, harm, leakage concern, or misuse concern scale corresponding to `q29_1`-`q29_15`. The scan output is saved as `audit_exogenous_sensitivity_item_scan.csv`.

## 3. Core model reproducibility
- Main OLS/HC3 manage_trust: b=0.714, SE=0.028, 95% CI [0.659, 0.770], p=2.846e-110.
- Main OLS/HC3 risk: b=-0.063, SE=0.023, 95% CI [-0.108, -0.018], p=0.005756.
- Main OLS/HC3 safe_management: b=0.193, SE=0.035, 95% CI [0.124, 0.262], p=6.116e-08.
- Indirect-association model a: Management trust -> Institutional trust: estimate=0.275, bootstrap 95% CI [0.214, 0.336].
- Indirect-association model b: Institutional trust -> Policy acceptance: estimate=0.144, bootstrap 95% CI [0.088, 0.200].
- Indirect-association model direct: estimate=0.675, bootstrap 95% CI [0.617, 0.734].
- Indirect-association model indirect: estimate=0.040, bootstrap 95% CI [0.023, 0.058].
- Indirect-association model total: estimate=0.714, bootstrap 95% CI [0.659, 0.769].
- A_no_controls_HC3: Trust x Risk=0.082, SE=0.031, 95% CI [0.022, 0.143], p=0.00783; positive, CI excludes zero.
- B_demographic_controls_HC3: Trust x Risk=0.081, SE=0.031, 95% CI [0.021, 0.141], p=0.008385; positive, CI excludes zero.
- C_z_standardized_trust_risk_HC3: Trust x Risk=0.059, SE=0.022, 95% CI [0.015, 0.103], p=0.008385; positive, CI excludes zero.
- D_policy_factor_score_HC3: Trust x Risk=0.106, SE=0.040, 95% CI [0.027, 0.184], p=0.008625; positive, CI excludes zero.
- Baseline R2=0.5079; interaction-model R2=0.5120; Delta R2=0.0041; Cohen's f2=0.0084.
- Simple slope at -1SD: b=0.647, 95% CI [0.572, 0.723].
- Simple slope at Mean: b=0.711, 95% CI [0.655, 0.767].
- Simple slope at +1SD: b=0.775, 95% CI [0.703, 0.847].
Interpretation: statistically significant but substantively modest interaction. Use restrained language.

## 4. Measurement robustness
Policy Acceptance scoring verdict: Specification-sensitive for the risk path. Risk is robust when institutional trust is not included, but it becomes weaker after institutional trust is added; this is expected because institutional trust is part of the specified indirect pathway.
- raw_mean_composite, without_institutional_trust, manage_trust: b=0.714, 95% CI [0.659, 0.770], p=2.09e-139.
- raw_mean_composite, without_institutional_trust, risk: b=-0.063, 95% CI [-0.108, -0.018], p=0.00566.
- raw_mean_composite, without_institutional_trust, safe_management: b=0.193, 95% CI [0.124, 0.262], p=4.942e-08.
- raw_mean_composite, with_institutional_trust, manage_trust: b=0.675, 95% CI [0.616, 0.734], p=3.312e-110.
- raw_mean_composite, with_institutional_trust, risk: b=-0.038, 95% CI [-0.082, 0.006], p=0.09358.
- raw_mean_composite, with_institutional_trust, safe_management: b=0.080, 95% CI [0.006, 0.155], p=0.03426.
- raw_mean_composite, with_institutional_trust, trust: b=0.144, 95% CI [0.088, 0.200], p=4.306e-07.
- z_mean_composite, without_institutional_trust, manage_trust: b=0.932, 95% CI [0.859, 1.004], p=2.09e-139.
- z_mean_composite, without_institutional_trust, risk: b=-0.082, 95% CI [-0.141, -0.024], p=0.00566.
- z_mean_composite, without_institutional_trust, safe_management: b=0.252, 95% CI [0.161, 0.342], p=4.942e-08.
- z_mean_composite, with_institutional_trust, manage_trust: b=0.880, 95% CI [0.803, 0.957], p=3.312e-110.
- z_mean_composite, with_institutional_trust, risk: b=-0.049, 95% CI [-0.107, 0.008], p=0.09358.
- z_mean_composite, with_institutional_trust, safe_management: b=0.105, 95% CI [0.008, 0.202], p=0.03426.
- z_mean_composite, with_institutional_trust, trust: b=0.188, 95% CI [0.115, 0.261], p=4.306e-07.
- factor_score, without_institutional_trust, manage_trust: b=0.934, 95% CI [0.861, 1.006], p=6.186e-140.
- factor_score, without_institutional_trust, risk: b=-0.082, 95% CI [-0.140, -0.023], p=0.006013.
- factor_score, without_institutional_trust, safe_management: b=0.251, 95% CI [0.161, 0.342], p=4.806e-08.
- factor_score, with_institutional_trust, manage_trust: b=0.882, 95% CI [0.805, 0.959], p=1.007e-110.
- factor_score, with_institutional_trust, risk: b=-0.049, 95% CI [-0.106, 0.009], p=0.09788.
- factor_score, with_institutional_trust, safe_management: b=0.104, 95% CI [0.007, 0.201], p=0.03473.
- factor_score, with_institutional_trust, trust: b=0.188, 95% CI [0.115, 0.261], p=4.003e-07.
The larger measurement audit uses multi-item observed constructs only: management trust, risk perception, and policy acceptance. It reports loadings, CR, AVE, approximate HTMT, and factor-score correlations; it is a measurement robustness screen, not a replacement for full SEM.
- management_trust vs risk_perception: factor-score r=-0.058, approximate HTMT=0.077.
- management_trust vs policy_acceptance: factor-score r=0.694, approximate HTMT=0.812.
- policy_acceptance vs risk_perception: factor-score r=-0.146, approximate HTMT=0.171.
Single-item institutional trust sensitivity should be named `measurement-error sensitivity under alternative reliability assumptions`, not latent SEM validation. The calculation is a covariance-regression correction under assumed reliability values; it is useful as a heuristic sensitivity check, but it is not equivalent to a fully identified latent-variable SEM with a validated multi-item institutional-trust scale.
- Reliability 0.60: indirect=0.123, bootstrap 95% CI [0.072, 0.191].
- Reliability 0.70: indirect=0.080, bootstrap 95% CI [0.047, 0.120].
- Reliability 0.80: indirect=0.060, bootstrap 95% CI [0.035, 0.088].
- Reliability 0.90: indirect=0.047, bootstrap 95% CI [0.028, 0.069].
- Reliability 0.95: indirect=0.043, bootstrap 95% CI [0.025, 0.063].

## 5. Information-type heterogeneity
Final specification: long-format OLS, `Consent_ij ~ ManagementTrust_i x InformationType_j + Risk_i x InformationType_j + ManagementTrust_i x Risk_i + controls + InformationType FE`, with respondent-level cluster-robust SE.
Joint test: Wald statistic=40.306, df=14, p=0.0002285. This tests whether management-trust slopes differ across information types overall.
| Information type | N | Slope | SE cluster | 95% CI | p |
|---|---:|---:|---:|---|---:|
| Financial account | 1094 | 0.173 | 0.046 | [0.083, 0.262] | 0.0001574 |
| Credit information | 1094 | 0.202 | 0.047 | [0.109, 0.295] | 2.151e-05 |
| Habits/preferences | 1094 | 0.100 | 0.049 | [0.005, 0.196] | 0.04002 |
| Photograph | 1094 | 0.262 | 0.047 | [0.169, 0.354] | 3.226e-08 |
| Family information | 1094 | 0.236 | 0.047 | [0.143, 0.328] | 5.794e-07 |
| Communication records | 1094 | 0.286 | 0.051 | [0.187, 0.385] | 1.479e-08 |
| Medical information | 1094 | 0.328 | 0.050 | [0.229, 0.427] | 7.539e-11 |
| Affiliation | 1094 | 0.280 | 0.047 | [0.188, 0.372] | 2.352e-09 |
| Home address | 1094 | 0.378 | 0.046 | [0.288, 0.467] | 1.741e-16 |
| Location information | 1094 | 0.285 | 0.051 | [0.185, 0.385] | 2.57e-08 |
| Email address | 1094 | 0.298 | 0.047 | [0.205, 0.390] | 2.733e-10 |
| Phone number | 1094 | 0.364 | 0.045 | [0.276, 0.451] | 3.879e-16 |
| Date of birth | 1094 | 0.373 | 0.044 | [0.286, 0.460] | 3.76e-17 |
| Name | 1094 | 0.293 | 0.042 | [0.211, 0.375] | 2.496e-12 |
| Gender | 1094 | 0.291 | 0.041 | [0.210, 0.372] | 2.241e-12 |
Use this as information-type heterogeneity only. Do not relabel the pattern as a sensitivity continuum unless an exogenous sensitivity measure is obtained.
Random-intercept MixedLM robustness was attempted but not used because estimation failed or was singular: not estimated: Singular matrix.

## 6. Results that should remain in the main manuscript
- Main citizen-sample OLS/HC3 association model.
- Management Trust -> Institutional Trust -> Policy Acceptance indirect association, with cross-sectional noncausal language.
- Management Trust x Risk Perception moderation, simple slopes, interaction plot, Delta R2, and Cohen's f2.
- Conditional indirect association / moderated mediation if described as PROCESS Model 7-like and noncausal.
- Information-type heterogeneity may remain only if reported as type-specific slopes with the joint test, not as exogenous sensitivity moderation.

## 7. Results that should move to Supplement
- Policy Acceptance factor-score/scoring robustness.
- Measurement-error sensitivity for single-item institutional trust.
- Alternative specifications and reverse-order specifications.
- Citizen-practitioner descriptive comparisons for comparable items only.
- Pairwise information-type slope contrasts, ordered logit, nonlinear risk, diagnostics, ANOVA/Tukey, and descriptive heatmaps.

## 8. Results that should be removed
- Outcome-derived `item_sensitivity_proxy` as a confirmatory Information Sensitivity variable.
- Any claim that the statistically significant sensitivity-proxy interactions validate a theory of exogenous information sensitivity.
- Multigroup citizen-practitioner structural models using non-comparable constructs.
- Direct coefficient-size dominance claims comparing management trust with binary safe-management perception.
- Any global fit claim from a just-identified 3-item Policy Acceptance CFA.

## 9. Remaining reviewer vulnerabilities
- The data are cross-sectional, so mediation and moderated mediation remain associational.
- The key Trust x Risk interaction is statistically reliable but small in incremental explanatory power.
- Institutional trust is single-item; sensitivity analysis helps but does not create a true multi-item latent measure.
- No independent information-type sensitivity scale was found in the current data. Item-specific heterogeneity is useful, but it cannot answer whether exogenous sensitivity strengthens trust effects.
- The Trust x Risk interaction is stable across scoring specifications, but the direct risk coefficient weakens once institutional trust is included; risk-related direct-effect claims should therefore be written cautiously.

## 10. Final assessment
The empirical core is usable for a Journal of Risk Research submission if the manuscript narrows its claim: management trust is positively associated with policy/data-use acceptance, institutional trust carries a small but robust indirect association, and the management-trust association is stronger under higher perceived risk. The strongest version of the paper should not claim that externally measured information sensitivity intensifies trust effects, because the previous sensitivity proxy was outcome-derived. The defensible heterogeneity claim is narrower: management-trust associations vary across information types, and the variation is statistically detectable in a respondent-clustered fixed-effects model.

Moderated mediation reproduction details: structure is PROCESS Model 7-like, with Risk Perception moderating the Management Trust -> Institutional Trust path; bootstrap N=5,000; seed=20260825; Management Trust and Risk are mean-centered; controls are age, sex, education, and safe-management perception. Interpret as conditional indirect association, not causal moderated mediation.
- Risk -1SD: estimate=0.029, bootstrap 95% CI [0.015, 0.047].
- Risk mean: estimate=0.039, bootstrap 95% CI [0.023, 0.057].
- Risk +1SD: estimate=0.049, bootstrap 95% CI [0.028, 0.072].
- Index of moderated mediation: estimate=0.012, bootstrap 95% CI [0.002, 0.025].

Reverse-order specifications remain compatible with cross-sectional covariance and should be used only to motivate cautious causal language.
- Reverse-order check estimated: management_trust_as_outcome.
- Reverse-order check estimated: institutional_trust_as_outcome.
- Reverse-order check estimated: management_trust_from_policy_and_risk.