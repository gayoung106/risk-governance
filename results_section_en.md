# Results

## 4. Overview of Results

This section interprets the results using `safe_management`, the positively oriented recoding of q25 described in §3.2.

**[Table 4] Summary of Main Regression Results (N=1,094)**

| Variable | Model 1 baseline OLS | Model 2 with controls | Model 3 HC3 |
|---|:---:|:---:|:---:|
| management trust (`manage_trust`) | 0.712*** (.024) | 0.714*** (.028) | 0.714*** (.028) |
| risk perception (`risk`) | -0.059* (.023) | -0.063** (.023) | -0.063** (.023) |
| positive perception of safe management (`safe_management`) | 0.192*** (.037) | 0.193*** (.035) | 0.193*** (.035) |
| Region of residence (`sq1`) | - | 0.002 (.003) | 0.002 (.003) |
| Gender (`sq2`, 1=female, reference=male) | - | 0.075* (.033) | 0.075* (.033) |
| Age (`sq3_1`) | - | -0.002 (.001) | -0.002 (.001) |
| R² | .504 | .508 | - |
| ΔR² | - | .004 | - |

Note: Standard errors are in parentheses. *p<.05, **p<.01, ***p<.001. `safe_management` is the positively oriented recoding of q25. The control variables in Models 2 and 3 are region of residence (`sq1`), gender (`sq2`), and age (`sq3_1`).

## 4.1 Positive perception of safe management and policy acceptance

Respondents who perceived their personal information as being managed safely had higher policy acceptance than those who did not (Table 4). The coefficient for `safe_management` was significant in both the baseline and controlled models (p<.001), and the direction and significance were retained after applying HC3 robust standard errors.

Because `manage_trust` is a continuous scale and `safe_management` is a binary dummy, the two unstandardized coefficients should not be interpreted as a direct ranking of explanatory power.

## 4.2 Positive association of management trust

Management trust showed a comparatively strong positive unstandardized association with policy acceptance (b=0.714, HC3 SE=0.028, 95% CI [0.659, 0.770], p<.001; Table 4). The association remained significant in both the baseline and controlled models.

**H1 supported:** Management trust is significantly and positively associated with policy acceptance, and the observed association is comparatively strong when evaluated using the unstandardized coefficient.

## 4.3 Negative association of risk perception

Risk perception was negatively associated with policy acceptance. In the controlled model, the coefficient for risk perception was `b=-0.063, p<.01` (Table 4), and the association remained significant after applying HC3 robust standard errors. The effect size is smaller than that for management trust.

**H2 supported:** Risk perception has a significant negative association with policy acceptance.

## 4.4 Exploratory indirect association through institutional trust

The bootstrap-based supplementary analysis showed a significant indirect association pattern in which management trust was linked to policy acceptance through institutional trust. Because the analysis is based on cross-sectional data, this result is interpreted as a statistical indirect association rather than a causal mediation mechanism.

**[Table 5] Summary of bootstrap indirect associations**

| Path/effect | Estimate | 95% CI |
|---|:---:|:---:|
| a: management trust -> institutional trust | 0.2747 | [0.2139, 0.3362] |
| b: institutional trust -> policy acceptance | 0.1440 | [0.0878, 0.1997] |
| Indirect association (management trust -> institutional trust -> policy acceptance) | 0.0396 | [0.0231, 0.0577] |
| Direct effect (management trust) | 0.6749 | [0.6172, 0.7339] |
| Total effect (management trust) | 0.7145 | [0.6592, 0.7687] |

**H3 exploratorily supported:** Institutional trust showed a significant indirect association pattern between management trust and policy acceptance. This result suggests that the positive association between management trust and policy acceptance co-occurs with diffuse trust in government agencies responsible for disaster response.

## 4.5 Conditional association under risk conditions

