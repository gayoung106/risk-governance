import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../clean/people_clean.csv")

X = df[['manage_trust','risk','safety_perception']]
X = sm.add_constant(X)
y = df['consent']

model = sm.OLS(y, X).fit(cov_type='HC3')

with open("../result/robust.txt", "w") as f:
    f.write(model.summary().as_text())

print(model.summary())