"""Read supported source files into consistently named tables."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import openpyxl
import pandas as pd

from .errors import UserError


@dataclass
class SourceTable:
    name: str
    frame: pd.DataFrame | None
    status: str = "included"
    exclusion_reason: str = ""
    error: str = ""


def _validate_headers(headers: list[object], table: str) -> list[str]:
    names = ["" if value is None else str(value) for value in headers]
    if any(not name.strip() for name in names):
        raise UserError(f"Table '{table}' has a blank column name. Give every column a name and try again.")
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise UserError(f"Table '{table}' has duplicate column names: {', '.join(duplicates)}.")
    return names


def read_source(path: Path, *, encoding: str = "utf-8-sig", delimiter: str = ",") -> list[SourceTable]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                headers = next(csv.reader(handle, delimiter=delimiter), None)
            if headers is None:
                raise UserError("The CSV is empty.")
            _validate_headers(headers, path.stem)
            frame = pd.read_csv(path, encoding=encoding, sep=delimiter, dtype_backend="numpy_nullable", keep_default_na=False)
            frame.columns = [str(column) for column in frame.columns]
            return [SourceTable(path.stem, frame)]
        except UnicodeDecodeError as exc:
            raise UserError(f"The CSV could not be decoded with '{encoding}'. Try --encoding with the correct value.") from exc
        except (csv.Error, pd.errors.ParserError) as exc:
            raise UserError(f"The CSV could not be read: {exc}") from exc

    if suffix == ".xlsx":
        try:
            workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
        except Exception as exc:
            raise UserError(f"The Excel workbook could not be opened: {exc}") from exc
        tables: list[SourceTable] = []
        for sheet in workbook.worksheets:
            if sheet.sheet_state != "visible":
                tables.append(SourceTable(sheet.title, None, "excluded", "Hidden sheet"))
                continue
            try:
                rows = list(sheet.iter_rows(values_only=True))
                if not rows:
                    tables.append(SourceTable(sheet.title, pd.DataFrame(), "included"))
                    continue
                headers = _validate_headers(list(rows[0]), sheet.title)
                tables.append(SourceTable(sheet.title, pd.DataFrame(rows[1:], columns=headers)))
            except UserError as exc:
                tables.append(SourceTable(sheet.title, None, "failed", error=str(exc)))
        workbook.close()
        return tables

    raise UserError("Version 1 supports .csv and .xlsx files only.")
