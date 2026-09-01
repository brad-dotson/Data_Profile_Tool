"""Project paths, input preservation, and run identifiers."""

from __future__ import annotations

import hashlib
import re
import shutil
from datetime import datetime
from pathlib import Path

from .errors import UserError

PROJECT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def validate_name(name: str) -> str:
    if not PROJECT_PATTERN.fullmatch(name):
        raise UserError("Project names may contain letters, numbers, hyphens, and underscores, and must start with a letter or number.")
    return name


def project_path(root: Path, name: str) -> Path:
    return root / "Projects" / validate_name(name)


def new_id(parent: Path) -> str:
    # Use the machine's local timezone and separators that stay readable in paths.
    local_now = datetime.now().astimezone()
    timezone_name = local_now.tzname() or local_now.strftime("%z") or "LOCAL"
    timezone_name = re.sub(r"[^A-Za-z0-9+-]", "_", timezone_name)
    base = f"{local_now.strftime('%Y_%m_%d_%H_%M_%S')}_{timezone_name}"
    candidate, number = base, 2
    while (parent / candidate).exists():
        candidate, number = f"{base}_{number}", number + 1
    return candidate


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""): digest.update(block)
    return digest.hexdigest()


def preserve_source(source: Path, project: Path) -> dict:
    if not source.is_file(): raise UserError(f"Source file not found: {source}")
    version_id = new_id(project / "input")
    folder = project / "input" / version_id
    folder.mkdir(parents=True)
    destination = folder / source.name
    temporary = folder / f".{source.name}.copying"
    try:
        shutil.copy2(source, temporary)
        if sha256(source) != sha256(temporary): raise UserError("The preserved source copy did not match the original.")
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return {"active_version": version_id, "original_filename": source.name,
            "preserved_path": str(destination.relative_to(project)), "sha256": sha256(destination),
            "size_bytes": destination.stat().st_size}
