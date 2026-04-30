import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../clean/people_clean.csv")

df['high_trust'] = (df['trust'] > df['trust'].median()).astype(int)

X = df[['manage_trust','risk']]
X = sm.add_constant(X)

model = sm.OLS(df['consent'], X).fit()

print(model.summary())