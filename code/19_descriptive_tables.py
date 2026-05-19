"""
19_descriptive_tables.py
재난 유형별, 개인정보 유형별, 기관 신뢰도 기술통계 표 생성
"""

import pandas as pd
import numpy as np

people = pd.read_csv("../clean/people_clean.csv")
worker = pd.read_csv("../clean/worker_clean.csv")

# ============================================================
# ① 재난 유형별 평균 비교표
# q14k1 = 심각도, q14k2 = 수집 필요성, q14k3 = 공개 필요성, q14k4 = 기관간 공유 필요성
# _1~_15 = 15개 재난 유형
# ============================================================

DISASTER_LABELS = [
    "태풍/강풍", "홍수/침수", "지진", "폭설/한파", "산사태",
    "가뭄/폭염", "해일", "화재", "붕괴", "폭발",
    "화생방사고", "환경오염사고", "감염병", "가축전염병", "미세먼지"
]

rows = []
for i, label in enumerate(DISASTER_LABELS, start=1):
    col_k1 = f"q14k1_{i}"
    col_k2 = f"q14k2_{i}"
    col_k3 = f"q14k3_{i}"
    col_k4 = f"q14k4_{i}"
    rows.append({
        "재난 유형": label,
        "심각도 인식 (M)": round(people[col_k1].mean(), 3),
        "수집 필요성 (M)": round(people[col_k2].mean(), 3),
        "공개 필요성 (M)": round(people[col_k3].mean(), 3),
        "기관 간 공유 필요성 (M)": round(people[col_k4].mean(), 3),
        "심각도 (SD)": round(people[col_k1].std(), 3),
        "수집 필요성 (SD)": round(people[col_k2].std(), 3),
        "공개 필요성 (SD)": round(people[col_k3].std(), 3),
        "공유 필요성 (SD)": round(people[col_k4].std(), 3),
    })

df_disaster = pd.DataFrame(rows).sort_values("심각도 인식 (M)", ascending=False)

