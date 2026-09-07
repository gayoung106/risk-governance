from __future__ import annotations

import math
import os
import warnings
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyreadstat
import scipy.stats as st
import statsmodels.formula.api as smf
import statsmodels.api as sm
from patsy import dmatrices


warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "clean"
RAW = ROOT / "raw"
OUT = ROOT / "result" / "ssci_reanalysis"
OUT.mkdir(parents=True, exist_ok=True)

BOOT_N = 5000
RNG = np.random.default_rng(20260825)

PEOPLE_CORE = ["consent", "manage_trust", "risk", "trust", "safe_management"]
DEMO_CONTROLS = ["sq1", "sq2", "sq3_1"]
INFO_LABELS = {
    1: "Name",
    2: "Gender",
    3: "Phone number",
    4: "Date of birth",
    5: "Home address",
    6: "Email address",
    7: "Affiliation",
    8: "Financial account",
    9: "Credit information",
    10: "Photograph",
    11: "Family information",
    12: "Medical information",
    13: "Location information",
    14: "Communication records",
    15: "Habits/preferences",
}


def star(p: float) -> str:
    if pd.isna(p):
        return ""
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    if p < 0.1:
        return "+"
    return ""


def ci_from_boot(vals: np.ndarray) -> tuple[float, float]:
    vals = vals[np.isfinite(vals)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def tidy_result(model, terms: list[str] | None = None) -> pd.DataFrame:
    params = model.params
    bse = model.bse
    pvals = model.pvalues
    conf = model.conf_int()
    rows = []
    for term in (terms or list(params.index)):
        if term not in params.index:
            continue
        rows.append(
            {
                "term": term,
                "coef": params[term],
                "se": bse[term],
                "ci_low": conf.loc[term, 0],
                "ci_high": conf.loc[term, 1],
                "p": pvals[term],
                "sig": star(pvals[term]),
            }
        )
    return pd.DataFrame(rows)


def alpha(df: pd.DataFrame) -> float:
    x = df.dropna()
    k = x.shape[1]
    cov = x.cov()
    return float(k / (k - 1) * (1 - np.trace(cov) / cov.values.sum()))


def load_labels() -> dict[str, dict[str, str]]:
    labels = {}
    for key, path in {
        "people": RAW / "raw_data_people.sav",
        "worker": RAW / "raw_data_worker.SAV",
    }.items():
        _, meta = pyreadstat.read_sav(path, encoding="cp949", apply_value_formats=False)
        labels[key] = {k.lower(): v for k, v in meta.column_names_to_labels.items()}
    return labels


def residualize(y: pd.Series, x: pd.DataFrame) -> pd.Series:
    x = sm.add_constant(x, has_constant="add")
    return sm.OLS(y, x, missing="drop").fit().resid


def ols_beta(y: np.ndarray, x: np.ndarray, idx: np.ndarray | None = None) -> np.ndarray:
    if idx is not None:
        y = y[idx]
        x = x[idx, :]
    return np.linalg.lstsq(x, y, rcond=None)[0]


def run_main_models(people: pd.DataFrame) -> dict[str, object]:
    df = people[PEOPLE_CORE + DEMO_CONTROLS].dropna().copy()
    formula = "consent ~ manage_trust + risk + safe_management + sq1 + C(sq2) + sq3_1"
    ols = smf.ols(formula, df).fit()
    hc3 = ols.get_robustcov_results(cov_type="HC3")
    hc3 = sm.regression.linear_model.RegressionResultsWrapper(hc3)

    inter_df = df.copy()
    inter_df["manage_c"] = inter_df["manage_trust"] - inter_df["manage_trust"].mean()
    inter_df["risk_c"] = inter_df["risk"] - inter_df["risk"].mean()
    inter = smf.ols(
        "consent ~ manage_c * risk_c + safe_management + sq1 + C(sq2) + sq3_1",
        inter_df,
    ).fit(cov_type="HC3")
    base = smf.ols(
        "consent ~ manage_c + risk_c + safe_management + sq1 + C(sq2) + sq3_1",
        inter_df,
    ).fit(cov_type="HC3")
    delta_r2 = inter.rsquared - base.rsquared

    levels = {
        "-1SD": -inter_df["risk"].std(),
        "Mean": 0.0,
        "+1SD": inter_df["risk"].std(),
    }
    cov = inter.cov_params()
    slopes = []
    for label, val in levels.items():
        b = inter.params["manage_c"] + val * inter.params["manage_c:risk_c"]
        var = (
            cov.loc["manage_c", "manage_c"]
            + val**2 * cov.loc["manage_c:risk_c", "manage_c:risk_c"]
            + 2 * val * cov.loc["manage_c", "manage_c:risk_c"]
        )
        se = math.sqrt(var)
        z = b / se
        p = 2 * (1 - st.norm.cdf(abs(z)))
        slopes.append(
            {
                "risk_level": label,
                "risk_c_value": val,
                "slope": b,
                "se": se,
                "ci_low": b - 1.96 * se,
                "ci_high": b + 1.96 * se,
                "p": p,
                "sig": star(p),
            }
        )
    slopes = pd.DataFrame(slopes)

    xs = np.linspace(inter_df["manage_c"].quantile(0.02), inter_df["manage_c"].quantile(0.98), 80)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for label, rv in levels.items():
        pred = (
            inter.params["Intercept"]
            + inter.params["manage_c"] * xs
            + inter.params["risk_c"] * rv
            + inter.params["manage_c:risk_c"] * xs * rv
        )
        ax.plot(xs + inter_df["manage_trust"].mean(), pred, label=f"Risk {label}")
    ax.set_xlabel("Management trust")
    ax.set_ylabel("Policy acceptance")
    ax.set_title("Management Trust x Risk Perception")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "interaction_plot.png", dpi=300)
    plt.close(fig)

    tidy_result(
        hc3,
        # NOTE: sq2 is stored as float64 (1.0/2.0) in people_clean.csv, so patsy's
        # treatment coding labels the dummy "C(sq2)[T.2.0]", not "C(sq2)[T.2]".
        # The literal label must match model.params.index exactly or tidy_result()
        # silently drops the term.
        ["manage_trust", "risk", "safe_management", "sq1", "C(sq2)[T.2.0]", "sq3_1"],
    ).to_csv(
        OUT / "main_ols_hc3.csv", index=False, encoding="utf-8-sig"
    )
    tidy_result(inter, ["manage_c", "risk_c", "manage_c:risk_c", "safe_management"]).to_csv(
        OUT / "moderation_hc3.csv", index=False, encoding="utf-8-sig"
    )
    slopes.to_csv(OUT / "simple_slopes.csv", index=False, encoding="utf-8-sig")
    return {"df": df, "ols": ols, "hc3": hc3, "inter": inter, "slopes": slopes, "delta_r2": delta_r2}


