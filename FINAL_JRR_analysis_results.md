# FINAL JRR Analysis Results

Single source of truth for the Journal of Risk Research manuscript, Methods/Results drafting, and Online Supplement planning. This document integrates the completed SSCI reanalysis and audit outputs. No new exploratory analysis is introduced here; numerical values are taken from verified output files in `result/ssci_reanalysis/` and prior retained result files where explicitly noted.

## 1. Study and Analysis Overview

The study examines public acceptance of personal-data use in disaster governance under a hybrid-governance/post-regulation institutional context. The final empirical story does not treat `legitimacy` as a directly measured dependent variable. The measured outcome is policy/data-use acceptance.

- General-public/citizen sample: N = 1,094.
- Disaster-management practitioner sample: N = 246.
- Core analysis sample: citizen sample, N = 1,094, after valid construction of core variables.
- Data structure: cross-sectional survey data. All mediation and moderated-mediation language must be associational rather than causal.
- Core variables: Management Trust, Risk Perception, Institutional Trust, Safety Management Perception, Policy/Data-use Acceptance.

Primary empirical question:

> The primary empirical question is whether the association between management trust and public acceptance of personal-data use becomes stronger as perceived risk increases.

Secondary empirical framing:

> Institutional trust is examined as an intervening mechanism, and information-type heterogeneity is examined as secondary evidence regarding whether the trust-consent association is uniform across different categories of personal information.

Numerical conflict note: older files such as `result/regression_with_controls.txt` used a different demographic-control coding (`female`, `age`, education dummies, income). The final verified audit models use `sq1`, `C(sq2)`, and `sq3_1` as demographic controls. Therefore, final manuscript numbers should follow the `result/ssci_reanalysis/` audit outputs unless a supplement explicitly reproduces the older control coding.

## 2. Variable and Measurement Summary
| Construct | Operationalization | Number of items | Scale | Reliability | Final analytical role | Measurement caveat |
| --- | --- | --- | --- | --- | --- | --- |
| Policy/Data-use Acceptance | Mean of q7_1, q8_1, q9_1 | 3 | 1-5; higher = greater acceptance | alpha = 0.8758; CR = 0.923884; AVE = 0.801823 | Primary dependent variable | 3-indicator single-factor model is just-identified; do not use global CFA fit as evidence. |
| Management Trust | Mean of q5_1 and q6_1 | 2 | 1-5; higher = greater trust in necessity/effectiveness of data use | alpha = 0.8336; CR = 0.923336; AVE = 0.857589 | Primary independent variable | Two-item measure; report reliability but do not overstate latent measurement depth. |
| Risk Perception | Mean of q21_1 and q22_1 | 2 | 1-5; higher = greater perceived leakage/misuse risk | alpha = 0.8329; CR = 0.923735; AVE = 0.858279 | Primary moderator; also included as predictor | Risk main association is specification-sensitive when institutional trust is added, but Trust x Risk is robust. |
| Institutional Trust | q26_1 | 1 | 1-5; higher = greater institutional trust | Single item; reliability not directly estimable | Intervening variable | Use measurement-error sensitivity only; do not call it latent SEM validation. |
| Safety Management Perception | q25 recoded to safe_management: 1 = safely managed, 0 = not safely managed | 1 | Binary positive-direction variable | Single binary item | Auxiliary predictor/control | Do not compare its coefficient magnitude directly with Management Trust because scale/measurement differ. |

Policy Acceptance loadings from the verified measurement audit:
| Item | Standardized loading/PCA one-factor score | Communality |
| --- | --- | --- |
| q7_1 | 0.890594 | 0.793158 |
| q8_1 | 0.895447 | 0.801826 |
| q9_1 | 0.90027 | 0.810486 |

## 3. Main Association Model

Final model: OLS with HC3 robust standard errors. Dependent variable: Policy/Data-use Acceptance. Predictors: Management Trust, Risk Perception, Safety Management Perception, and demographic controls (`sq1`, `C(sq2)`, `sq3_1`). Verified source: `main_ols_hc3.csv`; R2 source: `audit_interaction_effect_size.csv` baseline model.

