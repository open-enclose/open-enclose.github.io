r"""The computation path must stay free of matplotlib.

`enclose.loci` imported `safe_log_power` from `enclose.style` until 2026-07-29, and
`enclose.style` imports `matplotlib.patches` at module level. So evaluating a single locus
pulled in the entire plotting stack. Under Pyodide that is a large download the explore page
should not pay for just to move a slider, and nothing in the test suite would have caught the
regression — every other test file imports matplotlib for its own reasons, so by the time an
assertion ran, `sys.modules` was already contaminated.

Hence the subprocess: each check starts a clean interpreter, imports exactly one module, and
reports what landed in `sys.modules`. An in-process version of this test would pass
unconditionally and prove nothing.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# The subprocess must find `enclose` the same way `python -m pytest` from the repo root does:
# via the repo root on sys.path. Pinning cwd here rather than inheriting it means these tests
# do not quietly become no-ops when someone runs pytest from a subdirectory.
REPO_ROOT = Path(__file__).resolve().parent.parent

# `matplotlib` alone is the thing under test; the rest are here because a stray import of any
# of them would be the same kind of mistake, just cheaper.
HEAVY = ("matplotlib", "scipy", "sympy")


def _modules_after(import_statement):
    """Return the set of `HEAVY` names present in a fresh interpreter's sys.modules."""
    code = (
        f"{import_statement}\n"
        "import sys, json\n"
        f"print(json.dumps([m for m in {HEAVY!r} if m in sys.modules]))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    return set(json.loads(result.stdout.strip().splitlines()[-1]))


@pytest.mark.parametrize(
    "module",
    ["enclose", "enclose.numerics", "enclose.model", "enclose.loci"],
)
def test_computation_path_is_matplotlib_free(module):
    """The layers a browser session needs for numbers must not drag in a plotting stack."""
    assert _modules_after(f"import {module}") == set(), (
        f"`import {module}` pulled in a heavy dependency. Something on the computation path "
        f"now imports it transitively — most likely a helper moved back into `enclose.style` "
        f"or a new `from .style import ...` in `model.py`/`loci.py`. Put pure-numpy helpers "
        f"in `enclose.numerics` instead."
    )


def test_figures_does_import_matplotlib():
    """The converse, so the test above cannot pass by the modules being broken or empty."""
    assert "matplotlib" in _modules_after("import enclose.figures")


def test_manufacturing_imports_scipy():
    """`labor_share` uses `brentq`; recorded here because it decides what the browser needs.

    scipy ships in the Pyodide distribution, so this is a documented cost rather than a
    blocker — but if it ever stops being true, the explore page's manufacturing section is
    what breaks.
    """
    assert "scipy" in _modules_after("import enclose.manufacturing")
