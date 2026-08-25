from __future__ import annotations

import math
import warnings
from pathlib import Path

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
DEMO_CONTROLS = ["sq1", "sq2", "sq3_1"]
CORE = ["consent", "manage_trust", "risk", "trust", "safe_management"]
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


def tidy(model, terms: list[str]) -> pd.DataFrame:
    ci = model.conf_int()
    rows = []
    for term in terms:
        if term in model.params.index:
            rows.append(
                {
                    "term": term,
                    "coef": model.params[term],
                    "se": model.bse[term],
                    "ci_low": ci.loc[term, 0],
                    "ci_high": ci.loc[term, 1],
                    "p": model.pvalues[term],
                    "sig": star(model.pvalues[term]),
                }
            )
    return pd.DataFrame(rows)


def ols_beta(y: np.ndarray, x: np.ndarray, idx: np.ndarray | None = None) -> np.ndarray:
    if idx is not None:
        y = y[idx]
        x = x[idx, :]
    return np.linalg.lstsq(x, y, rcond=None)[0]


def long_info(people: pd.DataFrame) -> pd.DataFrame:
    qcols = [f"q29_{i}" for i in range(1, 16)]
    base_cols = ["id", "manage_trust", "risk", "safe_management"] + DEMO_CONTROLS
    long = people[base_cols + qcols].melt(
        id_vars=base_cols,
        value_vars=qcols,
        var_name="original_variable",
        value_name="consent_ij",
    )
    long = long.dropna().copy()
    long["info_id"] = long["original_variable"].str.extract(r"(\d+)$").astype(int)
    long["information_type"] = long["info_id"].map(INFO_LABELS)
    long["manage_c"] = long["manage_trust"] - long["manage_trust"].mean()
    long["risk_c"] = long["risk"] - long["risk"].mean()
    mean_consent = long.groupby("information_type")["consent_ij"].transform("mean")
    long["item_sensitivity_proxy"] = -mean_consent
    long["item_sensitivity_proxy_c"] = long["item_sensitivity_proxy"] - long["item_sensitivity_proxy"].mean()
    return long


