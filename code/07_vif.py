import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("../clean/people_clean.csv")

X = df[['manage_trust','risk','safe_management']]
X = X.dropna()

vif = pd.DataFrame()
vif["variable"] = X.columns
vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif)

with open("../result/vif.txt", "w") as f:
    f.write(vif.to_string())
