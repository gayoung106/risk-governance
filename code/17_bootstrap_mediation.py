"""
17_bootstrap_mediation.py
부트스트랩 매개효과 분석 (현대적 방법론)
- Preacher & Hayes (2008) 방식의 bootstrapped indirect effect
- 5,000회 반복, 95% 신뢰구간
- 통제변수 포함 버전과 비교
- 세 가지 간접 경로:
  (a) manage_trust → trust → consent  [핵심 매개 경로]
  (b) manage_trust → safe_management → trust → consent  [안전관리 경로]
  (c) safe_management → trust → consent  [안전관리 긍정 인식 경로]
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

np.random.seed(42)
N_BOOT = 5000

df = pd.read_csv("../clean/people_clean.csv")

# 통제변수 준비
df['female'] = (df['sq2'] == 2).astype(float)
df['age'] = df['sq3_1']
df['edu_college'] = (df['tdq4'] == 2).astype(float)
df['edu_grad'] = (df['tdq4'] == 3).astype(float)
df['income'] = df['dq4']

controls = ['female', 'age', 'edu_college', 'edu_grad', 'income']
vars_needed = ['consent', 'manage_trust', 'risk', 'safe_management', 'trust'] + controls
analysis_df = df[vars_needed].dropna().reset_index(drop=True)
n = len(analysis_df)
print(f"분석 N = {n}")

# ─────────────────────────────────────────────────────────────
# 부트스트랩 함수
# ─────────────────────────────────────────────────────────────
def get_indirect_effects(data):
    """
    Baron-Kenny 3단계 구조에서 간접효과 계산
    간접효과 1: manage_trust → trust → consent (a1 * b1)
    간접효과 2: safe_management → trust → consent (a2 * b1)
    """
    # Step 2: M(trust) = f(manage_trust, safe_management, risk, controls)
    Xm_cols = ['manage_trust', 'safe_management', 'risk'] + controls
    Xm = sm.add_constant(data[Xm_cols])
    Ym = data['trust']
    m2 = sm.OLS(Ym, Xm).fit()

    a1 = m2.params['manage_trust']        # manage_trust → trust 경로 계수
    a2 = m2.params['safe_management']   # safe_management → trust 경로 계수

    # Step 3: consent = f(manage_trust, trust, safe_management, risk, controls)
    Xy_cols = ['manage_trust', 'trust', 'safe_management', 'risk'] + controls
    Xy = sm.add_constant(data[Xy_cols])
    Yy = data['consent']
    m3 = sm.OLS(Yy, Xy).fit()

    b1 = m3.params['trust']               # trust → consent 경로 계수

    indirect1 = a1 * b1   # manage_trust의 간접효과 (trust 경유)
    indirect2 = a2 * b1   # safe_management의 간접효과 (trust 경유)

    # manage_trust 직접효과
    direct_mt = m3.params['manage_trust']

    return indirect1, indirect2, direct_mt, a1, a2, b1

# ─────────────────────────────────────────────────────────────
# 관측값 (원 데이터) 효과 추정
# ─────────────────────────────────────────────────────────────
obs_ind1, obs_ind2, obs_direct, obs_a1, obs_a2, obs_b1 = get_indirect_effects(analysis_df)

# ─────────────────────────────────────────────────────────────
# 부트스트랩 반복
# ─────────────────────────────────────────────────────────────
print(f"부트스트랩 {N_BOOT}회 반복 시작...")
boot_ind1 = np.zeros(N_BOOT)
boot_ind2 = np.zeros(N_BOOT)
boot_direct = np.zeros(N_BOOT)

for i in range(N_BOOT):
    boot_idx = np.random.choice(n, size=n, replace=True)
    boot_data = analysis_df.iloc[boot_idx].reset_index(drop=True)
    try:
        b_ind1, b_ind2, b_direct, _, _, _ = get_indirect_effects(boot_data)
        boot_ind1[i] = b_ind1
        boot_ind2[i] = b_ind2
        boot_direct[i] = b_direct
    except Exception:
        boot_ind1[i] = np.nan
        boot_ind2[i] = np.nan
        boot_direct[i] = np.nan

# NaN 제거
valid = ~(np.isnan(boot_ind1) | np.isnan(boot_ind2))
boot_ind1 = boot_ind1[valid]
boot_ind2 = boot_ind2[valid]
boot_direct = boot_direct[valid]
n_valid = len(boot_ind1)
print(f"유효 부트스트랩 반복 수: {n_valid}")

# ─────────────────────────────────────────────────────────────
# 95% 신뢰구간 (백분위수 방법)
# ─────────────────────────────────────────────────────────────
ci_ind1 = (np.percentile(boot_ind1, 2.5), np.percentile(boot_ind1, 97.5))
ci_ind2 = (np.percentile(boot_ind2, 2.5), np.percentile(boot_ind2, 97.5))
ci_direct = (np.percentile(boot_direct, 2.5), np.percentile(boot_direct, 97.5))

# 유의성: 95% CI가 0을 포함하지 않으면 유의
sig_ind1 = "유의 (95% CI 0 불포함)" if not (ci_ind1[0] <= 0 <= ci_ind1[1]) else "비유의 (CI 0 포함)"
sig_ind2 = "유의 (95% CI 0 불포함)" if not (ci_ind2[0] <= 0 <= ci_ind2[1]) else "비유의 (CI 0 포함)"

# ─────────────────────────────────────────────────────────────
# 3단계 상세 회귀 결과 (원 데이터, 통제변수 포함)
# ─────────────────────────────────────────────────────────────
# Step 1: manage_trust → safe_management
X1 = sm.add_constant(analysis_df[['manage_trust', 'risk'] + controls])
m_step1 = sm.OLS(analysis_df['safe_management'], X1).fit()

# Step 2: trust = f(manage_trust, safe_management, risk, controls)
X2 = sm.add_constant(analysis_df[['manage_trust', 'safe_management', 'risk'] + controls])
m_step2 = sm.OLS(analysis_df['trust'], X2).fit()

# Step 3: consent = f(manage_trust, trust, safe_management, risk, controls)
X3 = sm.add_constant(analysis_df[['manage_trust', 'trust', 'safe_management', 'risk'] + controls])
m_step3 = sm.OLS(analysis_df['consent'], X3).fit()

# ─────────────────────────────────────────────────────────────
# 결과 출력 및 저장
# ─────────────────────────────────────────────────────────────
output = []
output.append("=" * 70)
output.append("부트스트랩 매개효과 분석 결과")
output.append(f"N = {n}, 부트스트랩 반복 = {N_BOOT}회 (유효 = {n_valid}회)")
output.append("통제변수: 성별(female), 연령(age), 교육(edu_college, edu_grad), 소득(income)")
output.append("=" * 70)

output.append("\n[1단계: manage_trust → safe_management]")
output.append(m_step1.summary().as_text())

output.append("\n[2단계: manage_trust + safe_management → trust (제도적 신뢰)]")
output.append(m_step2.summary().as_text())

output.append("\n[3단계: manage_trust + trust + safe_management → consent]")
output.append(m_step3.summary().as_text())

output.append("\n" + "=" * 70)
output.append("부트스트랩 간접효과 요약")
output.append("=" * 70)
output.append(f"\n[간접효과 1] manage_trust → trust → consent (관리신뢰의 간접효과)")
output.append(f"  경로계수: a1(manage→trust) = {obs_a1:.4f}")
output.append(f"  경로계수: b1(trust→consent) = {obs_b1:.4f}")
output.append(f"  간접효과 추정치 = {obs_ind1:.4f}")
output.append(f"  부트스트랩 SE = {np.std(boot_ind1):.4f}")
output.append(f"  95% CI = [{ci_ind1[0]:.4f}, {ci_ind1[1]:.4f}]")
output.append(f"  유의성: {sig_ind1}")

output.append(f"\n[간접효과 2] safe_management → trust → consent (안전관리 긍정 인식 경로)")
output.append(f"  경로계수: a2(safety→trust) = {obs_a2:.4f}")
output.append(f"  경로계수: b1(trust→consent) = {obs_b1:.4f}")
output.append(f"  간접효과 추정치 = {obs_ind2:.4f}")
output.append(f"  부트스트랩 SE = {np.std(boot_ind2):.4f}")
output.append(f"  95% CI = [{ci_ind2[0]:.4f}, {ci_ind2[1]:.4f}]")
output.append(f"  유의성: {sig_ind2}")

output.append(f"\n[manage_trust 직접효과 (trust 통제 후)]")
output.append(f"  직접효과 추정치 = {obs_direct:.4f}")
output.append(f"  부트스트랩 SE = {np.std(boot_direct):.4f}")
output.append(f"  95% CI = [{ci_direct[0]:.4f}, {ci_direct[1]:.4f}]")

output.append(f"\n[총효과 분해 (manage_trust → consent)]")
output.append(f"  직접효과 = {obs_direct:.4f}")
output.append(f"  간접효과 (trust 경유) = {obs_ind1:.4f}")
output.append(f"  총효과 = {obs_direct + obs_ind1:.4f}")
output.append(f"  간접효과 비율 = {obs_ind1/(obs_direct + obs_ind1)*100:.1f}%")

output.append("\n[매개 유형 판정]")
if not (ci_ind1[0] <= 0 <= ci_ind1[1]):
    if abs(m_step3.params.get('manage_trust', 0)) > 0.01 and m_step3.pvalues.get('manage_trust', 1) < 0.05:
        output.append("  → 부분 매개 (partial mediation): 직접효과와 간접효과 모두 유의")
    else:
        output.append("  → 완전 매개 (full mediation): 간접효과 유의, 직접효과 비유의")
else:
    output.append("  → 매개 미지지 (indirect effect CI includes zero)")

result_text = "\n".join(output)
with open("../result/bootstrap_mediation.txt", "w", encoding="utf-8") as f:
    f.write(result_text)

print(result_text)
print("\n결과 저장: result/bootstrap_mediation.txt")