In the final model with control variables, the interaction term between mean-centered management trust and mean-centered risk perception was significantly and positively associated with policy acceptance (b=0.0811, HC3 SE=0.0308, 95% CI [0.0208, 0.1414], p=.0084). The increase in explained variance from adding the interaction was ΔR²=0.0041, from R²=.5079 in the baseline model to R²=.5120 in the interaction model, with Cohen's f²=0.0084. Thus, the interaction is statistically significant, although its incremental explanatory power is small. Simple-slope analysis showed that the management trust-policy acceptance slope was b=0.6474 (95% CI [0.5722, 0.7226]) when risk perception was −1SD, b=0.7111 (95% CI [0.6547, 0.7674]) at the mean, and b=0.7747 (95% CI [0.7027, 0.8466]) when risk perception was +1SD.

The direction and significance of this interaction were retained across alternative specifications, including models with and without controls, standardized variables, and a factor-score-based dependent variable. Because the incremental explanatory power (ΔR², f²) is small, the interaction is reported as statistically significant but substantively modest.

**H4 supported:** Under higher risk perception, the positive slope between management trust and policy acceptance was significantly stronger, and this result was robust across several alternative model specifications. The incremental explanatory power, however, was small.

## 4.5b Conditional indirect association (moderated mediation)

To examine whether the indirect association management trust -> institutional trust -> policy acceptance varied by the level of risk perception, a bootstrapped conditional indirect association with 5,000 resamples was estimated in which risk perception moderates the management trust-institutional trust path, or the first stage. The conditional indirect association was 0.0294 (95% CI [0.0154, 0.0467]) when risk perception was −1SD, 0.0390 (95% CI [0.0228, 0.0566]) at the mean, and 0.0487 (95% CI [0.0277, 0.0720]) when risk perception was +1SD. The Index of Moderated Mediation was 0.0123 (95% CI [0.0021, 0.0247]), and the interval did not include 0. This indicates a conditional pattern in which the indirect association through institutional trust becomes stronger as risk perception increases. This finding is interpreted as a conditional indirect association rather than as a causal moderated mediation effect.

## 4.5c Information-type heterogeneity

To examine whether the management trust-policy acceptance association was uniform across types of personal information, the agreement items for 15 information types were reconstructed in long format, and a model with information-type fixed effects and respondent-level cluster-robust standard errors was estimated. The Wald test of the joint hypothesis that all information-type-specific management trust slopes are equal was statistically significant (χ²=40.31, df=14, p<.001). Across all 15 information types, the management trust slopes were positive and statistically significant (p<.05), ranging from relatively lower values for name (0.293) and gender (0.291) to relatively higher values for address (0.378), date of birth (0.373), and telephone number (0.364). This provides evidence of heterogeneity showing that the positive association between management trust and policy acceptance differs significantly by information type. It should not be interpreted as a measure of the exogenous sensitivity of the information.

## 4.6 Robustness Checks

The core directions of the results were maintained when HC3 robust standard errors were applied and when the inclusion of control variables was varied. Ordered logit models are presented as robustness checks that account for the possible ordinal interpretation of the dependent variable and are used to verify whether the directions of the key coefficients are consistent with those from OLS.

The VIFs for the key predictors were approximately 1.08 for management trust, 1.20 for risk perception, and 1.26 for positive perception of safe management, which are low by conventional standards. Some control-variable dummies may show high VIFs, but these are not interpreted as indicating multicollinearity among the key predictors.

## 4.7 Integrated Summary of Results

The results are summarized in five points. First, positive perception of safe management is positively associated with policy acceptance. Second, management trust shows a comparatively strong positive unstandardized association with policy acceptance. Third, risk perception is negatively associated with policy acceptance, although this direct association shows some specification sensitivity when institutional trust is added to the model. Fourth, the interaction between management trust and risk perception is statistically significant and robust across several alternative specifications, but its incremental explanatory power is small; the corresponding conditional indirect association through institutional trust also becomes stronger at higher levels of risk. Fifth, the management trust-policy acceptance association differs significantly by information type.
