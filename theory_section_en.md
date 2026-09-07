# Theoretical Background and Hypotheses

## 2. Theoretical Background

### 2.1 Research Problem and Scientific Gap

Existing privacy research has primarily explained decisions to provide personal information through the framework of risk-benefit calculation, or privacy calculus (Acquisti & Grossklags, 2005; Dinev & Hart, 2006). From this perspective, citizens are treated as rational actors who weigh the risks and utility of providing information. Yet this explanation is insufficient in contexts such as disaster data governance, where multiple public and private actors are involved, the urgency of response makes procedural consent difficult to secure, and responsibility can often be identified only after the fact. Citizens do not merely calculate their own risks and benefits; they also judge whether the use of personal information by disaster response agencies is necessary and effective.

More specifically, prior research has not jointly addressed two questions: (1) whether judgments about the necessity and effectiveness of data use (management trust) and direct evaluations of the current safety status (positive perception of safe management) have distinct pathways to policy acceptance; and (2) whether these judgments are differently associated with policy acceptance depending on the level of risk perception. This study treats these issues as the scientific gap and examines them in the context of disaster data governance.

In this study, policy acceptance (`consent`) is measured as the mean level of agreement with the collection of personal information for disaster response (q7), disclosure upon request (q8), and sharing across agencies (q9). Policy acceptance is therefore operationalized not as an abstract attitude but as agreement with three concrete data-processing activities required by disaster data governance. Sections 2.2 to 2.4 explain the mechanisms through which this level of agreement is associated with management trust, risk perception, and positive perception of safe management.

### 2.2 Mechanism of management trust: performance-based trust grounded in judgments of necessity and effectiveness

Management trust (`manage_trust`) is measured as the mean of the perception that government use of personal information for disaster response is necessary (q5) and the perception that collected personal information is effective in improving public safety (q6). This construct therefore does not refer to an evaluation of agencies' practical data security or management capacity itself, such as access control, encryption, or log management, which are captured by the `management` and `safety` variables in the worker sample. Rather, it refers to a performance-based judgment about the necessity of the policy instrument's purpose and the effectiveness of its implementation. Without this distinction, the label "management trust" may be confused with variables that measure practical management systems in the worker sample.

Viewed through the trust model of Mayer, Davis, & Schoorman (1995), q5, or perceived necessity, corresponds to a judgment that the agency's objective is aligned with the public interest, whereas q6, or perceived effectiveness, corresponds to a judgment about the agency's ability to achieve that objective. Management trust should therefore be understood in a restricted sense as performance-based trust that combines judgments about the necessity of the purpose and implementation capacity, rather than as comprehensive trust that also includes integrity.

When citizens cannot directly verify the technical details of data processing (Luhmann, 1979), these judgments of necessity and effectiveness can operate as cognitive shortcuts that substitute for verification (Xu, Dinev, Smith, & Hart, 2011). Citizens who judge the policy purpose to be necessary and effective may be more likely to cooperate on the basis of that judgment rather than calculate each risk independently (Mutimukwe, Kolkowska, & Grönlund, 2020). Management trust is therefore expected to be positively associated with policy acceptance.

### 2.3 Mechanism of risk perception: loss of control and defensive attitudes

Risk perception (`risk`) is measured as the mean of subjective evaluations of the possibility of personal information leakage (q21) and misuse (q22). Beck (1992)'s theory of risk society provides a macro-level account of why such risk emerges. Modern institutions manage risk while also producing new risks, and data use for disaster response may therefore be perceived both as a means of public safety and as a source of institutional risk. However, a separate account of psychological mechanisms is needed to explain why this macro-level condition reduces policy acceptance at the individual level.

Slovic (1987)'s research on risk perception provides this micro-level mechanism. Risk judgments are not merely probability calculations; they are strongly shaped by controllability and the unpredictability of consequences. Leakage and misuse of personal information are risks whose timing and scope of consequences are difficult for individuals to control or predict. In short, Beck's theory of risk society explains the institutional sources of risk, whereas Slovic's theory of risk perception explains why such risk leads to changes in individual attitudes. The two theories are therefore complementary at the macro and micro levels. Citizens with higher risk perception are more likely to perceive data use as a potential harm beyond their control, and this loss of control is expected to induce defensive or avoidant attitudes rather than cooperation. Risk perception is therefore expected to be negatively associated with policy acceptance.

### 2.4 Competing explanations and boundary condition: conditional operation of management trust by risk level

The privacy calculus perspective and the policy evaluation perspective offer different predictions about how policy acceptance is formed. From the privacy calculus perspective, risk perception, as perceived cost, is the key variable shaping policy acceptance, while performance-based judgments such as management trust, or judgments about the necessity and effectiveness of policy, are treated as secondary. By contrast, the policy evaluation perspective suggests that citizens decide whether to cooperate on the basis of judgments about the necessity of the policy purpose and the effectiveness of implementation, rather than through individual risk-benefit calculations alone. These explanations are not mutually exclusive, but the question of which perception is more strongly associated with policy acceptance, and whether this relative importance varies by risk level, requires empirical examination.

