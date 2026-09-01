# Prioritized Future Improvements

This document prevents valuable ideas from bloating Version 1. Priorities may change after real user testing.

## Version 1: Profile — implement now

Keep the workflow simple while adding inexpensive safeguards against misleading summaries:

- Distinguish physical/storage datatype from analytical role.
- Support reviewed roles: categorical, continuous, continuous_categorical, identifier, date, text, geography, and ignore.
- Add reviewed dataset- or column-specific missing-value tokens and report possible/interpreted missingness alongside raw missingness.
- Detect leading/trailing whitespace and other normalization candidates without silently changing the source or hiding the raw categories.
- Give each role a small, clearly defined Version 1 summary; do not add role-specific validation yet.
- Infer using physical type, unique count, and unique ratio rather than unique count alone.
- Distinguish actual null, empty string, and whitespace-only counts.
- Add unique percentage.
- Add zero and NaN counts for numeric columns.
- Add minimum, average, and maximum string lengths for string-like columns.
- Preserve observed facts, inferred roles, and reviewed roles as separate fields.
- Allow optional, blank-by-default context fields: intended use, row definition/grain, owner, table/column descriptions, units, and an importance reason.
- Warn on high-cardinality categorical output and preserve privacy defaults.

Version 1 does not infer business meaning, grain, units, ownership, relationships, or fitness for purpose.

## Version 2: Check

Add explicit, user-reviewed checks:

- Schema presence and physical-type compatibility
- Identifier uniqueness, missingness, and formatting
- Continuous parsing, expected ranges, zeros, missingness, and outliers
- Categorical allowed values, unexpected values, rare values, and missing sentinels
- Date parsing, plausible ranges, future dates, and freshness
- Geography reference lists and hierarchy consistency
- Text patterns and length limits
- Severity, evidence detail, and actionable failure messages
- Optional candidate-key suggestions, clearly labeled as inferences
- User-declared primary and foreign-key checks across tables

Relationship checks should rely on explicit user metadata or reliable database constraints. Version 2 should not claim to understand relationships merely because column names resemble one another.

## Version 3: Report

Create a polished PDF that prioritizes decisions:

- Executive dataset overview
- Important fields and user context
- Most consequential missingness, invalidity, outliers, and failed checks
- Concise distributions and categorical views
- Table relationship findings when configured
- Clear exclusions and limitations
- Recommended investigation order
- Configurable branding and disclosure text
- Privacy-aware evidence

The PDF is a presentation layer over structured results, not a second analysis implementation.

## Version 4: Agent-ready understanding

Create a structured metadata package and conversational agent experience. See `docs/agent-vision.md`.

The user should be able to ask what the data contains, what a field means, what appears risky, which findings are observed versus inferred, and what additional context is needed. A later cleaning/validation agent may use reviewed metadata and findings to propose actions without silently altering data.

## Version 5: Longitudinal comparison and monitoring

- Compare schema, profile metrics, category sets, and distributions across runs.
- Show row-count, null-rate, unique-rate, zero-rate, and summary-statistic deltas.
- Detect new, removed, or type-changed columns and tables.
- Detect new/disappearing categories and numeric/categorical drift.
- Compare against prior runs and user-selected baselines.
- Support schedules, notifications, and streaming or recurring workflows later.
- Preserve configuration-version context so changes in rules are not confused with changes in data.

## Later platform capabilities

- Database and warehouse connectors
- Catalog, glossary, lineage, and ownership integrations
- Extraction of declared primary/foreign keys and source documentation
- Query and table selection for large databases
- Sampling and approximate-statistic policies with clear disclosure
- Multi-table relationship discovery with confidence and human review
- Data contracts and reusable schema/configuration templates
- Optional cleaning workflows kept separate from profiling evidence
- Hosted UI, interactive exploration, or collaborative annotations

## Concepts that require context

These cannot be reliably inferred from values alone:

- What one row represents
- Intended use and fitness for purpose
- Units, currency, scale, timezone, and periodicity
- Whether duplicates are valid events or data errors
- Which fields are keys or join relationships
- Accuracy against real-world truth
- Business-critical fields and acceptable missingness
- Sensitive-data handling requirements

The tool may suggest or ask about these later, but user or source-system metadata remains authoritative.
