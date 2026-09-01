"""Command-line entry point for the Version 1 workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import load_config, make_config, roles_from_config, save_config, validate_schema
from .errors import UserError
from .outputs import write_outputs
from .profiling import profile
from .projects import preserve_source, project_path
from .sources import read_source


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def add_source_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--encoding", default="utf-8-sig", help="CSV encoding (default: utf-8-sig)")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter (default: comma)")
    parser.add_argument("--categorical-threshold", type=int, default=50,
                        help="Unique-value threshold used during automatic role inference (default: 50)")
    parser.add_argument("--categorical-ratio-threshold", type=float, default=0.20,
                        help="Unique/non-null ratio used during automatic role inference (default: 0.20)")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="data-profile", description="Create a simple blind or configured data profile.")
    root.add_argument("--projects-root", type=Path, default=repository_root(), help=argparse.SUPPRESS)
    commands = root.add_subparsers(dest="command", required=True)
    blind = commands.add_parser("blind", help="Create a new project and blind profile")
    blind.add_argument("source", type=Path); blind.add_argument("--name", required=True)
    add_source_options(blind)
    reblind = commands.add_parser("reblind", help="Profile a newer source version while preserving history")
    reblind.add_argument("project"); reblind.add_argument("source", type=Path, nargs="?")
    reblind.add_argument("--encoding", default="utf-8-sig"); reblind.add_argument("--delimiter", default=",")
    reblind.add_argument("--categorical-threshold", type=int)
    reblind.add_argument("--categorical-ratio-threshold", type=float)
    configured = commands.add_parser("configured", help="Create a profile using the reviewed YAML roles")
    configured.add_argument("project"); configured.add_argument("--encoding", default="utf-8-sig"); configured.add_argument("--delimiter", default=",")
    return root


def validate_settings(threshold: int, ratio: float) -> None:
    if threshold < 1: raise UserError("--categorical-threshold must be at least 1.")
    if not 0 <= ratio <= 1: raise UserError("--categorical-ratio-threshold must be between 0 and 1.")


def write_profile(project: Path, kind: str, result, metadata: dict) -> Path:
    output = write_outputs(project, kind, result, metadata)
    if result.warnings:
        print(f"\nProfile completed with {len(result.warnings)} warning(s):", file=sys.stderr)
        for warning in result.warnings:
            print(f"- {warning}", file=sys.stderr)
        print("The output was still created. These warnings did not change or truncate the source data.\n", file=sys.stderr)
    return output


def run_blind(args: argparse.Namespace) -> Path:
    project = project_path(args.projects_root, args.name)
    if project.exists():
        raise UserError(
            f"Project '{args.name}' already exists. Nothing was overwritten.\n\nYou may choose one of these options:\n"
            f"  1. Run the configured profile: data-profile configured {args.name}\n"
            f"  2. Preserve and profile updated data: data-profile reblind {args.name} PATH_TO_NEW_SOURCE\n"
            "  3. Use a different project name with data-profile blind\n"
            f"  4. Open Projects/{args.name}/ to review the existing project"
        )
    validate_settings(args.categorical_threshold, args.categorical_ratio_threshold)
    project.mkdir(parents=True)
    try:
        source_info = preserve_source(args.source.resolve(), project)
        preserved = project / source_info["preserved_path"]
        tables = read_source(preserved, encoding=args.encoding, delimiter=args.delimiter)
        settings = {"categorical_threshold": args.categorical_threshold,
                    "categorical_ratio_threshold": args.categorical_ratio_threshold,
                    "csv_encoding": args.encoding, "csv_delimiter": args.delimiter}
        result = profile(tables, threshold=args.categorical_threshold, ratio_threshold=args.categorical_ratio_threshold)
        states = {table.name: {"include": table.status == "included", "status": table.status,
                               "exclusion_reason": table.exclusion_reason or table.error} for table in tables}
        config = make_config(project_name=args.name, source=source_info, settings=settings, inferred=result.inferred, table_states=states)
        save_config(project / "dataset-config.yaml", config)
        return write_profile(project, "blind", result, {"project": args.name, "source": source_info})
    except Exception as exc:
        (project / "ERROR.txt").write_text(f"The project was created, but profiling did not finish.\n\n{exc}\n", encoding="utf-8")
        raise


def run_reblind(args: argparse.Namespace) -> Path:
    project = project_path(args.projects_root, args.project)
    config_path = project / "dataset-config.yaml"
    previous = load_config(config_path)
    source_info = previous.get("source", {})
    if args.source is not None:
        source_info = preserve_source(args.source.resolve(), project)
    preserved = project / source_info.get("preserved_path", "")
    settings = previous.get("profiling", {"categorical_threshold": 50, "categorical_ratio_threshold": .20})
    threshold = args.categorical_threshold if args.categorical_threshold is not None else int(settings.get("categorical_threshold", 50))
    ratio = args.categorical_ratio_threshold if args.categorical_ratio_threshold is not None else float(settings.get("categorical_ratio_threshold", .20))
    validate_settings(threshold, ratio)
    settings = {**settings, "categorical_threshold": threshold, "categorical_ratio_threshold": ratio}
    tables = read_source(preserved, encoding=args.encoding, delimiter=args.delimiter)
    result = profile(tables, threshold=threshold, ratio_threshold=ratio)
    states = {table.name: {"include": table.status == "included", "status": table.status,
                           "exclusion_reason": table.exclusion_reason or table.error} for table in tables}
    updated = make_config(project_name=args.project, source=source_info, settings=settings, inferred=result.inferred,
                          table_states=states, previous=previous)
    save_config(config_path, updated)
    return write_profile(project, "blind", result, {"project": args.project, "source": source_info, "rerun": True})


def run_configured(args: argparse.Namespace) -> Path:
    project = project_path(args.projects_root, args.project)
    config = load_config(project / "dataset-config.yaml")
    if config.get("reviewed") is not True:
        raise UserError("The YAML is not marked reviewed. Review the roles, set 'reviewed: true', and run this command again.")
    source = config.get("source", {})
    preserved = project / source.get("preserved_path", "")
    settings = config.get("profiling", {})
    threshold, ratio = int(settings.get("categorical_threshold", 50)), float(settings.get("categorical_ratio_threshold", .20))
    tables = read_source(preserved, encoding=settings.get("csv_encoding", args.encoding), delimiter=settings.get("csv_delimiter", args.delimiter))
    actual = {table.name: set(table.frame.columns) for table in tables if table.frame is not None}
    validate_schema(config, actual)
    configured_tables = config.get("tables", {})
    for table in tables:
        table_config = configured_tables.get(table.name)
        if table_config is not None and not table_config.get("include", True):
            table.status = "excluded"
            table.exclusion_reason = table_config.get("exclusion_reason") or "Excluded in dataset-config.yaml"
    result = profile(tables, threshold=threshold, ratio_threshold=ratio, configured_roles=roles_from_config(config))
    return write_profile(project, "configured", result, {"project": args.project, "source": source})


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        output = {"blind": run_blind, "reblind": run_reblind, "configured": run_configured}[args.command](args)
        print(f"Profile complete.\n\nOpen: {output}")
        return 0
    except UserError as exc:
        print(f"Could not complete the profile.\n\n{exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Could not complete the profile because of an unexpected error.\n\n{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
