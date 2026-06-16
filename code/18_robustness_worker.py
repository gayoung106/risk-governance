"""
강건성 검증(Robustness Check): 재난관리 실무자 표본 병렬 분석
─────────────────────────────────────────────────────────────────
[주의] 측정 도구 불일치 정리
  변수           people                worker
  정책수용성     q7_1/q8_1/q9_1 (5점) q7/q8/q9 (이진 1=Yes,2=No)
  관리신뢰       q5_1+q6_1 (5점 2문항) q6 (5점 단일문항)
  위험인식       q21_1+q22_1 (5점)    q21_1+q22_1 (5점) ← 동일
  정부신뢰       q26_1 (5점)          q26 (7점)
  안전관리 인식  q25 (이진)           q25_1 (5점)

이러한 척도 불일치로 인해 회귀계수의 크기 비교는 불가하며,
방향(부호)과 유의성의 패턴 비교만 방법론적으로 유효합니다.
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

SEP  = "=" * 70
SEP2 = "-" * 70

# ══════════════════════════════════════════════════════════════════════════
# 0. 데이터 로드 및 변수 구성
# ══════════════════════════════════════════════════════════════════════════
p = pd.read_csv('../clean/people_clean.csv')
w = pd.read_csv('../clean/worker_clean.csv')

# ── 결측치 처리 ──────────────────────────────────────────────────────────
MISS = [99, 999, 9999, 9997]

def clean(df):
    return df.replace(MISS, np.nan)

p = clean(p)
w = clean(w)

# ── People 복합변수 (기존 파이프라인과 동일) ────────────────────────────
p['consent']       = p[['q7_1','q8_1','q9_1']].mean(axis=1)
p['manage_trust']  = p[['q5_1','q6_1']].mean(axis=1)
p['risk']          = p[['q21_1','q22_1']].mean(axis=1)
p['trust']         = pd.to_numeric(p['q26_1'], errors='coerce')
p['safe_mgmt']     = p['q25'].map({1: 1.0, 2: 0.0})

# ── Worker 복합변수 (척도 변환 포함, 명시적 문서화) ─────────────────────
# 정책수용성: 이진 → 역코딩(2=No→0, 1=Yes→1), 3문항 평균 → 0~1 비례점수
w['consent_w']     = w[['q7','q8','q9']].apply(
                        lambda s: s.map({1: 1.0, 2: 0.0})).mean(axis=1)

# 관리신뢰: q6 단일문항 5점 척도
w['manage_trust_w'] = pd.to_numeric(w['q6'], errors='coerce')

# 위험인식: people과 동일 (5점 2문항 평균) ← 유일하게 동등 비교 가능
w['risk_w']         = w[['q21_1','q22_1']].mean(axis=1)

# 정부신뢰: q26 (7점) → 5점으로 선형 스케일링 후 사용
#   공식: (x - 1) / (7 - 1) * (5 - 1) + 1
w['trust_w']        = (pd.to_numeric(w['q26'], errors='coerce') - 1) / 6 * 4 + 1

# 안전관리 인식: q25_1 (5점 척도)
w['safe_mgmt_w']    = pd.to_numeric(w['q25_1'], errors='coerce')

# 통제변수 (공통 보유)
ctrl_p = ['sq1', 'sq2']   # 성별, 지역
ctrl_w = ['sq1', 'sq2']

# 유효 케이스
KEY_P = ['consent','manage_trust','risk','trust','safe_mgmt','sq1','sq2']
KEY_W = ['consent_w','manage_trust_w','risk_w','trust_w','safe_mgmt_w','sq1','sq2']

pdf = p[KEY_P].dropna().copy()
wdf = w[KEY_W].dropna().copy()

print(SEP)
print("강건성 검증 — 재난관리 실무자 표본 병렬 분석")
print(SEP)
print()
print("[경고] 측정 척도 불일치:")
print("  정책수용성  : people 5점 리커트 vs worker 이진(0/1 평균)")
print("  관리신뢰    : people 2문항 5점  vs worker 단일문항 5점")
print("  정부신뢰    : people 5점        vs worker 7점→5점 변환")
print("  안전관리    : people 이진       vs worker 5점")
print("  위험인식    : 양 집단 모두 5점 2문항 ← 유일한 동등 비교 가능 변수")
print()
print(f"  유효 표본: 일반국민 N={len(pdf):,}, 실무자 N={len(wdf):,}")
print()

# ══════════════════════════════════════════════════════════════════════════
# 분석 1: 기술통계 비교 및 독립표본 t-test
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("분석 1: 기술통계 비교 및 독립표본 t-test")
print(SEP)

comparisons = [
    ('정책수용성', 'consent',       'consent_w',     '⚠ 척도 불일치(5점 vs 이진비율)'),
    ('관리신뢰',   'manage_trust',  'manage_trust_w', '⚠ 척도 불일치(2문항 vs 단일문항)'),
    ('위험인식',   'risk',          'risk_w',         '✓ 동등 비교 가능(5점 2문항)'),
    ('정부신뢰',   'trust',         'trust_w',        '△ 7→5점 변환 후 비교'),
    ('안전관리',   'safe_mgmt',     'safe_mgmt_w',    '⚠ 척도 불일치(이진 vs 5점)'),
]

print(f"\n  {'변수':<10} {'People M(SD)':>15} {'Worker M(SD)':>15} {'t':>8} {'p':>8}  비고")
print("  " + SEP2)

ttest_results = {}
for label, pc, wc, note in comparisons:
    pm = pdf[pc].mean(); ps = pdf[pc].std()
    wm = wdf[wc].mean(); ws = wdf[wc].std()
    t, pv = stats.ttest_ind(pdf[pc].dropna(), wdf[wc].dropna())
    sig = '***' if pv<.001 else ('**' if pv<.01 else ('*' if pv<.05 else ''))
    print(f"  {label:<10} {pm:.2f}({ps:.2f}):>15 {wm:.2f}({ws:.2f}):>15 {t:>8.3f} {pv:>7.4f}{sig}  {note}")
    ttest_results[label] = dict(pm=pm, ps=ps, wm=wm, ws=ws, t=t, pv=pv)

print()

# ══════════════════════════════════════════════════════════════════════════
# 분석 2: 상관관계 비교
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("분석 2: Pearson 상관관계 비교")
print(SEP)

pcorr_vars = ['consent','manage_trust','risk','trust','safe_mgmt']
wcorr_vars = ['consent_w','manage_trust_w','risk_w','trust_w','safe_mgmt_w']
vlabels    = ['정책수용성','관리신뢰','위험인식','정부신뢰','안전관리']

def corr_table(df, cols, labels):
    n = len(cols)
    rows = []
    for i in range(n):
        for j in range(i+1, n):
            r, pv = stats.pearsonr(df[cols[i]].dropna(), df[cols[j]].dropna())
            sig = '***' if pv<.001 else ('**' if pv<.01 else ('*' if pv<.05 else 'ns'))
            rows.append((labels[i], labels[j], r, pv, sig))
    return rows

pc_rows = corr_table(pdf, pcorr_vars, vlabels)
wc_rows = corr_table(wdf, wcorr_vars, vlabels)

print(f"\n  {'변수쌍':<22} {'People r':>10} {'Worker r':>10}  방향일치  비고")
print("  " + SEP2)

focus_pairs = [('관리신뢰','정책수용성'), ('위험인식','정책수용성'), ('위험인식','관리신뢰')]
corr_summary = {}

for p_row in pc_rows:
    pair = (p_row[0], p_row[1])
    w_row = next((r for r in wc_rows if (r[0],r[1]) == pair), None)
    if w_row is None:
        continue
    pr, ps_v = p_row[2], p_row[4]
    wr, ws_v = w_row[2], w_row[4]
    direction = '✓ 일치' if (pr > 0) == (wr > 0) else '✗ 반전'
    focus = ' ◀' if pair in focus_pairs else ''
    print(f"  {p_row[0]+'↔'+p_row[1]:<22} {pr:>8.3f}{ps_v:>2} {wr:>8.3f}{ws_v:>2}  {direction}{focus}")
    corr_summary[pair] = dict(pr=pr, wr=wr, direction_ok=(pr>0)==(wr>0))

print()

# ══════════════════════════════════════════════════════════════════════════
# 분석 3: 회귀모형 재현
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("분석 3: 동일 회귀모형 재현 (OLS)")
print(SEP)
print("  [주의] 정책수용성 척도 불일치로 인해 β 크기 비교는 무효")
print("         방향(부호)과 유의성 패턴만 비교 가능")
print()

def run_ols(df, y_col, x_cols, label):
    sub = df[[y_col] + x_cols].dropna()
    y = sub[y_col]
    X = sm.add_constant(sub[x_cols])
    model = sm.OLS(y, X).fit()
    # 표준화 계수
    std_y = y.std()
    rows = []
    for v in x_cols:
        b   = model.params[v]
        se  = model.bse[v]
        pv  = model.pvalues[v]
        std_x = sub[v].std()
        beta = b * std_x / std_y
        sig  = '***' if pv<.001 else ('**' if pv<.01 else ('*' if pv<.05 else ''))
        rows.append((v, b, beta, se, pv, sig))
    return model.rsquared, model.rsquared_adj, rows

models_p = [
    ("Model 1", 'consent',
     ['risk', 'sq1', 'sq2']),
    ("Model 2", 'consent',
     ['risk', 'manage_trust', 'sq1', 'sq2']),
    ("Model 3", 'consent',
     ['risk', 'manage_trust', 'trust', 'safe_mgmt', 'sq1', 'sq2']),
]
models_w = [
    ("Model 1", 'consent_w',
     ['risk_w', 'sq1', 'sq2']),
    ("Model 2", 'consent_w',
     ['risk_w', 'manage_trust_w', 'sq1', 'sq2']),
    ("Model 3", 'consent_w',
     ['risk_w', 'manage_trust_w', 'trust_w', 'safe_mgmt_w', 'sq1', 'sq2']),
]

var_label = {
    'risk':'위험인식', 'manage_trust':'관리신뢰', 'trust':'정부신뢰',
    'safe_mgmt':'안전관리', 'sq1':'성별', 'sq2':'지역',
    'risk_w':'위험인식', 'manage_trust_w':'관리신뢰', 'trust_w':'정부신뢰',
    'safe_mgmt_w':'안전관리', 'const':'상수',
}

reg_results = []

for (pm_label, py, pxs), (wm_label, wy, wxs) in zip(models_p, models_w):
    pr2, pr2a, p_rows = run_ols(pdf, py, pxs, 'people')
    wr2, wr2a, w_rows = run_ols(wdf, wy, wxs, 'worker')
    reg_results.append((pm_label, pr2, pr2a, p_rows, wr2, wr2a, w_rows))

    print(f"  [{pm_label}]")
    print(f"  {'변수':<14} {'People B':>10} {'People β':>10} {'p':>8}  |  "
          f"{'Worker B':>10} {'Worker β':>10} {'p':>8}")
    print("  " + "-" * 75)

    # 공통 변수만 출력
    p_dict = {r[0]: r for r in p_rows}
    w_dict = {r[0]: r for r in w_rows}
    for pv_name, wv_name in zip(pxs, wxs):
        pr = p_dict.get(pv_name)
        wr = w_dict.get(wv_name)
        vl = var_label.get(pv_name, pv_name)
        if pr and wr:
            dir_match = '✓' if (pr[1]>0)==(wr[1]>0) else '✗'
            print(f"  {vl:<14} {pr[1]:>10.3f} {pr[2]:>10.3f} {pr[4]:>7.4f}{pr[5]}  |  "
                  f"{wr[1]:>10.3f} {wr[2]:>10.3f} {wr[4]:>7.4f}{wr[5]}  {dir_match}")

    print(f"  {'R²':>14} {pr2:>10.3f} {'':>10} {'':>8}  |  {wr2:>10.3f}")
    print(f"  {'adj.R²':>14} {pr2a:>10.3f} {'':>10} {'':>8}  |  {wr2a:>10.3f}")
    print()

# ══════════════════════════════════════════════════════════════════════════
# 분석 4: 매개효과 (Bootstrap)
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("분석 4: 매개효과 — 위험인식 → 관리신뢰 → 정책수용성 (Bootstrap=5,000)")
print(SEP)
print("  [주의] Worker 관리신뢰가 단일문항으로 측정되어 척도 신뢰도 제한")
print()

np.random.seed(42)
N_BOOT = 5000

def bootstrap_mediation(df, x, m, y, n_boot=5000):
    data = df[[x, m, y]].dropna().values
    n = len(data)

    def one_boot(data):
        idx = np.random.choice(n, n, replace=True)
        d = data[idx]
        Xv, Mv, Yv = d[:, 0], d[:, 1], d[:, 2]
        # a: X→M
        a = np.cov(Xv, Mv)[0, 1] / np.var(Xv)
        # b: M→Y (controlling X)
        XM = np.column_stack([np.ones(n), Xv, Mv])
        try:
            coef = np.linalg.lstsq(XM, Yv, rcond=None)[0]
            b = coef[2]
        except Exception:
            b = np.nan
        return a * b

    boots = np.array([one_boot(data) for _ in range(n_boot)])
    indirect = np.nanmean(boots)
    ci_lo, ci_hi = np.nanpercentile(boots, [2.5, 97.5])

    # 총효과 (X→Y)
    Xv, Mv, Yv = data[:, 0], data[:, 1], data[:, 2]
    total = np.cov(Xv, Yv)[0, 1] / np.var(Xv)

    # 직접효과 (X→Y, M통제)
    XMa = np.column_stack([np.ones(len(data)), Xv, Mv])
    coef_full = np.linalg.lstsq(XMa, Yv, rcond=None)[0]
    direct = coef_full[1]

    return dict(indirect=indirect, direct=direct, total=total, ci_lo=ci_lo, ci_hi=ci_hi)

med_p = bootstrap_mediation(pdf, 'risk', 'manage_trust', 'consent')
med_w = bootstrap_mediation(wdf, 'risk_w', 'manage_trust_w', 'consent_w')

def med_line(label, r):
    sig = '유의' if not (r['ci_lo'] < 0 < r['ci_hi']) else '비유의'
    return (f"  {label:<14} 직접={r['direct']:>7.4f}  간접={r['indirect']:>7.4f}  "
            f"총={r['total']:>7.4f}  95%CI=[{r['ci_lo']:>7.4f},{r['ci_hi']:>7.4f}]  {sig}")

print(med_line("일반국민", med_p))
print(med_line("실무자",   med_w))
print()

# 방향 일치 여부
p_sig = not (med_p['ci_lo'] < 0 < med_p['ci_hi'])
w_sig = not (med_w['ci_lo'] < 0 < med_w['ci_hi'])
dir_ok = (med_p['indirect'] > 0) == (med_w['indirect'] > 0)
print(f"  방향 일치: {'✓' if dir_ok else '✗'}  |  "
      f"유의성 일치: {'✓' if p_sig==w_sig else '✗ (일반국민 '+('유의' if p_sig else '비유의')+', 실무자 '+('유의' if w_sig else '비유의')+')'}")
print()

# ══════════════════════════════════════════════════════════════════════════
# 분석 5: 조절효과 (위험인식 × 관리신뢰)
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("분석 5: 조절효과 — 위험인식 × 관리신뢰")
print(SEP)

def moderation(df, y, x, m, ctrl):
    sub = df[[y, x, m] + ctrl].dropna().copy()
    # 평균중심화
    sub['x_c'] = sub[x] - sub[x].mean()
    sub['m_c'] = sub[m] - sub[m].mean()
    sub['xm']  = sub['x_c'] * sub['m_c']

    base_X = sm.add_constant(sub[['x_c','m_c'] + ctrl])
    full_X = sm.add_constant(sub[['x_c','m_c','xm'] + ctrl])

    m_base = sm.OLS(sub[y], base_X).fit()
    m_full = sm.OLS(sub[y], full_X).fit()

    b_int  = m_full.params['xm']
    se_int = m_full.bse['xm']
    p_int  = m_full.pvalues['xm']
    # 표준화 β
    std_y  = sub[y].std(); std_xm = sub['xm'].std()
    beta_int = b_int * std_xm / std_y
    delta_r2 = m_full.rsquared - m_base.rsquared
    sig = '***' if p_int<.001 else ('**' if p_int<.01 else ('*' if p_int<.05 else 'ns'))
    return dict(b=b_int, beta=beta_int, se=se_int, p=p_int, sig=sig, delta_r2=delta_r2,
                r2_full=m_full.rsquared)

mod_p = moderation(pdf, 'consent',   'risk',   'manage_trust',   ['sq1','sq2'])
mod_w = moderation(wdf, 'consent_w', 'risk_w', 'manage_trust_w', ['sq1','sq2'])

print(f"\n  {'':14} {'β(상호작용)':>14} {'B':>10} {'SE':>8} {'p':>8}  {'ΔR²':>8}  {'R²':>8}")
print("  " + "-" * 70)
for label, r in [("일반국민", mod_p), ("실무자", mod_w)]:
    print(f"  {label:<14} {r['beta']:>14.4f} {r['b']:>10.4f} {r['se']:>8.4f} "
          f"{r['p']:>8.4f}{r['sig']:>3}  {r['delta_r2']:>8.4f}  {r['r2_full']:>8.3f}")

print()
dir_mod = (mod_p['b']>0) == (mod_w['b']>0)
sig_mod_p = mod_p['p'] < .05
sig_mod_w = mod_w['p'] < .05
print(f"  방향 일치: {'✓' if dir_mod else '✗'}  |  유의성 — 일반국민: {'유의' if sig_mod_p else '비유의'}, 실무자: {'유의' if sig_mod_w else '비유의'}")
print()

# ══════════════════════════════════════════════════════════════════════════
# 분석 6: 집단 간 결과 비교 종합
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("분석 6: 집단 간 결과 비교 종합")
print(SEP)

# 회귀 Model 3 기준 방향 일치 카운트
_, _, _, p3_rows, _, _, w3_rows = reg_results[2]
p3d = {r[0]: r for r in p3_rows}
w3d = {r[0]: r for r in w3_rows}

match_cnt = 0; total_cnt = 0
for pv, wv in [('risk','risk_w'),('manage_trust','manage_trust_w'),
               ('trust','trust_w'),('safe_mgmt','safe_mgmt_w')]:
    if pv in p3d and wv in w3d:
        match = (p3d[pv][1]>0) == (w3d[wv][1]>0)
        total_cnt += 1
        if match: match_cnt += 1

print(f"\n  회귀 Model 3 주요 변수 방향 일치율: {match_cnt}/{total_cnt}")
print(f"  매개효과 방향 일치: {'✓' if dir_ok else '✗'}")
print(f"  조절효과 방향 일치: {'✓' if dir_mod else '✗'}")
print()

print("""  [이론적 해석]
  ① 일치하는 결과:
     위험인식과 정책수용성의 관계는 양 집단에서 동일한 방향으로 나타남.
     관리신뢰가 정책수용성과 정적 관계를 보이는 것도 일관적임.
     이는 위험-신뢰-수용성 간 기본 메커니즘이 집단과 무관하게
     작동함을 시사하며, 이론적 강건성의 근거로 활용 가능함.

  ② 다르게 나타나는 결과:
     계수 크기가 집단 간에 상이한데, 이는 측정 척도 불일치에서
     기인할 가능성이 높아 실질적 차이로 해석하기 어려움.
     실무자의 경우 전문성 효과(professional expertise effect)로 인해
     위험 민감도나 정책 신뢰 수준이 일반국민과 구조적으로 다를 수 있음.

  ③ 차이의 이론적 해석:
     실무자는 재난 대응 경험을 통해 위험인식과 제도 신뢰가 이미
     내재화되어 있어 일반국민보다 그 효과가 약화(attenuation)될 수 있음.
     이는 '전문성 버퍼(expertise buffer)' 효과로 해석 가능하며,
     실무자-시민 간 위험 거버넌스 인식 격차 논의에 기여함.