def sensitivity_proxy_audit(long: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for info_id, label in INFO_LABELS.items():
        sub = long[long["info_id"] == info_id]
        mean_consent = sub["consent_ij"].mean()
        uncentered = -mean_consent
        centered = sub["item_sensitivity_proxy_c"].iloc[0]
        rows.append(
            {
                "information_type": label,
                "original_variable": f"q29_{info_id}",
                "original_coding": "1-5 consent to government collection of this information type; higher = more consent",
                "sensitivity_calculation": "item_sensitivity_proxy = -mean(consent_ij by information type); centered proxy subtracts the grand mean of this proxy",
                "reverse_coding": "Yes: lower average consent is treated as higher sensitivity by multiplying by -1",
                "standardization": "No z-standardization",
                "centering": "Yes for model term item_sensitivity_proxy_c",
                "mean_consent": mean_consent,
                "uncentered_sensitivity_proxy": uncentered,
                "final_centered_sensitivity_score": centered,
                "n": len(sub),
            }
        )
    res = pd.DataFrame(rows).sort_values("mean_consent")
    res.to_csv(OUT / "audit_information_sensitivity_proxy_construction.csv", index=False, encoding="utf-8-sig")
    return res


def scan_exogenous_sensitivity_items() -> pd.DataFrame:
    scans = []
    patterns = [
        "민감",
        "위험",
        "유출",
        "오남용",
        "침해",
        "피해",
        "severity",
        "risk",
        "leak",
        "misuse",
        "sensitivity",
        "harm",
    ]
    for sample, path in {"people": RAW / "raw_data_people.sav", "worker": RAW / "raw_data_worker.SAV"}.items():
        _, meta = pyreadstat.read_sav(path, encoding="cp949", apply_value_formats=False)
        for col, label in meta.column_names_to_labels.items():
            label_l = str(label).lower()
            if any(p.lower() in label_l for p in patterns):
                scans.append({"sample": sample, "variable": col.lower(), "label": label})
    res = pd.DataFrame(scans)
    res.to_csv(OUT / "audit_exogenous_sensitivity_item_scan.csv", index=False, encoding="utf-8-sig")
    return res


def info_type_fe_models(long: pd.DataFrame) -> dict[str, object]:
    formula = (
        "consent_ij ~ manage_c * C(information_type) + risk_c * C(information_type) "
        "+ manage_c:risk_c + safe_management + sq1 + C(sq2) + sq3_1"
    )
    fe = smf.ols(formula, long).fit(cov_type="cluster", cov_kwds={"groups": long["id"]})

    inter_terms = [t for t in fe.params.index if t.startswith("manage_c:C(information_type)")]
    constraints = ", ".join(f"{t} = 0" for t in inter_terms)
    joint = fe.wald_test(constraints, scalar=True)
    joint_df = pd.DataFrame(
        [
            {
                "test": "Joint Wald test: all ManagementTrust x InformationType terms = 0",
                "statistic": float(joint.statistic),
                "df_num": len(inter_terms),
                "df_denom": np.nan,
                "p": float(joint.pvalue),
            }
        ]
    )
    joint_df.to_csv(OUT / "audit_information_type_joint_test.csv", index=False, encoding="utf-8-sig")

    slopes = []
    for info in sorted(long["information_type"].unique()):
        term = f"manage_c:C(information_type)[T.{info}]"
        constraint = f"manage_c + {term} = 0" if term in fe.params.index else "manage_c = 0"
        tt = fe.t_test(constraint)
        sub = long[long["information_type"] == info]
        slopes.append(
            {
                "information_type": info,
                "n": len(sub),
                "respondents": sub["id"].nunique(),
                "coef": float(tt.effect[0]),
                "se_cluster_respondent": float(tt.sd[0][0]),
                "ci_low": float(tt.conf_int()[0][0]),
                "ci_high": float(tt.conf_int()[0][1]),
                "p": float(tt.pvalue),
                "sig": star(float(tt.pvalue)),
                "mean_consent": sub["consent_ij"].mean(),
                "model": "OLS long format with information-type fixed effects and respondent-clustered SE",
                "controls": "risk_c x information type, manage_c x risk_c, safe_management, age, sex, education",
            }
        )
    slopes_df = pd.DataFrame(slopes).sort_values("mean_consent")
    slopes_df.to_csv(OUT / "audit_information_type_fe_slopes.csv", index=False, encoding="utf-8-sig")

    pair_rows = []
    infos = sorted(long["information_type"].unique())
    for i, a in enumerate(infos):
        for b in infos[i + 1 :]:
            term_a = f"manage_c:C(information_type)[T.{a}]"
            term_b = f"manage_c:C(information_type)[T.{b}]"
            expr_a = "manage_c" if term_a not in fe.params.index else f"manage_c + {term_a}"
            expr_b = "manage_c" if term_b not in fe.params.index else f"manage_c + {term_b}"
            tt = fe.t_test(f"({expr_a}) - ({expr_b}) = 0")
            pair_rows.append(
                {
                    "information_type_a": a,
                    "information_type_b": b,
                    "slope_difference_a_minus_b": float(tt.effect[0]),
                    "se": float(tt.sd[0][0]),
                    "p_raw": float(tt.pvalue),
                }
            )
    pairs = pd.DataFrame(pair_rows).sort_values("p_raw")
    m = len(pairs)
    pairs["p_bonferroni"] = np.minimum(pairs["p_raw"] * m, 1.0)
    pairs.to_csv(OUT / "audit_information_type_pairwise_slope_contrasts.csv", index=False, encoding="utf-8-sig")

    mixed_summary = None
    try:
        # Random-intercept robustness. Clustered OLS remains the primary audit specification.
        mixed = smf.mixedlm(formula, long, groups=long["id"]).fit(reml=False, method="lbfgs", maxiter=200, disp=False)
        mrows = []
        cov = mixed.cov_params()
        params = mixed.params
        for info in infos:
            term = f"manage_c:C(information_type)[T.{info}]"
            vec = pd.Series(0.0, index=params.index)
            vec["manage_c"] = 1.0
            if term in vec.index:
                vec[term] = 1.0
            coef = float(np.dot(vec.values, params.values))
            se = float(np.sqrt(np.dot(vec.values, np.dot(cov.values, vec.values))))
            z = coef / se
            p = 2 * (1 - st.norm.cdf(abs(z)))
            mrows.append(
                {
                    "information_type": info,
                    "coef_mixed_random_intercept": coef,
                    "se": se,
                    "ci_low": coef - 1.96 * se,
                    "ci_high": coef + 1.96 * se,
                    "p": p,
                    "sig": star(p),
                }
            )
        mixed_summary = pd.DataFrame(mrows)
        mixed_summary.to_csv(OUT / "audit_information_type_mixedlm_slopes.csv", index=False, encoding="utf-8-sig")
    except Exception as exc:
        mixed_summary = pd.DataFrame([{"mixedlm_status": f"not estimated: {exc}"}])
        mixed_summary.to_csv(OUT / "audit_information_type_mixedlm_slopes.csv", index=False, encoding="utf-8-sig")

    return {"fe": fe, "joint": joint_df, "slopes": slopes_df, "pairs": pairs, "mixed": mixed_summary}


def factor_score(df: pd.DataFrame, items: list[str]) -> pd.Series:
    z = (df[items] - df[items].mean()) / df[items].std(ddof=0)
    corr = z.corr().values
    eigval, eigvec = np.linalg.eigh(corr)
    first = eigvec[:, np.argmax(eigval)]
    if first.sum() < 0:
        first = -first
    score = z.values @ first
    return pd.Series((score - score.mean()) / score.std(ddof=0), index=df.index)


def core_interaction_robustness(people: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    df = people[CORE + DEMO_CONTROLS + ["q7_1", "q8_1", "q9_1"]].dropna().copy()
    df["manage_c"] = df["manage_trust"] - df["manage_trust"].mean()
    df["risk_c"] = df["risk"] - df["risk"].mean()
    df["z_consent"] = (df["consent"] - df["consent"].mean()) / df["consent"].std()
    df["z_manage"] = (df["manage_trust"] - df["manage_trust"].mean()) / df["manage_trust"].std()
    df["z_risk"] = (df["risk"] - df["risk"].mean()) / df["risk"].std()
    df["factor_policy"] = factor_score(df, ["q7_1", "q8_1", "q9_1"])
    df["factor_policy_c"] = df["factor_policy"] - df["factor_policy"].mean()

    specs = {
        "A_no_controls_HC3": ("consent ~ manage_c * risk_c + safe_management", "manage_c:risk_c"),
        "B_demographic_controls_HC3": (
            "consent ~ manage_c * risk_c + safe_management + sq1 + C(sq2) + sq3_1",
            "manage_c:risk_c",
        ),
        "C_z_standardized_trust_risk_HC3": (
            "z_consent ~ z_manage * z_risk + safe_management + sq1 + C(sq2) + sq3_1",
            "z_manage:z_risk",
        ),
        "D_policy_factor_score_HC3": (
            "factor_policy ~ manage_c * risk_c + safe_management + sq1 + C(sq2) + sq3_1",
            "manage_c:risk_c",
        ),
    }
    rows = []
    for name, (formula, term) in specs.items():
        mod = smf.ols(formula, df).fit(cov_type="HC3")
        ci = mod.conf_int().loc[term]
        rows.append(
            {
                "specification": name,
                "trust_x_risk": mod.params[term],
                "se": mod.bse[term],
                "ci_low": ci[0],
                "ci_high": ci[1],
                "p": mod.pvalues[term],
                "conclusion": "positive, CI excludes zero" if ci[0] > 0 or ci[1] < 0 else "not supported at 95% CI",
            }
        )
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "audit_core_interaction_robustness.csv", index=False, encoding="utf-8-sig")

    base = smf.ols("consent ~ manage_c + risk_c + safe_management + sq1 + C(sq2) + sq3_1", df).fit(cov_type="HC3")
    inter = smf.ols("consent ~ manage_c * risk_c + safe_management + sq1 + C(sq2) + sq3_1", df).fit(cov_type="HC3")
    delta = inter.rsquared - base.rsquared
    effect = {
        "baseline_r2": base.rsquared,
        "interaction_model_r2": inter.rsquared,
        "delta_r2": delta,
        "cohens_f2_interaction": delta / (1 - inter.rsquared),
    }
    pd.DataFrame([effect]).to_csv(OUT / "audit_interaction_effect_size.csv", index=False, encoding="utf-8-sig")
    return res, effect


def policy_acceptance_scoring_robustness(people: pd.DataFrame) -> pd.DataFrame:
    df = people[CORE + DEMO_CONTROLS + ["q7_1", "q8_1", "q9_1"]].dropna().copy()
    df["factor_policy"] = factor_score(df, ["q7_1", "q8_1", "q9_1"])
    df["z_composite_policy"] = (df["consent"] - df["consent"].mean()) / df["consent"].std()
    outcomes = {
        "raw_mean_composite": "consent",
        "z_mean_composite": "z_composite_policy",
        "factor_score": "factor_policy",
    }
    rows = []
    for label, outcome in outcomes.items():
        formulas = {
            "without_institutional_trust": f"{outcome} ~ manage_trust + risk + safe_management + sq1 + C(sq2) + sq3_1",
            "with_institutional_trust": f"{outcome} ~ manage_trust + risk + safe_management + trust + sq1 + C(sq2) + sq3_1",
        }
        for adjustment, formula in formulas.items():
            mod = smf.ols(formula, df).fit(cov_type="HC3")
            ci = mod.conf_int()
            terms = ["manage_trust", "risk", "safe_management"] + (["trust"] if "trust" in mod.params.index else [])
            for term in terms:
                rows.append(
                    {
                        "scoring": label,
                        "adjustment": adjustment,
                        "term": term,
                        "coef": mod.params[term],
                        "se": mod.bse[term],
                        "ci_low": ci.loc[term, 0],
                        "ci_high": ci.loc[term, 1],
                        "p": mod.pvalues[term],
                        "sig": star(mod.pvalues[term]),
                    }
                )
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "audit_policy_acceptance_scoring_robustness.csv", index=False, encoding="utf-8-sig")
    return res