def bootstrap_mediation(people: pd.DataFrame) -> dict[str, object]:
    df = people[PEOPLE_CORE + DEMO_CONTROLS].dropna().copy()
    med_formula = "trust ~ manage_trust + risk + safe_management + sq1 + C(sq2) + sq3_1"
    out_formula = "consent ~ manage_trust + trust + risk + safe_management + sq1 + C(sq2) + sq3_1"
    total_formula = "consent ~ manage_trust + risk + safe_management + sq1 + C(sq2) + sq3_1"
    med = smf.ols(med_formula, df).fit(cov_type="HC3")
    out = smf.ols(out_formula, df).fit(cov_type="HC3")
    total = smf.ols(total_formula, df).fit(cov_type="HC3")
    a = med.params["manage_trust"]
    b = out.params["trust"]
    direct = out.params["manage_trust"]
    indirect = a * b
    total_eff = total.params["manage_trust"]

    boots = []
    n = len(df)
    y_m, x_m = dmatrices(med_formula, df, return_type="dataframe")
    y_o, x_o = dmatrices(out_formula, df, return_type="dataframe")
    y_t, x_t = dmatrices(total_formula, df, return_type="dataframe")
    y_m_np, x_m_np = np.ravel(y_m.values), x_m.values
    y_o_np, x_o_np = np.ravel(y_o.values), x_o.values
    y_t_np, x_t_np = np.ravel(y_t.values), x_t.values
    m_manage_i = list(x_m.columns).index("manage_trust")
    o_trust_i = list(x_o.columns).index("trust")
    o_manage_i = list(x_o.columns).index("manage_trust")
    t_manage_i = list(x_t.columns).index("manage_trust")
    for _ in range(BOOT_N):
        idx = RNG.integers(0, n, n)
        try:
            mb = ols_beta(y_m_np, x_m_np, idx)
            ob = ols_beta(y_o_np, x_o_np, idx)
            tb = ols_beta(y_t_np, x_t_np, idx)
            boots.append(
                [
                    mb[m_manage_i],
                    ob[o_trust_i],
                    ob[o_manage_i],
                    mb[m_manage_i] * ob[o_trust_i],
                    tb[t_manage_i],
                ]
            )
        except Exception:
            continue
    boots = np.asarray(boots)
    rows = []
    for name, est, col in [
        ("a: Management trust -> Institutional trust", a, 0),
        ("b: Institutional trust -> Policy acceptance", b, 1),
        ("direct", direct, 2),
        ("indirect", indirect, 3),
        ("total", total_eff, 4),
    ]:
        lo, hi = ci_from_boot(boots[:, col])
        rows.append({"effect": name, "estimate": est, "boot_ci_low": lo, "boot_ci_high": hi})
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "mediation_bootstrap.csv", index=False, encoding="utf-8-sig")
    return {"df": df, "med": med, "out": out, "total": total, "summary": res, "boot": boots}


