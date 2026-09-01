"""Write human-friendly and machine-readable profiling outputs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from .profiling import ProfileResult
from .projects import new_id


def _write_sheet(writer: pd.ExcelWriter, frame: pd.DataFrame, name: str, frozen_columns: int) -> None:
    frame.to_excel(writer, sheet_name=name, index=False)
    workbook, worksheet = writer.book, writer.sheets[name]
    header = workbook.add_format({"bold": True, "font_color": "white", "bg_color": "#1F4E78", "border": 1})
    percent = workbook.add_format({"num_format": "0.0%"})
    for index, column in enumerate(frame.columns):
        worksheet.write(0, index, column, header)
        values = frame[column].astype(str) if len(frame) else pd.Series(dtype=str)
        width = min(max(len(str(column)) + 2, values.str.len().max() + 2 if len(values) else 12), 45)
        worksheet.set_column(index, index, width, percent if "percent" in str(column) or "ratio" in str(column) else None)
    worksheet.freeze_panes(1, frozen_columns)
    worksheet.autofilter(0, 0, max(len(frame), 1), max(len(frame.columns) - 1, 0))


def write_outputs(project: Path, kind: str, result: ProfileResult, metadata: dict) -> Path:
    parent = project / "outputs" / kind
    run_id = new_id(parent)
    temporary = parent / f".{run_id}.writing"
    final = parent / run_id
    temporary.mkdir(parents=True)
    result.overview.to_csv(temporary / "dataset-overview.csv", index=False)
    result.columns.to_csv(temporary / "column-summary.csv", index=False)
    result.attributes.to_csv(temporary / "attribute-breakdown.csv", index=False)
    project_name = str(metadata["project"])
    workbook_name = f"{project_name}_{kind}_profile.xlsx"
    workbook_path = temporary / workbook_name
    with pd.ExcelWriter(workbook_path, engine="xlsxwriter", engine_kwargs={"options": {"strings_to_formulas": False}}) as writer:
        _write_sheet(writer, result.overview, "Dataset Overview", 1)
        _write_sheet(writer, result.columns, "Column Summary", 3)
        _write_sheet(writer, result.attributes, "Attribute Breakdown", 2)
    created_at = datetime.now().astimezone()
    payload = {**metadata, "run_id": run_id, "created_at_local": created_at.isoformat(),
               "timezone": str(created_at.tzinfo), "output_kind": kind,
               "files": [workbook_name, "dataset-overview.csv", "column-summary.csv", "attribute-breakdown.csv"]}
    (temporary / "run-metadata.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    parent.mkdir(parents=True, exist_ok=True)
    temporary.replace(final)
    return final