| Predictor | b | HC3 SE | 95% CI | p | Interpretation |
| --- | --- | --- | --- | --- | --- |
| manage_trust | 0.714486 | 0.028427 | [0.658709, 0.770263] | 2.84599e-110 | Positive association with policy/data-use acceptance. |
| risk | -0.063207 | 0.022844 | [-0.108031, -0.018383] | 0.005756 | Negative association in the primary composite-score specification. |
| safe_management | 0.192968 | 0.035385 | [0.123537, 0.262399] | 6.11626e-08 | Positive association with policy/data-use acceptance. |
| sq1 | 0.001623 | 0.003431 | [-0.005108, 0.008355] | 0.636209 | Residence control; not statistically distinguishable from zero in exported HC3 table. |
| sq3_1 | -0.002353 | 0.001459 | [-0.005216, 0.000511] | 0.107212 | Age control; not statistically distinguishable from zero in exported HC3 table. |
| C(sq2) | included | not exported | not exported | not exported | Sex categorical control included in verified formula; dummy coefficients were not exported in final CSV. |

Model N = 1,094. Baseline R2 = 0.507893. Adjusted R2 was not exported in the final audit CSV; do not import adjusted R2 from older control-coding outputs as the final value.

## 4. Institutional-Trust Mediation

Specified association structure: `Management Trust -> Institutional Trust -> Policy/Data-use Acceptance`. This is an indirect association consistent with the theoretically specified mediation structure, not causal mediation.

| Path/effect | Estimate | SE | Bootstrap 95% CI | p |
| --- | --- | --- | --- | --- |
| a: Management trust -> Institutional trust | 0.274684 | not exported | [0.213893, 0.336236] | not exported |
| b: Institutional trust -> Policy acceptance | 0.144035 | not exported | [0.087774, 0.199679] | not exported |
| direct | 0.674922 | not exported | [0.617236, 0.733857] | not exported |
| indirect | 0.039564 | not exported | [0.023096, 0.057651] | not exported |
| total | 0.714486 | not exported | [0.659236, 0.768735] | not exported |

Bootstrap details: 5,000 resamples; seed = 20260825 in the final reanalysis script; controls = risk, safe_management, sq1, C(sq2), sq3_1. Centering is not required for the simple indirect-association model.

## 5. Core Moderation: Management Trust x Risk Perception

This is the core manuscript result. Final moderation model: mean-centered Management Trust, mean-centered Risk Perception, their interaction, Safety Management Perception, and demographic controls (`sq1`, `C(sq2)`, `sq3_1`), with HC3 robust SE.

| Term | b | HC3 SE | 95% CI | p |
| --- | --- | --- | --- | --- |
| manage_c | 0.711055 | 0.028761 | [0.654685, 0.767425] | 6.04335e-135 |
| risk_c | -0.065036 | 0.022855 | [-0.109832, -0.02024] | 0.004434 |
| manage_c:risk_c | 0.081083 | 0.030758 | [0.020798, 0.141368] | 0.008385 |
| safe_management | 0.192609 | 0.035494 | [0.123041, 0.262176] | 5.74843e-08 |

| Model quantity | Value |
| --- | --- |
| Baseline R2 | 0.507893 |
| Interaction model R2 | 0.511989 |
| Delta R2 | 0.004096 |
| Cohen's f2 for interaction | 0.008393 |

The interaction was statistically robust but modest in incremental explanatory power.

## 6. Simple Slopes
| Risk level | Management-trust slope | SE | 95% CI | p |
| --- | --- | --- | --- | --- |
| -1 SD | 0.647437 | 0.038373 | [0.572226, 0.722647] | 0.0 in output; numerical underflow |
| Mean | 0.711055 | 0.028761 | [0.654684, 0.767426] | 0.0 in output; numerical underflow |
| +1 SD | 0.774674 | 0.036698 | [0.702746, 0.846601] | 0.0 in output; numerical underflow |

