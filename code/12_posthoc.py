import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_csv("../clean/people_clean.csv")

df['trust_group'] = pd.qcut(df['trust'], 3, labels=['low','mid','high'])

tukey = pairwise_tukeyhsd(
    endog=df['consent'],
    groups=df['trust_group'],
    alpha=0.05
)

print(tukey)

with open("../result/posthoc.txt", "w") as f:
    f.write(str(tukey))