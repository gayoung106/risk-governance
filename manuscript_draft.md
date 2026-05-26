# Legitimacy Perception Under Hybrid Governance: Managerial Trust, Risk, and Perceived Safe Management in Korean Disaster Data Policy

## Abstract

Public acceptance of disaster-related personal data use depends not only on legal authorization or procedural safeguards, but also on whether citizens trust the institutions that manage data and whether they believe collected information is safely managed. Using a survey of the South Korean public (N = 1,094), this study examines how managerial trust, perceived risk, institutional trust, and perceived safe management are associated with acceptance of disaster data policy.

A central measurement correction is incorporated throughout the manuscript. The original q25 item asks whether personal information collected by disaster-response government agencies is safely managed, with raw coding 1 = yes and 2 = no. The analysis therefore recodes this item as `safe_management`, where 1 indicates perceived safe management and 0 indicates the absence of such perception. Under this coding, the empirical result is clear: perceived safe management is positively associated with policy acceptance (β = 0.191, p < .001). Managerial trust is also positively associated with acceptance and is substantially larger in magnitude (β = 0.713, p < .001). Perceived risk is inversely associated with acceptance (β = -0.064, p < .01). Bootstrap mediation analysis indicates that institutional trust partially mediates the relationship between managerial trust and policy acceptance, and moderation analysis shows that the association between managerial trust and acceptance becomes stronger under higher perceived risk.

The study contributes a comparative governance legitimacy framing: both perceived safe management and managerial trust matter for disaster data acceptance, but relational and competence-based managerial trust is the stronger explanatory factor. The findings suggest that disaster data governance requires not only visible safety measures but also durable institutional practices that make data-managing authorities trustworthy.

**Keywords:** disaster data governance; policy acceptance; managerial trust; perceived safe management; risk perception; governance legitimacy

## 1. Introduction

Disaster response increasingly relies on the collection and use of personal data. Location records, health information, contact histories, and other sensitive data can support rapid public intervention, but they also raise concerns about privacy, secondary use, surveillance expansion, and accountability. The legitimacy of disaster data governance therefore cannot be reduced to formal legality. Citizens must also judge whether the institutions collecting and managing data are competent, responsible, and trustworthy.

This article analyzes public acceptance of disaster-related personal data use in South Korea. The Korean context is analytically useful because disaster response combines strong public authority with procedural accountability and data protection requirements. This hybrid governance environment makes it possible to examine how citizens evaluate both formal safety management and broader managerial trust.

The study asks three questions. First, are managerial trust and perceived safe management positively associated with policy acceptance? Second, is managerial trust a stronger explanatory factor than perceived safe management? Third, do institutional trust and perceived risk condition the relationship between managerial trust and policy acceptance? To answer these questions, the study estimates OLS regression models, heteroscedasticity-robust specifications, ordered logit models, bootstrap mediation models, and moderation models.

The analysis corrects a crucial coding issue. The q25 item is coded 1 = yes, personal information is safely managed, and 2 = no, it is not safely managed. The item is therefore recoded as `safe_management`, where 1 = perceived safe management and 0 = otherwise. This makes the coefficient direction substantively interpretable: a positive coefficient means that citizens who believe their data are safely managed are more accepting of disaster data use.

## 2. Theory and Hypotheses

### 2.1 Disaster Data Governance and Policy Acceptance

Disaster data governance involves a distinctive legitimacy problem. Emergency conditions increase the need for information sharing, but they also increase the stakes of institutional misuse. Citizens may support data use when it is linked to public safety, yet still require credible assurance that the data will be managed responsibly.

Policy acceptance is therefore treated here as an indicator of governance legitimacy perception. It reflects not only individual willingness to share data, but also an evaluation of whether the governing arrangement is credible enough to justify data use.

### 2.2 Managerial Trust and Perceived Safe Management

Managerial trust refers to confidence that data-managing authorities have the competence, integrity, and responsibility required to handle personal information appropriately. It is a broad relational and competence-based evaluation of the managing institution.

Perceived safe management is a more direct judgment: whether citizens believe that personal information collected by disaster-response government agencies is safely managed. It should be positively associated with policy acceptance. However, managerial trust is expected to have a stronger explanatory role because it captures a broader judgment about the authority responsible for data governance.