Conclusion: The positive association between management trust and policy/data-use acceptance became stronger as perceived risk increased. Do not imply that the interaction has a large effect size; report Delta R2 and f2 alongside the slopes.

## 7. Core Interaction Robustness Audit
| Specification | Trust x Risk | SE | 95% CI | p | Conclusion |
| --- | --- | --- | --- | --- | --- |
| A_no_controls_HC3 | 0.082109 | 0.030876 | [0.021593, 0.142625] | 0.00783 | positive, CI excludes zero |
| B_demographic_controls_HC3 | 0.081083 | 0.030758 | [0.020798, 0.141368] | 0.008385 | positive, CI excludes zero |
| C_z_standardized_trust_risk_HC3 | 0.058815 | 0.022311 | [0.015086, 0.102544] | 0.008385 | positive, CI excludes zero |
| D_policy_factor_score_HC3 | 0.105545 | 0.040183 | [0.026787, 0.184302] | 0.008625 | positive, CI excludes zero |

Final robustness judgment: ROBUST. The Trust x Risk interaction retained the same positive direction and remained statistically significant across all prespecified alternative specifications.

## 8. Moderated Mediation

Final structure: PROCESS Model 7-like association structure. Risk Perception moderates the `Management Trust -> Institutional Trust` path; Institutional Trust is then associated with Policy/Data-use Acceptance. This is similar to PROCESS Model 7, but implemented directly through OLS path models and bootstrap resampling in Python rather than through the PROCESS macro. Interpret as conditional indirect association, not causal moderated mediation.

| Risk level | Conditional indirect association | Bootstrap 95% CI |
| --- | --- | --- |
| -1 SD | 0.029382 | [0.015369, 0.046659] |
| Mean | 0.039043 | [0.022787, 0.056634] |
| +1 SD | 0.048704 | [0.027734, 0.072043] |

Index of Moderated Mediation: estimate = 0.012313, bootstrap 95% CI = [0.002092, 0.024693].

Final interpretation: The indirect association through institutional trust became stronger as perceived risk increased. Do not describe this as causal moderated mediation.

## 9. Policy-Acceptance Measurement Robustness

Policy Acceptance CR = 0.923884; AVE = 0.801823. The 3-indicator single-factor model is just-identified; do not use CFI, RMSEA, SRMR, or similar global fit language as evidence of excellent fit.

