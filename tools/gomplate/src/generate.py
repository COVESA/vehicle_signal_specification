#!/usr/bin/env python3
"""Convert .vspec3 files using gomplate and copy .yaml files from spec/ to generated/."""

from __future__ import annotations

import logging
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from dependencies import resolve_gomplate_tool

# ── Constants ───
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
SPEC_DIR = ROOT_DIR / "spec"
GENERATED_DIR = ROOT_DIR / "generated"
CONFIG_PATH = ROOT_DIR / "tools" / "gomplate" / "src" / "config" / "gomplateConfig.yaml"
LOCAL_BIN_DIR = ROOT_DIR / ".tools" / "bin"

_PATH_RESOLVE_RE = re.compile(r"(?:\\|/)\.\./\.\./")

log = logging.getLogger("Generate")


def _setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def _error(msg: str) -> None:
    log.error(msg)
    sys.exit(1)


def _ensure_dirs(path: Path, cache: set[Path]) -> None:
    """Create parent directories once, tracked via *cache*."""

    if path.parent not in cache:
        path.parent.mkdir(parents=True, exist_ok=True)
        cache.add(path.parent)


def _resolved_gomplate_config() -> str:
    config = CONFIG_PATH.read_text(encoding="utf-8")
    root_posix = ROOT_DIR.as_posix()
    log.debug(f"Resolve Gomplate config {CONFIG_PATH}")
    return _PATH_RESOLVE_RE.sub(f"{root_posix}/", config.replace("\\", "/"))


def convert_vspec3_files(gomplate_cmd: str) -> None:
    """Render vspec3 in spec via gomplate."""

    vspec3_files = sorted(SPEC_DIR.rglob("*.vspec3"))
    if not vspec3_files:
        log.debug(f"No .vspec3 files found in {SPEC_DIR}")
        return

    log.debug(f"Found {len(vspec3_files)} .vspec3 files in {SPEC_DIR}")

    for f in vspec3_files:
        log.debug(f"  {f}")

    config = _resolved_gomplate_config()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(config)
        tmp_path = Path(tmp.name)

    created_dirs: set[Path] = set()
    try:
        for src in vspec3_files:
            dst = (GENERATED_DIR / src.relative_to(SPEC_DIR)).with_suffix(".vspec")
            _ensure_dirs(dst, created_dirs)

            cmd = [gomplate_cmd, "-f", str(src), "-o", str(dst), "--config", str(tmp_path)]
            log.debug(f"Running: {' '.join(cmd)}")

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            if proc.returncode != 0:
                _error(f"Template rendering failed for {src}:\n{proc.stderr}")
            if proc.stdout:
                log.debug(f"stdout: {proc.stdout.strip()}")
            if proc.stderr:
                log.debug(f"stderr: {proc.stderr.strip()}")

            log.debug(f"Rendered: {src.relative_to(ROOT_DIR)} -> {dst.relative_to(ROOT_DIR)}")
    finally:
        tmp_path.unlink(missing_ok=True)


def copy_yaml_files() -> None:
    """Copy Quantities / Units YAML files from spec"""

    yaml_files = sorted(SPEC_DIR.rglob("*.yaml"))

    if not yaml_files:
        log.debug(f"No .yaml files found in {SPEC_DIR}")
        return

    log.debug(f"Found {len(yaml_files)} .yaml files in {SPEC_DIR}")

    for f in yaml_files:
        log.debug(f"  {f}")

    created_dirs: set[Path] = set()
    for src in yaml_files:
        dst = GENERATED_DIR / src.relative_to(SPEC_DIR)
        _ensure_dirs(dst, created_dirs)
        shutil.copy2(src, dst)


def main() -> None:
    _setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    log.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

    if not SPEC_DIR.is_dir():
        _error(f"Spec directory not found: {SPEC_DIR}")

    gomplate_cmd = resolve_gomplate_tool(LOCAL_BIN_DIR, args.verbose)
    convert_vspec3_files(gomplate_cmd)
    copy_yaml_files()


if __name__ == "__main__":
    main()
