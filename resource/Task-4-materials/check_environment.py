#!/usr/bin/env python3
"""Check that the supplied xarray source tree is usable in the current environment.

This checks the environment only; it does not test the requested feature.
"""
from __future__ import annotations

import argparse
import importlib
import os
from pathlib import Path
import subprocess
import sys

REFERENCE_PYTHON = (3, 9)
RECOMMENDED_DASK = "2022.8.1"
REQUIRED_PACKAGES = ("numpy", "pandas", "pytest", "packaging", "dask")
SANITY_TESTS = [
    "xarray/tests/test_dataset.py::TestDataset::test_constructor_with_coords",
    "xarray/tests/test_dataarray.py::TestDataArray::test_get_index",
    "xarray/tests/test_dataset.py::TestDataset::test_to_and_from_dict",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    ns = parser.parse_args()
    repo = ns.repo.resolve()

    if not (repo / "xarray" / "__init__.py").is_file():
        print(f"ERROR: not an xarray source tree: {repo}")
        return 2

    print("== Python environment ==")
    print(f"Python: {sys.version.split()[0]}")
    if sys.version_info[:2] != REFERENCE_PYTHON:
        print("WARNING: the reference environment uses Python 3.9.")

    versions = {}
    for package in REQUIRED_PACKAGES:
        try:
            module = importlib.import_module(package)
            version = getattr(module, "__version__", "unknown")
            versions[package] = version
            print(f"{package}: {version}")
        except Exception as exc:
            print(f"ERROR: cannot import {package}: {exc}")
            return 2
    if versions.get("dask") != RECOMMENDED_DASK:
        print(f"NOTE: recommended Dask version is {RECOMMENDED_DASK}.")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo) + os.pathsep + env.get("PYTHONPATH", "")
    verify_import = (
        "import pathlib, xarray; "
        "p=pathlib.Path(xarray.__file__).resolve(); print('xarray:', p); "
        f"assert p.is_relative_to(pathlib.Path({str(repo)!r}).resolve())"
    )
    result = subprocess.run([sys.executable, "-c", verify_import], cwd=repo, env=env)
    if result.returncode != 0:
        print("ERROR: Python is not importing xarray from the supplied source tree.")
        return 2

    dask_smoke = (
        "import dask.array as da, xarray as xr; "
        "a=da.arange(6, chunks=3); ds=xr.Dataset({'a': ('x', a)}); "
        "assert ds['a'].chunks == ((3, 3),); print('Dask/xarray smoke: PASS')"
    )
    if subprocess.run([sys.executable, "-c", dask_smoke], cwd=repo, env=env).returncode:
        print("ERROR: Dask/xarray integration smoke check failed.")
        return 2

    print("\n== Repository sanity tests ==")
    cmd = [sys.executable, "-m", "pytest", "-q", *SANITY_TESTS]
    result = subprocess.run(cmd, cwd=repo, env=env)
    if result.returncode != 0:
        print("ERROR: repository sanity tests did not pass.")
        return result.returncode

    print("\nEnvironment check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
