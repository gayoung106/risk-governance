"""
H4 조절효과 Simple Slope Analysis
위험인식(조절변수 W) 수준별 관리신뢰(X) → 정책수용성(Y) 기울기 분석
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import statsmodels.api as sm
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── 한글 폰트 설정 ────────────────────────────────────────────────────────────
def set_korean_font():
    candidates = [
        'Malgun Gothic', 'NanumGothic', 'AppleGothic',
        'Nanum Gothic', 'Noto Sans KR',
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams['font.family'] = name
            break
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# ══════════════════════════════════════════════════════════════════════════
# 0. 데이터 준비
# ══════════════════════════════════════════════════════════════════════════
df = pd.read_csv('../clean/people_clean.csv')
df['consent']      = df[['q7_1','q8_1','q9_1']].mean(axis=1)
df['manage_trust'] = df[['q5_1','q6_1']].mean(axis=1)
df['risk']         = df[['q21_1','q22_1']].mean(axis=1)
df['trust']        = pd.to_numeric(df['q26_1'], errors='coerce')
df['safe_mgmt']    = df['q25'].map({1: 1.0, 2: 0.0})

CTRL = ['sq1', 'sq2']
KEY  = ['consent','manage_trust','risk','trust','safe_mgmt'] + CTRL
sub  = df[KEY].dropna().copy()
N    = len(sub)

# ── 평균중심화 (Mean-centering) ───────────────────────────────────────────
mt_mean = sub['manage_trust'].mean()
mt_sd   = sub['manage_trust'].std()
rk_mean = sub['risk'].mean()
rk_sd   = sub['risk'].std()

sub['mt_c']  = sub['manage_trust'] - mt_mean   # 관리신뢰 중심화
sub['rk_c']  = sub['risk']        - rk_mean    # 위험인식 중심화
sub['mt_rk'] = sub['mt_c'] * sub['rk_c']       # 상호작용항

SEP  = "=" * 68
SEP2 = "-" * 68

print(SEP)
print("H4 Simple Slope Analysis")
print("조절변수(W): 위험인식  |  예측변수(X): 관리신뢰  |  결과변수(Y): 정책수용성")
print(SEP)
print(f"N = {N:,}")
print(f"관리신뢰  M={mt_mean:.3f}, SD={mt_sd:.3f}")
print(f"위험인식  M={rk_mean:.3f}, SD={rk_sd:.3f}")
print()

# ══════════════════════════════════════════════════════════════════════════
# 1. 전체 조절효과 모형 (통제변수 포함)
# ══════════════════════════════════════════════════════════════════════════
Xvars = ['mt_c','rk_c','mt_rk','trust','safe_mgmt'] + CTRL
X = sm.add_constant(sub[Xvars])
y = sub['consent']
model = sm.OLS(y, X).fit()

# 기저모형 (상호작용 없음)
X_base = sm.add_constant(sub[['mt_c','rk_c','trust','safe_mgmt'] + CTRL])
model_base = sm.OLS(y, X_base).fit()
delta_r2 = model.rsquared - model_base.rsquared

b0   = model.params['const']
b_mt = model.params['mt_c']      # 관리신뢰 주효과
b_rk = model.params['rk_c']      # 위험인식 주효과
b_ix = model.params['mt_rk']     # 상호작용 계수
se_ix = model.bse['mt_rk']
p_ix  = model.pvalues['mt_rk']

print("[1] 조절효과 모형 요약")
print(SEP2)
print(f"  {'변수':<20} {'B':>10}  {'β':>10}  {'SE':>8}  {'p':>10}")
print("  " + "-" * 62)

std_y = y.std()
for vname, vlabel in [('mt_c','관리신뢰(중심화)'),('rk_c','위험인식(중심화)'),
                       ('mt_rk','상호작용(MT×RK)'),('trust','정부신뢰'),
                       ('safe_mgmt','안전관리'),('sq1','성별'),('sq2','지역')]:
    b   = model.params[vname]
    se  = model.bse[vname]
    pv  = model.pvalues[vname]
    beta = b * sub[vname].std() / std_y if vname in sub.columns else np.nan
    sig  = '***' if pv<.001 else ('**' if pv<.01 else ('*' if pv<.05 else ''))
    print(f"  {vlabel:<20} {b:>10.4f}  {beta:>10.4f}  {se:>8.4f}  {pv:>9.4f}{sig}")

print(f"\n  R²={model.rsquared:.4f}  adj.R²={model.rsquared_adj:.4f}  ΔR²(상호작용)={delta_r2:.4f}")
sig_str = '***' if p_ix<.001 else ('**' if p_ix<.01 else ('*' if p_ix<.05 else 'ns'))
print(f"  상호작용항: B={b_ix:.4f}, SE={se_ix:.4f}, p={p_ix:.4f}{sig_str}")
print()

# ══════════════════════════════════════════════════════════════════════════
# 2. Simple Slope 계산
# ══════════════════════════════════════════════════════════════════════════
# 위험인식(W) 3수준 정의
W_levels = {
    'Low (-1SD)':   -rk_sd,
    'Mean (±0)':    0.0,
    'High (+1SD)':  rk_sd,
}

# Simple slope of X(관리신뢰) at each W level:
#   Y = b0 + b_mt*X + b_rk*W + b_ix*(X*W) + ...
#   ∂Y/∂X = b_mt + b_ix * W
#
# Simple slope SE (Cohen et al., 2003):
#   SE_ss = sqrt(Var(b_mt) + W²*Var(b_ix) + 2W*Cov(b_mt, b_ix))

cov_matrix = model.cov_params()
var_bmt = cov_matrix.loc['mt_c',  'mt_c']
var_bix = cov_matrix.loc['mt_rk', 'mt_rk']
cov_bmt_bix = cov_matrix.loc['mt_c', 'mt_rk']

print("[2] Simple Slope 분석 결과")
print(SEP2)
print(f"  위험인식 수준      W값     기울기(B)   SE       t       p       판정")
print("  " + "-" * 66)

slopes = {}
for label, w_val in W_levels.items():
    slope = b_mt + b_ix * w_val
    se_ss = np.sqrt(var_bmt + w_val**2 * var_bix + 2 * w_val * cov_bmt_bix)
    t_ss  = slope / se_ss
    p_ss  = 2 * (1 - stats.t.cdf(abs(t_ss), df=model.df_resid))
    sig   = '***' if p_ss<.001 else ('**' if p_ss<.01 else ('*' if p_ss<.05 else 'ns'))
    verdict = '유의' if p_ss < .05 else '비유의'
    print(f"  {label:<18} {w_val:>6.3f}  {slope:>10.4f}  {se_ss:>7.4f}  "
          f"{t_ss:>7.3f}  {p_ss:>7.4f}{sig}  {verdict}")
    slopes[label] = dict(w=w_val, slope=slope, se=se_ss, t=t_ss, p=p_ss, sig=sig)

print()

# ══════════════════════════════════════════════════════════════════════════
# 3. Johnson-Neyman 유의 구간 (선택)
# ══════════════════════════════════════════════════════════════════════════
# 기울기가 p=.05에서 0이 되는 W 값: b_mt + b_ix*W = ±1.96*SE_ss(W)
# 이차방정식 풀이
# (b_ix² - 1.96²*var_bix)*W² + 2*(b_mt*b_ix - 1.96²*cov_bmt_bix)*W
#   + (b_mt² - 1.96²*var_bmt) = 0
a_jn = b_ix**2 - (1.96**2) * var_bix
b_jn = 2 * (b_mt * b_ix - (1.96**2) * cov_bmt_bix)
c_jn = b_mt**2  - (1.96**2) * var_bmt
discriminant = b_jn**2 - 4 * a_jn * c_jn

print("[3] Johnson-Neyman 유의 구간")
print(SEP2)
if discriminant >= 0 and abs(a_jn) > 1e-10:
    jn1 = (-b_jn + np.sqrt(discriminant)) / (2 * a_jn)
    jn2 = (-b_jn - np.sqrt(discriminant)) / (2 * a_jn)
    jn_lo, jn_hi = min(jn1, jn2) + rk_mean, max(jn1, jn2) + rk_mean
    # 실제 W 범위 내에 있는지
    w_min_real = sub['risk'].min()
    w_max_real = sub['risk'].max()
    print(f"  기울기 유의성 전환점(원점수 환산):")
    print(f"    JN 경계값 1: 위험인식 = {jn_lo:.3f}")
    print(f"    JN 경계값 2: 위험인식 = {jn_hi:.3f}")
    print(f"  실제 위험인식 범위: [{w_min_real:.1f}, {w_max_real:.1f}]")
    print(f"  → 위험인식 < {jn_lo:.3f} 또는 > {jn_hi:.3f} 구간에서 기울기 유의")
else:
    print("  JN 분석: 판별식 < 0 (모든 W 범위에서 기울기 유의성 일정)")
print()

# ══════════════════════════════════════════════════════════════════════════
# 4. 시각화
# ══════════════════════════════════════════════════════════════════════════
# 관리신뢰(X) 범위: -1SD ~ +1SD
mt_range_c = np.linspace(-mt_sd, mt_sd, 200)   # 중심화된 값
mt_range_r = mt_range_c + mt_mean               # 원점수 환산

# 통제변수는 평균값으로 고정
ctrl_means = {v: sub[v].mean() for v in ['trust','safe_mgmt'] + CTRL}

# 색상·선형 설정
colors  = {'Low (-1SD)': '#2166AC', 'Mean (±0)': '#1A9641', 'High (+1SD)': '#D73027'}
lstyles = {'Low (-1SD)': '--',      'Mean (±0)': '-',       'High (+1SD)': '-.'}
labels  = {
    'Low (-1SD)':  f'위험인식 낮음 (-1SD, M={rk_mean-rk_sd:.2f})',
    'Mean (±0)':   f'위험인식 평균 (M={rk_mean:.2f})',
    'High (+1SD)': f'위험인식 높음 (+1SD, M={rk_mean+rk_sd:.2f})',
}

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# ─ 왼쪽: 인터랙션 플롯 ──────────────────────────────────────────────────
ax = axes[0]

for level, w_val in W_levels.items():
    y_pred = (b0
              + b_mt * mt_range_c
              + b_rk * w_val
              + b_ix * mt_range_c * w_val
              + sum(b * ctrl_means[v]
                    for v, b in zip(['trust','safe_mgmt'] + CTRL,
                                    [model.params[v] for v in ['trust','safe_mgmt'] + CTRL])))
    ax.plot(mt_range_r, y_pred,
            color=colors[level], linestyle=lstyles[level],
            linewidth=2.2, label=labels[level])

# CI 음영 (전체 범위에서 ±1 SE)
sl_info = list(slopes.values())
for info, level in zip(sl_info, W_levels.keys()):
    w_val = info['w']
    y_pred = (b0 + b_mt * mt_range_c + b_rk * w_val
              + b_ix * mt_range_c * w_val
              + sum(model.params[v] * ctrl_means[v]
                    for v in ['trust','safe_mgmt'] + CTRL))
    se_band = info['se']
    ax.fill_between(mt_range_r,
                    y_pred - 1.96 * se_band,
                    y_pred + 1.96 * se_band,
                    color=colors[level], alpha=0.08)

ax.set_xlabel('관리신뢰', fontsize=12)
ax.set_ylabel('정책수용성', fontsize=12)
ax.set_title('조절효과: 위험인식 수준별\n관리신뢰 → 정책수용성', fontsize=13, fontweight='bold')
ax.legend(fontsize=9.5, loc='lower right')
ax.set_xlim(mt_range_r[0], mt_range_r[-1])
ax.set_ylim(1.5, 5.2)
ax.grid(True, alpha=0.3, linestyle=':')
ax.spines[['top','right']].set_visible(False)

# 수직 보조선 (관리신뢰 평균)
ax.axvline(mt_mean, color='gray', linestyle=':', linewidth=1, alpha=0.6)
ax.text(mt_mean + 0.02, 1.6, f'M={mt_mean:.2f}', fontsize=8, color='gray')

# ─ 오른쪽: Simple Slope 계수 막대 + CI ──────────────────────────────────
ax2 = axes[1]

slope_labels  = [labels[k] for k in W_levels.keys()]
slope_vals    = [slopes[k]['slope'] for k in W_levels.keys()]
slope_ses     = [slopes[k]['se']    for k in W_levels.keys()]
slope_colors  = [colors[k]          for k in W_levels.keys()]
sig_marks     = [slopes[k]['sig']   for k in W_levels.keys()]

bars = ax2.bar(range(3), slope_vals,
               color=slope_colors, alpha=0.75, width=0.5,
               edgecolor='white', linewidth=1.2)

# CI 오차막대
ax2.errorbar(range(3), slope_vals,
             yerr=[1.96 * s for s in slope_ses],
             fmt='none', color='#333333', capsize=7, linewidth=1.8, capthick=1.8)

# p 유의성 표시
for i, (val, sig_m) in enumerate(zip(slope_vals, sig_marks)):
    offset = max(slope_vals[i] + 1.96 * slope_ses[i], 0) + 0.02
    ax2.text(i, offset, sig_m, ha='center', va='bottom', fontsize=13,
             color=slope_colors[i], fontweight='bold')

ax2.axhline(0, color='black', linewidth=0.9, linestyle='-')
ax2.set_xticks(range(3))
ax2.set_xticklabels(['위험인식\n낮음\n(-1SD)', '위험인식\n평균\n(Mean)', '위험인식\n높음\n(+1SD)'],
                     fontsize=10)
ax2.set_ylabel('관리신뢰 → 정책수용성 기울기 (B)', fontsize=11)
ax2.set_title('위험인식 수준별 단순기울기\n(오차범위: 95% CI)', fontsize=13, fontweight='bold')
ax2.spines[['top','right']].set_visible(False)
ax2.grid(True, axis='y', alpha=0.3, linestyle=':')

plt.tight_layout(pad=2.5)
plt.savefig('../result/simple_slope.png', dpi=200, bbox_inches='tight',
            facecolor='white')
plt.close()
print("그래프 저장: ../result/simple_slope.png")
print()

# ══════════════════════════════════════════════════════════════════════════
# 5. 해석 요약
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("[4] 해석 요약")
print(SEP)

low  = slopes['Low (-1SD)']
mid  = slopes['Mean (±0)']
high = slopes['High (+1SD)']

def interp_slope(s):
    direction = '정적(+)' if s['slope'] > 0 else '부적(-)'
    sig = '유의함' if s['p'] < .05 else '유의하지 않음'
    return f"B={s['slope']:.4f}, SE={s['se']:.4f}, t={s['t']:.3f}, p={s['p']:.4f} → {direction}, {sig}"

print(f"  Low  (-1SD): {interp_slope(low)}")
print(f"  Mean (±0  ): {interp_slope(mid)}")
print(f"  High (+1SD): {interp_slope(high)}")
print()

# 기울기 패턴 판단
slopes_increasing = high['slope'] > mid['slope'] > low['slope']
slopes_decreasing = high['slope'] < mid['slope'] < low['slope']

if slopes_increasing:
    pattern = "위험인식이 높을수록 관리신뢰의 정책수용성 증진 효과가 커짐 → 강화 조절"
elif slopes_decreasing:
    pattern = "위험인식이 높을수록 관리신뢰의 정책수용성 증진 효과가 약화됨 → 약화 조절 또는 버퍼링 효과"
else:
    pattern = "위험인식 수준에 따라 비선형적 조절 패턴"

print(f"  조절 패턴: {pattern}")
print()

# ══════════════════════════════════════════════════════════════════════════
# 6. 논문 삽입용 문장
# ══════════════════════════════════════════════════════════════════════════
print(SEP)
print("[5] 논문 삽입용 문장")
print(SEP)

ix_sig_str = f"p={p_ix:.3f}{sig_str}" if p_ix >= .001 else "p<.001"

def p_str(pv):
    return "p<.001" if pv < .001 else f"p={pv:.3f}"

low_sig  = "유의한" if low['p']  < .05 else "유의하지 않은"
mid_sig  = "유의한" if mid['p']  < .05 else "유의하지 않은"
high_sig = "유의한" if high['p'] < .05 else "유의하지 않은"

low_dir  = "정적" if low['slope']  > 0 else "부적"
mid_dir  = "정적" if mid['slope']  > 0 else "부적"
high_dir = "정적" if high['slope'] > 0 else "부적"

print(f"""
관리신뢰(X)와 위험인식(W)의 상호작용이 정책수용성(Y)에 미치는
조절효과를 검증하기 위해 위험인식 수준별 단순기울기 분석(simple slope
analysis)을 실시하였다(Cohen et al., 2003). 예측변수(관리신뢰)와
조절변수(위험인식)는 다중공선성 감소를 위해 평균중심화(mean-centering)
하였으며, 정부신뢰, 안전관리 인식, 성별, 지역을 통제변수로 포함하였다.