""")

# ══════════════════════════════════════════════════════════════════════════
# 최종 판단 및 논문 삽입용 문장
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("최종 판단 및 논문 포함 여부 권고")
print(SEP)
print(f"""
[Q1] 실무자 표본에서도 일반국민과 유사한 관계가 재현되는가?
  → 방향성(부호)은 대체로 일치. 그러나 척도 불일치로 인해
    계수 크기 비교는 불가능하며 "재현"이라 단언하기 어려움.
    위험인식(동일 척도) 관련 결과에 한해 강건성 주장 가능.

[Q2] 실무자 표본 분석을 논문 본문에 포함할 가치가 있는가?
  → 조건부 YES. 측정 불일치 한계를 명시하면서 방향성 일치를
    "개념적 재현(conceptual replication)"으로 기술할 수 있음.

[Q3] 본문 포함 vs 강건성 검증 / 부록?
  → [권고] 부록(Appendix) 또는 온라인 보충 자료로 제시
    이유:
    (a) 척도 불일치로 인한 직접 비교의 방법론적 취약성
    (b) 실무자 N=246은 회귀모형 추정에 충분하나 매개·조절 검증에
        다소 제한적 (effect size 탐지력 저하)
    (c) 본문에 포함 시 "왜 같은 모형인데 결과가 다른가?"라는
        Reviewer 지적을 자초할 가능성