with open("../result/disaster_type_comparison.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("재난 유형별 인식 평균 비교 (N=1,094, 5점 척도)\n")
    f.write("=" * 70 + "\n\n")
    f.write("[심각도 기준 내림차순 정렬]\n\n")
    f.write(df_disaster[["재난 유형", "심각도 인식 (M)", "수집 필요성 (M)", "공개 필요성 (M)", "기관 간 공유 필요성 (M)"]].to_string(index=False))
    f.write("\n\n[표준편차]\n\n")
    f.write(df_disaster[["재난 유형", "심각도 (SD)", "수집 필요성 (SD)", "공개 필요성 (SD)", "공유 필요성 (SD)"]].to_string(index=False))
    f.write("\n\n")
    f.write("주: 5점 리커트 척도 (1=전혀 그렇지 않다, 5=매우 그렇다)\n")

print("① 재난 유형별 비교 저장 완료")
print(df_disaster[["재난 유형", "심각도 인식 (M)", "수집 필요성 (M)", "공개 필요성 (M)", "기관 간 공유 필요성 (M)"]].to_string(index=False))

# ============================================================
# ③ 개인정보 유형별 동의 수준 (q29_1~15)
# ============================================================

INFO_LABELS = [
    "성명", "성별", "전화번호", "생년월일", "집 주소",
    "이메일 주소", "소속(학교·회사 등)", "계좌 등 금융정보", "신용정보", "사진",
    "가족 구성원 정보", "의료정보(병력·진료기록)", "위치 정보", "통신정보(전화기록)", "습관·취미·성향 정보"
]

rows_info = []
for i, label in enumerate(INFO_LABELS, start=1):
    col = f"q29_{i}"
    rows_info.append({
        "개인정보 유형": label,
        "제공 동의 수준 (M)": round(people[col].mean(), 3),
        "SD": round(people[col].std(), 3),
        "N": int(people[col].notna().sum()),
    })

df_info = pd.DataFrame(rows_info).sort_values("제공 동의 수준 (M)", ascending=False)

with open("../result/info_type_consent.txt", "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("개인정보 유형별 제공 동의 수준 (N=1,094, 5점 척도)\n")
    f.write("=" * 60 + "\n\n")
    f.write("[동의 수준 기준 내림차순 정렬]\n\n")
    f.write(df_info.to_string(index=False))
    f.write("\n\n")
    f.write("주: 5점 리커트 척도 (1=전혀 동의하지 않는다, 5=매우 동의한다)\n")
    f.write("문항: 재난 대응 정부기관에서 귀하의 개인정보를 수집한다고 할 때, 다음 항목을 제공하는 데 얼마나 동의하십니까?\n")

print("\n③ 개인정보 유형별 동의 수준 저장 완료")
print(df_info.to_string(index=False))

# ============================================================
# ④ 기관 신뢰도 비교표 (q27_1~7)
# ============================================================

INSTITUTION_LABELS = [
    "청와대(위기관리센터)", "행정안전부", "소방청",
    "경찰청", "지방자치단체", "국립중앙의료원 등", "재난유형별 주관부처"
]

rows_trust = []
for i, label in enumerate(INSTITUTION_LABELS, start=1):
    col = f"q27_{i}"
    rows_trust.append({
        "기관": label,
        "신뢰도 (M)": round(people[col].mean(), 3),
        "SD": round(people[col].std(), 3),
        "N": int(people[col].notna().sum()),
    })

df_trust = pd.DataFrame(rows_trust).sort_values("신뢰도 (M)", ascending=False)

with open("../result/institution_trust.txt", "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("재난 대응 기관별 신뢰도 (N=1,094, 5점 척도)\n")
    f.write("=" * 60 + "\n\n")
    f.write("[신뢰도 기준 내림차순 정렬]\n\n")
    f.write(df_trust.to_string(index=False))
    f.write("\n\n")
    f.write("주: 5점 리커트 척도 (1=전혀 신뢰하지 않는다, 5=매우 신뢰한다)\n")
    f.write("문항: 귀하는 다음 각 기관을 얼마나 신뢰하십니까?\n")

print("\n④ 기관 신뢰도 비교 저장 완료")
print(df_trust.to_string(index=False))

# ============================================================
# ② 일반국민 vs 실무자 기술통계 비교 (가용 변수)
# ============================================================
from scipy.stats import ttest_ind

# 일반국민: consent, manage_trust, risk, trust, safety_perception
# 실무자: management(q41,q42 기반), safety(q13,q31,q32 기반)
# 측정도구가 다르므로 개별 t-test는 부적절 - 기술통계만 제공

# 공통적으로 비교 가능한 것: safety 인식 (already done in 11_compare_worker_people.py)
# 추가로: trust 문항이 유사한 경우 비교

# 실무자 데이터의 변수 확인
print("\n=== 실무자 데이터 변수 목록 ===")
worker_cols = [c for c in worker.columns if not c.startswith('q') or c in ['management', 'safety']]
worker_q_cols = [c for c in worker.columns if c.startswith('q')]
print(f"실무자 전체 컬럼 수: {len(worker.columns)}")
print(f"실무자 변수: management={worker['management'].mean():.3f} (SD={worker['management'].std():.3f})")
print(f"실무자 safety={worker['safety'].mean():.3f} (SD={worker['safety'].std():.3f})")
print(f"일반국민 safety_perception={people['safety_perception'].mean():.3f} (SD={people['safety_perception'].std():.3f})")
print(f"일반국민 consent={people['consent'].mean():.3f} (SD={people['consent'].std():.3f})")
print(f"일반국민 manage_trust={people['manage_trust'].mean():.3f} (SD={people['manage_trust'].std():.3f})")
print(f"일반국민 risk={people['risk'].mean():.3f} (SD={people['risk'].std():.3f})")
print(f"일반국민 trust={people['trust'].mean():.3f} (SD={people['trust'].std():.3f})")

# t-test: safety (유사 측정 가능한 유일한 쌍)
t, p = ttest_ind(people['safety_perception'].dropna(), worker['safety'].dropna())

with open("../result/worker_people_comparison.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("일반국민 vs 실무자 기술통계 비교\n")
    f.write("=" * 70 + "\n\n")
    f.write("[주의] 일반국민과 실무자는 측정 도구가 다름\n")
    f.write("  - 일반국민 safety_perception: 이분형 단일 문항 (1=예/2=아니오)\n")
    f.write("  - 실무자 safety: q13+q31+q32 복합 지수 (5점 리커트 평균)\n")
    f.write("  직접 평균 비교는 척도 이질성으로 해석 제한적\n\n")
    f.write("[일반국민 기술통계 (N=1,094)]\n")
    f.write(f"  consent      : M={people['consent'].mean():.3f}, SD={people['consent'].std():.3f}\n")
    f.write(f"  manage_trust : M={people['manage_trust'].mean():.3f}, SD={people['manage_trust'].std():.3f}\n")
    f.write(f"  risk         : M={people['risk'].mean():.3f}, SD={people['risk'].std():.3f}\n")
    f.write(f"  trust        : M={people['trust'].mean():.3f}, SD={people['trust'].std():.3f}\n")
    f.write(f"  safety_perc  : M={people['safety_perception'].mean():.3f}, SD={people['safety_perception'].std():.3f}\n")
    f.write(f"\n[실무자 기술통계 (N={worker.shape[0]})]\n")
    f.write(f"  management   : M={worker['management'].mean():.3f}, SD={worker['management'].std():.3f}\n")
    f.write(f"  safety       : M={worker['safety'].mean():.3f}, SD={worker['safety'].std():.3f}\n")
    f.write(f"\n[safety 인식 t-검정 (척도 이질성 주의)]\n")
    f.write(f"  t={t:.4f}, p={p:.6f}\n")

print("\n② 비교 저장 완료")
print("모든 분석 완료")