| Scoring | Adjustment | Term | b | SE | 95% CI | p |
| --- | --- | --- | --- | --- | --- | --- |
| raw_mean_composite | without_institutional_trust | manage_trust | 0.714486 | 0.028427 | [0.658771, 0.770201] | 2.0899e-139 |
| raw_mean_composite | without_institutional_trust | risk | -0.063207 | 0.022844 | [-0.107981, -0.018433] | 0.00566 |
| raw_mean_composite | without_institutional_trust | safe_management | 0.192968 | 0.035385 | [0.123614, 0.262321] | 4.94245e-08 |
| raw_mean_composite | with_institutional_trust | manage_trust | 0.674922 | 0.030259 | [0.615615, 0.734228] | 3.31179e-110 |
| raw_mean_composite | with_institutional_trust | risk | -0.037757 | 0.022517 | [-0.08189, 0.006376] | 0.093577 |
| raw_mean_composite | with_institutional_trust | safe_management | 0.080282 | 0.037923 | [0.005954, 0.15461] | 0.034262 |
| raw_mean_composite | with_institutional_trust | trust | 0.144035 | 0.028494 | [0.088187, 0.199882] | 4.30611e-07 |
| z_mean_composite | without_institutional_trust | manage_trust | 0.93175 | 0.037071 | [0.859093, 1.004407] | 2.0899e-139 |
| z_mean_composite | without_institutional_trust | risk | -0.082428 | 0.029791 | [-0.140817, -0.024038] | 0.00566 |
| z_mean_composite | without_institutional_trust | safe_management | 0.251647 | 0.046145 | [0.161204, 0.342089] | 4.94245e-08 |
| z_mean_composite | with_institutional_trust | manage_trust | 0.880155 | 0.03946 | [0.802815, 0.957496] | 3.31179e-110 |
| z_mean_composite | with_institutional_trust | risk | -0.049239 | 0.029364 | [-0.106792, 0.008314] | 0.093577 |
| z_mean_composite | with_institutional_trust | safe_management | 0.104694 | 0.049455 | [0.007765, 0.201624] | 0.034262 |
| z_mean_composite | with_institutional_trust | trust | 0.187834 | 0.037159 | [0.115004, 0.260663] | 4.30611e-07 |
| factor_score | without_institutional_trust | manage_trust | 0.933733 | 0.037078 | [0.861061, 1.006405] | 6.1863e-140 |
| factor_score | without_institutional_trust | risk | -0.081865 | 0.029801 | [-0.140274, -0.023456] | 0.006013 |
| factor_score | without_institutional_trust | safe_management | 0.251359 | 0.046051 | [0.161102, 0.341617] | 4.8065e-08 |
| factor_score | with_institutional_trust | manage_trust | 0.882048 | 0.039451 | [0.804726, 0.959371] | 1.00694e-110 |
| factor_score | with_institutional_trust | risk | -0.048619 | 0.029373 | [-0.106188, 0.008951] | 0.097878 |
| factor_score | with_institutional_trust | safe_management | 0.104152 | 0.049326 | [0.007475, 0.200828] | 0.034728 |
| factor_score | with_institutional_trust | trust | 0.18816 | 0.037121 | [0.115404, 0.260916] | 4.00316e-07 |

Final measurement-robustness judgment: Risk main association is SPECIFICATION-SENSITIVE when Institutional Trust is added. Risk is negative and statistically distinguishable from zero in the primary composite model without Institutional Trust and in the factor-score model without Institutional Trust, but becomes weaker after Institutional Trust is included. The theoretically central Trust x Risk interaction remains robust under factor-score DV.

Larger measurement screen:
| Factor A | Factor B | Factor-score correlation | Approximate HTMT |
| --- | --- | --- | --- |
| management_trust | risk_perception | -0.058025 | 0.076741 |
| management_trust | policy_acceptance | 0.694007 | 0.812019 |
| policy_acceptance | risk_perception | -0.145978 | 0.170658 |

## 10. Institutional-Trust Measurement-Error Sensitivity

Institutional Trust is single-item. The following is a measurement-error sensitivity analysis under alternative reliability assumptions, not latent SEM validation and not validation of the single-item measure.

| Assumed reliability | a path | b path | Indirect association | 95% CI | Conclusion |
| --- | --- | --- | --- | --- | --- |
| 0.6 | 0.274684 | 0.446746 | 0.122714 | [0.072422, 0.190651] | No conclusion change; CI excludes zero. |
| 0.7 | 0.274684 | 0.292309 | 0.080293 | [0.046509, 0.120348] | No conclusion change; CI excludes zero. |
| 0.8 | 0.274684 | 0.217218 | 0.059666 | [0.034542, 0.087731] | No conclusion change; CI excludes zero. |
| 0.9 | 0.274684 | 0.172822 | 0.047472 | [0.028072, 0.06913] | No conclusion change; CI excludes zero. |
| 0.95 | 0.274684 | 0.156799 | 0.04307 | [0.025034, 0.063365] | No conclusion change; CI excludes zero. |

Across all tested reliability assumptions (.60, .70, .80, .90, .95), the indirect association CI excluded zero. This mitigates, but does not eliminate, the single-item measurement vulnerability.

## 11. Information-Type Heterogeneity