This study argues that, under higher risk perception, citizens face greater uncertainty and therefore rely more heavily on judgments about the necessity and effectiveness of the policy, that is, management trust, rather than calculating individual risks on their own. Risk level thus functions as a boundary condition that changes the extent to which management trust operates in relation to policy acceptance. This logic implies that, among those with higher risk perception, the policy evaluation perspective, and specifically management trust, will show relatively greater explanatory relevance than predicted by the privacy calculus perspective alone.

### 2.5 Conceptual distinction between positive perception of safe management and management trust

Positive perception of safe management (`safe_management`) is a binary judgment about whether collected personal information is currently being managed safely. The original q25 item is coded as `1=yes` and `2=no`; this study recodes it as `safe_management=1` (yes) and `0` (no). The detailed procedure is described in the methods section.

This perception is conceptually distinct from management trust. Positive perception of safe management is a direct evaluation of the "current status," whereas management trust (q5, q6) is a performance-based judgment about the necessity of the policy purpose and the effectiveness of implementation. The former is closer to a factual judgment, whereas the latter is an evaluative judgment about the necessity and effectiveness of the policy instrument itself. Although the two perceptions are related, they are separate constructs and are therefore expected to have independent pathways to policy acceptance.

Management trust is a specific judgment about a particular policy instrument, namely the use of personal information by disaster response agencies. By contrast, institutional trust (`trust`, q26) is diffuse trust in the agency itself. This distinction corresponds to Luhmann (1979)'s logic of interpersonal and system trust. On this basis, management trust may be directly associated with policy acceptance and may also be indirectly associated with it through a pathway in which specific judgments about the necessity and effectiveness of the policy purpose generalize into diffuse trust in the agency.

## 2.6 Hypotheses

**H1: Management trust will be positively associated with policy acceptance.**

**H1a: Positive perception of safe management will be positively associated with policy acceptance.**

**H2: Risk perception will be negatively associated with policy acceptance.**

**H3: Management trust will show a significant indirect association with policy acceptance through diffuse institutional trust (`trust`).**

**H4: Under higher risk perception, the positive slope between management trust and policy acceptance will be stronger.**

## 2.7 Summary of the Research Model

**[Figure 1]** The core moderated mediation structure (management trust -> institutional trust -> policy acceptance; risk perception moderates the management trust -> institutional trust path) is presented in `result/figure/figure1_research_model.png` (submission original: `.tif`). The text diagram below summarizes the full model, including the direct paths of positive perception of safe management and risk perception.

```text
Management trust ───────────────→ policy acceptance
   │                                  ↑
   └────→ institutional trust ────────┘

Positive perception of safe management ─────→ policy acceptance

Risk perception ───────────────→ policy acceptance
Management trust × risk perception ────→ policy acceptance
```

The research model examines the comparative association structure of positive perception of safe management and management trust. The key questions are whether both perceptions are positively associated with policy acceptance, whether management trust is also indirectly associated through diffuse institutional trust, and whether these associations vary by risk level. The relative magnitude of the association between management trust and positive perception of safe management is not proposed as an a priori hypothesis and is discussed exploratorily in the interpretation of the results.

## References

Acquisti, A., & Grossklags, J. (2005). Privacy and rationality in individual decision making. _IEEE Security & Privacy, 3_(1), 26-33.

Beck, U. (1992). _Risk society: Towards a new modernity_. Sage.

Dinev, T., & Hart, P. (2006). An extended privacy calculus model for e-commerce transactions. _Information Systems Research, 17_(1), 61-80.

Luhmann, N. (1979). _Trust and power_. Wiley.

Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. _Academy of Management Review, 20_(3), 709-734.

Mutimukwe, C., Kolkowska, E., & Grönlund, Å. (2020). Information privacy in e-service: Effect of organizational privacy assurances on individual privacy concerns, perceptions, trust and self-disclosure behavior. _Government Information Quarterly, 37_(1), 101413. https://doi.org/10.1016/j.giq.2019.101413

Slovic, P. (1987). Perception of risk. _Science, 236_(4799), 280-285.

Trein, P., & Varone, F. (2024). Citizens' agreement to share personal data for public policies: Trust and issue importance. _Journal of European Public Policy, 31_(9), 2483-2508. https://doi.org/10.1080/13501763.2023.2205434

Xu, H., Dinev, T., Smith, J., & Hart, P. (2011). Information privacy concerns: Linking individual perceptions with institutional privacy assurances. _Journal of the Association for Information Systems, 12_(12), 798-824. https://doi.org/10.17705/1jais.00281
