# AGENTS.md

This file provides repository-specific guidance for Codex and other coding agents.

## Mission

Build a simple, reusable data-profiling tool. A user supplies a dataset, receives a blind profile, reviews column roles, and receives a configured profile. Repeated datasets and runs must remain clearly separated.

Each dataset has exactly one evolving configuration file. Do not split dataset metadata, column roles, important-field declarations, or future validation expectations across competing configuration files.

Treat one input file as one dataset project. Model CSV and Excel worksheet data consistently as named source tables, and retain `source_table` in structured outputs even when only one table exists. Never silently omit a discovered sheet: report exclusions and reasons in the dataset overview.

Create user dataset projects only under `Projects/<user-provided-name>/`. Keep that project's source information, single YAML configuration, and every run output together there. Do not scatter user artifacts across repository-level `data/`, `output/`, or per-table project folders.

For CSV and Excel, `blind` creates the project and preserves a byte-for-byte source copy under a versioned `input/` directory. An existing project name must fail safely with actionable `configured` and `reblind` commands. `reblind` preserves history and updates the one YAML without discarding compatible reviewed settings.

## Current phase

Version 1 is implemented and being tested and refined. Do not implement Version 2 checks, Version 3 PDF reporting, Version 4 agent behavior, or Version 5 monitoring unless the user explicitly changes the scope.

Before substantive work, read `README.md`, `HOW_TO.md`, and the files under `docs/`.

## Scope guardrails

- Keep Version 1 limited to profiling CSV and Excel data, reviewing column roles, and producing a configured profile.
- Do not add employer- or client-specific fields, compensation logic, client rules, employee checks, or algorithm preparation.
- Do not modify source datasets during profiling.
- Do not commit private datasets, generated profiles, credentials, or secrets.
- Preserve the blanket `Projects/*` ignore rule and test representative inputs, YAML, outputs, logs, and reports with `git check-ignore` when changing project layout.
- Do not commit, push, create branches, or open pull requests unless the user explicitly requests it.
- Preserve unrelated user changes and inspect Git state before editing.

## Working style

- The user commonly dictates requests by voice. Resolve obvious transcription ambiguity from context and surface consequential uncertainty before acting.
- Work in small, reviewable checkpoints and explain meaningful tradeoffs in plain language.
- Prefer a complete narrow workflow over speculative extensibility.
- Add or update tests and documentation with implementation changes.
- Keep `HOW_TO.md` accurate and runnable as the primary user acceptance path; never document unimplemented commands as available.
- Keep domain-specific rules configurable and outside the core profiling engine.
- Preserve the simple interaction: run once, edit one configuration file, run again.
- Follow `docs/error-handling.md`: distinguish warnings, table failures, and run failures; use atomic writes; and present user choices in plain language.

## Intended boundaries

Keep these concerns distinct:

1. Read a source into an internal table.
2. Profile that table without mutating it.
3. Read and validate reviewed configuration.
4. Render outputs.

This separation should allow future database inputs and PDF outputs without rewriting the profiling behavior. It does not require a complex framework in Version 1.