This valid analysis is distinct from the invalid outcome-derived information-sensitivity proxy analysis. Final specification: long-format OLS, `Consent_ij ~ ManagementTrust_i x InformationType_j + Risk_i x InformationType_j + ManagementTrust_i x Risk_i + controls + InformationType FE`, with respondent-level cluster-robust SE.

| Information type | Management-trust slope | Cluster-robust SE | 95% CI | p |
| --- | --- | --- | --- | --- |
| Financial account | 0.17272 | 0.045704 | [0.083141, 0.262299] | 0.000157 |
| Credit information | 0.201748 | 0.047485 | [0.108679, 0.294817] | 2.15052e-05 |
| Habits/preferences | 0.100118 | 0.048753 | [0.004564, 0.195673] | 0.040017 |
| Photograph | 0.261556 | 0.047309 | [0.168833, 0.354279] | 3.22566e-08 |
| Family information | 0.235869 | 0.047193 | [0.143372, 0.328365] | 5.79417e-07 |
| Communication records | 0.286296 | 0.050547 | [0.187225, 0.385366] | 1.47924e-08 |
| Medical information | 0.328176 | 0.050415 | [0.229365, 0.426988] | 7.53896e-11 |
| Affiliation | 0.279724 | 0.046844 | [0.187912, 0.371536] | 2.35161e-09 |
| Home address | 0.377624 | 0.045835 | [0.287788, 0.46746] | 1.74092e-16 |
| Location information | 0.284756 | 0.051137 | [0.184529, 0.384982] | 2.56954e-08 |
| Email address | 0.297848 | 0.047178 | [0.20538, 0.390316] | 2.73286e-10 |
| Phone number | 0.363854 | 0.044687 | [0.276269, 0.451439] | 3.87916e-16 |
| Date of birth | 0.373313 | 0.044336 | [0.286417, 0.460209] | 3.75993e-17 |
| Name | 0.292776 | 0.041804 | [0.210842, 0.37471] | 2.49567e-12 |
| Gender | 0.291147 | 0.041482 | [0.209843, 0.37245] | 2.24081e-12 |

Joint Wald test: statistic = 40.306472, df = 14, p = 0.000229. The positive association between management trust and willingness to provide personal information varied significantly across information types.

All 15 information-type slopes were positive. All 15 were statistically distinguishable from zero at p < .05 in the respondent-clustered fixed-effects model. Random-intercept MixedLM robustness was attempted but not used because estimation failed/singular (`not estimated: Singular matrix`).

## 12. Information-Sensitivity Proxy Audit

The previous `item_sensitivity_proxy` was generated from the same outcome family used in the item-specific consent model:

`item_sensitivity_proxy_j = -mean(consent by information type j)`

| Information type | Original variable | Original coding | Sensitivity calculation | Final centered sensitivity score |
| --- | --- | --- | --- | --- |
| Financial account | q29_8 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.852163 |
| Credit information | q29_9 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.744302 |
| Habits/preferences | q29_15 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.501158 |
| Photograph | q29_10 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.44997 |
| Family information | q29_11 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.361304 |
| Communication records | q29_14 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.353991 |
| Medical information | q29_12 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.066971 |
| Affiliation | q29_7 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | 0.032236 |
| Home address | q29_5 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | -0.007983 |
| Location information | q29_13 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | -0.146923 |
| Email address | q29_6 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | -0.37727 |
| Phone number | q29_3 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | -0.478732 |
| Date of birth | q29_4 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | -0.519866 |
| Name | q29_1 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | -0.837051 |
| Gender | q29_2 | 1-5 consent to government collection of this information type; higher = more consent | item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy | -0.994272 |

FINAL STATUS: INVALID FOR CONFIRMATORY ANALYSIS.

Reason: the predictor is outcome-derived, creating circularity/endogeneity by construction. Therefore, the following should not be used as substantive evidence in the final manuscript:

- `Trust x item_sensitivity_proxy = -0.08676795593230056`, p = 0.005529362088624037 from the previous proxy model.
- `Risk x item_sensitivity_proxy = -0.0886682574812616`, p = 0.0008317816431268972 from the previous proxy model.
- The interpretation that trust becomes weaker as information sensitivity increases.
- The phrase objective information sensitivity for this proxy.