def bootstrap_moderated_mediation(people: pd.DataFrame) -> dict[str, object]:
    df = people[PEOPLE_CORE + DEMO_CONTROLS].dropna().copy()
    df["manage_c"] = df["manage_trust"] - df["manage_trust"].mean()
    df["risk_c"] = df["risk"] - df["risk"].mean()
    a_formula = "trust ~ manage_c * risk_c + safe_management + sq1 + C(sq2) + sq3_1"
    b_formula = "consent ~ manage_c + risk_c + trust + safe_management + sq1 + C(sq2) + sq3_1"
    a_mod = smf.ols(a_formula, df).fit(cov_type="HC3")
    b_mod = smf.ols(b_formula, df).fit(cov_type="HC3")
    b = b_mod.params["trust"]
    risk_sd = df["risk"].std()
    levels = {"-1SD": -risk_sd, "Mean": 0.0, "+1SD": risk_sd}
    rows = []
    for label, rv in levels.items():
        est = (a_mod.params["manage_c"] + a_mod.params["manage_c:risk_c"] * rv) * b
        rows.append({"risk_level": label, "risk_c_value": rv, "conditional_indirect": est})
    imm = a_mod.params["manage_c:risk_c"] * b

    n = len(df)
    y_a, x_a = dmatrices(a_formula, df, return_type="dataframe")
    y_b, x_b = dmatrices(b_formula, df, return_type="dataframe")
    y_a_np, x_a_np = np.ravel(y_a.values), x_a.values
    y_b_np, x_b_np = np.ravel(y_b.values), x_b.values
    a_manage_i = list(x_a.columns).index("manage_c")
    a_inter_i = list(x_a.columns).index("manage_c:risk_c")
    b_trust_i = list(x_b.columns).index("trust")
    cond_boot = {label: [] for label in levels}
    imm_boot = []
    for _ in range(BOOT_N):
        idx = RNG.integers(0, n, n)
        try:
            ab = ols_beta(y_a_np, x_a_np, idx)
            bbeta = ols_beta(y_b_np, x_b_np, idx)
            bb = bbeta[b_trust_i]
            for label, rv in levels.items():
                cond_boot[label].append((ab[a_manage_i] + ab[a_inter_i] * rv) * bb)
            imm_boot.append(ab[a_inter_i] * bb)
        except Exception:
            continue
    for row in rows:
        lo, hi = ci_from_boot(np.asarray(cond_boot[row["risk_level"]]))
        row["boot_ci_low"] = lo
        row["boot_ci_high"] = hi
    imm_lo, imm_hi = ci_from_boot(np.asarray(imm_boot))
    res = pd.DataFrame(rows)
    res.loc[len(res)] = {
        "risk_level": "Index of moderated mediation",
        "risk_c_value": np.nan,
        "conditional_indirect": imm,
        "boot_ci_low": imm_lo,
        "boot_ci_high": imm_hi,
    }
    res.to_csv(OUT / "moderated_mediation_bootstrap.csv", index=False, encoding="utf-8-sig")
    return {"a_model": a_mod, "b_model": b_mod, "summary": res}


