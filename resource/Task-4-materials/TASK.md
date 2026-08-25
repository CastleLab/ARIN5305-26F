# Feature Task: Dataset metadata and dictionary representation

Improve `xarray.Dataset` so that users can inspect variable type and shape metadata and serialize Dataset contents in a flexible, consistent way.

## Requirements

- Add read-only dtype and shape mappings:
  - `Dataset.dtypes` and `Dataset.shapes`: data-variable names to NumPy dtypes and shape tuples, excluding coordinates.
  - `Dataset.data_vars.dtypes` and `Dataset.data_vars.shapes`: the corresponding mappings for the data-variable view.
  - `Dataset.coords.dtypes` and `Dataset.coords.shapes`: coordinate names to NumPy dtypes and shape tuples.
- These mappings must reflect the Dataset's current state whenever accessed, including when variables are replaced, renamed, or change between data-variable and coordinate roles through operations such as `set_coords()` and `reset_coords()`.
- Extend `Dataset.to_dict()` with the following `data` modes while keeping the existing default behavior backward compatible:
  - `True` or `"list"`: serialize data as Python lists.
  - `"array"`: preserve underlying array objects for data variables and coordinates; lazy arrays must not be eagerly computed.
  - `"numpy"`: represent data variables and coordinates as NumPy `ndarray` objects, materializing lazy data when needed.
  - `False` or `"schema"`: return schema information without data values.
  - unsupported values must raise a clear `ValueError`.
- With `encoding=True`, Dataset-level, data-variable, and coordinate encodings must be included. Data-containing representations must remain usable with `Dataset.from_dict()`, restoring these encodings and preserving the array or laziness semantics of the chosen representation.
- Schema output must report `dtype` and `shape` consistently with the Dataset's current variables and metadata mappings.
- Preserve existing behavior outside these requirements.

## Working constraints

- Work only inside the working folder; do not inspect other local folders.
- Do not access the network or external services.
- Do not rely on memory or guess the implementation. Read the task, local source, and relevant tests before designing the changes.
- Validate carefully using existing tests and any additional tests you choose to write inside the working folder.
