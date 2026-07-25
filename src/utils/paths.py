"""Project-root and Depth-Anything-V2 path helpers."""

from __future__ import annotations

import os
import sys
from importlib.util import find_spec


def get_project_root() -> str:
    """Repository root (parent of ``src/``)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_dav2_root() -> str:
    """Path to the vendored Depth-Anything-V2 checkout."""
    return os.path.join(get_project_root(), "third_party", "Depth-Anything-V2")


def setup_dav2_import() -> str:
    """Make ``depth_anything_v2`` importable.

    Returns:
        Absolute path to the vendored Depth-Anything-V2 repository root when
        using the submodule, or an empty string when an installed package is used.

    Raises:
        FileNotFoundError: If neither the installed package nor the vendored
        submodule is available.
    """
    if find_spec("depth_anything_v2") is not None:
        return ""

    dav2_root = get_dav2_root()
    if not os.path.isdir(dav2_root):
        raise FileNotFoundError(
            "depth_anything_v2 is not installed and Depth-Anything-V2 was not found at "
            f"{dav2_root}\n"
            "Install with:\n"
            "  pip install -e .[depth-anything-V2]\n"
            "or run from the repo root:\n"
            "  git submodule update --init --recursive"
        )
    if dav2_root not in sys.path:
        sys.path.insert(0, dav2_root)
    return dav2_root


def resolve_from_root(path: str) -> str:
    """Expand ``~`` and resolve a path relative to the project root."""
    path = os.path.expanduser(path)
    if os.path.isabs(path):
        return path
    return os.path.join(get_project_root(), path)


def resolve_checkpoint(path: str) -> str:
    """Resolve a model checkpoint path.

    Search order (first existing file wins):
      1. Absolute / ``~`` path
      2. ``<project_root>/<path>``
      3. ``<dav2_root>/<path>``  (Depth-Anything-V2 convention: ``checkpoints/...``)
    """
    path = os.path.expanduser(path)
    if os.path.isabs(path):
        return path

    root = get_project_root()
    candidates = [
        os.path.join(root, path),
        os.path.join(get_dav2_root(), path),
    ]
    for cand in candidates:
        if os.path.isfile(cand):
            return cand
    # Return the DA-v2 location so error messages point to the right place.
    return os.path.join(get_dav2_root(), path)
