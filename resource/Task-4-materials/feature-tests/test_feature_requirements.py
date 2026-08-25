"""External feature tests for the Dataset metadata/dictionary task.

Keep this file outside the agent workspace.
Every assertion in this file traces to an explicit requirement in TASK.md.
"""
from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from xarray import Dataset


def _sample_dataset() -> Dataset:
    return Dataset(
        {
            "temperature": ("x", np.array([1.5, 2.5, 3.5], dtype=np.float32)),
            "count": ("x", np.array([1, 2, 3], dtype=np.int16)),
        },
        coords={
            "x": np.array([10, 20, 30], dtype=np.int64),
            "station": np.array("A", dtype="U1"),
        },
        attrs={"title": "sample"},
    )


def _assert_metadata_views(ds: Dataset, data_names, coord_names) -> None:
    for mapping in (
        ds.dtypes,
        ds.shapes,
        ds.data_vars.dtypes,
        ds.data_vars.shapes,
        ds.coords.dtypes,
        ds.coords.shapes,
    ):
        assert isinstance(mapping, Mapping)
    assert set(ds.dtypes) == set(data_names)
    assert set(ds.shapes) == set(data_names)
    assert set(ds.data_vars.dtypes) == set(data_names)
    assert set(ds.data_vars.shapes) == set(data_names)
    assert set(ds.coords.dtypes) == set(coord_names)
    assert set(ds.coords.shapes) == set(coord_names)


def test_dataset_metadata_views() -> None:
    ds = _sample_dataset()
    _assert_metadata_views(ds, {"temperature", "count"}, {"x", "station"})
    assert ds.dtypes == {
        "temperature": np.dtype("float32"),
        "count": np.dtype("int16"),
    }
    assert ds.shapes == {"temperature": (3,), "count": (3,)}
    assert ds.data_vars.dtypes == ds.dtypes
    assert ds.data_vars.shapes == ds.shapes
    assert ds.coords.dtypes == {
        "x": np.dtype("int64"),
        "station": np.dtype("U1"),
    }
    assert ds.coords.shapes == {"x": (3,), "station": ()}
    assert isinstance(ds.dtypes["temperature"], np.dtype)
    assert isinstance(ds.data_vars.dtypes["count"], np.dtype)
    assert isinstance(ds.coords.dtypes["x"], np.dtype)


def test_empty_dataset_metadata_views_are_frozen_and_empty() -> None:
    ds = Dataset()
    _assert_metadata_views(ds, set(), set())
    assert dict(ds.dtypes) == {}
    assert dict(ds.shapes) == {}
    assert dict(ds.data_vars.dtypes) == {}
    assert dict(ds.data_vars.shapes) == {}
    assert dict(ds.coords.dtypes) == {}
    assert dict(ds.coords.shapes) == {}


def test_all_metadata_views_are_read_only_and_live_after_replacement() -> None:
    ds = _sample_dataset()
    for mapping, key, value in (
        (ds.dtypes, "count", np.dtype("int8")),
        (ds.shapes, "count", (99,)),
        (ds.data_vars.dtypes, "count", np.dtype("int8")),
        (ds.data_vars.shapes, "count", (99,)),
        (ds.coords.dtypes, "x", np.dtype("int8")),
        (ds.coords.shapes, "x", (99,)),
    ):
        with pytest.raises(TypeError):
            mapping[key] = value

    ds["count"] = (("x", "y"), np.ones((3, 2), dtype=np.float64))
    ds.coords["station"] = ("x", np.array([1, 2, 3], dtype=np.int32))
    assert ds.dtypes["count"] == np.dtype("float64")
    assert ds.shapes["count"] == (3, 2)
    assert ds.data_vars.dtypes["count"] == np.dtype("float64")
    assert ds.data_vars.shapes["count"] == (3, 2)
    assert ds.coords.dtypes["station"] == np.dtype("int32")
    assert ds.coords.shapes["station"] == (3,)