Information-Type Heterogeneity remains usable because it estimates type-specific slopes without converting outcome means into a confirmatory predictor.

## 13. Citizen-Practitioner Comparison

Citizens: N = 1,094. Practitioners: N = 246. The core Management Trust and 3-item Policy/Data-use Acceptance measures are not fully comparable across samples. Therefore: no multigroup SEM, no structural path comparison, and no Group x Trust x Risk analysis should be used as core evidence.

| Comparable descriptive measure | Citizen N | Practitioner N | Citizen mean | Practitioner mean | Difference | Cohen d | Welch p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Comparable item-specific consent mean | 1094 | 246 | 2.785436 | 2.875339 | -0.089903 | -0.123344 | 0.061656 |
| Comparable risk mean | 1094 | 246 | 3.817642 | 3.197154 | 0.620487 | 0.766385 | 2.56782e-20 |
| Agency trust series mean | 1094 | 246 | 3.000653 | 3.325784 | -0.325131 | -0.481201 | 5.77798e-13 |

Final status: Online Supplement descriptive comparison only.

## 14. Other Robustness Analyses
| Analysis | Purpose | Key result | Final status |
| --- | --- | --- | --- |
| Ordered logit | Outcome-scale robustness | manage_trust = 2.5259, p < .001; risk = -0.1684, p = .027; safe_management = 0.6364, p < .001. Source: result/ordered_logit.txt. | Supplement |
| Risk squared | Nonlinearity check | No final verified numeric CSV in ssci_reanalysis outputs. Prior audit classification: Supplement only; do not cite numeric result until final supplement table is rebuilt. | Supplement / hold numeric citation |
| Alternative controls | Control-specification robustness | Core predictors retain direction and statistical distinguishability in no-control, demographic-control, and z-standardized specifications. Source: alternative_specifications.csv. | Supplement |
| Reverse-order specification | Cross-sectional ordering sensitivity | Reverse-order associations can also be estimated from the covariance structure; use only to motivate noncausal language. Source: reverse_order_specifications.csv. | Supplement |
| ANOVA/Tukey | Descriptive/group comparison based on categorized continuous variables | Not part of final main mechanism; risks arbitrary categorization and redundancy. | Remove or Supplement only if needed |
| Residual diagnostics | Diagnostics | Not a main figure/result. Residual histogram and Durbin-Watson should not be emphasized. | Supplement diagnostics only |

## 15. Final Evidence Classification

### A. MAIN TEXT
- Measurement/descriptive assessment
- Main OLS + HC3 association model
- Institutional-trust indirect association
- Management Trust x Risk moderation
- Simple slopes
- Moderated mediation / conditional indirect association
- Information-Type Heterogeneity as type-specific slopes with joint Wald test

### B. ONLINE SUPPLEMENT
- Core interaction robustness specifications
- Policy factor-score/latent-score robustness
- Institutional-trust measurement-error sensitivity
- Ordered logit
- Alternative controls
- Reverse-order specification
- Risk squared/nonlinear specification if numeric supplement table is rebuilt
- Citizen-practitioner descriptive comparison
- Additional information-type slope details and pairwise contrasts
- Additional diagnostics

### C. DO NOT USE / REMOVE
- Outcome-derived Information Sensitivity Proxy: INVALID FOR CONFIRMATORY ANALYSIS
- Direct coefficient-size dominance claims comparing Management Trust with binary Safety Management Perception
- Just-identified 3-item CFA global-fit claims
- Citizen-practitioner structural comparison using non-comparable constructs
- Causal mediation or causal moderated-mediation language

