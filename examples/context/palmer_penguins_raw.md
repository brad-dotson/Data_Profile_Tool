# Palmer Penguins Raw Example: Source Context

## Why this example is here

`examples/palmer_penguins_raw.csv` is a well-documented real-world scientific dataset with 344 observations and 17 fields. It provides dates, identifiers, categorical text, continuous measurements, isotope values, comments, and genuine missingness without deliberate corruption by this repository.

It is especially useful for evaluating whether a profile remains understandable when physical measurement, study metadata, biological categories, and free-text notes coexist.

## Original source

The file is the published `penguins_raw.csv` from the **palmerpenguins** project. The package was developed as a modern, approachable alternative to the Iris dataset for statistics and data-science education. The raw data were imported from species-specific packages in the Environmental Data Initiative repository. [palmerpenguins project](https://github.com/allisonhorst/palmerpenguins)

The package citation is: Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). *palmerpenguins: Palmer Archipelago (Antarctica) penguin data*. [DOI: 10.5281/zenodo.3960218](https://doi.org/10.5281/zenodo.3960218).

The data are available under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). The package documentation also asks users to follow the Palmer Station LTER data-access policy and appropriately cite the underlying research and data packages.

## Collection method

The measurements were collected from 2007 through 2009 by Dr. Kristen Gorman in collaboration with Palmer Station Long Term Ecological Research. The observations cover adult male and female Adélie, Chinstrap, and Gentoo penguins breeding on Biscoe, Dream, and Torgersen islands in the Palmer Archipelago, Antarctica.

Recorded information includes:

- bill length and depth;
- flipper length and body mass;
- clutch observations, including egg date and completion;
- molecularly determined sex; and
- carbon and nitrogen stable-isotope measurements from red blood cells.

The R Journal's dataset article describes these origins, the EDI source packages, variables, and educational uses. [Palmer Archipelago Penguins Data in the palmerpenguins R Package](https://journal.r-project.org/articles/RJ-2022-020/)

The complete field and scientific methods are documented in Gorman, Williams, and Fraser (2014), which studied ecological sexual dimorphism and environmental variability among the three *Pygoscelis* species. [Original PLOS ONE study](https://doi.org/10.1371/journal.pone.0090081)

## What one row represents

One row represents one sampled penguin observation. The raw fields include study name, sample number, species, region, island, life stage, individual ID, clutch completion, egg date, body measurements, sex, stable-isotope values, and comments.

The repository file contains:

- 152 Adélie observations;
- 124 Gentoo observations;
- 68 Chinstrap observations;
- 168 observations from Biscoe, 124 from Dream, and 52 from Torgersen; and
- study seasons represented by `PAL0708`, `PAL0809`, and `PAL0910`.

An individual ID should be treated as an identifier, not a continuous number. Sample number is likewise an ordered label within study context and should not automatically be interpreted as a quantitative outcome.

## Raw versus curated Palmer Penguins

The palmerpenguins package provides both `penguins_raw` and a simpler `penguins` table. This repository intentionally includes the raw version. According to the package paper, the raw table has 17 variables and 336 missing cells, or roughly 5.7% of all cells. The curated version retains all 344 observations but reduces and renames fields, converts categories, changes one recorded sex value from `.` to missing, and derives year from clutch observations.

That distinction matters: results or field names documented for the curated eight-variable dataset should not be assumed to match this raw file exactly.

## Data quality and analytical cautions

- Missingness differs across measurements and metadata; it should be reported before filtering.
- Species, island, and study year are not independent. Study design and ecological context can confound simple pooled relationships.
- Male and female body measurements differ, and species differ in size. A pooled correlation can obscure group structure.
- Sample sizes are unequal across species, sex, island, and year.
- Stable-isotope values require domain knowledge; their signs and scales should not be treated as generic negative outliers.
- Comments may explain unusual or missing measurements and should not be discarded without review.
- These are sampled breeding penguins in a specific region and period, not a census of all penguins or all populations of the three species.

The dataset article identifies suitable learning uses including wrangling, visualization, linear modeling, principal components analysis, clustering, classification, grouping, and examples of Simpson's paradox. Those uses still require attention to study structure rather than treating every row as exchangeable.

## Changes made for this repository

None. `palmer_penguins_raw.csv` is copied from the published package path without altering rows, fields, missing cells, or values. Its filename was made explicit for the examples folder, but its contents remain the published raw CSV.

## Appropriate uses

- Profiling mixed scientific variables and missingness
- Assigning identifier, date, categorical, continuous, and text roles
- Comparing raw and reviewed role classification
- Teaching grouping and confounding across species, island, sex, and year
- Testing future metadata-grounded agent explanations
- Demonstrating why negative isotope values are not automatically erroneous

## Inappropriate uses and cautions

- Do not interpret correlations as causal ecological relationships.
- Do not generalize to all penguin species, regions, or time periods.
- Do not treat missing measurements as absence of the biological characteristic.
- Do not merge raw and curated field definitions without documenting the transformation.
- Do not “correct” scientific values based only on generic range intuition.

## Guidance for a future agent

An agent should identify this as field-collected ecological data, retain the distinction between raw and curated Palmer Penguins, and ground interpretation in species, island, sex, and year. It should use measurement units from field names, recognize comments as contextual evidence, and avoid labeling isotope values or group differences as quality defects without scientific rules.

## Key references

- [palmerpenguins repository and license](https://github.com/allisonhorst/palmerpenguins)
- [R Journal dataset article](https://journal.r-project.org/articles/RJ-2022-020/)
- [Original ecological study](https://doi.org/10.1371/journal.pone.0090081)
- [Package citation DOI](https://doi.org/10.5281/zenodo.3960218)
- [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)

