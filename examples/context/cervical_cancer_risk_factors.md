# Cervical Cancer Risk Factors Example: Source Context

## Why this example is here

`examples/cervical_cancer_risk_factors.xlsx` is the multi-table and mixed-physical-type Version 1 example. Its primary table has 858 rows, and the workbook adds a data dictionary and source notes so the application can be tested against a realistic multi-sheet input.

This is health-related data. Although the public dataset is de-identified and openly licensed, future agents should use restraint: a data profile describes fields and distributions; it does not provide medical advice, assess an individual, or validate clinical conclusions.

## Original source and purpose

UCI's **Cervical Cancer (Risk Factors)** dataset contains demographic information, habits, medical-history variables, and four screening or diagnosis indicators for 858 patients. UCI describes the associated task as classification and reports 36 original variables with integer and real feature types. [UCI dataset page](https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors)

The dataset accompanied research on transfer learning under partial observability for cervical-cancer screening. The introductory publication is Fernandes, K., Cardoso, J. S., and Fernandes, J. (2017), “Transfer Learning with Partial Observability Applied to Cervical Cancer Screening,” *Pattern Recognition and Image Analysis*, pp. 243–250. [Publication record and DOI](https://doi.org/10.1007/978-3-319-58838-4_27)

The canonical dataset citation is: Fernandes, K., Cardoso, J., & Fernandes, J. (2017). *Cervical Cancer (Risk Factors)*. UCI Machine Learning Repository. [DOI: 10.24432/C5Z310](https://doi.org/10.24432/C5Z310).

UCI licenses the dataset under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Collection method and population

UCI states that the data were collected at Hospital Universitario de Caracas in Caracas, Venezuela. The fields combine demographic information, behavioral factors, and historical medical records. UCI also explains that some patients declined to answer certain questions because of privacy concerns, producing missing values. [UCI dataset documentation](https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors)

Subsequent peer-reviewed use of the same public dataset describes the records as early screening data collected from March 2012 through September 2013 and reports patient ages from 13 to 84. That article also describes the cohort as largely low-income and of low socioeconomic and educational status. These details matter for representativeness and should not be generalized beyond the documented population. [Study-population description](https://pmc.ncbi.nlm.nih.gov/articles/PMC8886038/)

The available documentation does not provide a full sampling protocol, questionnaire instrument, consent procedure, or complete data-entry workflow. A future agent should state that limitation rather than infer a random or population-representative sample.

## What one row represents

One original row represents one patient record containing some combination of:

- age and reproductive-history fields;
- smoking, contraceptive, and IUD history;
- sexually transmitted disease history;
- prior diagnosis indicators; and
- four outcome/indicator fields: Hinselmann, Schiller, Citology, and Biopsy.

The four final indicators are not interchangeable. They represent different screening or diagnostic results and should remain separately named unless a reviewed analytical objective defines a target.

## Missingness and analytical cautions

Missingness is a defining property of this dataset, not a formatting accident. In the repository workbook there are 3,622 blank cells inherited from source `?` markers. Two fields—time since first and last STD diagnosis—each have 787 missing values, while several IUD, contraceptive, and STD fields also have substantial missingness.

Important cautions include:

- Missing answers may reflect privacy choices and therefore may not be missing at random.
- The outcome indicators are highly imbalanced. In the repository representation, positive counts are 35 for Hinselmann, 74 for Schiller, 44 for Citology, and 55 for Biopsy out of 858 rows.
- Binary 0/1 storage does not by itself establish that every variable should be treated identically; some are exposures, some history indicators, and some outcomes.
- The cohort is tied to one hospital and period. Geographic, socioeconomic, healthcare-access, and temporal differences limit broader generalization.
- A profile can reveal missingness and distributions but cannot establish clinical validity, fairness, diagnosis quality, or causal risk.

Research using this dataset commonly addresses missing-data handling and class imbalance. Those are modeling and validation decisions, not Version 1 profiling actions.

## Changes made for this repository

The original UCI delivery is one CSV. This repository converts it to a three-sheet workbook:

- `Risk Factors` — all 858 patient rows;
- `Data Dictionary` — field names, intended physical types, and concise descriptions; and
- `Source Notes` — provenance, license, citation, and transformation notes.

Additional representation changes are:

- a derived string `record_id` (`PAT-0001` through `PAT-0858`) was added solely to test identifier-like strings;
- source `?` markers became genuinely blank Excel cells;
- columns containing only 0/1 among observed values were stored as Excel booleans; and
- numeric fields were stored as numeric Excel values where possible.

The derived identifiers are not hospital identifiers and do not link back to people. The workbook does not add diagnoses, correct values, impute missing answers, or rebalance outcomes.

## Appropriate uses

- Testing a multi-sheet Excel input as one project
- Profiling strings, integers, floats, booleans, and missing cells
- Reviewing high missingness and differing analytical roles
- Testing future schema-aware and missingness checks
- Demonstrating why context and role matter more than storage type
- Exploring responsible metadata for future agent-assisted understanding

## Inappropriate uses and cautions

- Do not use this tool or context file for diagnosis, treatment, or patient-level risk assessment.
- Do not interpret missing answers as negative responses.
- Do not assume the four screening/diagnosis indicators are equivalent ground truth.
- Do not claim population prevalence from this hospital cohort.
- Do not infer that the derived `record_id` existed in the clinical source.
- Do not expose row-level combinations unnecessarily; even public de-identified health data warrants careful handling.

## Guidance for a future agent

An agent should begin by stating that this is a public, de-identified, single-hospital screening dataset adapted into a workbook for software testing. It should distinguish original variables from the derived `record_id`, treat missingness as potentially informative, and avoid medical conclusions. Any recommendation to impute, drop fields, combine outcomes, or rebalance classes requires an explicit analytical purpose and belongs outside blind profiling.

## Key references

- [UCI Cervical Cancer (Risk Factors)](https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors)
- [Canonical dataset DOI](https://doi.org/10.24432/C5Z310)
- [Introductory transfer-learning publication](https://doi.org/10.1007/978-3-319-58838-4_27)
- [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)

