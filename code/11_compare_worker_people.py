import pandas as pd
from scipy.stats import ttest_ind

people = pd.read_csv("../clean/people_clean.csv")
worker = pd.read_csv("../clean/worker_clean.csv")

# -------------------------
# 평균 비교
# -------------------------
people_mean = people['safe_management'].mean()
worker_mean = worker['safety'].mean()

print("people safety:", people_mean)
print("worker safety:", worker_mean)

# -------------------------
# t-test
# -------------------------
t, p = ttest_ind(
    people['safe_management'].dropna(),
    worker['safety'].dropna()
)

print("t-test:", t, p)

# -------------------------
# 저장
# -------------------------
with open("../result/compare_worker_people.txt", "w") as f:
    f.write(f"people_mean: {people_mean:.4f}\n")
    f.write(f"worker_mean: {worker_mean:.4f}\n")
    f.write(f"t-value: {t:.4f}\n")
    f.write(f"p-value: {p:.10f}\n")

print("저장 완료")
