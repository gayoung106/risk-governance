"""
16_regression_with_controls.py
통제변수(성별, 연령, 교육, 소득) 포함 회귀분석 재추정
- 인구통계 변수: sq2(성별), sq3_1(연령), tdq4(교육), dq4(소득)
- Model 1: 기본모형 (기존)
- Model 2: 인구통계 통제 후 핵심 예측변수
- Model 3: HC3 강건 표준오차 (통제변수 포함)
- 목적: 주요 발견의 통제 후 강건성 확인
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("../clean/people_clean.csv")

# ─────────────────────────────
# 인구통계 통제변수 준비
# ─────────────────────────────
# sq2: 성별 (1=남, 2=여) → 더미: 1=여성
df['female'] = (df['sq2'] == 2).astype(float)

# sq3_1: 실제 연령 (연속)
df['age'] = df['sq3_1']

# tdq4: 교육수준 (1=고졸이하, 2=대졸, 3=대학원)
# 더미 변수화 (고졸이하 = 참조범주)
df['edu_college'] = (df['tdq4'] == 2).astype(float)
df['edu_grad'] = (df['tdq4'] == 3).astype(float)

# dq4: 소득수준 (1~5 순서형, 연속변수로 투입)
df['income'] = df['dq4']

# 결측치 확인
controls = ['female', 'age', 'edu_college', 'edu_grad', 'income']
main_vars = ['consent', 'manage_trust', 'risk', 'safe_management', 'trust']
analysis_df = df[main_vars + controls].dropna()
print(f"분석 사례 수 (결측 제거 후): {len(analysis_df)}")
print(f"원 표본 대비 유지율: {len(analysis_df)/len(df)*100:.1f}%")

# ─────────────────────────────
# Model 1: 기본 OLS (통제변수 없음)
# ─────────────────────────────
X1 = sm.add_constant(analysis_df[['manage_trust', 'risk', 'safe_management']])
y = analysis_df['consent']
model1 = sm.OLS(y, X1).fit()

# ─────────────────────────────
# Model 2: OLS + 통제변수
# ─────────────────────────────
pred2 = ['manage_trust', 'risk', 'safe_management'] + controls
X2 = sm.add_constant(analysis_df[pred2])
model2 = sm.OLS(y, X2).fit()

# ─────────────────────────────
# Model 3: HC3 강건 표준오차 + 통제변수
# ─────────────────────────────
model3 = sm.OLS(y, X2).fit(cov_type='HC3')

# ─────────────────────────────
# VIF 계산 (통제변수 포함)
# ─────────────────────────────
vif_df = pd.DataFrame()
vif_df['variable'] = pred2
vif_df['VIF'] = [variance_inflation_factor(X2.values, i+1) for i in range(len(pred2))]

# ─────────────────────────────
# 결과 저장
# ─────────────────────────────
output = []
output.append("=" * 70)
output.append("회귀분석 재추정 결과 (통제변수 포함)")
output.append(f"분석 표본 N = {len(analysis_df)}")
output.append("=" * 70)

output.append("\n[Model 1: 기본 OLS - 통제변수 없음]")
output.append(model1.summary().as_text())

output.append("\n[Model 2: OLS + 인구통계 통제변수]")
output.append(model2.summary().as_text())

output.append("\n[Model 3: HC3 강건 표준오차 + 통제변수]")
output.append(model3.summary().as_text())

output.append("\n[VIF 진단 - 통제변수 포함 모형]")
output.append(vif_df.to_string(index=False))

output.append("\n\n[핵심 계수 비교표]")
output.append(f"{'변수':<25} {'Model1 β':>10} {'Model2 β':>10} {'Model3 z':>10} {'Model2 p':>10}")
output.append("-" * 65)
for var in ['manage_trust', 'risk', 'safe_management']:
    b1 = model1.params.get(var, np.nan)
    b2 = model2.params.get(var, np.nan)
    b3 = model3.tvalues.get(var, np.nan)
    p2 = model2.pvalues.get(var, np.nan)
    output.append(f"{var:<25} {b1:>10.4f} {b2:>10.4f} {b3:>10.4f} {p2:>10.4f}")

output.append("\n[통제변수 계수]")
for var in controls:
    b2 = model2.params.get(var, np.nan)
    p2 = model2.pvalues.get(var, np.nan)
    output.append(f"{var:<25} {b2:>10.4f}  p={p2:.4f}")

output.append(f"\nModel1 R²={model1.rsquared:.4f}  Adj.R²={model1.rsquared_adj:.4f}")
output.append(f"Model2 R²={model2.rsquared:.4f}  Adj.R²={model2.rsquared_adj:.4f}")
output.append(f"Model2 vs Model1 ΔR²={model2.rsquared - model1.rsquared:.4f}")

result_text = "\n".join(output)
with open("../result/regression_with_controls.txt", "w", encoding="utf-8") as f:
    f.write(result_text)

print(result_text)
print("\n결과 저장: result/regression_with_controls.txt")