def latent_policy_acceptance(people: pd.DataFrame) -> dict[str, object]:
    items = ["q7_1", "q8_1", "q9_1"]
    df = people[items + ["manage_trust", "risk", "safe_management", "trust"] + DEMO_CONTROLS].dropna().copy()
    z = (df[items] - df[items].mean()) / df[items].std(ddof=0)
    corr = z.corr().values
    eigval, eigvec = np.linalg.eigh(corr)
    first = eigvec[:, np.argmax(eigval)]
    if first.sum() < 0:
        first = -first
    loadings = first * math.sqrt(eigval.max())
    communalities = loadings**2
    cr = float(loadings.sum() ** 2 / (loadings.sum() ** 2 + np.sum(1 - communalities)))
    ave = float(np.mean(communalities))
    factor_score = z.values @ first
    df["latent_policy_score"] = (factor_score - factor_score.mean()) / factor_score.std(ddof=0)
    model = smf.ols(
        "latent_policy_score ~ manage_trust + risk + safe_management + trust + sq1 + C(sq2) + sq3_1",
        df,
    ).fit(cov_type="HC3")
    meas = pd.DataFrame(
        {
            "item": items,
            "standardized_loading_pca": loadings,
            "communality": communalities,
        }
    )
    meas.loc[len(meas)] = {"item": "Composite reliability", "standardized_loading_pca": cr, "communality": np.nan}
    meas.loc[len(meas)] = {"item": "AVE", "standardized_loading_pca": ave, "communality": np.nan}
    meas.loc[len(meas)] = {
        "item": "Model fit note",
        "standardized_loading_pca": np.nan,
        "communality": np.nan,
    }
    meas.to_csv(OUT / "latent_policy_measurement.csv", index=False, encoding="utf-8-sig")
    tidy_result(model, ["manage_trust", "risk", "safe_management", "trust"]).to_csv(
        OUT / "latent_policy_paths.csv", index=False, encoding="utf-8-sig"
    )
    return {"measurement": meas, "model": model}


def corrected_cov_regression(df: pd.DataFrame, y: str, predictors: list[str], reliability_var: str, reliability: float):
    dat = df[[y] + predictors].dropna()
    xvars = predictors
    s = dat[[y] + xvars].cov()
    means = dat[[y] + xvars].mean()
    s_xx = s.loc[xvars, xvars].copy()
    s_xy = s.loc[xvars, y].copy()
    s_xx.loc[reliability_var, reliability_var] = s_xx.loc[reliability_var, reliability_var] * reliability
    beta = np.linalg.solve(s_xx.values, s_xy.values)
    intercept = means[y] - np.dot(beta, means[xvars].values)
    return intercept, pd.Series(beta, index=xvars)


def single_indicator_sensitivity(people: pd.DataFrame) -> pd.DataFrame:
    df = people[PEOPLE_CORE + DEMO_CONTROLS].dropna().copy()
    a_formula = "trust ~ manage_trust + risk + safe_management + sq1 + C(sq2) + sq3_1"
    a_model = smf.ols(a_formula, df).fit()
    a_path = a_model.params["manage_trust"]
    y_a, x_a = dmatrices(a_formula, df, return_type="dataframe")
    y_a_np, x_a_np = np.ravel(y_a.values), x_a.values
    a_manage_i = list(x_a.columns).index("manage_trust")
    predictors = ["manage_trust", "trust", "risk", "safe_management", "sq1", "sq3_1"]
    rows = []
    n = len(df)
    for rel in [0.60, 0.70, 0.80, 0.90, 0.95]:
        _, beta = corrected_cov_regression(df, "consent", predictors, "trust", rel)
        b_path = beta["trust"]
        indirect = a_path * b_path
        boot_vals = []
        for _ in range(BOOT_N):
            idx = RNG.integers(0, n, n)
            sample = df.iloc[idx]
            try:
                aa = ols_beta(y_a_np, x_a_np, idx)[a_manage_i]
                _, bbeta = corrected_cov_regression(sample, "consent", predictors, "trust", rel)
                boot_vals.append(aa * bbeta["trust"])
            except Exception:
                continue
        lo, hi = ci_from_boot(np.asarray(boot_vals))
        rows.append(
            {
                "assumed_reliability": rel,
                "a_path": a_path,
                "b_path_corrected": b_path,
                "indirect_corrected": indirect,
                "boot_ci_low": lo,
                "boot_ci_high": hi,
                "conclusion_changes": "No" if lo > 0 or hi < 0 else "Yes/unclear",
            }
        )
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "single_indicator_trust_sensitivity.csv", index=False, encoding="utf-8-sig")
    return res


