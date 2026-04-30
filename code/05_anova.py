import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

df = pd.read_csv("../clean/people_clean.csv")

# -------------------------
# 그룹 변수 생성 (중요)
# -------------------------
df['risk_group'] = pd.qcut(df['risk'], 3, labels=['low','mid','high'])
df['trust_group'] = pd.qcut(df['trust'], 3, labels=['low','mid','high'])

# -------------------------
# ANOVA 1: risk → consent
# -------------------------
model1 = ols('consent ~ C(risk_group)', data=df).fit()
anova1 = sm.stats.anova_lm(model1, typ=2)

# -------------------------
# ANOVA 2: trust → consent
# -------------------------
model2 = ols('consent ~ C(trust_group)', data=df).fit()
anova2 = sm.stats.anova_lm(model2, typ=2)

# -------------------------
# ANOVA 3: safety → consent
# -------------------------
model3 = ols('consent ~ C(safety_perception)', data=df).fit()
anova3 = sm.stats.anova_lm(model3, typ=2)

# -------------------------
# 저장
# -------------------------
with open("../result/anova.txt", "w") as f:
    f.write("=== risk ANOVA ===\n")
    f.write(anova1.to_string())
    f.write("\n\n=== trust ANOVA ===\n")
    f.write(anova2.to_string())
    f.write("\n\n=== safety ANOVA ===\n")
    f.write(anova3.to_string())

print("ANOVA 완료")