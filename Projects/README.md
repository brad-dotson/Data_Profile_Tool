# Projects

This is the user-facing home for profiled data sources.

The initial `blind` command will create one folder here using the project name supplied by the user. For example:

```text
Projects/
└── weather-analysis/
    ├── input/
    │   └── <source-version-id>/
    │       └── weather.xlsx
    ├── dataset-config.yaml
    └── outputs/
        ├── blind/<run-id>/
        └── configured/<run-id>/
```

A project represents one supplied source:

- One CSV file with one named source table
- One Excel workbook with one or many worksheet-backed source tables
- In the future, one database source with one or many tables

All tables from that source stay together in the project. Standardized output tables use `source_table` so users can filter and identify results without splitting one source into multiple projects.

The first `blind` command creates the project and copies its flat-file source into `input/`; there is no separate setup command. The `reblind` action can reuse the active preserved source or copy an updated source into a new version folder. Earlier inputs and outputs remain intact.

Everything inside a user-created project is ignored by Git because it may contain private data. This includes preserved inputs, `dataset-config.yaml`, outputs, metadata, logs, checks, outliers, and reports. Only this guide is intended to be committed.