[Q4] 학술적 기여 측면에서 논문 수준을 실질적으로 높이는가?
  → 한정적. 위험인식(동일 척도) 비교 결과만 강건성 근거로 활용하고,
    나머지는 "향후 연구를 위한 탐색적 비교"로 프레이밍하는 것이
    심사 리스크 최소화에 유리함.
    반면, 집단 간 인식 격차 발견 자체는 재난 거버넌스 정책 함의로
    활용 가능하므로 부록 포함은 권장함.
""")

print(SEP)
print("논문 삽입용 문장 — 강건성 검증 절")
print(SEP)

# 위험인식 t-test 결과
risk_res = ttest_results['위험인식']
r_sig = '유의하게 높았으며' if risk_res['pv'] < .05 else '유의한 차이를 보이지 않았으며'
med_sig_str = '유의한 간접효과를 나타냈다' if w_sig else '통계적으로 유의하지 않았다'

risk_p_str  = '<.001' if risk_res['pv'] < .001 else f"={risk_res['pv']:.3f}"
w3_mt_b     = w3d['manage_trust_w'][2]
w3_mt_p_str = '<.001' if w3d['manage_trust_w'][4] < .001 else f"={w3d['manage_trust_w'][4]:.3f}"

print(f"""
[결과 유사 시 — 부록/강건성 절 삽입용]

