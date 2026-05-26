"""
19_descriptive_tables.py

기술통계 및 비교분석
- UTF-8 인코딩 수정
- safe_management 기준 반영
- descriptive reporting 정리
- result 저장 형식 통일
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# ============================================================
# 데이터 로드
# ============================================================
people = pd.read_csv("../clean/people_clean.csv").copy()
worker = pd.read_csv("../clean/worker_clean.csv").copy()

# ============================================================
# 재난 유형 라벨
# ============================================================
DISASTER_LABELS = [
    "태풍/강풍",
    "홍수/침수",
    "지진",
    "폭설/한파",
    "산사태",
    "가뭄",
    "폭염",
    "화재",
    "붕괴",
    "감염병",
    "방사능 사고",
    "환경오염 사고",
    "감염병",
    "가축전염병",
    "미세먼지"
]

# ============================================================
# 재난 유형별 인식 비교
# ============================================================
rows = []

for i, label in enumerate(DISASTER_LABELS, start=1):

    col_k1 = f"q14k1_{i}"
    col_k2 = f"q14k2_{i}"
    col_k3 = f"q14k3_{i}"
    col_k4 = f"q14k4_{i}"

    rows.append({
        "재난 유형": label,

        "심각성 인식 (M)": round(
            people[col_k1].mean(), 3
        ),

        "수집 필요성 (M)": round(
            people[col_k2].mean(), 3
        ),

        "공개 필요성 (M)": round(
            people[col_k3].mean(), 3
        ),

        "기관 간 공유 필요성 (M)": round(
            people[col_k4].mean(), 3
        ),

        "심각성 인식 (SD)": round(
            people[col_k1].std(), 3
        ),

        "수집 필요성 (SD)": round(
            people[col_k2].std(), 3
        ),

        "공개 필요성 (SD)": round(
            people[col_k3].std(), 3
        ),

        "기관 간 공유 필요성 (SD)": round(
            people[col_k4].std(), 3
        ),
    })

df_disaster = (
    pd.DataFrame(rows)
    .sort_values("심각성 인식 (M)", ascending=False)
)

# ============================================================
# 저장
# ============================================================
with open(
    "../result/disaster_type_comparison.txt",
    "w",
    encoding="utf-8-sig"
) as f:

    f.write("=" * 70 + "\n")
    f.write("재난 유형별 인식 비교\n")
    f.write("=" * 70 + "\n\n")

    f.write("[평균 비교]\n\n")

    f.write(
        df_disaster[
            [
                "재난 유형",
                "심각성 인식 (M)",
                "수집 필요성 (M)",
                "공개 필요성 (M)",
                "기관 간 공유 필요성 (M)"
            ]
        ].to_string(index=False)
    )

    f.write("\n\n")

    f.write("[표준편차]\n\n")

    f.write(
        df_disaster[
            [
                "재난 유형",
                "심각성 인식 (SD)",
                "수집 필요성 (SD)",
                "공개 필요성 (SD)",
                "기관 간 공유 필요성 (SD)"
            ]
        ].to_string(index=False)
    )

# ============================================================
# 개인정보 유형별 동의 수준
# ============================================================
INFO_LABELS = [
    "성명",
    "성별",
    "전화번호",
    "생년월일",
    "주소",
    "이메일 주소",
    "소속기관 정보",
    "계좌 및 금융정보",
    "신용정보",
    "사진",
    "가족 구성원 정보",
    "의료정보",
    "위치정보",
    "통신정보",
    "소득 및 소비정보"
]

rows_info = []

for i, label in enumerate(INFO_LABELS, start=1):

    col = f"q29_{i}"

    rows_info.append({
        "개인정보 유형": label,

        "제공 동의 수준 (M)": round(
            people[col].mean(), 3
        ),

        "SD": round(
            people[col].std(), 3
        ),

        "N": int(
            people[col].notna().sum()
        ),
    })

df_info = (
    pd.DataFrame(rows_info)
    .sort_values(
        "제공 동의 수준 (M)",
        ascending=False
    )
)

# ============================================================
# 저장
# ============================================================
with open(
    "../result/info_type_consent.txt",
    "w",
    encoding="utf-8-sig"
) as f:

    f.write("=" * 60 + "\n")
    f.write("개인정보 유형별 제공 동의 수준\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        df_info.to_string(index=False)
    )

# ============================================================
# 기관 신뢰 비교
# ============================================================
INSTITUTION_LABELS = [
    "질병관리청",
    "행정안전부",
    "소방청",
    "경찰청",
    "지방자치단체",
    "국립중앙의료원",
    "재난정보 주관부처"
]

rows_trust = []

for i, label in enumerate(INSTITUTION_LABELS, start=1):

    col = f"q27_{i}"

    rows_trust.append({
        "기관": label,

        "신뢰 수준 (M)": round(
            people[col].mean(), 3
        ),

        "SD": round(
            people[col].std(), 3
        ),

        "N": int(
            people[col].notna().sum()
        ),
    })

df_trust = (
    pd.DataFrame(rows_trust)
    .sort_values(
        "신뢰 수준 (M)",
        ascending=False
    )
)

# ============================================================
# 저장
# ============================================================
with open(
    "../result/institution_trust.txt",
    "w",
    encoding="utf-8-sig"
) as f:

    f.write("=" * 60 + "\n")
    f.write("기관별 신뢰 수준 비교\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        df_trust.to_string(index=False)
    )

# ============================================================
# 국민 vs 실무자 비교
# ============================================================

# 주의:
# 척도 자체가 완전히 동일하지 않음
# descriptive comparison 수준으로 제한

t, p = ttest_ind(
    people["safe_management"].dropna(),
    worker["safety"].dropna()
)

with open(
    "../result/worker_people_comparison.txt",
    "w",
    encoding="utf-8-sig"
) as f:

    f.write("=" * 70 + "\n")
    f.write("국민 vs 실무자 기술통계 비교\n")
    f.write("=" * 70 + "\n\n")

    f.write("[주의]\n")
    f.write("국민과 실무자는 측정 척도가 다르므로 직접 비교에는 한계가 있음.\n\n")

    # --------------------------------------------------------
    # 국민
    # --------------------------------------------------------
    f.write("[국민 표본]\n")

    f.write(
        f"consent               : M={people['consent'].mean():.3f}, "
        f"SD={people['consent'].std():.3f}\n"
    )

    f.write(
        f"manage_trust          : M={people['manage_trust'].mean():.3f}, "
        f"SD={people['manage_trust'].std():.3f}\n"
    )

    f.write(
        f"risk                  : M={people['risk'].mean():.3f}, "
        f"SD={people['risk'].std():.3f}\n"
    )

    f.write(
        f"trust                 : M={people['trust'].mean():.3f}, "
        f"SD={people['trust'].std():.3f}\n"
    )

    f.write(
        f"safe_management       : M={people['safe_management'].mean():.3f}, "
        f"SD={people['safe_management'].std():.3f}\n"
    )

    # --------------------------------------------------------
    # 실무자
    # --------------------------------------------------------
    f.write("\n[실무자 표본]\n")

    f.write(
        f"management            : M={worker['management'].mean():.3f}, "
        f"SD={worker['management'].std():.3f}\n"
    )

    f.write(
        f"safety                : M={worker['safety'].mean():.3f}, "
        f"SD={worker['safety'].std():.3f}\n"
    )

    # --------------------------------------------------------
    # t-test
    # --------------------------------------------------------
    f.write("\n[safe_management vs safety t-test]\n")

    f.write(
        f"t = {t:.4f}\n"
    )

    f.write(
        f"p = {p:.6f}\n"
    )

# ============================================================
# 콘솔 출력
# ============================================================
print("=" * 60)
print("Descriptive analysis completed")
print("=" * 60)

print("\nSaved files:")
print("- disaster_type_comparison.txt")
print("- info_type_consent.txt")
print("- institution_trust.txt")
print("- worker_people_comparison.txt")
