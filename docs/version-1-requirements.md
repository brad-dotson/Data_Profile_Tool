# Version 1 Requirements

This document records the implemented Version 1 requirements.

## User workflow

1. The user identifies a CSV or Excel source and a dataset-project name.
2. The user runs the tool's `blind` action.
3. The tool creates the named project, preserves a copy of the source, creates a blind profile, and initializes the dataset's single configuration file without changing the original source.
4. The user edits that configuration file to review roles and add dataset context.
5. The user runs the tool's `configured` action.
6. The tool validates the configuration and creates a configured profile using the reviewed roles as authoritative.
7. Inputs, the one configuration file, and outputs remain together under `Projects/<dataset-project>/`.

## Inputs

- CSV files
- Excel workbooks (`.xlsx` initially)
- One dataset project per input file
- One named source table for a CSV; its default name is the filename without the extension
- One named source table per Excel worksheet
- All visible worksheet tables are included in the blind profile by default
- Hidden worksheets are discovered and reported but excluded by default
- The YAML configuration can include or exclude each table and records the reason for exclusions

Future input types should feed the same internal table interface, but database support is not a Version 1 requirement.

Version 1 expects each included worksheet to contain one rectangular table with headers in its first row. Multiple independent tables within one worksheet, merged title areas, and irregular report-style sheets are not initially supported.

For flat files, the initial `blind` action copies the source byte-for-byte into a versioned folder under `Projects/<project>/input/`. The preserved copy—not the original external path—becomes the active profiling source. The original external file is never modified.

A separate project-initialization command is not required for the standard CSV and Excel workflow. Future database connectors will define connection and extraction behavior separately; Version 1 should not pretend to copy an entire database.

## Initial analytical roles

Version 1 supports reviewed roles with deliberately limited profiling behavior:

- `categorical` — value counts and percentages
- `continuous` — numeric descriptive statistics
- `continuous_categorical` — both numeric descriptive statistics and value counts/percentages for an intentionally dual-use numeric field
- `identifier` — completeness and distinctness without exposing a full value breakdown
- `date` — completeness and chronological minimum/maximum when parseable
- `text` — completeness, distinctness, and string-length statistics without a full value breakdown
- `geography` — categorical-style breakdown without geographic validity claims
- `ignore` — retain in inventory but skip detailed profiling

Physical/storage datatype and analytical role are separate output and configuration fields. For example, a numeric employee number may have an integer physical type and an identifier analytical role. Version 1 does not add identifier, date, or geography validation; those checks belong to Version 2.

## Blind inference

The blind command automatically infers a role for every included source-table column and writes the suggestions into the newly created YAML configuration.

The evolved Version 1 heuristic uses physical type, unique count, and unique ratio:

- Boolean physical columns suggest `categorical`.
- Date/datetime physical columns suggest `date`.
- Numeric columns suggest `continuous` when unique count is at least 50, or when a column with at least 50 non-null rows has a unique ratio of at least 20%; otherwise they suggest `categorical`.
- String columns suggest `text` under the same high-cardinality rule; otherwise they suggest `categorical`.
- Mixed or unsupported physical types receive a visible warning and a conservative suggestion rather than causing failure.

Unique ratio is `unique non-null count / non-null count`. An all-null column has a zero unique ratio and requires review.

The blind command accepts optional `--categorical-threshold <positive-integer>` and `--categorical-ratio-threshold <number-between-0-and-1>` values, defaulting to 50 and 0.20. The ratio rule begins once the non-null row count reaches the configured count threshold, preventing tiny samples from appearing high-cardinality merely because most values differ. The combined `continuous_categorical` role is user-assigned rather than inferred.

The heuristic does not infer `identifier` or `geography`, because values alone cannot establish those meanings reliably. The user can assign them in YAML.

The output must label this as an inference, not a fact. The effective threshold is saved in the dataset YAML and run metadata. Reviewed per-column roles override it during configured profiling.

## Column Summary

At minimum, one row per source column with:

- Source-table name
- Column name
- Source/storage datatype
- Row count
- Non-null count
- Null count
- Null percentage
- Empty-string count and percentage
- Whitespace-only count and percentage, excluding empty strings
- Unique non-null count
- Unique ratio, defined as unique non-null count divided by non-null count
- Optional representative value, omitted by default for privacy
- Zero count for numeric columns
- NaN count for numeric columns when distinguishable by the parser; these values also contribute to null count
- Minimum, average, and maximum string length for string-like columns
- Inferred analytical role
- Configured analytical role, when applicable
- Count, mean, standard deviation, minimum, 25th percentile, median, 75th percentile, and maximum for continuous columns
- Minimum and maximum for configured date columns when parseable

