# How to Use the Data Profile Tool

Use this guide when you have a dataset and want to understand it quickly.

> **Current status:** Version 1 is implemented. This guide is the hands-on operating guide and acceptance path.

## What you will do

1. Run a blind profile on a CSV or Excel file.
2. Review the generated summary.
3. Edit one YAML configuration file.
4. Run the configured profile.
5. Find everything for that dataset together under `Projects/`.

You will not need to edit Python code.

## Before your first run

Open a terminal in the repository and activate its Python environment:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install -e .
```

These setup steps should only be necessary when preparing a new local environment or updating dependencies.

If you want to test the tool before using your own data, start with one of the public datasets documented in [examples/README.md](examples/README.md). For example:

```bash
data-profile blind examples/automobile_messy.csv --name automobile-demo
```

## Step 1: Choose a project name

Every supplied data source gets one project folder. Choose a short name that will still make sense later, such as:

- `weather-analysis`
- `fantasy-football-2026`
- `logistics-orders`

The tool will create that project beneath `Projects/`. Do not create separate projects for worksheets or tables that belong to the same source.

## Step 2: Run the blind profile

Run:

```bash
data-profile blind <path-to-source> --name <project-name>
```

Example with a CSV:

```bash
data-profile blind data/fantasy_players.csv --name fantasy-football-2026
```

Example with an Excel workbook:

```bash
data-profile blind data/weather.xlsx --name weather-analysis
```

The blind run uses physical datatype, unique count, and unique ratio. Its default high-cardinality boundary is 50 unique non-null values. For datasets with at least 50 non-null rows, a 20% unique ratio is also high-cardinality evidence. This avoids treating nearly every field in a tiny dataset as high-cardinality. Numeric high-cardinality columns suggest continuous; string high-cardinality columns suggest text. Lower-cardinality columns suggest categorical.

To use different boundaries for this project:

```bash
data-profile blind data/weather.xlsx --name weather-analysis \
  --categorical-threshold 50 \
  --categorical-ratio-threshold 0.10
```

The tool saves both effective thresholds in `dataset-config.yaml` and run metadata. They are starting heuristics, not final classifications.

The blind run will:

- Create the named project; no separate setup command is required.
- Copy the source into a versioned folder under the project's `input/` directory without changing the original.
- Discover its tables.
- Suggest analytical roles using the initial unique-value rule.
- Create a blind Excel summary.
- Automatically create the project's single YAML configuration file, populated with every discovered table, column, and suggested role.
- Print the exact locations of the summary and configuration.

## Step 3: Find the project

Open the folder named in your command:

```text
Projects/
└── <project-name>/
    ├── input/
    │   └── <source-version-id>/
    │       └── <preserved-source-file>
    ├── dataset-config.yaml
    └── outputs/
        └── blind/
            └── <run-id>/