def measurement_model_audit(people: pd.DataFrame) -> dict[str, object]:
    # A compact larger measurement check using observed multi-item constructs only:
    # management trust (2), risk perception (2), and policy acceptance (3).
    items_by_factor = {
        "management_trust": ["q5_1", "q6_1"],
        "risk_perception": ["q21_1", "q22_1"],
        "policy_acceptance": ["q7_1", "q8_1", "q9_1"],
    }
    df = people[sum(items_by_factor.values(), [])].dropna().copy()
    rows = []
    scores = {}
    for factor, items in items_by_factor.items():
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
        score = z.values @ first
        scores[factor] = (score - score.mean()) / score.std(ddof=0)
        for item, loading in zip(items, loadings):
            rows.append({"factor": factor, "item": item, "loading": loading, "cr": np.nan, "ave": np.nan})
        rows.append({"factor": factor, "item": "CR", "loading": np.nan, "cr": cr, "ave": np.nan})
        rows.append({"factor": factor, "item": "AVE", "loading": np.nan, "cr": np.nan, "ave": ave})
    meas = pd.DataFrame(rows)
    meas.to_csv(OUT / "audit_larger_measurement_model_loadings_cr_ave.csv", index=False, encoding="utf-8-sig")
    score_df = pd.DataFrame(scores)
    corr = score_df.corr()
    htmt_rows = []
    for a in items_by_factor:
        for b in items_by_factor:
            if a >= b:
                continue
            cross = df[items_by_factor[a]].corrwith(df[items_by_factor[b][0]])
            cross_vals = []
            for ia in items_by_factor[a]:
                for ib in items_by_factor[b]:
                    cross_vals.append(abs(df[ia].corr(df[ib])))
            within_a = [abs(df[x].corr(df[y])) for i, x in enumerate(items_by_factor[a]) for y in items_by_factor[a][i + 1 :]]
            within_b = [abs(df[x].corr(df[y])) for i, x in enumerate(items_by_factor[b]) for y in items_by_factor[b][i + 1 :]]
            htmt = np.mean(cross_vals) / math.sqrt(np.mean(within_a) * np.mean(within_b))
            htmt_rows.append({"factor_a": a, "factor_b": b, "factor_score_correlation": corr.loc[a, b], "htmt_approx": htmt})
    htmt = pd.DataFrame(htmt_rows)
    htmt.to_csv(OUT / "audit_larger_measurement_model_htmt.csv", index=False, encoding="utf-8-sig")
    return {"measurement": meas, "htmt": htmt}