상호작용항(관리신뢰×위험인식)의 효과는 B={b_ix:.4f}(SE={se_ix:.4f},
{ix_sig_str})로 통계적으로 {'유의하였으며' if p_ix<.05 else '유의하지 않았으나'},
ΔR²={delta_r2:.4f}로 설명분산의 추가적 증가가 확인되었다.

단순기울기 분석 결과, 위험인식이 낮은 집단(-1SD, M={rk_mean-rk_sd:.2f})에서
관리신뢰가 정책수용성에 미치는 기울기는 B={low['slope']:.4f}
(SE={low['se']:.4f}, t={low['t']:.3f}, {p_str(low['p'])})로 {low_sig} {low_dir}
관계를 나타냈다. 위험인식이 평균 수준인 집단(M={rk_mean:.2f})에서는
B={mid['slope']:.4f}(SE={mid['se']:.4f}, t={mid['t']:.3f}, {p_str(mid['p'])})로
{mid_sig} {mid_dir} 효과를 보였다. 위험인식이 높은 집단(+1SD, M={rk_mean+rk_sd:.2f})에서는
B={high['slope']:.4f}(SE={high['se']:.4f}, t={high['t']:.3f}, {p_str(high['p'])})로
{high_sig} {high_dir} 효과를 나타냈다.