def test_metadata_views_follow_variable_roles() -> None:
    ds = Dataset(
        {
            "a": ("x", np.array([1, 2], dtype=np.int16)),
            "b": ("x", np.array([1.0, 2.0], dtype=np.float32)),
        },
        coords={"x": np.array([0, 1], dtype=np.int64)},
    )
    as_coord = ds.set_coords("b")
    assert "b" not in as_coord.dtypes
    assert "b" not in as_coord.shapes
    assert "b" not in as_coord.data_vars.dtypes
    assert "b" not in as_coord.data_vars.shapes
    assert as_coord.coords.dtypes["b"] == np.dtype("float32")
    assert as_coord.coords.shapes["b"] == (2,)

    restored = as_coord.reset_coords("b")
    assert restored.dtypes["b"] == np.dtype("float32")
    assert restored.shapes["b"] == (2,)
    assert restored.data_vars.dtypes["b"] == np.dtype("float32")
    assert restored.data_vars.shapes["b"] == (2,)
    assert "b" not in restored.coords.dtypes
    assert "b" not in restored.coords.shapes


def test_metadata_views_follow_renamed_variables() -> None:
    ds = _sample_dataset()
    renamed = ds.rename({"temperature": "temp", "station": "site"})
    assert "temperature" not in renamed.dtypes
    assert "temperature" not in renamed.shapes
    assert renamed.dtypes["temp"] == np.dtype("float32")
    assert renamed.shapes["temp"] == (3,)
    assert renamed.data_vars.dtypes["temp"] == np.dtype("float32")
    assert renamed.data_vars.shapes["temp"] == (3,)
    assert "station" not in renamed.coords.dtypes
    assert "station" not in renamed.coords.shapes
    assert renamed.coords.dtypes["site"] == np.dtype("U1")
    assert renamed.coords.shapes["site"] == ()


def test_dataset_to_dict_list_and_schema_modes() -> None:
    ds = _sample_dataset()
    listed = ds.to_dict(data="list")
    assert listed["data_vars"]["temperature"]["data"] == [1.5, 2.5, 3.5]
    assert listed["coords"]["x"]["data"] == [10, 20, 30]
    assert ds.to_dict(data=True) == listed

    schema = ds.to_dict(data="schema")
    assert schema == ds.to_dict(data=False)
    assert "data" not in schema["data_vars"]["temperature"]
    assert "data" not in schema["coords"]["x"]


def test_empty_dataset_schema_alias_and_metadata_are_consistent() -> None:
    ds = Dataset(attrs={"kind": "empty"})
    assert dict(ds.dtypes) == {}
    assert dict(ds.shapes) == {}
    assert ds.to_dict(data="schema") == ds.to_dict(data=False)


def test_schema_matches_dtype_and_shape_views_for_scalar_and_multidimensional_variables() -> None:
    ds = Dataset(
        {
            "matrix": (("x", "y"), np.arange(6, dtype=np.int32).reshape(2, 3)),
            "scalar": np.array(2.5, dtype=np.float64),
        },
        coords={
            "x": np.array([0, 1], dtype=np.int16),
            "aux": ("y", np.array([1.0, 2.0, 3.0], dtype=np.float32)),
        },
    )
    schema = ds.to_dict(data="schema")
    for name, dtype in ds.dtypes.items():
        spec = schema["data_vars"][name]
        assert np.dtype(spec["dtype"]) == dtype
        assert tuple(spec["shape"]) == ds.shapes[name]
    for name, dtype in ds.coords.dtypes.items():
        spec = schema["coords"][name]
        assert np.dtype(spec["dtype"]) == dtype
        assert tuple(spec["shape"]) == ds.coords.shapes[name]


def test_pandas_datetime_coordinate_metadata_and_schema_are_consistent() -> None:
    times = pd.date_range("2001-01-01", periods=3)
    ds = Dataset({"a": ("time", [1, 2, 3])}, coords={"time": times})
    assert np.issubdtype(ds.coords.dtypes["time"], np.datetime64)
    assert ds.coords.dtypes["time"] == ds["time"].dtype
    assert ds.coords.shapes["time"] == (3,)
    schema = ds.to_dict(data="schema")
    assert np.dtype(schema["coords"]["time"]["dtype"]) == ds.coords.dtypes["time"]
    assert tuple(schema["coords"]["time"]["shape"]) == ds.coords.shapes["time"]


