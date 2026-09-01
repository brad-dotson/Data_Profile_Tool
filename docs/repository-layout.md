# Repository Layout

## Tracked source repository

```text
Data_Profile_Tool/
├── AGENTS.md
├── HOW_TO.md
├── README.md
├── requirements.txt
├── Projects/
│   └── README.md
├── docs/
│   ├── agent-vision.md
│   ├── decisions.md
│   ├── error-handling.md
│   ├── future-improvements.md
│   ├── market-research.md
│   ├── project-scope.md
│   ├── repository-layout.md
│   ├── roadmap.md
│   ├── user-flow.md
│   └── version-1-requirements.md
├── examples/
├── src/
│   └── data_profile_tool/
└── tests/
```

The package under `src/data_profile_tool/` contains the Version 1 reader, profiler, configuration, project, output, and command modules. `tests/` contains the automated acceptance coverage.

## Local projects

`Projects/` is the only user-facing home for datasets, configuration, and generated results. Each child directory is named by the user during the first command:

```text
Projects/
└── <dataset-project>/
    ├── input/
    │   └── <source-version-id>/
    │       └── <preserved-source-file>
    ├── dataset-config.yaml
    └── outputs/
        ├── blind/<run-id>/
        └── configured/<run-id>/
```

This is the implemented convention. YAML is the accepted format and `dataset-config.yaml` is the authoritative filename. The `blind` action creates the named project folder and initial configuration automatically.

There is exactly one configuration file per project. It is reused and extended over time rather than copied into separate blind, configured, validation, or reporting configurations. Run outputs may contain snapshots of the effective configuration for auditability, but those snapshots are not editable sources of truth.

One logical supplied source maps to one project. Within that project, a CSV has one named source table, an Excel workbook may have multiple worksheet-backed source tables, and a future database source may contain many tables. Flat-file versions are copied under `input/<source-version-id>/`, and YAML identifies the active version. All outputs remain in the one project folder. Table inclusion and per-column settings remain nested in the one YAML file.

Project contents are ignored by Git by default because they may contain private data. `Projects/README.md` is tracked so the folder and instructions remain visible in a fresh clone.

The ignore rule covers the entire user-created project tree: inputs, YAML, outputs, metadata, logs, checks, outliers, and reports. New artifact types under a project do not require separate ignore rules.

## Naming rules

- Dataset-project names should be stable, short, and filesystem-safe.
- Run directories should sort chronologically and be unique.
- Run identifiers use the machine's local timezone in `YYYY_MM_DD_HH_MM_SS_TZ` form.
- Flat-file source-version identifiers use the same readable local-time form.
- Output names should state whether they are blind or configured.
- One authoritative configuration belongs to each dataset project.

## Separation of concerns

Future code should keep four responsibilities distinct without overengineering them:

- Readers load CSV, Excel, and future sources.
- Profiling functions calculate summaries from an in-memory table.
- Configuration functions validate reviewed analytical roles.
- Writers serialize structured results to Excel and future formats.

The entry point coordinates these pieces and owns project/run creation.
