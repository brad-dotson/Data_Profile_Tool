# Roadmap

## Current checkpoint: align before building

- Document goals, boundaries, outputs, and repository conventions.
- Preserve selected legacy artifacts as context.
- Resolve the pending Version 1 product decisions.

## Version 1: Profile

1. Implement the accepted `data-profile blind`, `reblind`, and `configured` command interface.
2. Define structured result schemas, role behavior, missingness metrics, and run metadata.
3. Build CSV ingestion and blind summaries.
4. Add Excel ingestion, multi-sheet discovery, visibility handling, and table-level isolation.
5. Write blind results to Excel.
6. Generate, edit, and validate the dataset's single configuration file.
7. Generate the configured profile.
8. Add `Projects/<user-provided-name>/` creation, versioned source preservation, and non-overwriting run behavior.
9. Test with small synthetic datasets representing different domains and awkward inputs.
10. Document an end-to-end example and declare Version 1 complete.

## Version 2: Check

Add configurable checks by analytical role:

- Identifier: uniqueness, missingness, and formatting
- Continuous: parsing, missingness, expected ranges, and explicit outlier methods
- Categorical: expected values, missingness, and rare values
- Date: parsing, valid ranges, and future-date rules
- Geography: reference-list and hierarchy consistency checks

Findings should identify affected counts and evidence without silently changing source data.

## Version 3: Report

- Render structured profile and check results into a polished PDF.
- Add concise narrative, tables, and useful visualizations.
- Add configurable title, branding, dataset context, and disclosure language.
- Review privacy rules for examples, rare categories, and row-level findings.

## Version 4: Agent-ready understanding

- Generate a versioned, schema-validated metadata package.
- Support evidence-grounded conversation over profiles, checks, context, and reports.
- Label observed, inferred, user-supplied, expected, and unknown information.
- Allow safe handoff to future validation or cleaning agents with explicit approval boundaries.

See `docs/agent-vision.md`.

## Version 5: Longitudinal comparison and monitoring

- Compare schema, metrics, categories, and distributions across runs.
- Show deltas and drift against prior runs or selected baselines.
- Preserve configuration-version context and later support scheduling or alerts.

## Later possibilities

- Database and query inputs
- Additional file formats
- Configuration reuse and schema-version management
- Deeper database relationship and lineage discovery
- Optional automated cleaning as a separate product concern
- Hosted or graphical interfaces, if the local workflow proves stable
