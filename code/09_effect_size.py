import pandas as pd

df = pd.read_csv("../clean/people_clean.csv")

corr = df[['consent','manage_trust','risk','trust']].corr()

print(corr)

with open("../result/effect_size.txt", "w") as f:
    f.write(corr.to_string())