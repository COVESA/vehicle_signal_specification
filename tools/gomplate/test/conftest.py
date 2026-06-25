from __future__ import annotations

import sys
import pytest
from pathlib import Path

GOMPLATE_BIN_DIR = Path(__file__).resolve().parent / "__pycache__/bin"

SRC_DIR = str(Path(__file__).resolve().parent.parent / "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dependencies import resolve_gomplate_tool  # noqa: E402


@pytest.fixture()
def workspace(tmp_path: Path) -> dict[str, Path]:
    """Create a temporary directory."""
    templates_dir = tmp_path / "templates"
    spec_dir = tmp_path / "spec"
    config_dir = tmp_path / "config"
    templates_dir.mkdir()
    spec_dir.mkdir()
    config_dir.mkdir()
    return {"root": tmp_path, "templates": templates_dir, "spec": spec_dir, "config": config_dir}


@pytest.fixture(scope="session")
def gomplate_cmd() -> str:
    """Ensure gomplate is available for the entire test session."""
    cmd = resolve_gomplate_tool(GOMPLATE_BIN_DIR, False)
    if cmd is None:
        pytest.skip("gomplate not installed.")
    return cmd
