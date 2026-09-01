# Data Profile Tool

A simple, reusable tool for understanding unfamiliar datasets before cleaning or modeling them.

For the hands-on operating instructions, start with [HOW_TO.md](HOW_TO.md).

## User flow

The intended user journey is deliberately short:

1. Provide a data source and choose a project name.
2. Run the tool's `blind` action.
3. Receive a blind summary and one dataset configuration file populated with suggested column roles.
4. Edit that single configuration file to correct roles and add dataset context, such as its colloquial name and important fields.
5. Run the tool's `configured` action on the same dataset.
6. Receive a configured summary that treats the edited configuration as authoritative.

Blind, reblind, and configured profiling are explicit actions in the same tool, backed by the same profiling engine rather than separate implementations. The goal is speed to understanding: provide data, run, review one YAML file, and run again.

See [User flow](docs/user-flow.md) for the detailed behavior.

This repository is a focused rebuild of the useful profiling workflow from a larger legacy data-cleaning project. It is not intended to reproduce that project's client-specific cleaning, compensation analysis, or algorithm-preparation logic.

## Project status

Version 1 is implemented. It profiles CSV and `.xlsx` sources, creates the project YAML automatically, and produces blind and configured Excel/CSV/JSON outputs. Versions 2 and later remain planning only.

The planned releases are:

- **Version 1 — Profile:** CSV and Excel input, blind summary, reviewed column configuration, and configured summary.
- **Version 2 — Check:** Configurable validation for identifiers, continuous values, categories, dates, geography, missingness, duplicates, ranges, and outliers.
- **Version 3 — Report:** A polished PDF report suitable for internal review or client delivery.
- **Version 4 — Understand:** An evidence-grounded conversational agent over the project's metadata, profiles, checks, and context.
- **Version 5 — Monitor:** Comparisons, deltas, drift, and recurring profiling across source versions.

See [Project scope](docs/project-scope.md), [Version 1 requirements](docs/version-1-requirements.md), and [Roadmap](docs/roadmap.md) for the agreed boundaries.

Long-term product research and direction are preserved in [Market research](docs/market-research.md), [Future improvements](docs/future-improvements.md), and [Agent vision](docs/agent-vision.md).

Failures and recovery follow [Error handling](docs/error-handling.md): explain what happened, preserve valid work, and present available choices rather than obscure technical failures.

## Example datasets

The tracked [examples](examples/README.md) provide three public, reusable test sources between 205 and 858 primary data rows:

- A deliberately messy Automobile CSV
- A three-sheet Cervical Cancer Risk Factors Excel workbook
- The raw Palmer Penguins CSV with realistic mixed scientific fields and missingness

Each example documents its source, license, citation, and any test-specific adaptation. No employer, client, or private data is included.

## Version 1 outputs

The blind and configured profiles will contain two primary tables:

- **Column Summary:** one row per source-table column, including `source_table`, source type, missingness, unique values, inferred/configured analytical role, and numeric statistics where applicable.
- **Attribute Breakdown:** one row per distinct categorical value, including `source_table`, count, and percentage.

Every source uses the same table-aware output schema. For CSV, `source_table` defaults to the filename without its extension. For Excel, it is the worksheet name. A multi-sheet workbook remains one dataset project containing multiple named source tables.

Output workbooks also include a **Dataset Overview** listing every discovered source table, whether it was included, and—when excluded—the reason. Hidden Excel sheets are visible there but excluded by default.

The blind heuristic uses physical datatype, unique count, and unique ratio. Its default high-cardinality rules are:

- 50 unique non-null values, or
- 20% unique among non-null values when the column has at least 50 non-null rows

High-cardinality numeric columns suggest continuous; high-cardinality strings suggest text; lower-cardinality columns suggest categorical. The count and ratio thresholds are optional command parameters and are saved in YAML and run metadata. These are suggestions; reviewed roles remain authoritative.

Users may assign `continuous_categorical` to numeric columns such as age or number of partners when both descriptive statistics and a full value-frequency breakdown are useful. The blind heuristic does not assign this combined role automatically.

## Dataset separation

## Projects folder

`Projects/` is the single user-facing home for dataset work. The name supplied to the initial `blind` command becomes a folder beneath `Projects/`. Everything generated for that source stays inside that folder, including all tables from a multi-sheet workbook or future database source.

Each project has a stable user-provided name, exactly one configuration file, and its own source information and run outputs:

```text
Projects/
└── fantasy-football/
    ├── input/
    │   └── <source-version-id>/
    ├── dataset-config.yaml
    └── outputs/
        ├── blind/
        └── configured/
```

The initial `blind` command creates the project and copies the source into a versioned folder under `input/`; users do not need a separate project-creation step. `reblind` can reuse the active preserved source or copy in a new version without deleting the old one.

That one configuration file evolves with the project. It can hold the project's display name, description, important fields, active source version, table settings, and reviewed column roles. Later versions can extend the same file with validation expectations rather than introducing competing configuration files.

All tables discovered in one source stay in that source's project folder. They remain distinguishable through `source_table` in the standardized outputs rather than being split into unrelated projects.

All contents beneath user-created project folders are ignored by Git—including inputs, YAML, outputs, metadata, logs, checks, and reports. The tracked [Projects guide](Projects/README.md) keeps the folder visible and explains its organization. YAML is the configuration format, and the executable name is `data-profile`.

## Repository layout

```text
Data_Profile_Tool/
├── AGENTS.md                 # Guidance for Codex and other coding agents
├── HOW_TO.md                 # Primary hands-on user guide and acceptance test
├── README.md                 # Project overview and quick start
├── Projects/                 # User-named local projects, configurations, and outputs
├── docs/                     # Requirements, workflow, decisions, and roadmap
├── examples/                 # Safe, synthetic examples (future)
├── src/data_profile_tool/    # Version 1 application code
├── tests/                    # Automated Version 1 tests
└── requirements.txt          # Python dependencies
```

Additional details are in [Repository layout](docs/repository-layout.md).

## Working locally

Open this folder in VS Code. It is configured to use the Python virtual environment in `.venv`.

If the environment is not active in a new terminal:

```bash
source .venv/bin/activate
```

Install the initial dependencies:

```bash
python -m pip install -e .
```

Then follow [HOW_TO.md](HOW_TO.md), beginning with `data-profile blind <source> --name <project>`.

## Principles

- Simple to run repeatedly on unrelated datasets.
- Never modify the source dataset while profiling it.
- Keep input handling, profiling, configuration, and output writing separate.
- Treat inferred types as suggestions and reviewed configuration as authoritative.
- Maintain one clear source of configuration per dataset.
- Prefer clear diagnostics over silent correction.
- Keep client- or domain-specific rules outside the profiling core.
- Build and finish one version before expanding into the next.
