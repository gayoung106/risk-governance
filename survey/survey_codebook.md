# Survey Codebook

## PEOPLE sample

### 1. Policy acceptance: `consent`

`consent` measures willingness to accept the collection, disclosure, and sharing of personal data for disaster response.

| Item | Content | Scale |
|---|---|---|
| q7 | Agreement with government disaster-response agencies collecting personal data | 1=strongly disagree to 5=strongly agree |
| q8 | Agreement with disclosure of personal data when requested for disaster and safety response | 1=strongly disagree to 5=strongly agree |
| q9 | Agreement with sharing personal data among disaster-response government agencies | 1=strongly disagree to 5=strongly agree |

```python
consent = mean(q7, q8, q9)
```

Higher values indicate higher policy acceptance.

### 2. Managerial trust: `manage_trust`

`manage_trust` captures trust in whether disaster-response agencies need and can effectively use personal data.

| Item | Content | Scale |
|---|---|---|
| q5 | Perceived necessity of government use of personal data for disaster and safety response | 1=not necessary at all to 5=very necessary |
| q6 | Perceived effectiveness of collected personal data for improving public safety | 1=not effective at all to 5=very effective |

```python
manage_trust = mean(q5, q6)
```

Higher values indicate higher managerial trust.

### 3. Risk perception: `risk`

`risk` captures perceived risk of personal data leakage and misuse.

| Item | Content | Scale |
|---|---|---|
| q21 | Perceived risk that personal data provided to disaster-response agencies may be leaked | 1=very low to 5=very high |
| q22 | Perceived risk that collected personal data may be misused for another purpose | 1=very low to 5=very high |

```python
risk = mean(q21, q22)
```

Higher values indicate higher risk perception.

### 4. Institutional trust: `trust`

`trust` measures trust in disaster-response government agencies that collect personal data.

| Item | Content | Scale |
|---|---|---|
| q26 | Trust in disaster-response government agencies collecting personal data | 1=do not trust at all to 5=trust very much |

```python
trust = q26
```

Higher values indicate higher institutional trust.

### 5. Perceived safe management: `safe_management`

q25 asks whether respondents believe their personal data collected by disaster-response government agencies are safely managed.

Raw coding:

| q25 raw value | Meaning |
|---:|---|
| 1 | Yes, safely managed |
| 2 | No, not safely managed |

Because the raw coding increases toward the negative response, the analysis uses a positive-direction recoded variable:

```python
safe_management = 1 if q25 == 1 else 0
```

| `safe_management` | Meaning |
|---:|---|
| 1 | Respondent perceives that personal data are safely managed |
| 0 | Respondent does not perceive that personal data are safely managed |

Revised note: `safe_management` is the preferred variable name and refers to the positive-direction recoded q25 variable, not raw q25.

## WORKER sample

### 1. Management: `management`

`management` summarizes organizational data-protection and management practices. Source items include q41 and q42 series, covering training, internal management plans, access restrictions, authentication, encryption, access logging, security programs, and facility protection.

```python
management = mean(q41*, q42*)
```

### 2. Safety: `safety`

`safety` captures workers' evaluation of safe management of personal data in disaster management and response. Source items include q13, q31_1, q31_2, q31_3, and q32.

```python
safety = mean(q13, q31_1, q31_2, q31_3, q32)
```

Higher values indicate more positive safety-management evaluation.

## Missing Values

The following values are treated as missing:

```python
99
999
9999
```

Columns containing open-ended or “other” markers such as `9997` or `et` are excluded from scale construction.