def information_type_heterogeneity(people: pd.DataFrame) -> dict[str, object]:
    qcols = [f"q29_{i}" for i in range(1, 16)]
    base_cols = ["id", "manage_trust", "risk", "safe_management"] + DEMO_CONTROLS
    df = people[base_cols + qcols].copy()
    long = df.melt(
        id_vars=base_cols,
        value_vars=qcols,
        var_name="info_col",
        value_name="item_consent",
    ).dropna()
    long["info_id"] = long["info_col"].str.extract(r"(\d+)$").astype(int)
    long["info_type"] = long["info_id"].map(INFO_LABELS)
    long["manage_c"] = long["manage_trust"] - long["manage_trust"].mean()
    long["risk_c"] = long["risk"] - long["risk"].mean()
    long["item_sensitivity_proxy"] = -long.groupby("info_type")["item_consent"].transform("mean")
    long["item_sensitivity_proxy_c"] = long["item_sensitivity_proxy"] - long["item_sensitivity_proxy"].mean()

    desc = (
        long.groupby(["info_id", "info_type"])["item_consent"]
        .agg(["count", "mean", "std"])
        .reset_index()
        .sort_values("mean")
    )
    desc.to_csv(OUT / "information_type_descriptives.csv", index=False, encoding="utf-8-sig")

    formula_fe = (
        "item_consent ~ manage_c * C(info_type) + risk_c * C(info_type) "
        "+ manage_c:risk_c + safe_management + sq1 + C(sq2) + sq3_1"
    )
    fe = smf.ols(formula_fe, long).fit(cov_type="cluster", cov_kwds={"groups": long["id"]})
    base = smf.ols(
        "item_consent ~ manage_c + risk_c + C(info_type) + manage_c:risk_c "
        "+ safe_management + sq1 + C(sq2) + sq3_1",
        long,
    ).fit(cov_type="cluster", cov_kwds={"groups": long["id"]})

    # A compact, interpretable sensitivity-proxy model. This uses the item mean as an empirical
    # proxy for item difficulty/sensitivity and should be described as exploratory.
    proxy = smf.ols(
        "item_consent ~ manage_c * item_sensitivity_proxy_c + risk_c * item_sensitivity_proxy_c "
        "+ manage_c:risk_c + safe_management + sq1 + C(sq2) + sq3_1",
        long,
    ).fit(cov_type="cluster", cov_kwds={"groups": long["id"]})

    slopes = []
    ref = sorted(long["info_type"].unique())[0]
    for info in sorted(long["info_type"].unique()):
        term = f"manage_c:C(info_type)[T.{info}]"
        slope = fe.params.get("manage_c", 0.0) + fe.params.get(term, 0.0)
        # Approximate CIs are easiest through linear constraints.
        constraint = f"manage_c + {term} = 0" if term in fe.params.index else "manage_c = 0"
        tt = fe.t_test(constraint)
        slopes.append(
            {
                "info_type": info,
                "manage_trust_slope": float(slope),
                "se": float(tt.sd[0][0]),
                "ci_low": float(tt.conf_int()[0][0]),
                "ci_high": float(tt.conf_int()[0][1]),
                "p": float(tt.pvalue),
                "sig": star(float(tt.pvalue)),
            }
        )
    slopes = pd.DataFrame(slopes).merge(desc[["info_type", "mean"]], on="info_type")
    slopes = slopes.sort_values("mean")
    slopes.to_csv(OUT / "information_type_management_slopes.csv", index=False, encoding="utf-8-sig")
    tidy_result(proxy, ["manage_c", "item_sensitivity_proxy_c", "manage_c:item_sensitivity_proxy_c", "risk_c:item_sensitivity_proxy_c"]).to_csv(
        OUT / "information_type_sensitivity_proxy.csv", index=False, encoding="utf-8-sig"
    )

    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    y = np.arange(len(slopes))
    ax.errorbar(
        slopes["manage_trust_slope"],
        y,
        xerr=[slopes["manage_trust_slope"] - slopes["ci_low"], slopes["ci_high"] - slopes["manage_trust_slope"]],
        fmt="o",
        color="#1f77b4",
        ecolor="#9bbad6",
        capsize=3,
    )
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(slopes["info_type"])
    ax.set_xlabel("Management-trust slope by information type")
    ax.set_title("Information-Type Heterogeneity")
    fig.tight_layout()
    fig.savefig(OUT / "information_type_slopes.png", dpi=300)
    plt.close(fig)

    return {"long": long, "fe": fe, "base": base, "proxy": proxy, "slopes": slopes, "desc": desc}