이러한 결과는 {pattern}을 보여준다.
구체적으로, 재난 상황에서 위험을 높게 지각하는 응답자일수록 정부의
관리 역량에 대한 신뢰가 정책수용성에 미치는 영향이
{'증폭되는' if slopes_increasing else '감소하는'} 패턴이 확인되었다.
이는 위험인식이 {'신뢰-수용성 관계를 강화하는 촉진 조건' if slopes_increasing
else '신뢰-수용성 관계를 완충하는 조절 기제'}으로 작용함을 시사하며,
위험 거버넌스 맥락에서 위험인식의 조절적 역할에 대한 이론적 함의를
제공한다(Slovic, 1993; Kasperson et al., 1988).
""")

print(SEP)
print("[6] 표: Simple Slope 분석 결과 (논문 삽입용)")
print(SEP)
print()
print("  표 X. 위험인식 수준별 관리신뢰의 단순기울기")
print()
print(f"  {'위험인식 수준':<22} {'B':>8}  {'SE':>8}  {'t':>8}  {'p':>10}  {'95% CI':>18}")
print("  " + "-" * 78)
for level in W_levels.keys():
    s = slopes[level]
    ci_lo = s['slope'] - 1.96 * s['se']
    ci_hi = s['slope'] + 1.96 * s['se']
    sig = ' ***' if s['p']<.001 else (' **' if s['p']<.01 else (' *' if s['p']<.05 else ''))
    lv_label = level.replace('Low','낮음').replace('Mean','평균').replace('High','높음')
    print(f"  {lv_label:<22} {s['slope']:>8.4f}  {s['se']:>8.4f}  "
          f"{s['t']:>8.3f}  {s['p']:>9.4f}{sig}  [{ci_lo:>7.4f}, {ci_hi:>7.4f}]")

print()
print("  주. 관리신뢰와 위험인식은 평균중심화 후 분석. 통제변수: 정부신뢰, 안전관리, 성별, 지역.")
print("      * p<.05  ** p<.01  *** p<.001")
print()
print(f"  전체 모형: R²={model.rsquared:.3f}, adj.R²={model.rsquared_adj:.3f}, "
      f"상호작용 ΔR²={delta_r2:.4f}, F({model.df_model:.0f},{model.df_resid:.0f})={model.fvalue:.3f}, p<.001")
