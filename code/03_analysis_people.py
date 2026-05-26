import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../clean/people_clean.csv")

# -------------------------
# 湲곕낯 ?듦퀎
# -------------------------
summary = df[['consent','manage_trust','risk','trust','safe_management']].describe()

with open("../result/people_summary.txt", "w") as f:
    f.write(summary.to_string())

print(summary)

# -------------------------
# ?뚭? 紐⑤뜽 1
# -------------------------
X = df[['manage_trust','risk','safe_management']]
X = sm.add_constant(X)
y = df['consent']

model = sm.OLS(y, X).fit()

with open("../result/regression_result.txt", "w") as f:
    f.write(model.summary().as_text())

print(model.summary())
