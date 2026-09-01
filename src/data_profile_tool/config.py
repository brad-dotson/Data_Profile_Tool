"""Read and maintain the single YAML configuration for each project."""

from __future__ import annotations

from pathlib import Path

import yaml

from .errors import UserError

ALLOWED_ROLES = {
    "categorical", "continuous", "continuous_categorical", "identifier",
    "date", "text", "geography", "ignore",
}


def load_config(path: Path) -> dict:
    if not path.exists(): raise UserError(f"Configuration file not found: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise UserError(f"The configuration YAML is invalid: {exc}") from exc
    return data


def save_config(path: Path, data: dict) -> None:
    temporary = path.with_suffix(".yaml.tmp")
    temporary.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    temporary.replace(path)


def roles_from_config(data: dict) -> dict[str, dict[str, str]]:
    roles: dict[str, dict[str, str]] = {}
    for table_name, table in data.get("tables", {}).items():
        if not table.get("include", True): continue
        roles[table_name] = {}
        for column_name, column in table.get("columns", {}).items():
            if not column.get("in_active_source", True): continue
            role = column.get("role")
            if role not in ALLOWED_ROLES:
                raise UserError(f"Invalid role '{role}' for {table_name}.{column_name}. Choose: {', '.join(sorted(ALLOWED_ROLES))}.")
            roles[table_name][column_name] = role
    return roles


def validate_schema(data: dict, actual: dict[str, set[str]]) -> None:
    problems: list[str] = []
    configured = data.get("tables", {})
    for table_name, table in configured.items():
        if not table.get("include", True) or not table.get("in_active_source", True): continue
        if table_name not in actual:
            problems.append(f"Configured table is not in the active source: {table_name}")
            continue
        expected = {name for name, column in table.get("columns", {}).items() if column.get("in_active_source", True)}
        missing = sorted(expected - actual[table_name])
        new = sorted(actual[table_name] - expected)
        if missing: problems.append(f"Configured columns missing from {table_name}: {', '.join(missing)}")
        if new: problems.append(f"Active source columns missing from the YAML for {table_name}: {', '.join(new)}")
    if problems:
        raise UserError("The YAML does not match the active source schema:\n- " + "\n- ".join(problems) + "\nRun reblind to reconcile the schema.")


def make_config(*, project_name: str, source: dict, settings: dict, inferred: dict,
                table_states: dict[str, dict[str, object]] | None = None, previous: dict | None = None) -> dict:
    previous = previous or {}
    preserve_reviewed_roles = previous.get("reviewed") is True
    old_tables = previous.get("tables", {})
    tables: dict = {}
    schema_changed = bool(previous)
    old_schema = {(t, c) for t, tv in old_tables.items() for c, cv in tv.get("columns", {}).items() if cv.get("in_active_source", True)}
    new_schema = {(t, c) for t, cv in inferred.items() for c in cv}
    if old_schema == new_schema: schema_changed = False
    table_states = table_states or {name: {"include": True, "in_active_source": True} for name in inferred}
    for table_name, state in table_states.items():
        columns = inferred.get(table_name, {})
        old_table = old_tables.get(table_name, {})
        new_columns = {}
        for column_name, facts in columns.items():
            old = old_table.get("columns", {}).get(column_name, {})
            new_columns[column_name] = {
                "in_active_source": True, **facts,
                "role": old.get("role", facts["role"]) if preserve_reviewed_roles else facts["role"],
                "description": old.get("description", ""), "unit": old.get("unit", ""),
            }
        for column_name, old in old_table.get("columns", {}).items():
            if column_name not in new_columns:
                new_columns[column_name] = {**old, "in_active_source": False}
        tables[table_name] = {"include": old_table.get("include", state.get("include", True)),
                              "in_active_source": True, "status": state.get("status", "included"),
                              "exclusion_reason": state.get("exclusion_reason", ""), "columns": new_columns}
    for table_name, old_table in old_tables.items():
        if table_name not in tables:
            tables[table_name] = {**old_table, "include": False, "in_active_source": False}
    context = previous.get("context", {"description": "", "intended_use": "", "row_definition": "", "owner": "", "important_fields": []})
    return {"version": 1, "project": {"id": project_name, "display_name": previous.get("project", {}).get("display_name", project_name)},
            "context": context, "source": source, "profiling": settings,
            "reviewed": previous.get("reviewed", False) if not schema_changed else False,
            "tables": tables}