**H1.** Managerial trust is positively associated with acceptance of disaster-related personal data use.

**H1a.** Perceived safe management is positively associated with policy acceptance, but managerial trust has stronger explanatory power.

### 2.3 Risk Perception

Risk perception refers to citizens' concern that personal data use may lead to privacy invasion, misuse, surveillance, or secondary use. Higher perceived risk should reduce acceptance of disaster data use.

**H2.** Perceived risk is inversely associated with policy acceptance.

### 2.4 Institutional Trust as a Mediating Mechanism

Managerial trust may affect policy acceptance directly and indirectly. When citizens trust the authority responsible for managing data, they may also develop broader institutional trust, which in turn supports acceptance.

**H3.** Institutional trust partially mediates the relationship between managerial trust and policy acceptance.

### 2.5 Managerial Trust Under Risk

When perceived risk is high, citizens may rely more heavily on trust in the managing authority. Managerial trust should therefore matter more under higher-risk conditions.

**H4.** The positive association between managerial trust and policy acceptance is stronger when perceived risk is higher.

## 3. Methods

### 3.1 Data

The study uses a cross-sectional survey of the South Korean public (N = 1,094). The unit of analysis is the individual respondent. The dependent variable is acceptance of personal data use for disaster response.

### 3.2 Measures

| Variable | Description | Coding and Interpretation |
| --- | --- | --- |
| consent | Acceptance of disaster-related personal data use | Higher values indicate higher acceptance |
| manage_trust | Trust in the authority managing personal data | Higher values indicate higher managerial trust |
| risk | Perceived risk of personal data use | Higher values indicate higher risk perception |
| trust | Institutional trust | Higher values indicate higher institutional trust |
| safe_management | Recoded q25 item | 1 = perceived safe management, 0 = otherwise |

The original q25 item asks: “Do you think your personal information collected by disaster-response government agencies is safely managed?” The raw coding is 1 = yes and 2 = no. The item was recoded as follows:

```python
safe_management = 1 if q25 == 1 else 0
```

This recoding aligns the variable with the substantive interpretation used in the manuscript.

### 3.3 Analytic Strategy

The analysis proceeds in four steps. First, OLS regression estimates the association between managerial trust, risk perception, perceived safe management, and policy acceptance. Second, HC3 robust standard errors and ordered logit models assess robustness. Third, bootstrap mediation analysis tests whether institutional trust mediates the relationship between managerial trust and policy acceptance. Fourth, an interaction model tests whether perceived risk conditions the association between managerial trust and acceptance.

## 4. Results

### 4.1 Main Regression Results

Managerial trust is strongly and positively associated with policy acceptance (β = 0.713, p < .001). Perceived safe management is also positively associated with policy acceptance (β = 0.191, p < .001). Perceived risk is inversely associated with policy acceptance (β = -0.064, p < .01).

| Predictor | Coefficient | Interpretation |
| --- | ---: | --- |
| Managerial trust | +0.713*** | Higher trust in data-managing authorities is associated with higher acceptance |
| Perceived safe management | +0.191*** | Believing that personal data are safely managed is associated with higher acceptance |
| Risk perception | -0.064** | Higher perceived risk is associated with lower acceptance |

These findings support the comparative governance legitimacy argument. Perceived safe management matters, but managerial trust is the stronger explanatory factor.

### 4.2 Robustness Checks

The coefficient directions and statistical significance remain stable when HC3 robust standard errors are used. Ordered logit models also reproduce the same substantive pattern: managerial trust and perceived safe management are positively associated with policy acceptance, while perceived risk is inversely associated with acceptance.

### 4.3 Mediation Through Institutional Trust

Bootstrap mediation analysis indicates that institutional trust partially mediates the relationship between managerial trust and policy acceptance. This suggests that managerial trust supports acceptance not only directly but also by strengthening broader institutional trust.

### 4.4 Moderation by Risk Perception

The interaction between managerial trust and perceived risk is positive and statistically significant. This indicates that the association between managerial trust and acceptance becomes stronger when perceived risk is higher. Under uncertainty, citizens appear to place greater weight on whether the managing authority is trustworthy.

## 5. Discussion