## 16. Final Empirical Claims Allowed
| Claim | Status |
| --- | --- |
| Management trust was positively associated with public acceptance of personal-data use in disaster governance. | SUPPORTED |
| Risk perception was negatively associated with acceptance in the primary composite-score specification, although this main association showed some sensitivity to alternative outcome scoring and institutional-trust adjustment. | PARTIALLY SUPPORTED |
| The positive association between management trust and policy acceptance became stronger as perceived risk increased. | SUPPORTED |
| This Trust x Risk interaction was robust across alternative control, standardization, and outcome-scoring specifications. | SUPPORTED |
| Institutional trust statistically accounted for part of the association between management trust and policy acceptance. | SUPPORTED as an indirect association, not causal mediation |
| The conditional indirect association through institutional trust became stronger at higher levels of perceived risk. | SUPPORTED as conditional indirect association |
| The positive association between management trust and willingness to provide personal information varied significantly across information types. | SUPPORTED |

## 17. Claims NOT Allowed
- Risk causes lower policy acceptance.
- Trust causes policy acceptance.
- Institutional trust causally mediates the relationship.
- Information sensitivity weakens the effect of trust.
- Financial information is objectively more sensitive because its consent rate is lower.
- Management trust is substantively more important than safety management solely because its coefficient is larger.
- The study directly measures governance legitimacy.
- Results establish causal moderated mediation.
- The outcome-derived information-sensitivity proxy is an exogenous or objective sensitivity measure.
- The 3-item Policy Acceptance CFA has excellent global fit based on just-identified fit indices.

## 18. Final Reviewer-Vulnerability Assessment
| Vulnerability | Why it matters | Robustness that helps | Unresolved limitation |
| --- | --- | --- | --- |
| Institutional Trust single-item measurement | Single item cannot estimate internal reliability directly and is vulnerable to measurement error. | Alternative reliability assumptions show the indirect association remains positive with CIs excluding zero. | This does not create a validated multi-item institutional-trust scale. |
| Cross-sectional design | Temporal ordering and causal mediation cannot be established. | Reverse-order specifications are documented and language is restricted to association. | Causal claims remain unavailable. |
| Hybrid governance as context | Hybrid governance/post-regulation is an institutional context rather than a directly measured causal variable. | The empirical story is narrowed to risk-trust mechanisms within this context. | Claims about hybrid governance effects must remain theoretical/contextual. |
| Risk main association specification sensitivity | Risk becomes weaker after Institutional Trust is included and in some scoring/adjusted models. | The central Trust x Risk interaction is robust across specifications. | Risk direct-effect language should be cautious. |
| Information-type differences without exogenous sensitivity scale | Type-specific slopes differ, but the data do not identify why they differ. | Respondent-clustered FE heterogeneity and joint Wald test are valid. | Cannot claim exogenous information sensitivity strengthens or weakens trust associations. |

