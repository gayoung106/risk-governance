# SSCI Reanalysis Report

Core question: Does trust matter more when perceived privacy risk is high?

## Step 1. Data and construct audit
- Citizen sample: N=1094; practitioner sample: N=246.
- Citizen core variables are available as policy acceptance, management trust, risk perception, institutional trust, and safe-management perception.
- Citizen-practitioner structural comparison is not recommended for the main trust mechanism because management trust and the 3-item policy-acceptance outcome are not fully comparable.
- Comparable citizen-practitioner analyses should be limited to item-specific information consent, leakage/misuse risk, and agency trust descriptives.
Recommended location: Main text for citizen construct audit; Supplement for citizen-practitioner comparability details.

## Step 2. Main OLS and HC3 association model
- manage_trust: b=0.714, HC3 SE=0.028, 95% CI [0.659, 0.770], p=0.0000***
- risk: b=-0.063, HC3 SE=0.023, 95% CI [-0.108, -0.018], p=0.0058**
- safe_management: b=0.193, HC3 SE=0.035, 95% CI [0.124, 0.262], p=0.0000***
Recommended location: Main text 4.2.

## Step 3. Institutional-trust mediation
- a: Management trust -> Institutional trust: estimate=0.275, bootstrap 95% CI [0.214, 0.336]
- b: Institutional trust -> Policy acceptance: estimate=0.144, bootstrap 95% CI [0.088, 0.200]
- direct: estimate=0.675, bootstrap 95% CI [0.617, 0.734]
- indirect: estimate=0.040, bootstrap 95% CI [0.023, 0.058]
- total: estimate=0.714, bootstrap 95% CI [0.659, 0.769]
Recommended location: Main text 4.3. Interpret as an indirect association, not causal mediation.

## Step 4. Risk moderation
- manage_c: b=0.711, HC3 SE=0.029, 95% CI [0.655, 0.767], p=0.0000***
- risk_c: b=-0.065, HC3 SE=0.023, 95% CI [-0.110, -0.020], p=0.0044**
- manage_c:risk_c: b=0.081, HC3 SE=0.031, 95% CI [0.021, 0.141], p=0.0084**
- Incremental R-squared for interaction: 0.0041.
- Simple slope at risk -1SD: b=0.647, 95% CI [0.572, 0.723], p=0.0000***
- Simple slope at risk Mean: b=0.711, 95% CI [0.655, 0.767], p=0.0000***
- Simple slope at risk +1SD: b=0.775, 95% CI [0.703, 0.847], p=0.0000***
Recommended location: Main text 4.4 with interaction_plot.png.

## Step 5. Integrated moderated mediation
- -1SD: estimate=0.029, bootstrap 95% CI [0.015, 0.046]
- Mean: estimate=0.039, bootstrap 95% CI [0.023, 0.057]
- +1SD: estimate=0.049, bootstrap 95% CI [0.028, 0.073]
- Index of moderated mediation: estimate=0.012, bootstrap 95% CI [0.002, 0.025]
Recommended location: Main text 4.5 if the IMM CI excludes zero; otherwise Supplement/robustness.

## Step 6. Latent Policy Acceptance robustness
- Three policy-acceptance items show CR=0.924 and AVE=0.802 in a one-factor score robustness check.
- A 3-indicator single-factor CFA is just-identified, so global model fit is not substantively informative unless a larger measurement model is estimated.
- Latent-score path manage_trust: b=0.882, HC3 SE=0.039, 95% CI [0.805, 0.959], p=0.0000***
- Latent-score path risk: b=-0.049, HC3 SE=0.029, 95% CI [-0.106, 0.009], p=0.0979+
- Latent-score path safe_management: b=0.104, HC3 SE=0.049, 95% CI [0.007, 0.201], p=0.0347*
- Latent-score path trust: b=0.188, HC3 SE=0.037, 95% CI [0.115, 0.261], p=0.0000***
Recommended location: Supplement, with a short main-text robustness sentence.

## Step 7. Single-item institutional trust sensitivity
- Reliability 0.60: a=0.275, corrected b=0.447, indirect=0.123, bootstrap 95% CI [0.072, 0.191], conclusion change=No
- Reliability 0.70: a=0.275, corrected b=0.292, indirect=0.080, bootstrap 95% CI [0.047, 0.120], conclusion change=No
- Reliability 0.80: a=0.275, corrected b=0.217, indirect=0.060, bootstrap 95% CI [0.035, 0.088], conclusion change=No
- Reliability 0.90: a=0.275, corrected b=0.173, indirect=0.047, bootstrap 95% CI [0.028, 0.069], conclusion change=No
- Reliability 0.95: a=0.275, corrected b=0.157, indirect=0.043, bootstrap 95% CI [0.025, 0.063], conclusion change=No
Recommended location: Online Supplement. Treat as measurement-error sensitivity, not a definitive latent SEM.

## Step 8. Information-type heterogeneity
- manage_c: b=0.277, cluster SE=0.031, 95% CI [0.215, 0.338], p=0.0000***
- item_sensitivity_proxy_c: b=-1.000, cluster SE=0.020, 95% CI [-1.040, -0.960], p=0.0000***
- manage_c:item_sensitivity_proxy_c: b=-0.087, cluster SE=0.031, 95% CI [-0.148, -0.025], p=0.0055**
- risk_c:item_sensitivity_proxy_c: b=-0.089, cluster SE=0.027, 95% CI [-0.141, -0.037], p=0.0008***
- Strongest management-trust slopes by information type: Home address (0.378); Date of birth (0.373); Phone number (0.364)
- Weakest management-trust slopes by information type: Habits/preferences (0.100); Financial account (0.173); Credit information (0.202)
Recommended location: Main text 4.6 only if framed as heterogeneity with item fixed effects; otherwise Supplement.

## Step 9. Citizen-practitioner comparison
- Comparable item-specific consent mean: citizen mean=2.785, practitioner mean=2.875, Cohen's d=-0.123, Welch p=0.0617.
- Comparable risk mean: citizen mean=3.818, practitioner mean=3.197, Cohen's d=0.766, Welch p=0.0000.
- Agency trust series mean: citizen mean=3.001, practitioner mean=3.326, Cohen's d=-0.481, Welch p=0.0000.
Recommended location: Supplement, because the main structural variables are not fully comparable across samples.

## Step 10. Interpretation rules and manuscript placement
- Replace legitimacy-as-DV language with policy/data-use acceptance in Methods and Results.
- Avoid claiming that management trust is substantively larger than safe-management perception based only on coefficient size, because the measures differ.
- Move ANOVA/Tukey, residual histograms, Durbin-Watson, quadratic risk, disaster-type heatmaps, and agency mean comparisons to Supplement unless directly tied to the risk-trust mechanism.
- State that cross-sectional covariance may be compatible with alternative orderings; results should be interpreted as theoretically specified associations rather than causal effects.
