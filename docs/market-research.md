# Data Profiling Market Research and User Needs

Research captured on 2026-08-29 to guide product development. This is directional market context, not a commitment to reproduce every enterprise feature.

## Executive finding

Leading products converge on a progression:

1. Observe structure, content, distributions, and missingness.
2. Add human context and expectations.
3. Validate and identify failing records.
4. Compare metrics over time and detect drift.
5. Communicate findings through catalogs, dashboards, alerts, and reports.

The Data Profile Tool already has a strong foundation: isolated projects, preserved inputs, explicit configuration, human-reviewed roles, comparable run artifacts, privacy defaults, and a simple run-review-run workflow.

The largest long-term opportunity is to bridge technical statistics with meaning, fitness for purpose, historical change, and a clear next action.

## Market patterns

### Databricks: historical profiles, slices, and drift

Databricks stores profile and drift metric tables. Metrics include count, nulls, distinctness, quantiles, frequent values, zeros, NaNs, and string lengths. It compares consecutive windows and baselines using distribution-drift measures, and supports time windows and data slices.

Sources:

- [Databricks data profiling](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling)
- [Databricks profile and drift metrics](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-output)

Product lesson: a profile should be a comparable, versioned observation rather than an isolated spreadsheet.

### AWS Glue: observations become reviewed rules

AWS Glue Data Quality analyzes tables, recommends editable rules, evaluates them, stores statistics, reports scores, supports anomaly detection, and can identify failed records. AWS distinguishes analyzers, which gather statistics, from rules, which assert a condition.

Sources:

- [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html)
- [AWS rule recommendations](https://docs.aws.amazon.com/glue/latest/dg/data-quality-getting-started.html)
- [AWS statistics and anomaly detection](https://docs.aws.amazon.com/glue/latest/dg/data-quality-anomaly-detection.html)

Product lesson: never silently turn an observed range or category set into an enduring rule. Suggestions require review.

### Alteryx: rapid visual comprehension

Alteryx emphasizes a holistic column view, data-quality bars, top values, histograms, data types, ranges, and drill-downs. It separates valid, mismatched, and missing values relative to the selected type.

Sources:

- [Alteryx Browse profiling](https://help.alteryx.com/current/en/designer/tools/in-out-tools/browse-tool.html)
- [Alteryx visual profiling](https://help.alteryx.com/dataprep/en/trifacta-application/concepts/feature-overviews/overview-of-visual-profiling.html)

Product lesson: later reports should prioritize what is surprising, important, or actionable rather than merely reproducing tables.

### Alation: statistics plus meaning, trust, and collaboration

Alation combines profiling with descriptions, data dictionaries, ownership/stewardship, warnings, endorsements, deprecations, samples, usage, lineage, checks, anomaly metrics, and root-cause workflows. It supports shallow and deep profiling.

Sources:

- [Working with Alation catalog data](https://docs.alation.com/en/latest/sources/WorkwithCatalogData/index.html)
- [Alation data-quality monitors](https://docs.alation.com/en/latest/steward/AlationDataQuality/ManageMonitors.html)
- [Alation data catalog](https://www.alation.com/product/data-catalog/)

Product lesson: technical facts become useful when paired with definitions, intended use, ownership, caveats, and trust signals.

### Collibra: current statistics and changes since prior runs

Collibra exposes descriptive statistics, types and shapes, quartiles, nulls, empties, uniques, and changes across runs. It treats nulls and empty strings as distinct conditions.

Sources:

- [Collibra data-quality concepts](https://productresources.collibra.com/docs/collibra/2026.02/Content/UnifiedDataQuality/ref_data-quality-concepts.htm)
- [Collibra data profile](https://productresources.collibra.com/docs/collibra/2026.02/Content/UnifiedDataQuality/co_profile.htm)

Product lesson: missingness has multiple forms, and deltas often matter more than isolated values.

### Great Expectations: explicit expectations and human-readable evidence

Great Expectations treats expectations as declarative assertions, validates batches, preserves results, and renders human-readable Data Docs. Its profiler-generated expectations are starting points, not domain truth, and validation output can vary from a Boolean result to complete failed-row evidence.

Sources:

- [Great Expectations: create an expectation](https://docs.greatexpectations.io/docs/core/define_expectations/create_an_expectation)
- [Great Expectations validation](https://docs.greatexpectations.io/docs/core/run_validations/)
- [Great Expectations result detail](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/choose_a_result_format/)

Product lesson: checks should be declarative, explainable, severity-aware, and capable of showing evidence without exposing more data than necessary.

## Data quality and literacy

Common quality dimensions include accuracy, completeness, consistency, timeliness, validity, and uniqueness. Relevance, reliability, accessibility, traceability, and fitness for purpose may also matter. Different use cases prioritize different dimensions; there is no universal quality score.

Sources:

- [IBM data-quality dimensions](https://www.ibm.com/think/topics/data-quality-dimensions)
- [NIST Research Data Framework: Data Quality](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/1500-18/NIST.SP.1500-18r2.html)

A user approaching unfamiliar data is trying to answer:

1. What is this dataset?
2. What does one row represent?
3. Which tables and columns exist?
4. What do fields mean?
5. Which fields matter for the intended use?
6. What is missing, unusual, or potentially misleading?
7. Is the data fit for this purpose?
8. What changed since the prior delivery?
9. Who can resolve ambiguity?
10. What should be investigated next?

Profiling answers structural questions well. Configuration adds human context. Checks address expectations. Reports and agents can translate results into decisions.

## Problems users repeatedly encounter

- Null, empty, whitespace, zero, and domain-specific sentinel values are conflated.
- Storage datatype is mistaken for analytical role.
- Fixed cardinality thresholds behave poorly across dataset sizes.
- Identifiers, free text, dates, ordinals, geography, currency, and percentages receive inappropriate summaries.
- Full categorical breakdowns become huge and expose sensitive or identifying values.
- Blank, duplicate, malformed, and special-character headers break naive implementations.
- Units, currency, scale, timezone, and grain are absent or misunderstood.
- Column profiles overlook keys and relationships between tables.
- A current snapshot hides schema and distribution changes over time.
- Generated rules overfit one observed batch.
- Quality scores imply certainty without purpose-specific rules and transparent weighting.
- Reports overwhelm users with metrics without identifying priorities or next actions.
- Sampling and approximate statistics are not disclosed.
- Data ownership, provenance, lineage, intended use, and business definitions are missing.

## Product implications

### Preserve the boundary between fact, inference, context, and expectation

- Fact: observed row count or null count.
- Inference: suggested analytical role.
- Context: user-supplied meaning, grain, unit, or importance.
- Expectation: reviewed rule such as uniqueness or allowed range.

Outputs and agent metadata must label these separately.

### Prefer fitness for purpose over a universal score

Quality depends on intended use. If a future score is introduced, expose its rules, severities, weights, exclusions, evidence, and limitations.

### Build for comparison without implementing monitoring early

Stable metric names, source hashes, run IDs, configuration versions, and machine-readable results allow later schema comparison and drift detection.

### Protect privacy and scale

Default to aggregates, suppress samples, identify high-cardinality output risks, and keep complete machine-readable results separate from concise human views.

### Make the next action obvious

Successful and failed runs should tell users what was learned, what needs review, what was excluded, and what they can do next.
