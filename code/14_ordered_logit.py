import pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel

df = pd.read_csv("../clean/people_clean.csv")

model = OrderedModel(
    df['consent'],
    df[['manage_trust','risk','safe_management']],
    distr='logit'
)

res = model.fit(method='bfgs')
print(res.summary())

with open("../result/ordered_logit.txt", "w") as f:
    f.write(str(res.summary()))
