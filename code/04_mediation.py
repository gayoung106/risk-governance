import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../clean/people_clean.csv")

# -------------------------
# 1단계: safety ~ manage_trust
# -------------------------
X1 = sm.add_constant(df['manage_trust'])
model1 = sm.OLS(df['safety_perception'], X1).fit()

# -------------------------
# 2단계: trust ~ safety + manage_trust
# -------------------------
X2 = sm.add_constant(df[['safety_perception','manage_trust']])
model2 = sm.OLS(df['trust'], X2).fit()

# -------------------------
# 3단계: consent ~ trust + manage_trust + risk
# -------------------------
X3 = sm.add_constant(df[['trust','manage_trust','risk']])
model3 = sm.OLS(df['consent'], X3).fit()

# -------------------------
# 저장
# -------------------------
with open("../result/mediation.txt", "w") as f:
    f.write("=== Step 1 ===\n")
    f.write(model1.summary().as_text())
    f.write("\n\n=== Step 2 ===\n")
    f.write(model2.summary().as_text())
    f.write("\n\n=== Step 3 ===\n")
    f.write(model3.summary().as_text())

print("매개효과 분석 완료")