```

For example:

```text
Projects/weather-analysis/
```

Everything for this source stays in that project folder.

The YAML records which preserved input version is active. Older source versions remain available for reproducibility.

## Step 4: Review the blind summary

Open `<project-name>_blind_profile.xlsx` under `outputs/blind/<run-id>/`.

Version 1 will contain:

- **Dataset Overview** — every discovered source table, its size, whether it was included, and any exclusion reason
- **Column Summary** — column names, datatypes, missingness, unique counts, suggested roles, and continuous statistics where applicable
- **Attribute Breakdown** — counts and percentages for values in suggested categorical columns

In Column Summary, `unique_count` is the number of distinct non-null values. `unique_ratio` is `unique_count / non_null_count`: for example, 20 distinct values among 100 non-null rows produces `20%`. A high ratio can help identify high-cardinality columns, but it is descriptive rather than a quality score.

In Attribute Breakdown, `value` contains the actual category (or a readable missing-value label). `value_kind` explains how to interpret it: `value` for an ordinary value, `null` for a true missing value, `empty` for an empty string, or `whitespace` for a string containing only whitespace. Most rows therefore say `value`; the field exists to keep the exceptional cases unambiguous.

The workbook keeps cell gridlines visible. Every sheet freezes its header row; Column Summary also freezes `source_table`, `column_name`, and `analytical_role`. In Column Summary, those three fields appear first, followed by `physical_type` and the remaining metrics.

Every summary row includes `source_table`:

- For CSV, it defaults to the filename without its extension.
- For Excel, it is the worksheet name.

A multi-sheet workbook remains one project. Its worksheet results are kept together and can be filtered by `source_table`.

Hidden Excel worksheets appear in Dataset Overview but are excluded by default with a stated reason.

## Step 5: Edit the YAML configuration

Open:

```text
Projects/<project-name>/dataset-config.yaml
```

This is the only editable configuration file for the project.

### Fields you should edit

Review or add:

- The dataset's display or colloquial name
- A short description or notes
- The fields most important to understanding the dataset
- Which source tables should be included
- Each column's `role`
- Optional descriptions or units
- Columns that should be ignored

Version 1 roles are:

- `categorical`
- `continuous`
- `continuous_categorical`
- `identifier`
- `date`
- `text`
- `geography`
- `ignore`

Version 1 gives these roles simple, appropriate summaries. Role-specific validity checks belong to Version 2. The tool will not infer identifier or geography meaning from values alone.

Use `continuous_categorical` for an occasional numeric field—such as age or number of partners—when you want both the continuous statistics in Column Summary and every value's count and percentage in Attribute Breakdown. The blind heuristic never assigns this combined role automatically; it is a deliberate user choice.

For each column, change `role`; do not change `inferred_role`. The inferred value records what the blind run suggested, while `role` is your reviewed choice and becomes authoritative in the configured profile.

You may also edit `project.display_name`, the fields under `context`, each table's `include` setting, and column `description` or `unit`. Set top-level `reviewed` to `true` only after reviewing the configuration.

### Fields managed by the tool

Do not edit `version`, `project.id`, `source`, `profiling`, `status`, `exclusion_reason`, `physical_type`, `inferred_role`, or `in_active_source` unless you are deliberately repairing a damaged project. `in_active_source` is maintained by the tool and records whether a table or column still exists in the currently active source. During `reblind`, removed columns remain documented with `in_active_source: false` so prior configuration history is not silently lost.

Do not create another configuration file for the configured profile. Later checks and report settings will also be added to this same YAML file.

## Step 6: Run the configured profile

After reviewing the roles, change this top-level line:

```yaml
reviewed: false
```

to:

```yaml
reviewed: true
```

Save the YAML file, then run:

```bash
data-profile configured <project-name>
```

Example:

```bash
data-profile configured weather-analysis
```

The tool will:

- Locate the project beneath `Projects/`.
- Validate the YAML against the source tables and columns.
- Explain any configuration problems instead of silently guessing.
- Apply the reviewed roles.
- Create a configured Excel summary in a new run folder.
- Leave the source and earlier outputs unchanged.

Find `<project-name>_configured_profile.xlsx` under:

```text
Projects/<project-name>/outputs/configured/<run-id>/
```

## Step 7: Interpret the configured summary

The configured workbook uses the same standardized sheets as the blind workbook:

- `Dataset Overview`
- `Column Summary`
- `Attribute Breakdown`

Continuous columns receive numeric summary statistics. Categorical columns receive value-level counts and percentages. `continuous_categorical` columns receive both. Ignored columns remain documented but do not receive detailed profiling.

The configured run may finish with friendly terminal warnings. A warning does not block the output or alter the source. In Version 1, warnings call attention to:

- A `continuous` or `continuous_categorical` column whose populated values cannot all be interpreted numerically. Statistics use the values that can be parsed; if none can be parsed, the numeric statistics remain blank.
- A `categorical`, `continuous_categorical`, or `geography` column whose distinct-value count reaches the project's categorical threshold. The complete Attribute Breakdown is still written and is never silently truncated.

Review the named column and change its `role` only if the result is not what you intended.

Because the structure remains consistent, you can compare the blind and configured summaries without learning a second output format.

## Run another dataset

Choose another project name and repeat the blind command:

```bash
data-profile blind <new-source> --name <new-project-name>
```

The new configuration and outputs will live in a separate folder beneath `Projects/`. They will not be mixed with an existing project.

## Rerun an existing project

Do not run `blind` again with an existing project name. It will refuse safely and clearly present your options:

```text
Project "weather-analysis" already exists, so no files were changed.