def test_dataset_to_dict_array_mode_preserves_underlying_numpy_arrays() -> None:
    ds = Dataset(
        {"a": ("x", np.array([1.0, 2.0, 3.0], dtype=np.float32))},
        coords={
            "x": np.array([0, 1, 2], dtype=np.int64),
            "aux": ("x", np.array([10, 20, 30], dtype=np.int16)),
        },
    )
    payload = ds.to_dict(data="array")
    assert isinstance(payload["data_vars"]["a"]["data"], np.ndarray)
    assert isinstance(payload["coords"]["aux"]["data"], np.ndarray)
    np.testing.assert_array_equal(payload["data_vars"]["a"]["data"], ds["a"].data)
    np.testing.assert_array_equal(payload["coords"]["aux"]["data"], ds["aux"].data)
    assert payload["data_vars"]["a"]["data"] is ds["a"].data
    assert payload["coords"]["aux"]["data"] is ds["aux"].data


def test_dataset_to_dict_array_mode_does_not_compute_dask_data() -> None:
    import dask.array as da
    from dask.callbacks import Callback

    class FailOnCompute(Callback):
        def _start(self, dsk):
            raise AssertionError("data='array' triggered Dask computation")

    lazy = da.arange(12, chunks=4).reshape((3, 4))
    ds = Dataset({"a": (("x", "y"), lazy)}, coords={"x": [0, 1, 2]})
    with FailOnCompute():
        payload = ds.to_dict(data="array")
    assert isinstance(payload["data_vars"]["a"]["data"], da.Array)


def test_dataset_to_dict_array_mode_does_not_compute_lazy_coordinates() -> None:
    import dask.array as da
    from dask.callbacks import Callback

    class FailOnCompute(Callback):
        def _start(self, dsk):
            raise AssertionError("data='array' triggered Dask coordinate computation")

    lazy_coord = da.arange(6, chunks=3)
    ds = Dataset(
        {"a": ("x", np.arange(6, dtype=np.int16))},
        coords={"aux": ("x", lazy_coord)},
    )
    with FailOnCompute():
        payload = ds.to_dict(data="array")
    assert isinstance(payload["coords"]["aux"]["data"], da.Array)


def test_dataset_to_dict_numpy_mode_returns_numpy_arrays() -> None:
    ds = Dataset(
        {"a": ("x", np.array([1.0, 2.0, 3.0], dtype=np.float32)), "s": np.array(5)},
        coords={"aux": ("x", np.array([10, 20, 30], dtype=np.int16))},
    )
    payload = ds.to_dict(data="numpy")
    assert isinstance(payload["data_vars"]["a"]["data"], np.ndarray)
    assert isinstance(payload["data_vars"]["s"]["data"], np.ndarray)
    assert payload["data_vars"]["s"]["data"].shape == ()
    assert isinstance(payload["coords"]["aux"]["data"], np.ndarray)
    np.testing.assert_array_equal(payload["data_vars"]["a"]["data"], ds["a"].to_numpy())
    np.testing.assert_array_equal(payload["coords"]["aux"]["data"], ds["aux"].to_numpy())


def test_dataset_to_dict_numpy_mode_materializes_dask_arrays() -> None:
    import dask.array as da
    from dask.callbacks import Callback

    class RecordCompute(Callback):
        def __init__(self):
            super().__init__()
            self.started = 0

        def _start(self, dsk):
            self.started += 1

    ds = Dataset(
        {"a": ("x", da.arange(6, chunks=3))},
        coords={"aux": ("x", da.ones(6, chunks=3))},
    )
    original_data = ds["a"].data
    original_coord = ds["aux"].data
    callback = RecordCompute()
    with callback:
        payload = ds.to_dict(data="numpy")
    assert callback.started >= 1
    assert ds["a"].data is original_data
    assert ds["aux"].data is original_coord
    assert isinstance(ds["a"].data, da.Array)
    assert isinstance(ds["aux"].data, da.Array)
    assert isinstance(payload["data_vars"]["a"]["data"], np.ndarray)
    assert isinstance(payload["coords"]["aux"]["data"], np.ndarray)
    np.testing.assert_array_equal(payload["data_vars"]["a"]["data"], np.arange(6))


def test_numpy_mode_handles_pandas_datetime_coordinate_as_ndarray() -> None:
    times = pd.date_range("2001-01-01", periods=3)
    ds = Dataset({"a": ("time", [1, 2, 3])}, coords={"time": times})
    payload = ds.to_dict(data="numpy")
    coord_data = payload["coords"]["time"]["data"]
    assert isinstance(coord_data, np.ndarray)
    assert np.issubdtype(coord_data.dtype, np.datetime64)
    assert coord_data.shape == (3,)
    np.testing.assert_array_equal(coord_data, times.to_numpy())