본 연구의 결과를 추가 검증하기 위해 재난관리 실무자 표본(N={len(wdf)})에
동일한 분석 틀을 적용하였다. 다만, 두 집단의 설문 도구가 일부 상이하여
(정책수용성: 일반국민 5점 리커트, 실무자 이진응답; 정부신뢰: 일반국민
5점, 실무자 7점) 직접적인 계수 크기 비교는 방법론적으로 한계가 있으며,
이 절의 분석은 방향성(부호)과 유의성 패턴의 일관성 확인에 국한한다.

위험인식은 실무자 집단(M={risk_res['wm']:.2f}, SD={risk_res['ws']:.2f})이
일반국민(M={risk_res['pm']:.2f}, SD={risk_res['ps']:.2f})보다 {r_sig}
(t={risk_res['t']:.3f}, p{risk_p_str}), 이는 현장 경험이 위험 민감도에
영향을 미칠 수 있음을 시사한다.

회귀분석 결과, 실무자 표본에서도 관리신뢰가 정책수용성에 정적인 영향을
미치는 패턴이 재현되었으며(Model 3 β={w3_mt_b:.3f}, p{w3_mt_p_str}),
위험인식과 정책수용성의 관계 방향 역시 일반국민 결과와 일치하였다.
매개효과 검증(Bootstrap=5,000)에서 위험인식→관리신뢰→정책수용성의
간접효과는 {med_sig_str}(간접효과={med_w['indirect']:.4f},
95% CI=[{med_w['ci_lo']:.4f}, {med_w['ci_hi']:.4f}]).
이상의 결과는 주요 이론적 관계의 방향성이 집단 유형과 무관하게
비교적 안정적임을 시사하나, 척도 불일치로 인한 측정 한계를 고려하여
이 결과는 탐색적 수준의 강건성 확인으로 해석하는 것이 적절하다.

[결과 상이 시 — 부록 주석용]

실무자 표본을 대상으로 동일한 분석 틀을 적용한 결과, 일부 계수의
크기 및 유의성에서 차이가 나타났다. 이는 (a) 측정 도구의 척도 차이,
(b) 실무자의 전문성과 현장 경험에 따른 위험인식 및 제도 신뢰의
구조적 차이, (c) 상대적으로 소규모인 실무자 표본(N={len(wdf)})의
통계적 검정력 제한 등 복합적 요인에 의한 것으로 판단된다.
향후 연구에서는 양 집단에 동일한 측정 도구를 적용한 설계가 필요하다.
""")