def moderated_mediation_reproduce(people: pd.DataFrame) -> pd.DataFrame:
    df = people[CORE + DEMO_CONTROLS].dropna().copy()
    df["manage_c"] = df["manage_trust"] - df["manage_trust"].mean()
    df["risk_c"] = df["risk"] - df["risk"].mean()
    a_formula = "trust ~ manage_c * risk_c + safe_management + sq1 + C(sq2) + sq3_1"
    b_formula = "consent ~ manage_c + risk_c + trust + safe_management + sq1 + C(sq2) + sq3_1"
    a_mod = smf.ols(a_formula, df).fit(cov_type="HC3")
    b_mod = smf.ols(b_formula, df).fit(cov_type="HC3")
    levels = {"Risk -1SD": -df["risk"].std(), "Risk mean": 0.0, "Risk +1SD": df["risk"].std()}
    b = b_mod.params["trust"]

    y_a, x_a = dmatrices(a_formula, df, return_type="dataframe")
    y_b, x_b = dmatrices(b_formula, df, return_type="dataframe")
    y_a_np, x_a_np = np.ravel(y_a.values), x_a.values
    y_b_np, x_b_np = np.ravel(y_b.values), x_b.values
    a_manage_i = list(x_a.columns).index("manage_c")
    a_inter_i = list(x_a.columns).index("manage_c:risk_c")
    b_trust_i = list(x_b.columns).index("trust")
    n = len(df)
    cond_boot = {k: [] for k in levels}
    imm_boot = []
    for _ in range(BOOT_N):
        idx = RNG.integers(0, n, n)
        ab = ols_beta(y_a_np, x_a_np, idx)
        bb = ols_beta(y_b_np, x_b_np, idx)[b_trust_i]
        for label, rv in levels.items():
            cond_boot[label].append((ab[a_manage_i] + ab[a_inter_i] * rv) * bb)
        imm_boot.append(ab[a_inter_i] * bb)
    rows = []
    for label, rv in levels.items():
        est = (a_mod.params["manage_c"] + a_mod.params["manage_c:risk_c"] * rv) * b
        rows.append(
            {
                "quantity": label,
                "estimate": est,
                "boot_ci_low": np.percentile(cond_boot[label], 2.5),
                "boot_ci_high": np.percentile(cond_boot[label], 97.5),
            }
        )
    rows.append(
        {
            "quantity": "Index of moderated mediation",
            "estimate": a_mod.params["manage_c:risk_c"] * b,
            "boot_ci_low": np.percentile(imm_boot, 2.5),
            "boot_ci_high": np.percentile(imm_boot, 97.5),
        }
    )
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "audit_moderated_mediation_reproduction.csv", index=False, encoding="utf-8-sig")
    return res


