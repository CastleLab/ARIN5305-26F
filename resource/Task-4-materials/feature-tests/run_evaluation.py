#!/usr/bin/env python3
"""Run external feature and targeted regression evaluation."""
from __future__ import annotations

import argparse
import importlib
import os
from pathlib import Path
import subprocess
import sys

REGRESSION_TESTS = [
    "xarray/tests/test_dataset.py::TestDataset::test_properties",
    "xarray/tests/test_dataset.py::TestDataset::test_coords_properties",
    "xarray/tests/test_dataset.py::TestDataset::test_data_vars_properties",
    "xarray/tests/test_dataset.py::TestDataset::test_coords_set",
    "xarray/tests/test_dataset.py::TestDataset::test_coords_to_dataset",
    "xarray/tests/test_dataset.py::TestDataset::test_coords_merge",
    "xarray/tests/test_dataset.py::TestDataset::test_coords_merge_mismatched_shape",
    "xarray/tests/test_dataset.py::TestDataset::test_equals_and_identical",
    "xarray/tests/test_dataset.py::TestDataset::test_to_and_from_dict",
    "xarray/tests/test_dataset.py::TestDataset::test_to_and_from_dict_with_time_dim",
    "xarray/tests/test_dataset.py::TestDataset::test_to_and_from_dict_with_nan_nat",
    "xarray/tests/test_dataset.py::TestDataset::test_to_dict_with_numpy_attrs",
    "xarray/tests/test_dataset.py::TestDataset::test_chunk",
    "xarray/tests/test_dataarray.py::TestDataArray::test_properties",
    "xarray/tests/test_dataarray.py::TestDataArray::test_coords",
    "xarray/tests/test_dataarray.py::TestDataArray::test_to_and_from_dict",
    "xarray/tests/test_dataarray.py::TestDataArray::test_to_and_from_dict_with_time_dim",
    "xarray/tests/test_dataarray.py::TestDataArray::test_to_and_from_dict_with_nan_nat",
    "xarray/tests/test_dataarray.py::TestDataArray::test_to_dict_with_numpy_attrs",
]


def run_pytest(repo: Path, args: list[str], label: str) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo) + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [sys.executable, "-m", "pytest", "-q", *args]
    print(f"\n== {label} ==")
    return subprocess.run(cmd, cwd=repo, env=env).returncode


def verify_local_import(repo: Path) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo) + os.pathsep + env.get("PYTHONPATH", "")
    code = (
        "import pathlib, xarray; "
        "p=pathlib.Path(xarray.__file__).resolve(); print('xarray:', p); "
        f"assert p.is_relative_to(pathlib.Path({str(repo)!r}).resolve())"
    )
    return subprocess.run([sys.executable, "-c", code], cwd=repo, env=env).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    ns = parser.parse_args()
    repo = ns.repo.resolve()

    if not (repo / "xarray" / "__init__.py").is_file():
        print(f"ERROR: not an xarray source tree: {repo}")
        return 2
    try:
        importlib.import_module("dask.array")
    except Exception as exc:
        print(f"ERROR: Dask is required for evaluation: {exc}")
        return 2
    if verify_local_import(repo) != 0:
        print("ERROR: evaluator is not importing xarray from the supplied repository.")
        return 2

    feature_tests = Path(__file__).with_name("test_feature_requirements.py").resolve()
    feature_rc = run_pytest(repo, [str(feature_tests)], "Feature evaluation")
    regression_rc = run_pytest(repo, REGRESSION_TESTS, "Targeted regression evaluation")

    print("\n== Summary ==")
    print("Feature evaluation:", "PASS" if feature_rc == 0 else "FAIL")
    print("Regression evaluation:", "PASS" if regression_rc == 0 else "FAIL")
    return 0 if feature_rc == 0 and regression_rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
