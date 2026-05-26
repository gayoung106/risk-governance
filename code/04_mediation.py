import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.utils import resample

# =========================================================
# 데이터 로드
# =========================================================
df = pd.read_csv("../clean/people_clean.csv")

# =========================================================
# 결측 제거
# =========================================================
use_cols = [
    "consent",
    "trust",
    "manage_trust",
    "risk",
    "safe_management"
]

df = df[use_cols].dropna().copy()

# =========================================================
# 1. MEDIATOR MODEL
# trust ~ manage_trust + risk + safe_management
# =========================================================
X_m = sm.add_constant(
    df[["manage_trust", "risk", "safe_management"]]
)

mediator_model = sm.OLS(
    df["trust"],
    X_m
).fit()

# =========================================================
# 2. OUTCOME MODEL
# consent ~ trust + manage_trust + risk + safe_management
# =========================================================
X_y = sm.add_constant(
    df[["trust", "manage_trust", "risk", "safe_management"]]
)

outcome_model = sm.OLS(
    df["consent"],
    X_y
).fit()

# =========================================================
# 3. TOTAL EFFECT MODEL
# consent ~ manage_trust + risk + safe_management
# =========================================================
X_total = sm.add_constant(
    df[["manage_trust", "risk", "safe_management"]]
)

total_model = sm.OLS(
    df["consent"],
    X_total
).fit()

# =========================================================
# 4. EFFECT 계산
# =========================================================

# a-path
a = mediator_model.params["manage_trust"]

# b-path
b = outcome_model.params["trust"]

# direct effect (c')
direct_effect = outcome_model.params["manage_trust"]

# total effect (c)
total_effect = total_model.params["manage_trust"]

# indirect effect (ab)
indirect_effect = a * b

# proportion mediated
proportion_mediated = indirect_effect / total_effect

# =========================================================
# 5. BOOTSTRAP
# =========================================================
n_boot = 5000
boot_indirect = []

for i in range(n_boot):

    boot = resample(df, replace=True)

    # mediator
    X_m_boot = sm.add_constant(
        boot[["manage_trust", "risk", "safe_management"]]
    )

    mediator_boot = sm.OLS(
        boot["trust"],
        X_m_boot
    ).fit()

    # outcome
    X_y_boot = sm.add_constant(
        boot[["trust", "manage_trust", "risk", "safe_management"]]
    )

    outcome_boot = sm.OLS(
        boot["consent"],
        X_y_boot
    ).fit()

    a_boot = mediator_boot.params["manage_trust"]
    b_boot = outcome_boot.params["trust"]

    boot_indirect.append(a_boot * b_boot)

# =========================================================
# 6. BOOTSTRAP CI
# =========================================================
ci_lower = np.percentile(boot_indirect, 2.5)
ci_upper = np.percentile(boot_indirect, 97.5)

# =========================================================
# 7. 결과 저장
# =========================================================
with open("../result/bootstrap_mediation.txt", "w", encoding="utf-8-sig") as f:

    f.write("==================================================\n")
    f.write("BOOTSTRAP MEDIATION ANALYSIS\n")
    f.write("==================================================\n\n")

    f.write("==================================================\n")
    f.write("MEDIATOR MODEL\n")
    f.write("trust ~ manage_trust + risk + safe_management\n")
    f.write("==================================================\n\n")

    f.write(mediator_model.summary().as_text())

    f.write("\n\n")

    f.write("==================================================\n")
    f.write("OUTCOME MODEL\n")
    f.write("consent ~ trust + manage_trust + risk + safe_management\n")
    f.write("==================================================\n\n")

    f.write(outcome_model.summary().as_text())

    f.write("\n\n")

    f.write("==================================================\n")
    f.write("TOTAL EFFECT MODEL\n")
    f.write("consent ~ manage_trust + risk + safe_management\n")
    f.write("==================================================\n\n")

    f.write(total_model.summary().as_text())

    f.write("\n\n")

    f.write("==================================================\n")
    f.write("MEDIATION EFFECTS\n")
    f.write("==================================================\n\n")

    f.write(f"a-path (manage_trust → trust): {a:.6f}\n")
    f.write(f"b-path (trust → consent): {b:.6f}\n")
    f.write(f"Direct effect (c'): {direct_effect:.6f}\n")
    f.write(f"Indirect effect (ab): {indirect_effect:.6f}\n")
    f.write(f"Total effect (c): {total_effect:.6f}\n")
    f.write(f"Proportion mediated: {proportion_mediated:.6f}\n")

    f.write("\n")

    f.write("==================================================\n")
    f.write("BOOTSTRAP CONFIDENCE INTERVAL\n")
    f.write("==================================================\n\n")

    f.write(f"95% Bootstrap CI: [{ci_lower:.6f}, {ci_upper:.6f}]\n")

# =========================================================
# 콘솔 출력
# =========================================================
print("==================================================")
print("Bootstrap mediation analysis completed")
print("==================================================")

print(f"Indirect effect: {indirect_effect:.6f}")
print(f"95% CI: [{ci_lower:.6f}, {ci_upper:.6f}]")
