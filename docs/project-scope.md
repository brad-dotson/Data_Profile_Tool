# Project Scope

## Goal

Create a simple tool that accepts an unfamiliar dataset and produces useful, repeatable profiles before any cleaning or modeling work begins.

The recurring workflow is:

1. Ingest a dataset.
2. Generate a blind profile.
3. Review and configure column roles.
4. Generate a configured profile.
5. Retain the configuration and outputs with that dataset, isolated from other datasets.

Each dataset has exactly one configuration file containing its identity, important fields, column roles, and later version-specific expectations.

Each input file is one dataset project. Multi-sheet Excel workbooks stay together as projects containing multiple named source tables. Profiles use a consistent `source_table` field even for single-table inputs.

Every project lives under `Projects/<user-provided-name>/`, which contains its single YAML configuration and all blind, configured, and later-version outputs.

## Audience

The initial audience is a hands-on analyst working locally. The workflow should remain understandable to someone who did not build the tool and should not require editing application code for each dataset.

## Version boundaries

### Version 1: Profile

- CSV and Excel sources
- Blind type inference
- Separate physical datatype and reviewed analytical role
- Column-level summary
- Categorical attribute breakdown
- Human-reviewed column-role configuration
- Configured profile
- Independent project folders and run history for unrelated datasets
- Preserved, versioned flat-file inputs and safe blind reruns
- Basic missingness distinctions, unique ratio, numeric zero/NaN counts, and string-length metrics
- Optional user context fields without automatic semantic claims

### Version 2: Check

- Identifier uniqueness and missingness
- Continuous ranges and outliers
- Expected categorical values
- Date validity and ranges
- Geography validity
- Configurable rules and clear findings

Checks report evidence; they do not silently clean the data.

### Version 3: Report

- Polished PDF output
- Clear narrative, tables, and visualizations
- Suitable for internal or client-facing delivery
- Based on the same structured profile and check results

## Explicitly out of scope for Version 1

- Cleaning or transforming source values
- Employer- or client-specific schemas or mappings
- Compensation, incentive, gender-ratio, or management analysis
- Client-specific business rules
- Duplicate-ID, outlier, range, geography, or category validation
- Database input
- PDF reports
- Dashboards or hosted applications
- Automatic interpretation of domain meaning

## Product principles

- One obvious workflow
- One authoritative configuration file per dataset
- Safe defaults
- Source data remains unchanged
- Human decisions override heuristics
- Dataset projects do not share configurations accidentally
- Outputs are both understandable to people and usable by later software
- New capabilities earn their complexity
