# Decision Log

Record consequential product and technical decisions here so voice discussions do not get lost.

## Accepted

### 2026-08-29 — Focused profiling rebuild

The new project will reproduce the useful blind and configured summaries without carrying forward the legacy cleaning and client-delivery pipeline.

### 2026-08-29 — Three-version progression

- Version 1 profiles data.
- Version 2 adds checks.
- Version 3 creates a polished PDF report.

Later-version needs may influence interfaces, but their features will not be implemented early.

### 2026-08-29 — Dataset isolation

Inputs, configurations, and outputs for unrelated datasets must remain visibly and operationally separate. Reruns must not silently overwrite prior results.

### 2026-08-29 — Initial inference rule

The blind run writes suggested roles for every included column into YAML. The Version 1 heuristic uses physical type plus default high-cardinality boundaries of 50 unique non-null values or a 20% unique ratio once a column has at least 50 non-null rows. High-cardinality numeric columns suggest continuous, high-cardinality strings suggest text, booleans suggest categorical, and physical datetimes suggest date. Count and ratio boundaries are optional command inputs and saved for reproducibility. Identifier, geography, and combined continuous/categorical meanings require user review.

### 2026-08-29 — Preserve source data

Profiling and checks report on source data without mutating it.

### 2026-08-29 — One configuration file per dataset

Each dataset has one authoritative, evolving configuration file. It contains dataset identity and context, important fields, per-column classifications, and later optional validation or report settings. Blind and configured runs must not create competing configuration sources.

### 2026-08-29 — Run, edit, run again

Blind and configured summaries are phases of the same tool. The intended interaction is: provide a dataset, run the tool, review its blind output and generated configuration, edit that one configuration, then run the tool again for the configured summary.

### 2026-08-29 — YAML configuration

Each dataset's single authoritative configuration file uses YAML. This supports readable metadata, important-field declarations, per-column roles, and later optional check and report settings in one file.

### 2026-08-29 — Explicit actions in one tool

The tool exposes explicit `blind`, `reblind`, and `configured` actions backed by shared implementation. It does not infer the intended phase automatically or maintain duplicated scripts.

### 2026-08-29 — Low-cost Version 1 profile improvements

Version 1 distinguishes physical type from analytical role; supports categorical, continuous, continuous_categorical, identifier, date, text, geography, and ignore roles with simple summaries; distinguishes null, empty, and whitespace-only values; and adds unique ratio, numeric zero/NaN counts, and string-length statistics. The combined role produces continuous statistics plus a categorical breakdown. It does not add role-specific checks or infer business meaning.

### 2026-08-31 — Preserve raw data; interpret rather than silently sanitize

The blind profile observes the preserved source as supplied. It does not silently trim strings, remove escape characters, replace sentinel values, or standardize categories before measuring them, because doing so would conceal the issues the profile is intended to reveal. Safety controls serialize values without executing them; future database connectors must use parameterized operations rather than mutate source text.

A later, explicit configuration may declare dataset- or column-specific missing-value tokens such as `?`, `NULL`, or `N/A`. Outputs should then retain raw missingness and add interpreted missingness or warnings side by side. Any optional normalized view must remain traceable to raw values and must never overwrite the preserved input.

### 2026-08-29 — Input sheets and output tabs are distinct

An input file represents one dataset project. A CSV supplies one named table, while an Excel workbook supplies one named table per worksheet. Multi-sheet workbooks remain one project, and table-level inclusion and column settings live in the project's single YAML file. Output workbooks use standardized tabs rather than creating output tabs for every input table.

### 2026-08-29 — Stable table-aware output schema

`Dataset Overview`, `Column Summary`, and `Attribute Breakdown` identify the source table consistently, including for single-table CSV and Excel inputs. CSV table names default to the source filename without its extension. This small redundancy keeps configuration, outputs, tests, automation, and future database support consistent.

### 2026-08-29 — Visible exclusions

Hidden Excel worksheets are discovered but excluded by default. Every discovered table remains listed in `Dataset Overview` and YAML with its visibility, inclusion status, and exclusion reason so no input silently disappears.

### 2026-08-29 — Projects is the user-facing home

Every supplied source receives one user-named folder under `Projects/`. Its source information, one authoritative YAML configuration, and all blind, configured, check, and report outputs stay together. Multi-sheet workbooks and future multi-table database sources remain one project rather than creating a project per table.

### 2026-08-29 — Root how-to guide is the acceptance path

`HOW_TO.md` is the primary hands-on user guide, separate from the overview in `README.md` and detailed design documents under `docs/`. Version 1 is not complete until a first-time user can follow the how-to without undocumented knowledge or editing application code.

### 2026-08-29 — Command and terminology

The executable is `data-profile`, with explicit `blind`, `reblind`, and `configured` actions. “Configured summary” is the primary term; “mapped summary” is retained only when discussing the legacy project.

### 2026-08-29 — Machine-readable artifacts

Each run stores CSV versions of standardized result tables and JSON run metadata alongside the human-readable Excel workbook. These portable formats support Versions 2 and 3 without adding a specialized storage dependency.

### 2026-08-29 — Sample-value privacy default

Raw representative or sample values are excluded by default because they can reveal identifiers or sensitive information and provide weak type evidence. A future explicit configuration setting may enable them when appropriate.

### 2026-08-29 — Project and run naming

The user supplies a stable filesystem-safe project name. Runs use readable machine-local timestamps in the form `YYYY_MM_DD_HH_MM_SS_TZ`, live beneath their action folder, and never silently overwrite an existing run.

### 2026-08-29 — Blind creates and preserves flat-file input

CSV and Excel users do not need a separate project-creation command. The initial `blind` action creates the project and copies the source byte-for-byte into a versioned `input/` folder. YAML records the active source version. External originals and earlier preserved versions are never modified or silently overwritten.

Future database connectors will define their own connection and extraction behavior rather than implying that the whole database is copied.

### 2026-08-29 — Explicit reblind workflow

`reblind <project>` produces a new blind run from the active preserved source. `reblind <project> <new-source>` preserves and activates a new source version before profiling it. Compatible reviewed settings remain, schema changes require review, and previous inputs and outputs stay intact.

Only a configuration marked `reviewed: true` preserves user-selected roles during reblind. An unreviewed configuration is still a set of suggestions, so changing an inference threshold refreshes both `inferred_role` and `role`. This prevents stale suggestions from contradicting the current inference while protecting deliberate reviewed choices.

The initial `blind` action refuses an existing project name, confirms that nothing changed, and presents labeled choices for `configured`, `reblind` with the active source, `reblind` with an updated source, or `blind` with another project name.

### 2026-08-29 — Project artifacts are private by default

Everything beneath a user-created `Projects/<name>/` folder is ignored by Git, including inputs, YAML, outputs, metadata, logs, checks, outliers, and future reports. Only `Projects/README.md` is exempt. Tests must verify representative ignore behavior.

### 2026-08-29 — Errors explain choices and preserve truth

Terminal errors state what happened, what changed or was preserved, and the user's choices. Harmless special characters are serialized safely. Ambiguous blank or duplicate headers fail clearly rather than being renamed silently. Table problems remain visible, and partial artifacts are never presented as successful runs. Detailed requirements live in `docs/error-handling.md`.

## Pending

No unresolved Version 1 product decisions are currently recorded.
