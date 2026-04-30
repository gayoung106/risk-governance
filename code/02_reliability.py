import pandas as pd

df = pd.read_csv("../clean/people_clean.csv")

# -------------------------
# Cronbach Alpha 함수
# -------------------------
def cronbach_alpha(df_items):
    df_items = df_items.dropna()
    item_scores = df_items.values

    item_variances = item_scores.var(axis=0, ddof=1)
    total_score = item_scores.sum(axis=1)
    n_items = df_items.shape[1]

    return (n_items / (n_items - 1)) * (
        1 - (item_variances.sum() / total_score.var(ddof=1))
    )

# -------------------------
# 변수 그룹 정의
# -------------------------
consent_cols = [c for c in df.columns if c.startswith(('q7','q8','q9'))]
manage_cols = [c for c in df.columns if c.startswith(('q5','q6'))]
risk_cols = [c for c in df.columns if c.startswith(('q21','q22'))]

# -------------------------
# Alpha 계산
# -------------------------
results = {}

if len(consent_cols) > 1:
    results['consent_alpha'] = cronbach_alpha(df[consent_cols])

if len(manage_cols) > 1:
    results['manage_alpha'] = cronbach_alpha(df[manage_cols])

if len(risk_cols) > 1:
    results['risk_alpha'] = cronbach_alpha(df[risk_cols])

# -------------------------
# 결과 저장
# -------------------------
with open("../result/reliability.txt", "w") as f:
    for k, v in results.items():
        f.write(f"{k}: {v:.4f}\n")

print(results)