# typings/

Hand-written stubs for third-party packages that ship no types.

`[tool.pyright] typeCheckingMode = "strict"` refuses to infer across an untyped
dependency. The temptation is to drop to `basic`, or scatter `# type: ignore`.
Both trade away type checking on *your* code to work around a gap in someone
else's. A stub is a few lines and confines the gap to one file.

## Adding one

1. `mkdir typings/<package>` and write `__init__.pyi`.
2. Declare only what you actually call — this is not a complete binding.
3. Untypeable arguments get `Any` explicitly, so the next reader can see the
   edge of what was checked.

```python
# typings/somepkg/__init__.pyi
from typing import Any


class Client:
    def __init__(self, api_key: str) -> None: ...
    def query(self, text: str, top_k: int = ...) -> list[dict[str, Any]]: ...
```

Pyright finds `typings/` automatically — it is the default `stubPath`.

## Also update

A dependency you import only through a stub is still a real dependency. One
imported *only* by another library (a parquet engine, a dotenv parser) is
invisible to import graphs and needs an exemption in two places, which must
agree:

- `pyproject.toml` → `[tool.deptry.per_rule_ignores] DEP002`
- `tach.toml` → `[external] exclude`

Comment *why* in both. An unexplained exemption is indistinguishable from a
stale one, and the next person deletes it.