## 19. Final Statistical Numbers Table
| Result ID | Analysis | Estimate | SE | CI | p | N | Main/Supplement | Verified source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAIN-01 | Main OLS/HC3: manage_trust | 0.714486 | 0.028427 | [0.658709, 0.770263] | 2.84599e-110 | 1094 | Main | main_ols_hc3.csv |
| MAIN-02 | Main OLS/HC3: risk | -0.063207 | 0.022844 | [-0.108031, -0.018383] | 0.005756 | 1094 | Main | main_ols_hc3.csv |
| MAIN-03 | Main OLS/HC3: safe_management | 0.192968 | 0.035385 | [0.123537, 0.262399] | 6.11626e-08 | 1094 | Main | main_ols_hc3.csv |
| MED-01 | Institutional-trust indirect association | 0.039564 | not exported | [0.023096, 0.057651] | not exported | 1094 | Main | mediation_bootstrap.csv |
| MED-02 | Institutional-trust direct association | 0.674922 | not exported | [0.617236, 0.733857] | not exported | 1094 | Main | mediation_bootstrap.csv |
| MED-03 | Institutional-trust total association | 0.714486 | not exported | [0.659236, 0.768735] | not exported | 1094 | Main | mediation_bootstrap.csv |
| MOD-01 | Trust x Risk interaction | 0.081083 | 0.030758 | [0.020798, 0.141368] | 0.008385 | 1094 | Main | moderation_hc3.csv |
| MOD-02 | Simple slope at risk -1SD | 0.647437 | 0.038373 | [0.572226, 0.722647] | 0.0 in output; numerical underflow | 1094 | Main | simple_slopes.csv |
| MOD-03 | Simple slope at risk Mean | 0.711055 | 0.028761 | [0.654684, 0.767426] | 0.0 in output; numerical underflow | 1094 | Main | simple_slopes.csv |
| MOD-04 | Simple slope at risk +1SD | 0.774674 | 0.036698 | [0.702746, 0.846601] | 0.0 in output; numerical underflow | 1094 | Main | simple_slopes.csv |
| MM-01 | Index of moderated mediation | 0.012313 | not exported | [0.002092, 0.024693] | not exported | 1094 | Main | audit_moderated_mediation_reproduction.csv |
| MM-02 | Risk -1SD | 0.029382 | not exported | [0.015369, 0.046659] | not exported | 1094 | Main | audit_moderated_mediation_reproduction.csv |
| MM-03 | Risk mean | 0.039043 | not exported | [0.022787, 0.056634] | not exported | 1094 | Main | audit_moderated_mediation_reproduction.csv |
| MM-04 | Risk +1SD | 0.048704 | not exported | [0.027734, 0.072043] | not exported | 1094 | Main | audit_moderated_mediation_reproduction.csv |
| HET-01 | Information-type heterogeneity joint Wald test | 40.306472 | NA | df = 14 | 0.000229 | 16410 item-responses / 1094 respondents | Main | audit_information_type_joint_test.csv |
| ROB-01 | A_no_controls_HC3 | 0.082109 | 0.030876 | [0.021593, 0.142625] | 0.00783 | 1094 | Supplement | audit_core_interaction_robustness.csv |
| ROB-02 | B_demographic_controls_HC3 | 0.081083 | 0.030758 | [0.020798, 0.141368] | 0.008385 | 1094 | Supplement | audit_core_interaction_robustness.csv |
| ROB-03 | C_z_standardized_trust_risk_HC3 | 0.058815 | 0.022311 | [0.015086, 0.102544] | 0.008385 | 1094 | Supplement | audit_core_interaction_robustness.csv |
| ROB-04 | D_policy_factor_score_HC3 | 0.105545 | 0.040183 | [0.026787, 0.184302] | 0.008625 | 1094 | Supplement | audit_core_interaction_robustness.csv |
| MEAS-01 | Policy Acceptance CR | 0.923884 | NA | NA | NA | 1094 | Main/Supplement | audit_larger_measurement_model_loadings_cr_ave.csv |
| MEAS-02 | Policy Acceptance AVE | 0.801823 | NA | NA | NA | 1094 | Main/Supplement | audit_larger_measurement_model_loadings_cr_ave.csv |
| MEAS-03 | Management Trust alpha | 0.8336 | NA | NA | NA | 1094 | Main/Supplement | result/reliability.txt |
| MEAS-04 | Risk Perception alpha | 0.8329 | NA | NA | NA | 1094 | Main/Supplement | result/reliability.txt |
| MEAS-05 | Policy Acceptance alpha | 0.8758 | NA | NA | NA | 1094 | Main/Supplement | result/reliability.txt |

## 20. Final Quality-Control Checklist
- [x] All N confirmed
- [x] coefficient confirmed
- [x] SE confirmed where exported
- [x] CI confirmed
- [x] p-value confirmed where exported
- [x] bootstrap CI confirmed
- [x] interaction specification confirmed
- [x] moderated-mediation path confirmed
- [x] information-type joint test confirmed
- [x] sensitivity proxy invalidation marked
- [x] causal language removed
- [x] Main/Supplement/Remove classification completed
- [x] conflicting older control-coding values flagged
- [x] no newly invented statistical values added

End of final analysis-results baseline.