Numeric statistics must remain blank or not applicable for other roles.

A configured `continuous` or `continuous_categorical` column with unparseable populated values produces a non-blocking terminal warning. Statistics use parseable values only; when none are parseable, numeric statistics remain blank. The tool reports counts without exposing the source values and does not silently change the reviewed role.

## Attribute Breakdown

At minimum, one row per distinct value of every categorical column with:

- Source-table name
- Column name
- Value
- Value kind: ordinary value, true null, empty string, or whitespace-only string
- Count
- Percentage of all rows
- Percentage of non-null rows
- An unambiguous representation of missing values

High-cardinality fields classified as categorical may create large outputs; Version 1 should warn clearly rather than silently truncate them.

During configured profiling, a categorical-style role whose distinct count reaches the project's categorical threshold produces a non-blocking terminal warning. The warning identifies the table and column, states the distinct count, confirms that output is complete, and suggests reviewing the role. This also applies to `continuous_categorical` and `geography` because they create Attribute Breakdown rows.

Actual nulls, empty strings, and whitespace-only strings remain distinct. Version 1 does not automatically treat values such as `N/A`, `Unknown`, `-`, `0`, `999`, or `1900-01-01` as missing. Dataset-specific sentinels belong in future reviewed checks.

## Configuration

Each dataset project has exactly one configuration file. It is the authoritative home for dataset-specific settings and evolves across profiling phases and future versions.

At minimum, it must support:

- Stable dataset-project identifier
- Colloquial or display name
- Optional description or notes
- Optional intended use
- Optional row definition/grain, supplied by the user rather than inferred
- Optional owner or subject-matter contact
- Source-file and Excel-sheet details where applicable
- Important fields, such as `pay`, with an optional reason explaining importance
- One entry per discovered source table, including inclusion status and exclusion reason
- One entry per source-table column
- Inferred and reviewed analytical roles
- Optional table and column descriptions and optional units
- A clear indication that the user has reviewed the configuration

It must also:

- List source column names exactly
- Qualify column settings by source table so repeated column names remain unambiguous
- Store one supported analytical role per column
- Be reusable for later files with a compatible schema
- Be validated before profiling
- Report unknown columns, missing configured columns, duplicate entries, and invalid roles
- Remain the single configuration source for the dataset; the tool must not create separate blind, mapped, check, or report configuration files

Version 2 may add expected ranges, allowed categories, uniqueness expectations, or other checks to this same file. Version 3 may add report metadata to it. Those later sections should remain optional until their versions are implemented.

The configuration format is YAML. One readable YAML file can represent dataset metadata, important fields, per-column settings, and future validation rules. The blind-summary workbook may display configuration information, but it must not become a second editable source of truth.

## Command behavior

The application is one tool with three explicit actions:

- `blind` creates a new project, copies and versions its flat-file source, creates the blind summary, and initializes the dataset YAML configuration.
- `reblind` creates another blind run for an existing project, using either its active preserved source or a newly supplied source version.
- `configured` validates that YAML and creates the configured summary.

The actions share readers, profiling calculations, configuration models, and output writers. They are not separate scripts or duplicated implementations. Explicit actions are preferred over automatically guessing the user's intent because they are predictable, easy to explain, and safe for future automation.

The executable is `data-profile`. The blind action accepts `--categorical-threshold` and `--categorical-ratio-threshold`, defaulting to 50 and 0.20. Reblind retains the project's stored settings unless the user supplies an override.

`blind` refuses if the requested project folder already exists. Its message must say that nothing changed and present the user's options: `configured`, `reblind` with the active source, `reblind` with an updated source, or `blind` with a different name. These are choices, not an implied mandatory fix.

`reblind <project>` reuses the active preserved source. `reblind <project> <new-source>` copies the new flat file into a new versioned input folder, marks it active in YAML, and preserves every earlier source version and output. It uses the threshold stored in YAML unless explicitly overridden.

When the prior configuration is marked reviewed, reblind retains compatible user-selected roles. When it is not reviewed, reblind refreshes both the inferred and working role from the current data and thresholds. It adds inferred settings for new tables and columns, marks removed items clearly, and requires configuration review after schema changes before `configured` can proceed.

## Outputs

