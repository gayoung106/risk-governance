"""
18_interaction_with_controls.py
통제변수 포함 조절효과(상호작용) 모형 재추정
- 기본 상호작용 모형 (기존)
- 통제변수 포함 상호작용 모형 (신규)
- 중심화(mean-centering) 적용
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("../clean/people_clean.csv")

# 통제변수 준비
df['female'] = (df['sq2'] == 2).astype(float)
df['age'] = df['sq3_1']
df['edu_college'] = (df['tdq4'] == 2).astype(float)
df['edu_grad'] = (df['tdq4'] == 3).astype(float)
df['income'] = df['dq4']

controls = ['female', 'age', 'edu_college', 'edu_grad', 'income']
vars_needed = ['consent', 'manage_trust', 'risk', 'safety_perception'] + controls
analysis_df = df[vars_needed].dropna().reset_index(drop=True)
n = len(analysis_df)
print(f"분석 N = {n}")

# ─────────────────────────────────────
# 중심화 (다중공선성 완화)
# ─────────────────────────────────────
analysis_df['mt_c'] = analysis_df['manage_trust'] - analysis_df['manage_trust'].mean()
analysis_df['risk_c'] = analysis_df['risk'] - analysis_df['risk'].mean()
analysis_df['interaction'] = analysis_df['mt_c'] * analysis_df['risk_c']

# ─────────────────────────────────────
# Model A: 기본 상호작용 (통제변수 없음, 중심화)
# ─────────────────────────────────────
XA = sm.add_constant(analysis_df[['mt_c', 'risk_c', 'safety_perception', 'interaction']])
yA = analysis_df['consent']
modelA = sm.OLS(yA, XA).fit()

# ─────────────────────────────────────
# Model B: 통제변수 포함 상호작용 모형
# ─────────────────────────────────────
XB_cols = ['mt_c', 'risk_c', 'safety_perception', 'interaction'] + controls
XB = sm.add_constant(analysis_df[XB_cols])
modelB = sm.OLS(yA, XB).fit()

# ─────────────────────────────────────
# Model C: HC3 강건 표준오차 + 통제변수
# ─────────────────────────────────────
modelC = sm.OLS(yA, XB).fit(cov_type='HC3')

# ─────────────────────────────────────
# 단순 기울기 분석 (Simple Slope)
# manage_trust의 효과를 risk 수준별로 계산
# ─────────────────────────────────────
risk_low = analysis_df['risk_c'].mean() - analysis_df['risk_c'].std()   # 평균 - 1SD
risk_high = analysis_df['risk_c'].mean() + analysis_df['risk_c'].std()  # 평균 + 1SD

b_mt = modelB.params['mt_c']
b_interaction = modelB.params['interaction']

slope_low_risk = b_mt + b_interaction * risk_low
slope_high_risk = b_mt + b_interaction * risk_high

# ─────────────────────────────────────
# 결과 출력 및 저장
# ─────────────────────────────────────
output = []
output.append("=" * 70)
output.append("조절효과 분석 재추정 (통제변수 포함, 중심화 적용)")
output.append(f"N = {n}")
output.append("예측변수 중심화: manage_trust, risk (평균 = 0)")
output.append("=" * 70)

output.append("\n[Model A: 기본 상호작용 모형 (통제변수 없음, 중심화)]")
output.append(modelA.summary().as_text())

output.append("\n[Model B: 통제변수 포함 상호작용 모형]")
output.append(modelB.summary().as_text())

output.append("\n[Model C: HC3 강건 표준오차 + 통제변수 + 상호작용]")
output.append(modelC.summary().as_text())

output.append("\n" + "=" * 70)
output.append("핵심 계수 비교")
output.append("=" * 70)
output.append(f"\n{'변수':<25} {'ModelA β':>10} {'ModelB β':>10} {'ModelC z':>10}")
output.append("-" * 55)
for var in ['mt_c', 'risk_c', 'safety_perception', 'interaction']:
    bA = modelA.params.get(var, np.nan)
    bB = modelB.params.get(var, np.nan)
    zC = modelC.tvalues.get(var, np.nan)
    output.append(f"{var:<25} {bA:>10.4f} {bB:>10.4f} {zC:>10.4f}")

output.append(f"\nModel A R² = {modelA.rsquared:.4f}")
output.append(f"Model B R² = {modelB.rsquared:.4f}  (ΔR²= {modelB.rsquared - modelA.rsquared:.4f})")

output.append(f"\n[단순 기울기 분석 (Simple Slope Analysis)]")
output.append(f"위험인식 낮은 집단 (평균-1SD)에서 manage_trust 효과: β = {slope_low_risk:.4f}")
output.append(f"위험인식 높은 집단 (평균+1SD)에서 manage_trust 효과: β = {slope_high_risk:.4f}")
output.append(f"→ 위험인식 고집단에서 관리신뢰 효과 {'증폭' if slope_high_risk > slope_low_risk else '약화'}")

output.append(f"\n[이론적 해석]")
output.append(f"상호작용항 β = {modelB.params.get('interaction', np.nan):.4f}")
output.append(f"p값 = {modelB.pvalues.get('interaction', np.nan):.4f}")
if modelB.pvalues.get('interaction', 1) < 0.05:
    if modelB.params.get('interaction', 0) > 0:
        output.append("→ 양의 상호작용 유의: 위험인식 증가 시 관리신뢰의 정적 효과 증폭")
        output.append("→ Beck의 신뢰 대체 메커니즘 지지 방향 (Luhmann/Giddens 이론과도 일치)")
    else:
        output.append("→ 음의 상호작용 유의: 위험인식 증가 시 관리신뢰 효과 약화")
else:
    output.append("→ 상호작용 비유의: 위험인식의 조절효과 지지 안 됨")

result_text = "\n".join(output)
with open("../result/interaction_with_controls.txt", "w", encoding="utf-8") as f:
    f.write(result_text)

print(result_text)
print("\n결과 저장: result/interaction_with_controls.txt")
