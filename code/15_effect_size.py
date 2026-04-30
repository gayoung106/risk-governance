
# trust 기준
ss_between = 86.446230
ss_total = 86.446230 + 556.254156

eta_sq = ss_between / ss_total

print("eta squared:", eta_sq)

with open("../result/effect_size.txt", "w") as f:
    f.write(f"eta_squared: {eta_sq:.4f}")