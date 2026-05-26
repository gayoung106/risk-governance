"""
18_interaction_with_controls.py

통제변수 포함 조절효과(상호작용) 분석
- mean-centering 적용
- interaction coefficient 명시
- HC3 robust SE 적용
- simple slope analysis 포함
- UTF-8 인코딩 수정
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm

# =========================================================
# 데이터 로드
# =========================================================
df = pd.read_csv("../clean/people_clean.csv").copy()

# =========================================================
# 통제변수 생성
# =========================================================
df["female"] = (df["sq2"] == 2).astype(float)
df["age"] = pd.to_numeric(df["sq3_1"], errors="coerce")

df["edu_college"] = (df["tdq4"] == 2).astype(float)
df["edu_grad"] = (df["tdq4"] == 3).astype(float)

df["income"] = pd.to_numeric(df["dq4"], errors="coerce")

controls = [
    "female",
    "age",
    "edu_college",
    "edu_grad",
    "income"
]

# =========================================================
# 분석 데이터 구성
# =========================================================
vars_needed = [
    "consent",
    "manage_trust",
    "risk",
    "safe_management"
] + controls

analysis_df = (
    df[vars_needed]
    .dropna()
    .reset_index(drop=True)
)

n = len(analysis_df)

print("=" * 60)
print(f"Analysis N = {n}")
print("=" * 60)

# =========================================================
# Mean-centering
# =========================================================
analysis_df["mt_c"] = (
    analysis_df["manage_trust"]
    - analysis_df["manage_trust"].mean()
)

analysis_df["risk_c"] = (
    analysis_df["risk"]
    - analysis_df["risk"].mean()
)

# =========================================================
# Interaction term
# =========================================================
analysis_df["interaction"] = (
    analysis_df["mt_c"]
    * analysis_df["risk_c"]
)

# =========================================================
# Model A
# 기본 interaction model
# =========================================================
XA = sm.add_constant(
    analysis_df[
        [
            "mt_c",
            "risk_c",
            "safe_management",
            "interaction"
        ]
    ]
)

y = analysis_df["consent"]

modelA = sm.OLS(y, XA).fit()

# =========================================================
# Model B
# 통제변수 포함 interaction model
# =========================================================
XB_cols = [
    "mt_c",
    "risk_c",
    "safe_management",
    "interaction"
] + controls

XB = sm.add_constant(
    analysis_df[XB_cols]
)

modelB = sm.OLS(y, XB).fit()

# =========================================================
# Model C
# HC3 robust SE
# =========================================================
modelC = sm.OLS(y, XB).fit(
    cov_type="HC3"
)

# =========================================================
# Simple Slope Analysis
# =========================================================
risk_low = (
    analysis_df["risk_c"].mean()
    - analysis_df["risk_c"].std()
)

risk_high = (
    analysis_df["risk_c"].mean()
    + analysis_df["risk_c"].std()
)

b_mt = modelB.params["mt_c"]
b_interaction = modelB.params["interaction"]

slope_low_risk = (
    b_mt
    + b_interaction * risk_low
)

slope_high_risk = (
    b_mt
    + b_interaction * risk_high
)

# =========================================================
# 결과 정리
# =========================================================
output = []

output.append("=" * 70)
output.append("INTERACTION ANALYSIS WITH CONTROLS")
output.append("=" * 70)

output.append(f"N = {n}")
output.append("Variables were mean-centered before interaction estimation.")
output.append("HC3 robust standard errors applied in Model C.")

# =========================================================
# Model A
# =========================================================
output.append("\n")
output.append("=" * 70)
output.append("MODEL A: BASIC INTERACTION MODEL")
output.append("=" * 70)

output.append(modelA.summary().as_text())

# =========================================================
# Model B
# =========================================================
output.append("\n")
output.append("=" * 70)
output.append("MODEL B: INTERACTION MODEL WITH CONTROLS")
output.append("=" * 70)

output.append(modelB.summary().as_text())

# =========================================================
# Model C
# =========================================================
output.append("\n")
output.append("=" * 70)
output.append("MODEL C: HC3 ROBUST STANDARD ERRORS")
output.append("=" * 70)

output.append(modelC.summary().as_text())

# =========================================================
# 핵심 coefficient 비교
# =========================================================
output.append("\n")
output.append("=" * 70)
output.append("KEY COEFFICIENT COMPARISON")
output.append("=" * 70)

output.append(
    f"\n{'Variable':<25} {'ModelA B':>12} {'ModelB B':>12} {'ModelC z':>12}"
)

output.append("-" * 65)

for var in [
    "mt_c",
    "risk_c",
    "safe_management",
    "interaction"
]:

    bA = modelA.params.get(var, np.nan)
    bB = modelB.params.get(var, np.nan)
    zC = modelC.tvalues.get(var, np.nan)

    output.append(
        f"{var:<25} {bA:>12.4f} {bB:>12.4f} {zC:>12.4f}"
    )

# =========================================================
# R-squared
# =========================================================
output.append("\n")
output.append(f"Model A R² = {modelA.rsquared:.4f}")
output.append(f"Model B R² = {modelB.rsquared:.4f}")

delta_r2 = modelB.rsquared - modelA.rsquared

output.append(f"ΔR² = {delta_r2:.4f}")

# =========================================================
# Interaction coefficient
# =========================================================
interaction_b = modelB.params["interaction"]
interaction_se = modelB.bse["interaction"]
interaction_p = modelB.pvalues["interaction"]

output.append("\n")
output.append("=" * 70)
output.append("INTERACTION EFFECT")
output.append("=" * 70)

output.append(f"Interaction coefficient (B): {interaction_b:.6f}")
output.append(f"Standard Error (SE): {interaction_se:.6f}")
output.append(f"p-value: {interaction_p:.6f}")

# =========================================================
# Simple slope
# =========================================================
output.append("\n")
output.append("=" * 70)
output.append("SIMPLE SLOPE ANALYSIS")
output.append("=" * 70)

output.append(
    f"Low risk group (-1SD): slope = {slope_low_risk:.4f}"
)

output.append(
    f"High risk group (+1SD): slope = {slope_high_risk:.4f}"
)

if slope_high_risk > slope_low_risk:
    output.append(
        "Interpretation: the positive effect of managerial trust becomes stronger under higher perceived risk."
    )
else:
    output.append(
        "Interpretation: the positive effect of managerial trust becomes weaker under higher perceived risk."
    )

# =========================================================
# Final interpretation
# =========================================================
output.append("\n")
output.append("=" * 70)
output.append("FINAL INTERPRETATION")
output.append("=" * 70)

if interaction_p < 0.05:

    if interaction_b > 0:

        output.append(
            "The interaction effect is positive and statistically significant."
        )

        output.append(
            "Higher perceived risk strengthens the positive relationship between managerial trust and policy acceptance."
        )

    else:

        output.append(
            "The interaction effect is negative and statistically significant."
        )

        output.append(
            "Higher perceived risk weakens the positive relationship between managerial trust and policy acceptance."
        )

else:

    output.append(
        "The interaction effect is not statistically significant."
    )

# =========================================================
# 결과 저장
# =========================================================
result_text = "\n".join(output)

with open(
    "../result/interaction_with_controls.txt",
    "w",
    encoding="utf-8-sig"
) as f:

    f.write(result_text)

# =========================================================
# 콘솔 출력
# =========================================================
print(result_text)

print("\nSaved:")
print("../result/interaction_with_controls.txt")