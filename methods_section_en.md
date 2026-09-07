# Methods

## 3. Research Design and Data

This study examines which perceptual factors are associated with citizens' policy acceptance of the use of personal information in disaster contexts. The unit of analysis is the individual respondent, and the data consist of a cross-sectional survey of 1,094 members of the Korean general public. The scope of inference is limited to individual-level perceptual associations. The study does not directly measure the objective performance of a governance system or the institutional structure itself.

## 3.1 Measurement of Variables

| Construct | Variable name | Items | Coding and construction | Direction of interpretation |
|---|---|---|---|---|
| policy acceptance | `consent` | q7, q8, q9 (original columns q7_1, q8_1, q9_1) | Three-item mean, α=.876 | Higher values indicate greater policy acceptance of personal information use |
| management trust | `manage_trust` | q5, q6 (original columns q5_1, q6_1) | Two-item mean, α=.834 | Higher values indicate greater trust in the necessity and effectiveness of agencies' data use |
| risk perception | `risk` | q21, q22 (original columns q21_1, q22_1) | Two-item mean, α=.833 | Higher values indicate greater perceived risk of personal information leakage and misuse |
| positive perception of safe management | `safe_management` | q25 | Binary dummy, 1=perceives information as managed safely, 0=does not | Higher values indicate greater positive perception of safe management |
| institutional trust | `trust` | q26 (original column q26_1) | Single item | Higher values indicate greater trust in government agencies responsible for disaster response |

## 3.2 Coding Direction and Recoding of q25

q25 asks: "Do you think that your personal information collected by government agencies responsible for disaster response is being managed safely?" In the original data, the item is coded as `1=yes` and `2=no`. Thus, the original coding of q25 is not a variable in which higher values indicate stronger positive perception of safe management; rather, higher values correspond to the response that the information is not being managed safely.

To ensure interpretive consistency, this study recodes q25 as a positively oriented dummy variable as follows:

```python
safe_management = 1 if q25 == 1 else 0
```

Thus, `safe_management=1` indicates that the respondent perceives personal information collected by government agencies responsible for disaster response as being managed safely, whereas `safe_management=0` indicates otherwise. All subsequent interpretations are based on this positively oriented variable.

## 3.3 Measurement Model Validity and Common Method Variance

Composite reliability (CR) and average variance extracted (AVE) were calculated for policy acceptance (three items), management trust (two items), and risk perception (two items). The values were as follows: policy acceptance CR=.924, AVE=.802; management trust CR=.923, AVE=.858; and risk perception CR=.924, AVE=.858. All values met conventional thresholds (CR≥.70, AVE≥.50), supporting convergent validity. However, because the single-factor models for these latent variables comprise only two or three items and are just-identified models with 0 degrees of freedom, global fit indices such as CFI, TLI, RMSEA, and SRMR are not used as evidence of validity in this study. Positive perception of safe management and institutional trust were measured with single items and were therefore excluded from CR/AVE calculation; this measurement limitation is discussed in §3.8.

To assess the possibility of Common Method Variance (CMV), the survey instrument distributed the relevant items across the questionnaire, and Harman's single-factor test was conducted as a supplementary diagnostic. Exploratory factor analysis of the items for policy acceptance, management trust, risk perception, and institutional trust extracted multiple factors with eigenvalues greater than 1, and the variance explained by the first factor was below the 50% criterion. Harman's test, however, does not rule out CMV, and this limitation is considered when interpreting the results.

## 3.4 Multicollinearity Diagnostics

Variance inflation factors (VIFs) were calculated for the key predictors: management trust, risk perception, and positive perception of safe management. The VIFs were 1.08, 1.20, and 1.26, respectively, well below conventional thresholds (VIF<10 and the commonly used conservative threshold of VIF<5). Some demographic control-variable dummies may show relatively high VIFs, but these values are not interpreted as evidence of multicollinearity among the key predictors.

## 3.5 Analytical Strategy

The main effects were tested using OLS regression with policy acceptance (`consent`) as the dependent variable and management trust (`manage_trust`), risk perception (`risk`), and positive perception of safe management (`safe_management`) as the key predictors. The final model included region of residence (`sq1`), gender (`sq2`, categorical), and age (`sq3_1`) as control variables. HC3 robust standard errors were applied to account for potential heteroskedasticity.

The role of institutional trust was explored through bootstrap estimation of indirect associations with 5,000 resamples. The central interest is the statistical indirect association linking management trust to policy acceptance through institutional trust. The indirect association of positive perception of safe management is presented only as a supplementary and exploratory pathway and is not interpreted as a causal mediation mechanism.

The conditional association of risk perception was examined by including an interaction term between mean-centered management trust and mean-centered risk perception. Simple slopes were calculated at the mean of risk perception and at ±1 standard deviation. In addition, to examine whether the indirect pathway management trust -> institutional trust -> policy acceptance varied by the level of risk perception, a conditional indirect association in which risk perception moderates the first stage of the mediation path, corresponding to a PROCESS Model 7-type structure, was estimated using bootstrapping. These estimates are interpreted as conditional indirect association estimates rather than causal moderated mediation effects.

To further examine whether the association between management trust and policy acceptance was uniform across information types, the agreement items for each type of personal information were reconstructed in long format. The model `item-level agreement ~ management trust × information type + risk perception × information type + management trust × risk perception + controls + information-type fixed effects` was estimated using respondent-level cluster-robust standard errors. Equality of the management trust slopes across information types was assessed using a joint Wald test.

Other alternative model specifications, including comparisons with and without control variables, standardized variables, factor-score-based dependent variables, reverse-order models, ordered logit models, sensitivity analyses for reliability assumptions regarding single-item institutional trust, and descriptive comparisons with the practitioner sample, are reported in the online appendix because they are not directly related to the core mechanism examined in the main text.

## 3.6 Software and Reproducibility

All analyses were conducted in Python 3.13.3. Data processing used pandas 3.0.2 and numpy 2.4.4; statistical models were estimated using statsmodels 0.14.6; confirmatory factor analysis used semopy 2.3.11 and factor_analyzer 0.5.1; descriptive statistics and tests used scipy 1.17.1; auxiliary classification and factor-score calculations used scikit-learn 1.8.0; and the original SPSS `.sav` file was loaded using pyreadstat 1.3.4. All bootstrap estimates, including indirect associations and conditional indirect association estimates, used 5,000 resamples, with the random seed fixed using numbers generated by `numpy.random.default_rng(20260825)` for reproducibility. Analysis scripts and result files are stored in the `code/` and `result/` directories, respectively. The original data (`raw/`) are not publicly available because of copyright restrictions.

## 3.7 Interpretation of Descriptive Statistics and Correlations

The distribution of q25 in the original data is `1=yes` for 515 respondents (47.07%) and `2=no` for 579 respondents (52.93%), with no missing values. After recoding into `safe_management`, 47.07% of the sample is classified as having positive perception of safe management.

The correlation between the positively oriented `safe_management` variable and policy acceptance is `r=.313`; see §3.2 for the coding direction.

## 3.8 Methodological Cautions

Because `safe_management` is based on a single binary item, it cannot fully capture the detailed dimensions of perceptions of safe management. This variable should therefore be interpreted not as a comprehensive evaluation of the safety management system but as respondents' binary subjective assessment of whether their personal information is being managed safely. In addition, given the limitations of cross-sectional data, the observed associations are not interpreted as causal effects.
