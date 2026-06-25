#!/usr/bin/env python3

from __future__ import annotations

import logging
import platform
import shutil
import stat
import sys
import urllib.request
import urllib.error
from pathlib import Path

GOMPLATE_VERSION = "v5.0.0"

log = logging.getLogger("DEPS")

_SYSTEM = platform.system().lower()
_MACHINE = platform.machine().lower()
_IS_WINDOWS = _SYSTEM == "windows"
_EXE_SUFFIX = ".exe" if _IS_WINDOWS else ""

_ARCH_MAP: dict[str, str] = {
    "x86_64": "amd64",
    "amd64": "amd64",
    "aarch64": "arm64",
    "arm64": "arm64",
}

_OS_MAP: dict[str, str] = {
    "windows": "windows",
    "linux": "linux",
    "darwin": "darwin",
}


def _error(msg: str) -> None:
    log.error(msg)
    sys.exit(1)


def _resolve_platform() -> tuple[str, str]:
    """Return OS name and arch for the current platform"""

    os_name = _OS_MAP.get(_SYSTEM)
    arch = _ARCH_MAP.get(_MACHINE)

    if os_name is None:
        _error(f"Unsupported OS: {platform.system()}")
    if arch is None:
        _error(f"Unsupported architecture: {platform.machine()}")

    log.debug(f"Current platform: {os_name}, arch: {arch}")

    return os_name, arch


def _download_gomplate_binary(dest: Path) -> None:
    """Download gomplate binary based on the current platform"""

    os_name, arch = _resolve_platform()
    ext = ".exe" if os_name == "windows" else ""
    url = (
        f"https://github.com/hairyhenderson/gomplate/releases/download/"
        f"{GOMPLATE_VERSION}/gomplate_{os_name}-{arch}{ext}"
    )

    log.debug(f"Downloading Gomplate: {url}")

    try:
        urllib.request.urlretrieve(url, str(dest))
        if not _IS_WINDOWS:
            dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except (urllib.error.URLError, OSError) as exc:
        _error(f"Download failed ({url}): {exc}")


def find_gomplate(bin_dir: Path) -> str | None:
    """Look for gomplate binary if it exist on the current platform"""
    gomplate_path = shutil.which("gomplate")
    if gomplate_path:
        log.debug(f"Gomplate found : {gomplate_path}")
        return gomplate_path

    local = bin_dir / f"gomplate{_EXE_SUFFIX}"
    if local.is_file():
        log.debug(f"Gomplate found : {str(local)}")
    else:
        log.debug("Gomplate not found")

    return str(local) if local.is_file() else None


def install_gomplate(bin_dir: Path) -> str:
    """install gomplate binary"""

    bin_dir.mkdir(parents=True, exist_ok=True)
    dest = bin_dir / f"gomplate{_EXE_SUFFIX}"
    _download_gomplate_binary(dest)

    return str(dest)


def resolve_gomplate_tool(bin_dir: Path, isVerbose: bool) -> str:
    """Return a working gomplate command, if not exist download it and install it"""

    log.setLevel(logging.DEBUG if isVerbose else logging.WARNING)

    cmd = find_gomplate(bin_dir)
    if cmd:
        return cmd

    return install_gomplate(bin_dir)