def practitioner_audit_and_comparison(people: pd.DataFrame, worker: pd.DataFrame, labels: dict[str, dict[str, str]]):
    rows = [
        {
            "construct": "Management trust",
            "people_items": "q5_1, q6_1",
            "worker_items": "No direct equivalent; closest worker items concern organizational practices or legal/procedural opinions.",
            "comparability": "Not comparable for structural model",
        },
        {
            "construct": "Risk perception",
            "people_items": "q21_1 leakage, q22_1 misuse",
            "worker_items": "q22_1 leakage, q25_1 misuse",
            "comparability": "Nearly identical",
        },
        {
            "construct": "Institutional trust",
            "people_items": "q26_1, q27_1-q27_7",
            "worker_items": "q32_1, q33_1-q33_7",
            "comparability": "Conceptually similar; q27/q33 agency series nearly identical but worker asks perception of general public trust",
        },
        {
            "construct": "Safety management perception",
            "people_items": "q25 binary",
            "worker_items": "q31_1 5-point",
            "comparability": "Conceptually similar but scale differs",
        },
        {
            "construct": "Policy acceptance",
            "people_items": "q7_1-q9_1; q29_1-q29_15 item-specific consent",
            "worker_items": "q37_1-q37_15 item-specific consent; q38_1 sharing consent",
            "comparability": "Item-specific consent comparable; core 3-item policy acceptance not fully comparable",
        },
    ]
    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / "citizen_worker_comparability_audit.csv", index=False, encoding="utf-8-sig")

    p = people.copy()
    w = worker.copy()
    p_info = p[[f"q29_{i}" for i in range(1, 16)]].mean(axis=1)
    w_info = w[[f"q37_{i}" for i in range(1, 16)]].mean(axis=1)
    p_risk = p[["q21_1", "q22_1"]].mean(axis=1)
    w_risk = w[["q22_1", "q25_1"]].mean(axis=1)
    p_agency = p[[f"q27_{i}" for i in range(1, 8)]].mean(axis=1)
    w_agency = w[[f"q33_{i}" for i in range(1, 8)]].mean(axis=1)
    comp_df = pd.DataFrame(
        {
            "citizen_info_consent": p_info,
            "worker_info_consent": pd.Series(w_info.values),
        }
    )

    def diff_row(name: str, citizen: pd.Series, worker_s: pd.Series) -> dict[str, float | str]:
        c = pd.to_numeric(citizen, errors="coerce").dropna()
        wv = pd.to_numeric(worker_s, errors="coerce").dropna()
        diff = c.mean() - wv.mean()
        pooled = math.sqrt(((len(c) - 1) * c.var(ddof=1) + (len(wv) - 1) * wv.var(ddof=1)) / (len(c) + len(wv) - 2))
        t, pval = st.ttest_ind(c, wv, equal_var=False)
        return {
            "measure": name,
            "citizen_n": len(c),
            "worker_n": len(wv),
            "citizen_mean": c.mean(),
            "worker_mean": wv.mean(),
            "difference_citizen_minus_worker": diff,
            "cohens_d": diff / pooled,
            "welch_p": pval,
        }

    comparisons = pd.DataFrame(
        [
            diff_row("Comparable item-specific consent mean", p_info, w_info),
            diff_row("Comparable risk mean", p_risk, w_risk),
            diff_row("Agency trust series mean", p_agency, w_agency),
        ]
    )
    comparisons.to_csv(OUT / "citizen_worker_descriptive_comparison.csv", index=False, encoding="utf-8-sig")
    return {"audit": audit, "comparisons": comparisons}


def reverse_and_alternative_specs(people: pd.DataFrame):
    df = people[PEOPLE_CORE + DEMO_CONTROLS].dropna().copy()
    specs = {
        "no_controls": "consent ~ manage_trust + risk + safe_management",
        "demographic_controls": "consent ~ manage_trust + risk + safe_management + sq1 + C(sq2) + sq3_1",
        "z_standardized": "z_consent ~ z_manage_trust + z_risk + z_safe_management + sq1 + C(sq2) + sq3_1",
        "interaction_controls": "consent ~ manage_trust * risk + safe_management + sq1 + C(sq2) + sq3_1",
    }
    zdf = df.copy()
    for col in ["consent", "manage_trust", "risk", "safe_management"]:
        zdf[f"z_{col}"] = (zdf[col] - zdf[col].mean()) / zdf[col].std()
    rows = []
    for name, formula in specs.items():
        dat = zdf if name == "z_standardized" else df
        mod = smf.ols(formula, dat).fit(cov_type="HC3")
        for term in ["manage_trust", "risk", "safe_management", "manage_trust:risk", "z_manage_trust", "z_risk", "z_safe_management"]:
            if term in mod.params.index:
                rows.append(
                    {
                        "specification": name,
                        "term": term,
                        "coef": mod.params[term],
                        "se": mod.bse[term],
                        "ci_low": mod.conf_int().loc[term, 0],
                        "ci_high": mod.conf_int().loc[term, 1],
                        "p": mod.pvalues[term],
                        "sig": star(mod.pvalues[term]),
                    }
                )
    alt = pd.DataFrame(rows)
    alt.to_csv(OUT / "alternative_specifications.csv", index=False, encoding="utf-8-sig")

    reverse_specs = {
        "management_trust_as_outcome": "manage_trust ~ consent + risk + safe_management + sq1 + C(sq2) + sq3_1",
        "institutional_trust_as_outcome": "trust ~ consent + manage_trust + risk + safe_management + sq1 + C(sq2) + sq3_1",
        "management_trust_from_policy_and_risk": "manage_trust ~ consent * risk + safe_management + sq1 + C(sq2) + sq3_1",
    }
    r_rows = []
    for name, formula in reverse_specs.items():
        mod = smf.ols(formula, df).fit(cov_type="HC3")
        for term in mod.params.index:
            if term == "Intercept" or term.startswith("C("):
                continue
            r_rows.append(
                {
                    "specification": name,
                    "term": term,
                    "coef": mod.params[term],
                    "se": mod.bse[term],
                    "ci_low": mod.conf_int().loc[term, 0],
                    "ci_high": mod.conf_int().loc[term, 1],
                    "p": mod.pvalues[term],
                    "sig": star(mod.pvalues[term]),
                }
            )
    rev = pd.DataFrame(r_rows)
    rev.to_csv(OUT / "reverse_order_specifications.csv", index=False, encoding="utf-8-sig")
    return {"alternative": alt, "reverse": rev}


