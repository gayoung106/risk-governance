# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Korean academic research project conducting statistical analysis on **risk governance, trust, and data regulation consent**. It examines how risk perception, trust management, and safety perception influence public consent to data regulation policies, using survey data from ~1,094 respondents (general public and workers).

## Setup and Running Scripts

```bash
# Activate the virtual environment (Windows)
source venv/Scripts/activate

# Run individual scripts from the code/ directory
cd code
python 01_preprocess.py
```

Dependencies are in `requirements.txt`. Key packages: `pandas`, `statsmodels`, `scipy`, `pyreadstat` (for SPSS `.sav` files), `matplotlib`, `seaborn`.

## Analysis Pipeline

The 15 scripts in `code/` form a **sequential pipeline** — each reads from prior outputs and writes to `../result/`. They must generally be run in order:

| Script                        | Purpose                                                      |
| ----------------------------- | ------------------------------------------------------------ |
| `01_preprocess.py`            | Load SPSS `.sav` files → clean CSVs in `clean/`              |
| `02_reliability.py`           | Cronbach's alpha for scale reliability                       |
| `03_analysis_people.py`       | Descriptive stats + baseline OLS regression                  |
| `04_mediation.py`             | Mediation analysis (manage_trust → safety → trust → consent) |
| `05_anova.py`                 | ANOVA by risk/trust/safety groups                            |
| `06_robust.py`                | Robust regression (HC3 standard errors)                      |
| `07_vif.py`                   | Variance Inflation Factor (multicollinearity)                |
| `08_diagnostics.py`           | Residual distribution plot                                   |
| `09_effect_size.py`           | Correlation matrices                                         |
| `10_subgroup.py`              | Subgroup analysis by trust level                             |
| `11_compare_worker_people.py` | t-test: workers vs. general public                           |
| `12_posthoc.py`               | Tukey HSD post-hoc tests                                     |
| `13_interaction.py`           | manage_trust × risk interaction effect                       |
| `14_ordered_logit.py`         | Ordered logit (consent as ordinal)                           |
| `15_effect_size.py`           | Eta-squared effect sizes                                     |

## Data Architecture

**Input** (in `raw/`, excluded from git):

- `raw_data_people.sav` — general public survey
- `raw_data_worker.sav` — worker survey

**Cleaned data** (in `clean/`):

- `people_clean.csv`, `worker_clean.csv`

**Outputs** (in `result/`): `.txt` regression/ANOVA summaries, `.png` diagnostic plots.

## Key Conventions

**Questionnaire item → composite index mapping** (items averaged, not summed):

- `q5`, `q6` → `manage_trust`
- `q7`, `q8`, `q9` → `consent`
- `q21`, `q22` → `risk`
- `q25` → `safe_management` (recoded binary item)
- `q26` → `trust` (single item)
- `q31`, `q32`, `q13` → worker safety items
- `q41`, `q42` → worker management items

**Missing value codes**: `99`, `999`, `9999` are treated as NA. Columns with suffix `et` or value `9997` are filtered out.

**Encoding**: SPSS files use `cp949` (Korean). All column names are lowercased after loading.

**Language**: All comments and variable names are in Korean.

# Language Policy

Unless explicitly requested otherwise,
all outputs should be written in Korean.

This includes:

- manuscript drafts
- theoretical explanations
- reviewer responses
- discussion sections
- policy implications
- reviewer simulations

However:

- preserve original English theoretical terms when academically necessary
- preserve journal names in English
- preserve variable names when appropriate

Writing style:

- Korean academic writing style
- SSCI/KCI-level formal tone
- governance and policy research terminology
- clear theoretical language

Avoid:

- awkward literal translation
- excessive English sentence structure
- informal wording