### 5.1 Perceived Safe Management as a Positive Legitimacy Signal

The first implication is straightforward: citizens who believe that disaster-related personal information is safely managed are more accepting of data use. This finding is consistent with general governance acceptance theory. Safety management perceptions contribute to legitimacy because they indicate that data use is being controlled and protected.

This interpretation depends on the corrected q25 coding. Since the raw item codes 1 as yes and 2 as no, using the raw item without recoding reverses the substantive direction. The recoded `safe_management` variable resolves this issue and supports a positive interpretation.

### 5.2 The Comparative Strength of Managerial Trust

The second implication is the stronger one: managerial trust has substantially greater explanatory power than perceived safe management. This does not mean that formal safety management is irrelevant. Rather, it means that citizens' broader trust in the managing authority carries more explanatory weight than a single direct evaluation of safe management.

For disaster data governance, this points to a practical distinction. Technical safeguards, compliance procedures, and data protection rules remain necessary. Yet policy acceptance depends more strongly on whether citizens regard the managing authority as competent, responsible, and trustworthy.

### 5.3 Risk and Conditional Trust

Risk perception reduces acceptance, but managerial trust becomes more important under higher perceived risk. This result suggests that risk communication should not rely only on minimizing public concern. A more credible strategy is to acknowledge risk while strengthening the institutional conditions that make responsible management believable.

### 5.4 Governance Legitimacy Implications

The findings support a comparative governance legitimacy framework. Perceived safe management and managerial trust are both positive legitimacy resources. However, they operate at different levels. Perceived safe management is a direct evaluation of whether personal information is protected. Managerial trust is a broader evaluation of the authority responsible for data governance. The latter has greater explanatory power in this study.

### 5.5 Limitations

The study is based on cross-sectional survey data and therefore does not establish causal effects. Perceived safe management is measured with a single binary item, which limits construct depth. Future research should use multi-item measures that distinguish safety, transparency, accountability, and auditability. Comparative research is also needed to assess whether the Korean pattern generalizes to other institutional contexts.

## 6. Conclusion

This study shows that both perceived safe management and managerial trust are positively associated with public acceptance of disaster-related personal data use. The stronger finding is comparative: managerial trust is a much more powerful explanatory factor than perceived safe management. Disaster data governance therefore requires not only visible safety measures and legal safeguards, but also durable institutional practices that make data-managing authorities credible and trustworthy.

## Appendix: Variable Coding

| Variable | Source | Final Coding |
| --- | --- | --- |
| q25 | “Do you think personal information collected by disaster-response government agencies is safely managed?” | Raw: 1 = yes, 2 = no |
| safe_management | Recoded q25 | 1 = perceived safe management, 0 = otherwise |
| consent | Policy acceptance | Higher values indicate higher acceptance |
| manage_trust | Managerial trust | Higher values indicate higher trust |
| risk | Risk perception | Higher values indicate higher perceived risk |
| trust | Institutional trust | Higher values indicate higher institutional trust |

## References

Acquisti, A., & Grossklags, J. (2005). Privacy and rationality in individual decision making. IEEE Security & Privacy, 3(1), 26-33.

Ansell, C., & Gash, A. (2008). Collaborative governance in theory and practice. Journal of Public Administration Research and Theory, 18(4), 543-571.

Beck, U. (1992). Risk society: Towards a new modernity. Sage.

Black, J. (2010). Risk-based regulation: Choices, practices and lessons being learnt. In Risk and Regulatory Policy. OECD.

Braithwaite, J. (2002). Restorative justice and responsive regulation. Oxford University Press.

Dinev, T., & Hart, P. (2006). An extended privacy calculus model for e-commerce transactions. Information Systems Research, 17(1), 61-80.

Hood, C., & Rothstein, H. (2001). Risk regulation under pressure. Risk Analysis, 21(1), 21-28.

Luhmann, N. (1979). Trust and power. Wiley.

Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. Academy of Management Review, 20(3), 709-734.

Nissenbaum, H. (2004). Privacy as contextual integrity. Washington Law Review, 79, 119-158.

Solove, D. J. (2013). Privacy self-management and the consent dilemma. Harvard Law Review, 126, 1880-1903.

Tyler, T. R. (2006). Why people obey the law. Princeton University Press.