def write_report(results: dict[str, object]):
    lines = []
    lines.append("# SSCI Reanalysis Report")
    lines.append("")
    lines.append("Core question: Does trust matter more when perceived privacy risk is high?")
    lines.append("")

    main = results["main"]
    med = results["mediation"]
    modmed = results["modmed"]
    latent = results["latent"]
    sens = results["single_indicator"]
    info = results["info"]
    group = results["group"]

    lines.append("## Step 1. Data and construct audit")
    lines.append(f"- Citizen sample: N={len(pd.read_csv(CLEAN / 'people_clean.csv'))}; practitioner sample: N={len(pd.read_csv(CLEAN / 'worker_clean.csv'))}.")
    lines.append("- Citizen core variables are available as policy acceptance, management trust, risk perception, institutional trust, and safe-management perception.")
    lines.append("- Citizen-practitioner structural comparison is not recommended for the main trust mechanism because management trust and the 3-item policy-acceptance outcome are not fully comparable.")
    lines.append("- Comparable citizen-practitioner analyses should be limited to item-specific information consent, leakage/misuse risk, and agency trust descriptives.")
    lines.append("Recommended location: Main text for citizen construct audit; Supplement for citizen-practitioner comparability details.")
    lines.append("")

    lines.append("## Step 2. Main OLS and HC3 association model")
    main_tbl = tidy_result(main["hc3"], ["manage_trust", "risk", "safe_management"])
    for _, r in main_tbl.iterrows():
        lines.append(f"- {r.term}: b={r.coef:.3f}, HC3 SE={r.se:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4f}{r.sig}")
    lines.append("Recommended location: Main text 4.2.")
    lines.append("")

    lines.append("## Step 3. Institutional-trust mediation")
    for _, r in med["summary"].iterrows():
        lines.append(f"- {r.effect}: estimate={r.estimate:.3f}, bootstrap 95% CI [{r.boot_ci_low:.3f}, {r.boot_ci_high:.3f}]")
    lines.append("Recommended location: Main text 4.3. Interpret as an indirect association, not causal mediation.")
    lines.append("")

    lines.append("## Step 4. Risk moderation")
    inter_tbl = tidy_result(main["inter"], ["manage_c", "risk_c", "manage_c:risk_c"])
    for _, r in inter_tbl.iterrows():
        lines.append(f"- {r.term}: b={r.coef:.3f}, HC3 SE={r.se:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4f}{r.sig}")
    lines.append(f"- Incremental R-squared for interaction: {main['delta_r2']:.4f}.")
    for _, r in main["slopes"].iterrows():
        lines.append(f"- Simple slope at risk {r.risk_level}: b={r.slope:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4f}{r.sig}")
    lines.append("Recommended location: Main text 4.4 with interaction_plot.png.")
    lines.append("")

    lines.append("## Step 5. Integrated moderated mediation")
    for _, r in modmed["summary"].iterrows():
        lines.append(f"- {r.risk_level}: estimate={r.conditional_indirect:.3f}, bootstrap 95% CI [{r.boot_ci_low:.3f}, {r.boot_ci_high:.3f}]")
    lines.append("Recommended location: Main text 4.5 if the IMM CI excludes zero; otherwise Supplement/robustness.")
    lines.append("")

    lines.append("## Step 6. Latent Policy Acceptance robustness")
    meas = latent["measurement"]
    cr = meas.loc[meas["item"] == "Composite reliability", "standardized_loading_pca"].iloc[0]
    ave = meas.loc[meas["item"] == "AVE", "standardized_loading_pca"].iloc[0]
    lines.append(f"- Three policy-acceptance items show CR={cr:.3f} and AVE={ave:.3f} in a one-factor score robustness check.")
    lines.append("- A 3-indicator single-factor CFA is just-identified, so global model fit is not substantively informative unless a larger measurement model is estimated.")
    lat_tbl = tidy_result(latent["model"], ["manage_trust", "risk", "safe_management", "trust"])
    for _, r in lat_tbl.iterrows():
        lines.append(f"- Latent-score path {r.term}: b={r.coef:.3f}, HC3 SE={r.se:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4f}{r.sig}")
    lines.append("Recommended location: Supplement, with a short main-text robustness sentence.")
    lines.append("")

    lines.append("## Step 7. Single-item institutional trust sensitivity")
    for _, r in sens.iterrows():
        lines.append(f"- Reliability {r.assumed_reliability:.2f}: a={r.a_path:.3f}, corrected b={r.b_path_corrected:.3f}, indirect={r.indirect_corrected:.3f}, bootstrap 95% CI [{r.boot_ci_low:.3f}, {r.boot_ci_high:.3f}], conclusion change={r.conclusion_changes}")
    lines.append("Recommended location: Online Supplement. Treat as measurement-error sensitivity, not a definitive latent SEM.")
    lines.append("")

    lines.append("## Step 8. Information-type heterogeneity")
    proxy_tbl = tidy_result(info["proxy"], ["manage_c", "item_sensitivity_proxy_c", "manage_c:item_sensitivity_proxy_c", "risk_c:item_sensitivity_proxy_c"])
    for _, r in proxy_tbl.iterrows():
        lines.append(f"- {r.term}: b={r.coef:.3f}, cluster SE={r.se:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4f}{r.sig}")
    top = info["slopes"].sort_values("manage_trust_slope", ascending=False).head(3)
    bottom = info["slopes"].sort_values("manage_trust_slope").head(3)
    lines.append("- Strongest management-trust slopes by information type: " + "; ".join(f"{r.info_type} ({r.manage_trust_slope:.3f})" for _, r in top.iterrows()))
    lines.append("- Weakest management-trust slopes by information type: " + "; ".join(f"{r.info_type} ({r.manage_trust_slope:.3f})" for _, r in bottom.iterrows()))
    lines.append("Recommended location: Main text 4.6 only if framed as heterogeneity with item fixed effects; otherwise Supplement.")
    lines.append("")

    lines.append("## Step 9. Citizen-practitioner comparison")
    for _, r in group["comparisons"].iterrows():
        lines.append(f"- {r.measure}: citizen mean={r.citizen_mean:.3f}, practitioner mean={r.worker_mean:.3f}, Cohen's d={r.cohens_d:.3f}, Welch p={r.welch_p:.4f}.")
    lines.append("Recommended location: Supplement, because the main structural variables are not fully comparable across samples.")
    lines.append("")

    lines.append("## Step 10. Interpretation rules and manuscript placement")
    lines.append("- Replace legitimacy-as-DV language with policy/data-use acceptance in Methods and Results.")
    lines.append("- Avoid claiming that management trust is substantively larger than safe-management perception based only on coefficient size, because the measures differ.")
    lines.append("- Move ANOVA/Tukey, residual histograms, Durbin-Watson, quadratic risk, disaster-type heatmaps, and agency mean comparisons to Supplement unless directly tied to the risk-trust mechanism.")
    lines.append("- State that cross-sectional covariance may be compatible with alternative orderings; results should be interpreted as theoretically specified associations rather than causal effects.")
    lines.append("")

    (OUT / "ssci_reanalysis_report.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    people = pd.read_csv(CLEAN / "people_clean.csv")
    worker = pd.read_csv(CLEAN / "worker_clean.csv")
    labels = load_labels()
    results = {
        "main": run_main_models(people),
        "mediation": bootstrap_mediation(people),
        "modmed": bootstrap_moderated_mediation(people),
        "latent": latent_policy_acceptance(people),
        "single_indicator": single_indicator_sensitivity(people),
        "info": information_type_heterogeneity(people),
        "group": practitioner_audit_and_comparison(people, worker, labels),
    }
    reverse_and_alternative_specs(people)
    write_report(results)
    print(f"Saved SSCI reanalysis outputs to {OUT}")


if __name__ == "__main__":
    main()
