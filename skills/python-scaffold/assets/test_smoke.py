"""Placeholder so a fresh scaffold has something to run.

Delete this the moment there is real behaviour to test. It asserts nothing
worth protecting — it exists because `pytest` exits 5 on an empty suite, and a
scaffold that fails its own pre-commit gate on the first run teaches you to
ignore the gate.
"""

import {{PKG}}


def test_package_imports() -> None:
    assert {{PKG}}.__name__ == "{{PKG}}"
