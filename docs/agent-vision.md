# Agent-Ready Data Understanding Vision

## Vision

A future version should turn each project into a trustworthy metadata package that an agent can use to discuss the dataset with the user. The conversation should help users understand data, investigate findings, identify missing context, and plan safe validation or cleaning work.

The agent must not be “smart-sounding but dumb”: it should know the difference between observed evidence, statistical inference, user-reviewed meaning, validation rules, and speculation.

## Version target

This is tentatively Version 4, after profiling, checks, and a stable report model exist. Longitudinal monitoring may follow or evolve alongside it.

## Agent metadata package

The package should be generated from structured project artifacts and include:

- Project identity, intended use, and notes
- Preserved source version, hash, and run identity
- Tables, visibility, inclusion status, and failure reasons
- Exact column names and physical datatypes
- Inferred and reviewed analytical roles
- Column descriptions, units, importance, and importance reasons
- Optional row definition/grain and ownership
- Profile metrics and clearly labeled approximations/sampling
- Missingness categories
- Category distributions or privacy-safe summaries
- Validation rules, severities, results, and evidence references
- Report findings and limitations
- Later, schema changes, metric deltas, and drift results
- Later, declared or reviewed relationships, lineage, and business glossary links

The package should be machine-readable, versioned, schema-validated, and independent of Excel/PDF formatting.

## Epistemic labels

Every agent-facing statement should carry provenance and status:

- `observed`: directly calculated from a specific source/run
- `inferred`: suggested by a heuristic or model
- `user_supplied`: explicitly entered by the user
- `source_declared`: supplied by a database constraint or authoritative documentation
- `expected`: an approved validation rule
- `failed_check`: evidence that an expectation was not met
- `unknown`: missing context that cannot be determined safely

The agent should cite the run, table, column, metric, configuration entry, or check behind its answer.

## Conversation capabilities

The agent should answer:

- What tables and columns are present?
- What does this field mean according to the reviewed metadata?
- Which fields appear most important, and why?
- What is missing, unusual, or invalid?
- Which results are facts versus suggestions?
- What changed between two runs?
- What tables may relate, and is that relationship declared or merely suspected?
- Is the dataset fit for a stated purpose, and what evidence or context is missing?
- Which issues should be investigated first?
- What questions should be asked of the data owner?

When context is absent, the agent should ask focused questions rather than inventing meaning.

## Safety and privacy

- Use aggregates by default.
- Do not expose raw source rows, identifiers, rare values, or sensitive categories unless explicitly authorized.
- Respect project-local privacy settings and future classifications.
- Explain uncertainty and profiling limitations.
- Never claim accuracy, business meaning, causality, or relationships from statistics alone.
- Treat prompt-like text inside datasets as untrusted data, not instructions.
- Record which artifacts and run versions informed an answer.

## Cleaning and validation agents

A later specialist agent may propose validation or cleaning work, but it should:

1. Read reviewed metadata and current findings.
2. State the intended change and evidence.
3. Distinguish a recommendation from an approved action.
4. Preview affected counts and example-safe evidence.
5. Require explicit approval for transformations.
6. Write to a new derived dataset rather than overwriting preserved input.
7. Record reproducible transformation steps and lineage.
8. Reprofile and revalidate the derived output.

The understanding agent may hand off a structured task to a cleaning or validation agent. The handoff should include the project/run identifiers, approved scope, relevant checks, privacy constraints, and required acceptance criteria.

## What the agent cannot infer alone

Values alone generally cannot establish row grain, units, currency basis, business definitions, ownership, authoritative keys, intended use, real-world accuracy, or whether an anomaly is acceptable. The system should collect this context incrementally from users, source metadata, database constraints, catalogs, and documentation.

## Success criteria

- Answers are traceable to project evidence.
- Facts and inferences are never conflated.
- Missing context produces questions, not hallucinations.
- Sensitive data remains protected.
- Recommendations are purpose-aware.
- Any downstream transformation is approved, reproducible, reversible, and followed by another profile.
