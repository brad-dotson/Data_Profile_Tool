# Automobile Messy Example: Source Context

## Why this example is here

`examples/automobile_messy.csv` is the deliberately difficult Version 1 test source. It is small enough to inspect manually but contains categorical, integer, and continuous fields alongside several kinds of missing or invalid representation. It is useful for checking whether a profile reveals problems without silently cleaning them.

This repository file is a **test adaptation**, not an untouched copy of the research dataset. An agent should use it to reason about profiling behavior, not to reproduce published automotive results.

## Original source

The base data are UCI's **Automobile**, also called the 1985 Auto Imports Database. UCI reports 205 observations and 25 features; the original file has 26 columns when the insurance-risk `symboling` field is included. The feature families are categorical, integer, and real-valued. UCI attributes the dataset to Jeffrey C. Schlimmer and dates its donation to May 1987. [UCI Automobile dataset page](https://archive.ics.uci.edu/dataset/10/automobile)

The source documentation says the database was compiled from:

- 1985 model import car and truck specifications in *Ward's Automotive Yearbook*;
- personal automobile manuals from Insurance Services Office; and
- an insurance collision report from the Insurance Institute for Highway Safety.

That makes this a compiled secondary dataset, not a single survey, experiment, or sensor collection. The public documentation does not provide enough detail to reconstruct record linkage or quality-control procedures across those inputs. Future analysis should not invent that provenance.

The canonical citation is: Schlimmer, J. (1985). *Automobile*. UCI Machine Learning Repository. [DOI: 10.24432/C5B01C](https://doi.org/10.24432/C5B01C).

UCI distributes the dataset under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/), which permits sharing and adaptation with attribution.

## What one row represents

One row describes an automobile model/configuration using three broad groups of information:

1. Vehicle specifications, such as make, body style, dimensions, engine characteristics, fuel system, horsepower, mileage, and price.
2. An assigned insurance risk rating, `symboling`, ranging from -3 to +3. UCI describes +3 as relatively risky and -3 as relatively safe.
3. `normalized-losses`, a normalized estimate of average insurance loss payment per insured vehicle year within a vehicle-size classification.

The row should not automatically be interpreted as an individual physical car, transaction, owner, crash, or insurance claim.

## Original data quality and known limitations

The source already contains genuine profiling challenges:

- Missing values are encoded with `?`, not as actual nulls.
- UCI reports missingness in normalized losses, number of doors, bore, stroke, horsepower, peak RPM, and price.
- Some variables that are analytically numeric can be physically read as strings because `?` shares the column.
- Several categories use compact domain codes such as `std`, `turbo`, `mpfi`, and `ohcv`.
- The documented make value `peugot` appears to be a misspelling, but it remains part of the published source vocabulary. A profiler should report it; correction requires a cleaning decision.
- The data describe the mid-1980s import market and should not be generalized to present-day vehicles, prices, safety, fuel economy, or insurance risk.
- The 205 rows are not documented as a statistically representative sample of all automobiles.

The dataset has historically been used for regression, including vehicle-price prediction. UCI notes an early instance-based price-prediction analysis that discarded records with missing values, leaving 159 cases. That historical choice is not a recommendation for this project; it illustrates why missingness and filtering decisions must be visible.

## Changes made for this repository

The repository adaptation adds headers from the UCI data dictionary and introduces a small deterministic set of test problems:

- one duplicate row;
- five blank cells;
- one literal `NULL` token;
- one invalid `num-of-doors` value, `three`;
- one misspelled fuel value, `gass`;
- one value with surrounding whitespace;
- one extreme price of `999999`; and
- the original `?` missing-value markers and source vocabulary remain present.

These additions exist solely to exercise profiling. They are not observations from UCI, Ward's, insurers, or vehicle manufacturers. Any future agent must distinguish `source-originated` issues from `repository-added test anomalies`.

## Appropriate uses

- Blind profiling and role-inference testing
- Demonstrating that nulls, blanks, whitespace, and sentinel strings are distinct
- Reviewing categorical vocabularies and high-cardinality behavior
- Testing detection-oriented Version 2 ideas such as invalid categories, duplicate rows, range checks, and outliers
- Teaching why physical type and analytical role can differ

## Inappropriate uses and cautions

- Do not use the adapted file for automotive market conclusions or model benchmarking against published results.
- Do not treat the added outlier or invalid entries as genuine historical records.
- Do not assume `?`, `NULL`, and blank all mean the same thing without a reviewed rule.
- Do not infer causality from vehicle attributes, price, symboling, or normalized losses.
- Do not normalize spelling or coded categories during profiling; that belongs to later reviewed cleaning.

## Guidance for a future agent

When this source is paired with a profile, an agent should first identify the repository adaptation, verify row count and source-table identity, and separate observed evidence from domain interpretation. It should call out sentinel values and mixed physical types, but it should not claim a value is wrong merely because it is unusual. The agent should cite this document when explaining why known anomalies exist.

## Key references

- [UCI Automobile dataset](https://archive.ics.uci.edu/dataset/10/automobile)
- [Canonical dataset DOI](https://doi.org/10.24432/C5B01C)
- [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)