@pytest.mark.parametrize("mode", [True, "list", "array", "numpy"])
def test_dataset_encoding_roundtrip_for_data_representations(mode) -> None:
    ds = _sample_dataset()
    ds.encoding = {"source": "memory"}
    ds["temperature"].encoding = {"scale_factor": 0.5}
    ds["x"].encoding = {"coord_key": "coord_value"}

    payload = ds.to_dict(data=mode, encoding=True)
    assert payload["encoding"] == ds.encoding
    assert payload["data_vars"]["temperature"]["encoding"] == ds["temperature"].encoding
    assert payload["coords"]["x"]["encoding"] == ds["x"].encoding

    rebuilt = Dataset.from_dict(payload)
    xr.testing.assert_identical(ds, rebuilt)
    assert rebuilt.encoding == ds.encoding
    assert rebuilt["temperature"].encoding == ds["temperature"].encoding
    assert rebuilt["x"].encoding == ds["x"].encoding


def test_schema_output_includes_requested_encodings_and_matches_metadata_views() -> None:
    ds = _sample_dataset()
    ds.encoding = {"source": "memory"}
    ds["temperature"].encoding = {"var_key": "var_value"}
    ds["x"].encoding = {"coord_key": "coord_value"}

    payload = ds.to_dict(data="schema", encoding=True)
    assert payload["encoding"] == ds.encoding
    assert payload["data_vars"]["temperature"]["encoding"] == ds["temperature"].encoding
    assert payload["coords"]["x"]["encoding"] == ds["x"].encoding
    assert "data" not in payload["data_vars"]["temperature"]
    assert np.dtype(payload["data_vars"]["temperature"]["dtype"]) == ds.dtypes["temperature"]
    assert tuple(payload["data_vars"]["temperature"]["shape"]) == ds.shapes["temperature"]


def test_array_roundtrip_preserves_lazy_arrays_and_encodings_without_compute() -> None:
    import dask.array as da
    from dask.callbacks import Callback

    class FailOnCompute(Callback):
        def _start(self, dsk):
            raise AssertionError("array-mode roundtrip triggered Dask computation")

    ds = Dataset(
        {"a": ("x", da.arange(6, chunks=3))},
        coords={"aux": ("x", da.ones(6, chunks=3))},
    )
    ds.encoding = {"source": "lazy"}
    ds["a"].encoding = {"var_key": "a_value"}
    ds["aux"].encoding = {"coord_key": "aux_value"}

    with FailOnCompute():
        payload = ds.to_dict(data="array", encoding=True)
        rebuilt = Dataset.from_dict(payload)

    assert isinstance(rebuilt["a"].data, da.Array)
    assert isinstance(rebuilt["aux"].data, da.Array)
    assert rebuilt.encoding == ds.encoding
    assert rebuilt["a"].encoding == ds["a"].encoding
    assert rebuilt["aux"].encoding == ds["aux"].encoding


def test_numpy_roundtrip_materializes_lazy_arrays_and_restores_encodings() -> None:
    import dask.array as da

    ds = Dataset(
        {"a": ("x", da.arange(6, chunks=3))},
        coords={"aux": ("x", da.ones(6, chunks=3))},
    )
    ds.encoding = {"source": "lazy"}
    ds["a"].encoding = {"var_key": "a_value"}
    ds["aux"].encoding = {"coord_key": "aux_value"}

    payload = ds.to_dict(data="numpy", encoding=True)
    assert isinstance(payload["data_vars"]["a"]["data"], np.ndarray)
    assert isinstance(payload["coords"]["aux"]["data"], np.ndarray)
    rebuilt = Dataset.from_dict(payload)
    assert rebuilt.encoding == ds.encoding
    assert rebuilt["a"].encoding == ds["a"].encoding
    assert rebuilt["aux"].encoding == ds["aux"].encoding
    np.testing.assert_array_equal(rebuilt["a"].data, np.arange(6))


def test_invalid_data_mode_raises_value_error_even_for_empty_dataset() -> None:
    with pytest.raises(ValueError, match="data"):
        Dataset().to_dict(data="invalid")


@pytest.mark.parametrize("bad_mode", [None, "ARRAY", "unsupported", 1])
def test_other_unsupported_data_modes_raise_value_error(bad_mode) -> None:
    with pytest.raises(ValueError, match="data"):
        _sample_dataset().to_dict(data=bad_mode)
