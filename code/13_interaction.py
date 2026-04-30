import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../clean/people_clean.csv")

df['interaction'] = df['manage_trust'] * df['risk']

X = df[['manage_trust','risk','interaction']]
X = sm.add_constant(X)

model = sm.OLS(df['consent'], X).fit()
print(model.summary())

with open("../result/interaction.txt", "w") as f:
    f.write(model.summary().as_text())