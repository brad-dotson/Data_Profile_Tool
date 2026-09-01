# Example Datasets

These tracked examples are public, reusable datasets chosen to exercise Version 1 against realistic inputs. They contain no project or client data.

## `automobile_messy.csv`

- **Rows:** 205
- **Use it for:** deliberately messy input, including source misspellings and missing-value markers plus added blank cells, a `NULL` token, surrounding whitespace, an invalid category, an extreme numeric outlier, and a duplicate row
- **Source:** UCI Machine Learning Repository, [Automobile](https://archive.ics.uci.edu/dataset/10/automobile)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Citation:** Schlimmer, J. (1985). *Automobile*. UCI Machine Learning Repository. https://doi.org/10.24432/C5B01C
- **Adaptation:** Column headers were added from the UCI data dictionary. A small, documented set of anomalies was added specifically for deterministic profiler testing; this file is not represented as the untouched research dataset.
- **Detailed context:** [Automobile source notes](context/automobile_messy.md)

## `cervical_cancer_risk_factors.xlsx`

- **Main table rows:** 858
- **Use it for:** a multi-sheet Excel source and many physical types, including numbers, integers, booleans, strings, and missing cells
- **Sheets:** `Risk Factors`, `Data Dictionary`, and `Source Notes`
- **Source:** UCI Machine Learning Repository, [Cervical Cancer (Risk Factors)](https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Citation:** Fernandes, K., Cardoso, J., & Fernandes, J. (2017). *Cervical Cancer (Risk Factors)*. UCI Machine Learning Repository. https://doi.org/10.24432/C5Z310
- **Adaptation:** The source CSV was converted to a workbook. A derived string `record_id` was added, its `?` missing-value markers became blank cells, 0/1-only fields became booleans, and source/dictionary sheets were added.
- **Detailed context:** [Cervical Cancer Risk Factors source notes](context/cervical_cancer_risk_factors.md)

## `palmer_penguins_raw.csv`

- **Rows:** 344
- **Use it for:** well-known real-world scientific data with dates, integers, floats, categorical text, free-text comments, and missing values
- **Source:** [palmerpenguins](https://github.com/allisonhorst/palmerpenguins), raw dataset
- **License:** CC0 1.0 Universal
- **Citation:** Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). *palmerpenguins: Palmer Archipelago (Antarctica) penguin data*. https://doi.org/10.5281/zenodo.3960218
- **Adaptation:** None; this is the published `penguins_raw.csv` file.
- **Detailed context:** [Palmer Penguins raw source notes](context/palmer_penguins_raw.md)

The source links and license notes are part of the repository so future contributors can audit why each file is safe to redistribute.
