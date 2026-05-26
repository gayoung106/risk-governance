import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# =========================================================
# 데이터 로드
# =========================================================
df = pd.read_csv("../clean/people_clean.csv").copy()

# =========================================================
# 그룹 변수 생성
# =========================================================
df["risk_group"] = pd.qcut(
    df["risk"],
    3,
    labels=["low", "mid", "high"]
)

df["trust_group"] = pd.qcut(
    df["trust"],
    3,
    labels=["low", "mid", "high"]
)

# =========================================================
# ANOVA 1
# risk → consent
# =========================================================
model1 = ols(
    "consent ~ C(risk_group)",
    data=df
).fit()

anova1 = sm.stats.anova_lm(
    model1,
    typ=2
)

# =========================================================
# ANOVA 2
# trust → consent
# =========================================================
model2 = ols(
    "consent ~ C(trust_group)",
    data=df
).fit()

anova2 = sm.stats.anova_lm(
    model2,
    typ=2
)

# =========================================================
# ANOVA 3
# safe_management → consent
# =========================================================
model3 = ols(
    "consent ~ C(safe_management)",
    data=df
).fit()

anova3 = sm.stats.anova_lm(
    model3,
    typ=2
)

# =========================================================
# 그룹 평균 계산
# =========================================================
risk_means = (
    df.groupby("risk_group")["consent"]
    .agg(["mean", "std", "count"])
)

trust_means = (
    df.groupby("trust_group")["consent"]
    .agg(["mean", "std", "count"])
)

safe_means = (
    df.groupby("safe_management")["consent"]
    .agg(["mean", "std", "count"])
)

# =========================================================
# 결과 저장
# =========================================================
with open(
    "../result/anova.txt",
    "w",
    encoding="utf-8-sig"
) as f:

    f.write("==================================================\n")
    f.write("ANOVA ANALYSIS\n")
    f.write("==================================================\n\n")

    # -----------------------------------------------------
    # RISK
    # -----------------------------------------------------
    f.write("==================================================\n")
    f.write("ANOVA 1: RISK → CONSENT\n")
    f.write("==================================================\n\n")

    f.write(anova1.to_string())

    f.write("\n\n")

    f.write("Group Means\n")
    f.write("----------------------------------------\n")
    f.write(risk_means.to_string())

    f.write("\n\n\n")

    # -----------------------------------------------------
    # TRUST
    # -----------------------------------------------------
    f.write("==================================================\n")
    f.write("ANOVA 2: TRUST → CONSENT\n")
    f.write("==================================================\n\n")

    f.write(anova2.to_string())

    f.write("\n\n")

    f.write("Group Means\n")
    f.write("----------------------------------------\n")
    f.write(trust_means.to_string())

    f.write("\n\n\n")

    # -----------------------------------------------------
    # SAFE MANAGEMENT
    # -----------------------------------------------------
    f.write("==================================================\n")
    f.write("ANOVA 3: SAFE MANAGEMENT → CONSENT\n")
    f.write("==================================================\n\n")

    f.write(anova3.to_string())

    f.write("\n\n")

    f.write("Group Means\n")
    f.write("----------------------------------------\n")
    f.write(safe_means.to_string())

# =========================================================
# 콘솔 출력
# =========================================================
print("==================================================")
print("ANOVA analysis completed")
print("==================================================")

print("\n[RISK GROUP]")
print(risk_means)

print("\n[TRUST GROUP]")
print(trust_means)

print("\n[SAFE MANAGEMENT]")
print(safe_means)