Choose what you want to do next:
  1. Create the configured profile from the reviewed YAML:
     data-profile configured weather-analysis
  2. Create another blind profile from the active preserved source:
     data-profile reblind weather-analysis
  3. Preserve and profile an updated source:
     data-profile reblind weather-analysis <path-to-new-source>
  4. Create an unrelated project with a different name:
     data-profile blind <source> --name <different-name>
```

To rerun the blind summary against the currently preserved source:

```bash
data-profile reblind weather-analysis
```

To profile an updated version of the same logical source:

```bash
data-profile reblind weather-analysis data/weather-updated.xlsx
```

When a new source is provided, `reblind` copies it into a new versioned `input/` folder and preserves prior source versions. It creates a new blind output without overwriting previous runs.

The one YAML configuration remains authoritative. If it is marked `reviewed: true`, matching user-selected roles are retained. If it is still `reviewed: false`, `reblind` refreshes both `inferred_role` and `role` from the current data and thresholds. New tables and columns receive inferred settings, removed items are clearly marked, and schema changes require review before the next configured run.

`reblind` uses both thresholds stored in YAML unless you explicitly provide new `--categorical-threshold` or `--categorical-ratio-threshold` values.

If you are experimenting with thresholds, leave `reviewed: false`; the next `reblind` will update the suggested `role` values. Set `reviewed: true` only after you have made deliberate role choices that should survive future reblind runs.

Reuse a configuration with a later version of the same logical dataset only after the tool confirms that its tables and columns are compatible.

### Why did the blind command say my project already exists?

The initial `blind` action only creates new projects, protecting existing inputs, configuration, and outputs. The message explicitly presents available choices; none is implied to be the only correction.

## Common questions

### Where did my output go?

Look under:

```text
Projects/<project-name>/outputs/
```

The command should also print the exact saved location after every successful run.

### Why is an Excel worksheet missing from the detailed summaries?

Check `Dataset Overview`. Every discovered worksheet should be listed with its visibility, inclusion status, and exclusion reason. Hidden worksheets are excluded by default. You can review table inclusion in `dataset-config.yaml`.

### Why was an ID or date classified incorrectly?

The first blind run intentionally uses a simple unique-value heuristic. Correct the role in `dataset-config.yaml`, then run the configured profile. More specialized identifier and date behavior belongs to Version 2.

### Can I change the initial categorical threshold?

Yes. Pass `--categorical-threshold <positive-integer>` and/or `--categorical-ratio-threshold <number-between-0-and-1>` to the blind or reblind command. New projects default to 50 and 0.20, and the effective settings are saved for reproducibility. Reblind uses the project's saved settings unless you explicitly override them; projects created before this default changed may therefore continue to use 300 until reblinded with `--categorical-threshold 50`.

### Can I edit the original dataset through this tool?

No. Version 1 profiles the source without cleaning or changing it.

### Should I commit the Projects folder to Git?

No. Everything inside each project—including copied inputs, YAML, spreadsheets, CSV/JSON artifacts, logs, checks, outliers, and future reports—is intentionally ignored by Git. Only `Projects/README.md` is tracked.

### What if my column names contain quotes, slashes, Unicode, or other special characters?

Supported special characters are preserved and safely serialized rather than interpreted as code, paths, formulas, or YAML. Blank or duplicate headers are ambiguous and produce a clear table-level error instead of being silently renamed. See [Error handling](docs/error-handling.md) for detailed behavior and recovery rules.

## Definition of an easy experience

A first-time user should be able to complete the workflow using only this guide:

1. Run one blind command.
2. Find and understand the blind workbook.
3. Edit one clearly structured YAML file.
4. Run one configured command.
5. Find and understand the configured workbook.

If any of those steps require undocumented knowledge, unnecessary code changes, or guessing where files went, the workflow needs improvement.