- A human-readable Excel workbook for the blind profile
- A human-readable Excel workbook for the configured profile
- A `Dataset Overview` sheet listing every discovered table, row and column counts, visibility, inclusion status, and exclusion reason
- One reusable reviewed configuration file per dataset
- Run metadata sufficient to identify the source, sheet, time, tool version, inference rule, and row/column counts
- Machine-readable CSV versions of each standardized output table plus JSON run metadata, stored with the human-readable workbook
- Workbook names follow `<project>_blind_profile.xlsx` and `<project>_configured_profile.xlsx`.
- Workbooks retain visible cell gridlines. Every sheet freezes its header row; Column Summary also freezes `source_table`, `column_name`, and `analytical_role`.
- Column Summary begins with `source_table`, `column_name`, `analytical_role`, `physical_type`, `row_count`, and `unique_count` in that order.
- Attribute Breakdown places the actual `value` before `value_kind`; `value_kind` distinguishes ordinary values from true nulls, empty strings, and whitespace-only strings.

Outputs must not overwrite previous runs without explicit user intent.

The profiling output workbook is separate from the input workbook. Its sheets follow a standardized output schema. Version 1 includes `Dataset Overview`, `Column Summary`, and `Attribute Breakdown`; later versions may add sheets such as `Outliers` and `Check Results`.

`Column Summary` and `Attribute Breakdown` always include `source_table`, even when the source contains only one table. This stable schema avoids conditional output formats and supports filtering, automation, database sources, and repeated column names. Do not add blank spacer rows between tables.

## Dataset and run isolation

- `Projects/` is the single user-facing location for project artifacts.
- The initial command's user-provided project name becomes the folder name under `Projects/`.
- Every dataset project has a stable, user-provided name.
- Every execution has a unique, readable local-time identifier in `YYYY_MM_DD_HH_MM_SS_TZ` form.
- Configurations are scoped to a dataset project.
- Each dataset project has exactly one configuration file across all runs.
- Blind and configured outputs are distinguishable.
- The tool prevents ambiguous reuse of configuration across incompatible schemas.
- All source tables from one multi-table source remain within the same project folder.
- Each flat-file source version is preserved under `input/<source-version-id>/`.
- Local project contents are ignored by Git by default.
- Every item beneath a user project is ignored, including inputs, YAML, outputs, metadata, logs, checks, and reports. Only `Projects/README.md` is exempt.

## Safety and privacy

- Profiling never mutates the source data.
- Blind profiling observes raw values rather than silently trimming, replacing sentinels, or otherwise sanitizing them.
- Safety handling serializes values without executing them; it does not erase meaningful source characters.
- A future reviewed interpretation may identify dataset- or column-specific missing-value tokens and report both raw and interpreted missingness without overwriting the preserved input.
- Local data and generated outputs are ignored by Git by default.
- Errors identify the problem without exposing unnecessary source values.
- Representative values, rare values, and future outlier records may contain sensitive information; output policy must be revisited before client-facing use.
- Raw representative/sample values are excluded by default. A later explicit configuration option may enable them when appropriate.
- User context fields such as intended use, grain, units, descriptions, and importance reasons are optional and blank by default; Version 1 never fabricates them.
- Follow the validation, recovery, and atomic-write requirements in `docs/error-handling.md`.

## Usability

- The common workflow should require very few commands or decisions.
- Error messages should say what happened and how to correct it.
- A user should not need to edit Python code for a new dataset.
- Documentation must include one small, synthetic end-to-end example when implementation begins.

## Acceptance criteria

Version 1 is complete when a new user can independently:

1. Profile a CSV and an Excel sheet.
2. Locate and understand both blind-summary tables.
3. Correct column roles without editing application code.
4. Produce a configured summary that honors those roles.
5. Run a second unrelated dataset without mixing its artifacts with the first.
6. Rerun either dataset without unintentionally overwriting earlier results.
7. Find and edit all dataset-specific settings in one configuration file.
8. Profile a multi-sheet workbook as one project while keeping its worksheet tables distinguishable.
9. See every excluded or hidden worksheet and understand why it was excluded.
10. Find the project's configuration and every output together under its user-provided name in `Projects/`.
11. Rerun blind profiling with the preserved source or a new source version without losing earlier inputs, configuration, or outputs.
12. Receive actionable `configured` and `reblind` instructions when `blind` encounters an existing project name.
13. Profile harmless special-character column names without unsafe interpretation.
14. Receive clear table-level errors for blank or duplicate headers rather than silent renaming.
15. Confirm that representative project inputs, YAML, outputs, logs, and reports are ignored by Git.
16. Distinguish null, empty, and whitespace-only values in summary metrics.
17. View unique ratio, numeric zero/NaN counts, and string-length statistics where applicable.
18. Review physical datatype separately from analytical role and assign any supported Version 1 role.
