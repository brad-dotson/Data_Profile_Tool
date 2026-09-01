# Error Handling and Recovery

Version 1 should fail clearly, preserve evidence, and tell the user what they can do next. It must not silently discard rows, rename ambiguous columns, omit source tables, overwrite artifacts, or present a partial run as successful.

## Message standard

Every actionable terminal error should contain:

1. What happened
2. Which project, source, table, column, or configuration entry was affected
3. What was preserved or not written
4. The user's available options
5. Exact commands or file locations when useful

Options should be labeled as choices rather than implied mandatory fixes.

Example for an existing project:

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

## Project and command validation

Reject before copying or profiling:

- Missing required arguments
- Missing or unreadable source paths
- Unsupported source extensions
- A categorical threshold that is not a positive integer
- Empty, absolute, traversal-based, reserved, or otherwise unsafe project names
- An initial `blind` request whose project already exists
- `reblind` or `configured` requests whose project does not exist

Project names should use a conservative documented character set. Never reinterpret a name into a different existing project silently.

## Safe source preservation

For CSV and Excel sources:

- Copy into a temporary project/version location first.
- Verify byte size and SHA-256 hash against the original.
- Atomically promote the verified copy into `input/`.
- Record hash, size, original filename, preserved path, and timestamp.
- Do not activate a source version when copying or verification fails.
- Never delete or overwrite an older source version automatically.

Insufficient disk space, permission failures, disappearing files, or source changes during copying must produce clear errors. A failed new copy must not replace the active source.

## CSV input problems

Handle or report empty files, encoding errors, unexpected delimiters, quoting errors, malformed rows, inconsistent field counts, and files too large for available memory.

Version 1 should offer explicit encoding and delimiter options rather than silently skipping malformed rows. Report the approximate row when the parser provides it and suggest the relevant option.

## Excel input problems

Handle or report corrupt or unsupported workbooks, encryption, no readable worksheets, hidden or empty worksheets, merged title regions, irregular tables, and multiple independent tables in one worksheet.

Hidden sheets are excluded by default but listed in Dataset Overview and YAML. An unreadable sheet should also remain visible with its status and reason when the workbook can still be inspected.

One bad worksheet should not prevent other valid worksheets from completing. Report successfully profiled, excluded, and failed tables. If no table can be profiled, the run fails.

## Column names

Preserve exact source names internally and serialize them safely when they contain spaces, quotes, commas, slashes, backslashes, brackets, punctuation, Unicode, newlines, tabs, or YAML-significant characters such as colons, hashes, ampersands, and leading dashes.

Use library serialization and direct column access. Never construct expressions, YAML, paths, or formulas by interpolating raw column names.

Blank or duplicate headers are ambiguous. Do not silently rename or deduplicate them. Mark the table as failed with a clear explanation and header positions. Other valid workbook tables may continue; if it is the only table, the run fails while retaining the preserved input and diagnostics.

Prevent spreadsheet-formula injection when writing source-derived text beginning with `=`, `+`, `-`, or `@`. Treat it as data, not an output formula.

## Values and analytical roles

Mixed types, missing values, infinities, timestamps, and long text should not cause unhandled exceptions.

- Blind cardinality inference remains a suggestion.
- A configured `continuous` or `continuous_categorical` column with some unparseable populated values completes with a warning that states how many values were excluded from numeric statistics.
- If none of its populated values can be interpreted numerically, the run still completes truthfully, leaves numeric statistics blank, and warns that the user may choose another role. Version 1 does not silently change the reviewed role.
- A configured categorical-style breakdown at or above the project's categorical threshold completes with a warning stating its distinct-value count. The Attribute Breakdown remains complete and is never silently truncated.
- Escape or replace XML-invalid control characters only in the Excel presentation layer and report a warning; never change the preserved source.
- Use an unambiguous missing-value representation that cannot be confused with literal source text.

## Output limits and failures

Excel has row, column, sheet-name, and cell-length limits. Standard output sheet names are not derived from source names.

If a result exceeds one worksheet's row limit, keep the complete CSV, split the workbook result across clearly numbered sheets, and record the split in Dataset Overview and run metadata.

Write outputs to a temporary run directory and atomically promote them only after all required artifacts are complete. Do not leave a directory that looks successful after failure. Preserve a concise diagnostic log inside the ignored project area.

## YAML configuration errors

Report invalid syntax with line and column when available, missing keys, invalid roles or thresholds, duplicate entries, unknown or missing tables/columns, review required after schema change, and missing or hash-mismatched active sources.

Never repair or rewrite reviewed YAML silently. Any future automatic migration must create a backup and summarize every change.

## Warnings versus errors

- **Warning:** The run remains complete and truthful, such as an excluded hidden sheet.
- **Table failure:** One table fails, but other tables can complete and the failure remains visible.
- **Run failure:** No usable table exists, integrity is uncertain, or required outputs cannot complete.

Successful commands end with completed, excluded, and failed table counts; warning count; and exact output paths.

## Git privacy requirement

Everything below `Projects/` is ignored by Git except `Projects/README.md`, including preserved sources, YAML, workbooks, CSV/JSON artifacts, logs, diagnostics, future checks, outliers, and reports.

Automated tests must verify representative files in every project subdirectory are ignored. Normal documentation must never suggest force-adding project data to Git.
