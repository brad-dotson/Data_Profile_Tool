# User Flow

The product should optimize for speed to understanding without requiring the user to edit application code.

## First run: blind profile

1. The user provides a CSV or Excel file and a short dataset-project name.
2. The user runs the tool's explicit `blind` action.
3. The tool creates `Projects/<dataset-project>/` using the user's project name; no separate initialization command is needed.
4. The tool copies the flat-file source into a versioned `input/` folder, reads the preserved copy without modifying it, and discovers its source tables.
5. The tool produces a Dataset Overview showing every discovered table and any exclusions.
6. The tool infers initial analytical roles and produces the blind Column Summary and Attribute Breakdown, identified by source table.
7. For Excel, visible worksheets are included by default; hidden worksheets are listed but excluded with a reason.
8. The tool automatically creates the dataset's one configuration file with source metadata, the effective inference threshold, table settings, every discovered column, and suggested roles.
9. The tool tells the user where the blind output and configuration were saved and what to do next.

## Review: one configuration file

The user opens the dataset's configuration file and may edit:

- Colloquial or display name
- Description or notes
- Important fields for understanding the dataset
- Which source tables should be included
- Analytical role for each column
- Whether a column should be ignored

The blind inference is a starting suggestion. The user's reviewed values become authoritative.

There is no separate mapped-summary configuration. Later validation and reporting settings will extend this same file in optional sections.

## Second run: configured profile

1. The user runs the same tool's explicit `configured` action for the dataset project.
2. The tool validates the configuration against the current source schema.
3. If configuration errors exist, the tool explains how to fix them and does not silently guess.
4. The tool produces a configured Column Summary and Attribute Breakdown.
5. Continuous statistics and categorical value breakdowns follow the reviewed roles; `continuous_categorical` produces both views for the same numeric column.
6. The new output receives its own run identifier and does not overwrite earlier results.

## Repeated use

Every unrelated source receives its own user-named folder under `Projects/` and one configuration file. A logistics configuration cannot silently affect fantasy-football or weather data.

A multi-sheet Excel workbook remains one project. Each worksheet is a named source table within it, and every output remains under that project's folder. A CSV is also represented as one named source table so the output format never changes based on table count. Future database tables will follow the same pattern.

Later deliveries of the same logical dataset may reuse its configuration only after the tool confirms schema compatibility.

Use `reblind <project>` to create another blind run from the active preserved source. Use `reblind <project> <new-source>` to preserve and profile an updated source version. Prior source versions and outputs remain intact.

If `blind` is given an existing project name, it refuses safely, confirms that nothing changed, and presents four labeled choices: configured profiling, reblind with the active source, reblind with a new source, or blind profiling under a different name.

## Intended experience

In plain language:

> Add data, run the tool, inspect the blind summary, edit one configuration file, and run again.

The executable is `data-profile` and exposes three explicit actions:

```text
data-profile blind <source> --name <dataset-project>
data-profile reblind <dataset-project> [new-source]
data-profile configured <dataset-project>
```

The blind action optionally accepts `--categorical-threshold <positive-integer>` and `--categorical-ratio-threshold <number-between-0-and-1>`, defaulting to 50 and 0.20. Reblind uses the project's saved thresholds unless explicitly overridden.

This avoids fragile automatic guessing while keeping both phases in one tool and one codebase.