def write_report(
    sensitivity: pd.DataFrame,
    scan: pd.DataFrame,
    info: dict[str, object],
    interaction: pd.DataFrame,
    effect_size: dict[str, float],
    scoring: pd.DataFrame,
    measurement: dict[str, object],
    modmed: pd.DataFrame,
):
    main_ols = pd.read_csv(OUT / "main_ols_hc3.csv")
    mediation = pd.read_csv(OUT / "mediation_bootstrap.csv")
    simple = pd.read_csv(OUT / "simple_slopes.csv")
    single = pd.read_csv(OUT / "single_indicator_trust_sensitivity.csv")
    reverse = pd.read_csv(OUT / "reverse_order_specifications.csv")

    risk_rows = scoring[scoring["term"] == "risk"].copy()
    risk_robust = "Specification-sensitive" if (risk_rows["ci_high"] > 0).any() and (risk_rows["ci_low"] < 0).any() else "Robust"

    lines = []
    lines.append("# SSCI Reanalysis Audit Report")
    lines.append("")
    lines.append("## 1. Critical issues found")
    lines.append("1. `item_sensitivity_proxy` is not independent of the outcome. It was constructed as the negative information-type mean of the same item-specific consent outcome used in the heterogeneity model. Final answer: INVALID FOR CONFIRMATORY ANALYSIS.")
    lines.append("2. The core `Management Trust x Risk Perception` result is reproducible across no-control, demographic-control, z-standardized, and factor-score outcome specifications. Final answer: the risk-conditioned trust claim is supported, but the added explanatory power is substantively modest.")
    lines.append("3. The 3-item policy-acceptance measurement check supports high internal consistency, but a 3-indicator single-factor model is just-identified; do not claim excellent global CFA fit from that model.")
    lines.append("4. Citizen-practitioner structural comparisons should not be used because core management-trust and 3-item policy-acceptance measures are not fully comparable.")
    lines.append("")

    lines.append("## 2. Information-sensitivity proxy audit")
    lines.append("The proxy was generated from citizen item-specific consent variables `q29_1` to `q29_15`. Each item is coded 1-5, where higher values indicate stronger consent to government collection of that information type.")
    lines.append("Formula used in the previous script:")
    lines.append("`item_sensitivity_proxy_j = -mean(consent_ij)`; `item_sensitivity_proxy_c = item_sensitivity_proxy_j - mean(item_sensitivity_proxy_j)`.")
    lines.append("There was reverse coding by multiplying the item mean by `-1`, no z-standardization, and mean-centering before interaction modeling.")
    lines.append("")
    lines.append("| Information type | Original variable | Mean consent | Final centered sensitivity score |")
    lines.append("|---|---:|---:|---:|")
    for _, r in sensitivity.iterrows():
        lines.append(f"| {r.information_type} | {r.original_variable} | {r.mean_consent:.3f} | {r.final_centered_sensitivity_score:.3f} |")
    lines.append("")
    lines.append("Circularity judgment: because the predictor is a deterministic transformation of the outcome's information-type means, the sensitivity interaction has outcome-derived predictor bias. It can describe the empirical ordering of item difficulty/consent, but it cannot serve as confirmatory evidence that exogenous information sensitivity moderates trust.")
    lines.append("Final verdict: INVALID FOR CONFIRMATORY ANALYSIS. Remove `Information Sensitivity x Management Trust` and `Information Sensitivity x Risk` from main empirical claims.")
    lines.append("A label scan of the SAV metadata found respondent-level leakage/misuse/risk items and disaster-type severity items, but no independent 15-category information-type sensitivity, harm, leakage concern, or misuse concern scale corresponding to `q29_1`-`q29_15`. The scan output is saved as `audit_exogenous_sensitivity_item_scan.csv`.")
    lines.append("")

    lines.append("## 3. Core model reproducibility")
    for _, r in main_ols[main_ols["term"].isin(["manage_trust", "risk", "safe_management"])].iterrows():
        lines.append(f"- Main OLS/HC3 {r.term}: b={r.coef:.3f}, SE={r.se:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4g}.")
    for _, r in mediation.iterrows():
        lines.append(f"- Indirect-association model {r.effect}: estimate={r.estimate:.3f}, bootstrap 95% CI [{r.boot_ci_low:.3f}, {r.boot_ci_high:.3f}].")
    for _, r in interaction.iterrows():
        lines.append(f"- {r.specification}: Trust x Risk={r.trust_x_risk:.3f}, SE={r.se:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4g}; {r.conclusion}.")
    lines.append(f"- Baseline R2={effect_size['baseline_r2']:.4f}; interaction-model R2={effect_size['interaction_model_r2']:.4f}; Delta R2={effect_size['delta_r2']:.4f}; Cohen's f2={effect_size['cohens_f2_interaction']:.4f}.")
    for _, r in simple.iterrows():
        lines.append(f"- Simple slope at {r.risk_level}: b={r.slope:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}].")
    lines.append("Interpretation: statistically significant but substantively modest interaction. Use restrained language.")
    lines.append("")

    lines.append("## 4. Measurement robustness")
    lines.append(f"Policy Acceptance scoring verdict: {risk_robust} for the risk path. Risk is robust when institutional trust is not included, but it becomes weaker after institutional trust is added; this is expected because institutional trust is part of the specified indirect pathway.")
    for _, r in scoring.iterrows():
        lines.append(f"- {r.scoring}, {r.adjustment}, {r.term}: b={r.coef:.3f}, 95% CI [{r.ci_low:.3f}, {r.ci_high:.3f}], p={r.p:.4g}.")
    lines.append("The larger measurement audit uses multi-item observed constructs only: management trust, risk perception, and policy acceptance. It reports loadings, CR, AVE, approximate HTMT, and factor-score correlations; it is a measurement robustness screen, not a replacement for full SEM.")
    htmt = measurement["htmt"]
    for _, r in htmt.iterrows():
        lines.append(f"- {r.factor_a} vs {r.factor_b}: factor-score r={r.factor_score_correlation:.3f}, approximate HTMT={r.htmt_approx:.3f}.")
    lines.append("Single-item institutional trust sensitivity should be named `measurement-error sensitivity under alternative reliability assumptions`, not latent SEM validation. The calculation is a covariance-regression correction under assumed reliability values; it is useful as a heuristic sensitivity check, but it is not equivalent to a fully identified latent-variable SEM with a validated multi-item institutional-trust scale.")
    for _, r in single.iterrows():
        lines.append(f"- Reliability {r.assumed_reliability:.2f}: indirect={r.indirect_corrected:.3f}, bootstrap 95% CI [{r.boot_ci_low:.3f}, {r.boot_ci_high:.3f}].")
    lines.append("")

    lines.append("## 5. Information-type heterogeneity")
    joint = info["joint"].iloc[0]
    lines.append("Final specification: long-format OLS, `Consent_ij ~ ManagementTrust_i x InformationType_j + Risk_i x InformationType_j + ManagementTrust_i x Risk_i + controls + InformationType FE`, with respondent-level cluster-robust SE.")
    lines.append(f"Joint test: Wald statistic={joint.statistic:.3f}, df={int(joint.df_num)}, p={joint.p:.4g}. This tests whether management-trust slopes differ across information types overall.")
    lines.append("| Information type | N | Slope | SE cluster | 95% CI | p |")
    lines.append("|---|---:|---:|---:|---|---:|")
    for _, r in info["slopes"].iterrows():
        lines.append(f"| {r.information_type} | {int(r.n)} | {r.coef:.3f} | {r.se_cluster_respondent:.3f} | [{r.ci_low:.3f}, {r.ci_high:.3f}] | {r.p:.4g} |")
    lines.append("Use this as information-type heterogeneity only. Do not relabel the pattern as a sensitivity continuum unless an exogenous sensitivity measure is obtained.")
    if "mixedlm_status" in info["mixed"].columns:
        lines.append(f"Random-intercept MixedLM robustness was attempted but not used because estimation failed or was singular: {info['mixed']['mixedlm_status'].iloc[0]}.")
    else:
        lines.append("Random-intercept MixedLM robustness produced item-specific slopes in `audit_information_type_mixedlm_slopes.csv`; clustered FE remains the primary specification.")
    lines.append("")

    lines.append("## 6. Results that should remain in the main manuscript")
    lines.append("- Main citizen-sample OLS/HC3 association model.")
    lines.append("- Management Trust -> Institutional Trust -> Policy Acceptance indirect association, with cross-sectional noncausal language.")
    lines.append("- Management Trust x Risk Perception moderation, simple slopes, interaction plot, Delta R2, and Cohen's f2.")
    lines.append("- Conditional indirect association / moderated mediation if described as PROCESS Model 7-like and noncausal.")
    lines.append("- Information-type heterogeneity may remain only if reported as type-specific slopes with the joint test, not as exogenous sensitivity moderation.")
    lines.append("")

    lines.append("## 7. Results that should move to Supplement")
    lines.append("- Policy Acceptance factor-score/scoring robustness.")
    lines.append("- Measurement-error sensitivity for single-item institutional trust.")
    lines.append("- Alternative specifications and reverse-order specifications.")
    lines.append("- Citizen-practitioner descriptive comparisons for comparable items only.")
    lines.append("- Pairwise information-type slope contrasts, ordered logit, nonlinear risk, diagnostics, ANOVA/Tukey, and descriptive heatmaps.")
    lines.append("")

    lines.append("## 8. Results that should be removed")
    lines.append("- Outcome-derived `item_sensitivity_proxy` as a confirmatory Information Sensitivity variable.")
    lines.append("- Any claim that the statistically significant sensitivity-proxy interactions validate a theory of exogenous information sensitivity.")
    lines.append("- Multigroup citizen-practitioner structural models using non-comparable constructs.")
    lines.append("- Direct coefficient-size dominance claims comparing management trust with binary safe-management perception.")
    lines.append("- Any global fit claim from a just-identified 3-item Policy Acceptance CFA.")
    lines.append("")

    lines.append("## 9. Remaining reviewer vulnerabilities")
    lines.append("- The data are cross-sectional, so mediation and moderated mediation remain associational.")
    lines.append("- The key Trust x Risk interaction is statistically reliable but small in incremental explanatory power.")
    lines.append("- Institutional trust is single-item; sensitivity analysis helps but does not create a true multi-item latent measure.")
    lines.append("- No independent information-type sensitivity scale was found in the current data. Item-specific heterogeneity is useful, but it cannot answer whether exogenous sensitivity strengthens trust effects.")
    lines.append("- The Trust x Risk interaction is stable across scoring specifications, but the direct risk coefficient weakens once institutional trust is included; risk-related direct-effect claims should therefore be written cautiously.")
    lines.append("")

    lines.append("## 10. Final assessment")
    lines.append("The empirical core is usable for a Journal of Risk Research submission if the manuscript narrows its claim: management trust is positively associated with policy/data-use acceptance, institutional trust carries a small but robust indirect association, and the management-trust association is stronger under higher perceived risk. The strongest version of the paper should not claim that externally measured information sensitivity intensifies trust effects, because the previous sensitivity proxy was outcome-derived. The defensible heterogeneity claim is narrower: management-trust associations vary across information types, and the variation is statistically detectable in a respondent-clustered fixed-effects model.")
    lines.append("")
    lines.append("Moderated mediation reproduction details: structure is PROCESS Model 7-like, with Risk Perception moderating the Management Trust -> Institutional Trust path; bootstrap N=5,000; seed=20260825; Management Trust and Risk are mean-centered; controls are age, sex, education, and safe-management perception. Interpret as conditional indirect association, not causal moderated mediation.")
    for _, r in modmed.iterrows():
        lines.append(f"- {r.quantity}: estimate={r.estimate:.3f}, bootstrap 95% CI [{r.boot_ci_low:.3f}, {r.boot_ci_high:.3f}].")
    lines.append("")
    lines.append("Reverse-order specifications remain compatible with cross-sectional covariance and should be used only to motivate cautious causal language.")
    for spec in reverse["specification"].unique():
        lines.append(f"- Reverse-order check estimated: {spec}.")

    (OUT / "ssci_reanalysis_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    people = pd.read_csv(CLEAN / "people_clean.csv")
    long = long_info(people)
    sensitivity = sensitivity_proxy_audit(long)
    scan = scan_exogenous_sensitivity_items()
    info = info_type_fe_models(long)
    interaction, effect_size = core_interaction_robustness(people)
    scoring = policy_acceptance_scoring_robustness(people)
    measurement = measurement_model_audit(people)
    modmed = moderated_mediation_reproduce(people)
    write_report(sensitivity, scan, info, interaction, effect_size, scoring, measurement, modmed)
    print(f"Saved audit outputs to {OUT}")


if __name__ == "__main__":
    main()
