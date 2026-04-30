import pandas as pd
import pyreadstat
import os

# -------------------------
# 경로 설정
# -------------------------
RAW_PATH = "../raw"
CLEAN_PATH = "../clean"

os.makedirs(CLEAN_PATH, exist_ok=True)

# -------------------------
# 숫자 변환 함수
# -------------------------
def to_numeric_safe(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

# -------------------------
# 기타(9997, et) 제거
# -------------------------
def filter_valid_cols(cols):
    return [c for c in cols if not ('9997' in c or 'et' in c)]

# -------------------------
# SAV 안전 로드 (인코딩 해결)
# -------------------------
def safe_read_sav(path):
    try:
        print(f" {path} → cp949 시도")
        df, meta = pyreadstat.read_sav(path, encoding="cp949")
        print(" cp949 성공")
        return df
    except:
        print(" cp949 실패 → utf-8 시도")
        try:
            df, meta = pyreadstat.read_sav(path, encoding="utf-8")
            print(" utf-8 성공")
            return df
        except:
            print(" utf-8 실패 → fallback")
            df, meta = pyreadstat.read_sav(path, apply_value_formats=False)
            print(" fallback 성공")
            return df

# -------------------------
# 데이터 로드
# -------------------------
worker_df = safe_read_sav(f"{RAW_PATH}/raw_data_worker.sav")
people_df = safe_read_sav(f"{RAW_PATH}/raw_data_people.sav")

# -------------------------
# 컬럼명 정리
# -------------------------
worker_df.columns = worker_df.columns.str.lower()
people_df.columns = people_df.columns.str.lower()

print("\n people 컬럼 일부")
print(people_df.columns[:20])

print("\n worker 컬럼 일부")
print(worker_df.columns[:20])

# -------------------------
# 결측값 처리
# -------------------------
worker_df = worker_df.replace([99, 999, 9999], pd.NA)
people_df = people_df.replace([99, 999, 9999], pd.NA)

# -------------------------
#  PEOPLE 변수 생성
# -------------------------
consent_cols = filter_valid_cols(
    [c for c in people_df.columns if c.startswith(('q7','q8','q9'))]
)

manage_cols = filter_valid_cols(
    [c for c in people_df.columns if c.startswith(('q5','q6'))]
)

risk_cols = filter_valid_cols(
    [c for c in people_df.columns if c.startswith(('q21','q22'))]
)

trust_cols = filter_valid_cols(
    [c for c in people_df.columns if c.startswith(('q25','q26'))]
)

print("\n PEOPLE 변수 컬럼")
print("consent:", consent_cols)
print("manage:", manage_cols)
print("risk:", risk_cols)
print("trust:", trust_cols)

# 숫자 변환
people_df = to_numeric_safe(people_df, consent_cols)
people_df = to_numeric_safe(people_df, manage_cols)
people_df = to_numeric_safe(people_df, risk_cols)
people_df = to_numeric_safe(people_df, trust_cols)

# index 생성
if consent_cols:
    people_df['consent'] = people_df[consent_cols].mean(axis=1)

if manage_cols:
    people_df['manage_trust'] = people_df[manage_cols].mean(axis=1)

if risk_cols:
    people_df['risk'] = people_df[risk_cols].mean(axis=1)

if trust_cols:
    people_df['trust'] = people_df[trust_cols].mean(axis=1)

print(" PEOPLE 변수 생성 완료")

# -------------------------
#  WORKER 변수 생성
# -------------------------
management_cols = filter_valid_cols(
    [c for c in worker_df.columns if c.startswith(('q41','q42'))]
)

safety_cols = filter_valid_cols(
    [c for c in worker_df.columns if c.startswith(('q13','q31','q32'))]
)

print("\n WORKER 변수 컬럼")
print("management:", management_cols)
print("safety:", safety_cols)

# 숫자 변환
worker_df = to_numeric_safe(worker_df, management_cols)
worker_df = to_numeric_safe(worker_df, safety_cols)

# index 생성
if management_cols:
    worker_df['management'] = worker_df[management_cols].mean(axis=1)

if safety_cols:
    worker_df['safety'] = worker_df[safety_cols].mean(axis=1)

print(" WORKER 변수 생성 완료")

# -------------------------
# 저장
# -------------------------
worker_df.to_csv(f"{CLEAN_PATH}/worker_clean.csv", index=False, encoding="utf-8-sig")
people_df.to_csv(f"{CLEAN_PATH}/people_clean.csv", index=False, encoding="utf-8-sig")

print("\n 전처리 완료")
print(" clean 폴더 저장")

# -------------------------
# 결과 확인 출력
# -------------------------
print("\n PEOPLE sample")
print(people_df[['consent','manage_trust','risk','trust']].head())

print("\n WORKER sample")
print(worker_df[['management','safety']].head())