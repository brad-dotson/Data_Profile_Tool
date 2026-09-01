"""Version 1 descriptive profiling without validation judgments."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime

import numpy as np
import pandas as pd

from .sources import SourceTable


@dataclass
class ProfileResult:
    overview: pd.DataFrame
    columns: pd.DataFrame
    attributes: pd.DataFrame
    inferred: dict[str, dict[str, dict[str, object]]]
    warnings: list[str]


def physical_type(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series): return "boolean"
    if pd.api.types.is_datetime64_any_dtype(series): return "datetime"
    if pd.api.types.is_integer_dtype(series): return "integer"
    if pd.api.types.is_numeric_dtype(series): return "number"
    present = series.dropna()
    if len(present) and present.map(lambda value: isinstance(value, (date, datetime))).all(): return "datetime"
    return "string"


def infer_role(series: pd.Series, threshold: int, ratio_threshold: float) -> str:
    kind = physical_type(series)
    if kind == "boolean": return "categorical"
    if kind == "datetime": return "date"
    non_null = int(series.notna().sum())
    unique = int(series.nunique(dropna=True))
    ratio = unique / non_null if non_null else 0.0
    # The ratio protects larger datasets from a fixed cutoff, but is deliberately
    # not applied to tiny samples where nearly every column looks high-cardinality.
    high_cardinality = unique >= threshold or (non_null >= threshold and ratio >= ratio_threshold)
    if kind in {"integer", "number"}:
        return "continuous" if high_cardinality else "categorical"
    return "text" if high_cardinality else "categorical"


def _safe_number(value: object) -> object:
    if value is None or value is pd.NA: return None
    try:
        if math.isnan(float(value)): return None
    except (TypeError, ValueError):
        pass
    return value.item() if hasattr(value, "item") else value


def _column_row(table: str, name: str, series: pd.Series, role: str) -> dict[str, object]:
    count = len(series)
    non_null = int(series.notna().sum())
    nulls = count - non_null
    strings = series.dropna().astype(str)
    empty = int((strings == "").sum())
    whitespace = int(strings.str.fullmatch(r"\s+").sum())
    numeric = pd.to_numeric(series, errors="coerce")
    row: dict[str, object] = {
        "source_table": table, "column_name": name, "physical_type": physical_type(series),
        "analytical_role": role, "row_count": count, "non_null_count": non_null,
        "null_count": nulls, "null_percent": nulls / count if count else 0.0,
        "empty_string_count": empty, "empty_string_percent": empty / count if count else 0.0,
        "whitespace_only_count": whitespace, "whitespace_only_percent": whitespace / count if count else 0.0,
        "unique_count": int(series.nunique(dropna=True)),
        "unique_ratio": series.nunique(dropna=True) / non_null if non_null else 0.0,
        "zero_count": int((numeric == 0).sum()), "nan_count": int(series.map(lambda value: isinstance(value, float) and math.isnan(value)).sum()),
        "min_length": int(strings.str.len().min()) if len(strings) else None,
        "average_length": float(strings.str.len().mean()) if len(strings) else None,
        "max_length": int(strings.str.len().max()) if len(strings) else None,
        "mean": None, "standard_deviation": None, "minimum": None, "q1": None,
        "median": None, "q3": None, "maximum": None, "earliest_date": None, "latest_date": None,
    }
    if role in {"continuous", "continuous_categorical"} and numeric.notna().any():
        row.update({
            "mean": _safe_number(numeric.mean()), "standard_deviation": _safe_number(numeric.std()),
            "minimum": _safe_number(numeric.min()), "q1": _safe_number(numeric.quantile(.25)),
            "median": _safe_number(numeric.median()), "q3": _safe_number(numeric.quantile(.75)),
            "maximum": _safe_number(numeric.max()),
        })
    if role == "date":
        dates = pd.to_datetime(series, errors="coerce")
        if dates.notna().any():
            row["earliest_date"], row["latest_date"] = dates.min(), dates.max()
    return row


def _attribute_rows(table: str, name: str, series: pd.Series) -> list[dict[str, object]]:
    total, non_null = len(series), int(series.notna().sum())
    keys = series.map(lambda value: ("null", "(null)") if pd.isna(value) else
                      (("empty", "(empty string)") if str(value) == "" else
                       (("whitespace", "(whitespace only)") if str(value).strip() == "" else ("value", str(value)))))
    counts = keys.value_counts(dropna=False)
    return [{"source_table": table, "column_name": name, "value": value,
             "value_kind": kind, "count": int(count),
             "percent_of_all_rows": int(count) / total if total else 0.0,
             "percent_of_non_null_rows": (int(count) / non_null if non_null and kind != "null" else None)}
            for (kind, value), count in counts.items()]


def profile(tables: list[SourceTable], *, threshold: int, ratio_threshold: float,
            configured_roles: dict[str, dict[str, str]] | None = None) -> ProfileResult:
    overview, columns, attributes, inferred, warnings = [], [], [], {}, []
    is_configured = configured_roles is not None
    configured_roles = configured_roles or {}
    for table in tables:
        frame = table.frame
        overview.append({"source_table": table.name, "status": table.status,
                         "row_count": len(frame) if frame is not None else None,
                         "column_count": len(frame.columns) if frame is not None else None,
                         "exclusion_reason": table.exclusion_reason, "error": table.error})
        if table.status != "included" or frame is None: continue
        inferred[table.name] = {}
        for name in frame.columns:
            series = frame[name]
            guessed = infer_role(series, threshold, ratio_threshold)
            role = configured_roles.get(table.name, {}).get(name, guessed)
            non_null = int(series.notna().sum())
            unique = int(series.nunique(dropna=True))
            if is_configured and role in {"continuous", "continuous_categorical"} and non_null:
                numeric_count = int(pd.to_numeric(series, errors="coerce").notna().sum())
                unparsed_count = non_null - numeric_count
                if numeric_count == 0:
                    warnings.append(
                        f"{table.name}.{name} is configured as {role}, but none of its {non_null} non-null values "
                        "could be interpreted as numbers. Numeric statistics are blank. You may choose a different role "
                        "in dataset-config.yaml."
                    )
                elif unparsed_count:
                    warnings.append(
                        f"{table.name}.{name} is configured as {role}, but {unparsed_count} of its {non_null} non-null "
                        f"values could not be interpreted as numbers. Numeric statistics use the {numeric_count} parsed "
                        "values; review the source values and role if that is not intended."
                    )
            if is_configured and role in {"categorical", "continuous_categorical", "geography"} and unique >= threshold:
                warnings.append(
                    f"{table.name}.{name} is configured as {role} and has {unique} distinct non-null values. "
                    f"Attribute Breakdown will contain at least {unique} rows for this column. The output is complete and "
                    "not truncated; you may choose a different role if a full breakdown is not useful."
                )
            inferred[table.name][name] = {"physical_type": physical_type(series), "inferred_role": guessed, "role": role}
            columns.append(_column_row(table.name, name, series, role))
            if role in {"categorical", "continuous_categorical", "geography"}:
                attributes.extend(_attribute_rows(table.name, name, series))
    overview_names = ["source_table", "status", "row_count", "column_count", "exclusion_reason", "error"]
    column_names = ["source_table", "column_name", "analytical_role", "physical_type", "row_count", "unique_count", "non_null_count",
                    "null_count", "null_percent", "empty_string_count", "empty_string_percent", "whitespace_only_count",
                    "whitespace_only_percent", "unique_ratio", "zero_count", "nan_count",
                    "min_length", "average_length", "max_length", "mean",
                    "standard_deviation", "minimum", "q1", "median", "q3", "maximum", "earliest_date", "latest_date"]
    attribute_names = ["source_table", "column_name", "value", "value_kind", "count",
                       "percent_of_all_rows", "percent_of_non_null_rows"]
    return ProfileResult(pd.DataFrame(overview, columns=overview_names), pd.DataFrame(columns, columns=column_names),
                         pd.DataFrame(attributes, columns=attribute_names), inferred, warnings)
