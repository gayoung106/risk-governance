import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

df = pd.read_csv("../clean/people_clean.csv")

X = df[['manage_trust','risk','safe_management']]
X = sm.add_constant(X)
y = df['consent']

model = sm.OLS(y, X).fit()

residuals = model.resid

plt.hist(residuals, bins=30)
plt.title("Residual Distribution")
plt.savefig("../result/residual_hist.png")

print("잔차 분석 완료")
