"""
20_figures_descriptive.py
기관 신뢰도, 개인정보 유형별 동의, 재난 유형별 평균 시각화
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

people = pd.read_csv("../clean/people_clean.csv")
os.makedirs("../result/figure", exist_ok=True)

# ============================================================
# Figure 2: 기관별 신뢰도 비교 (수평 막대)
# ============================================================
INSTITUTION_LABELS = [
    "청와대(위기관리센터)", "행정안전부", "지방자치단체",
    "경찰청", "재난유형별 주관부처", "국립중앙의료원 등", "소방청"
]
trust_means = [people[f"q27_{i}"].mean() for i in range(1, 8)]
trust_sds   = [people[f"q27_{i}"].std()  for i in range(1, 8)]

order = np.argsort(trust_means)
labels_sorted = [INSTITUTION_LABELS[i] for i in order]
means_sorted  = [trust_means[i] for i in order]
sds_sorted    = [trust_sds[i]   for i in order]

fig, ax = plt.subplots(figsize=(9, 5))
colors = ['#c9e4f7' if m < 3.0 else '#4baede' for m in means_sorted]
bars = ax.barh(labels_sorted, means_sorted, xerr=sds_sorted,
               color=colors, edgecolor='white', capsize=4, height=0.6)
ax.axvline(x=3.0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='중립(3.0)')
for i, (m, s) in enumerate(zip(means_sorted, sds_sorted)):
    ax.text(m + s + 0.03, i, f'{m:.2f}', va='center', fontsize=9)
ax.set_xlabel('신뢰도 (5점 척도)', fontsize=11)
ax.set_title('재난 대응 기관별 신뢰도 비교 (N=1,094)', fontsize=12, fontweight='bold')
ax.set_xlim(1, 5.3)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("../result/figure/institution_trust.png", dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2: 기관 신뢰도 저장 완료")

# ============================================================
# Figure 3: 개인정보 유형별 제공 동의 수준 (수평 막대)
# ============================================================
INFO_LABELS = [
    "성명", "성별", "전화번호", "생년월일", "집 주소",
    "이메일 주소", "소속(학교·회사)", "계좌 등 금융정보", "신용정보", "사진",
    "가족 구성원 정보", "의료정보", "위치 정보", "통신정보", "습관·취미·성향"
]
info_means = [people[f"q29_{i}"].mean() for i in range(1, 16)]
info_sds   = [people[f"q29_{i}"].std()  for i in range(1, 16)]

order = np.argsort(info_means)
il_sorted = [INFO_LABELS[i] for i in order]
im_sorted = [info_means[i]  for i in order]
is_sorted = [info_sds[i]    for i in order]

fig, ax = plt.subplots(figsize=(9, 6))
colors = ['#f4b8b8' if m < 2.5 else ('#fde68a' if m < 3.0 else '#86c5a5')
          for m in im_sorted]
ax.barh(il_sorted, im_sorted, xerr=is_sorted,
        color=colors, edgecolor='white', capsize=3, height=0.65)
ax.axvline(x=3.0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='중립(3.0)')
for i, (m, s) in enumerate(zip(im_sorted, is_sorted)):
    ax.text(m + s + 0.03, i, f'{m:.2f}', va='center', fontsize=8.5)
ax.set_xlabel('제공 동의 수준 (5점 척도)', fontsize=11)
ax.set_title('개인정보 유형별 재난 대응 기관 제공 동의 수준 (N=1,094)', fontsize=11, fontweight='bold')
ax.set_xlim(1, 5.5)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("../result/figure/info_type_consent.png", dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3: 개인정보 유형별 동의 저장 완료")

# ============================================================
# Figure 4: 재난 유형별 감염병 vs 비감염병 비교 (심각도/수집/공개/공유)
#           — 15개 유형 전체 히트맵
# ============================================================
DISASTER_LABELS = [
    "태풍/강풍", "홍수/침수", "지진", "폭설/한파", "산사태",
    "가뭄/폭염", "해일", "화재", "붕괴", "폭발",
    "화생방사고", "환경오염사고", "감염병", "가축전염병", "미세먼지"
]
dims = ["심각도\n인식", "수집\n필요성", "공개\n필요성", "기관간\n공유 필요성"]
data = []
for i in range(1, 16):
    row = [
        people[f"q14k1_{i}"].mean(),
        people[f"q14k2_{i}"].mean(),
        people[f"q14k3_{i}"].mean(),
        people[f"q14k4_{i}"].mean(),
    ]
    data.append(row)

mat = np.array(data)
order = np.argsort(mat[:, 0])[::-1]  # 심각도 기준 내림차순
mat_sorted = mat[order]
labels_sorted = [DISASTER_LABELS[i] for i in order]

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(mat_sorted, aspect='auto', cmap='YlOrRd', vmin=2.5, vmax=4.5)
ax.set_xticks(range(4))
ax.set_xticklabels(dims, fontsize=10)
ax.set_yticks(range(15))
ax.set_yticklabels(labels_sorted, fontsize=9)
for i in range(15):
    for j in range(4):
        ax.text(j, i, f'{mat_sorted[i, j]:.2f}', ha='center', va='center', fontsize=8,
                color='black' if mat_sorted[i, j] < 4.0 else 'white')
plt.colorbar(im, ax=ax, label='평균 (5점 척도)', shrink=0.7)
ax.set_title('재난 유형별 심각도 및 개인정보 활용 필요성 인식 (N=1,094)', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig("../result/figure/disaster_type_heatmap.png", dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4: 재난 유형별 히트맵 저장 완료")

print("\n모든 Figure 저장 완료 → result/figure/")
