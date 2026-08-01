"""The shipped Pyodide wheel must match the source it was built from.

`content/05-explore.md` runs `pyodide/enclose-0.1.0-py3-none-any.whl` in the browser, not
this repository's source. Nothing else in the suite exercises that artifact, so without
these tests a stale wheel is invisible: every test passes, the figures regenerate, the site
deploys green, and the interactive page quietly serves last week's model.

That is not hypothetical. The wheel once shipped a `wedge_panel` predating the joint
$(\mu,\tau)$ selection locus, so the page reported "no combined threshold is derived" at
parameter values where the threshold exists and is plotted correctly by the same function
in `enclose/figures.py`.

If these fail, run:

    python scripts/build_wheel.py
"""

import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WHEEL = ROOT / "pyodide" / "enclose-0.1.0-py3-none-any.whl"

REBUILD = "stale wheel -- run `python scripts/build_wheel.py`"


def _wheel_sources():
    with zipfile.ZipFile(WHEEL) as z:
        return {
            n: z.read(n) for n in z.namelist()
            if n.startswith("enclose/") and n.endswith(".py")
        }


def test_wheel_exists():
    """The explore page hardcodes this exact filename; a version bump breaks it silently."""
    assert WHEEL.is_file(), f"{WHEEL.name} is missing -- run scripts/build_wheel.py"


def test_wheel_ships_every_source_module():
    packaged = set(_wheel_sources())
    on_disk = {f"enclose/{p.name}" for p in (ROOT / "enclose").glob("*.py")}
    assert on_disk - packaged == set(), f"modules missing from the wheel: {REBUILD}"


@pytest.mark.parametrize("module", sorted(p.name for p in (ROOT / "enclose").glob("*.py")))
def test_wheel_module_matches_source(module):
    """Byte-compare rather than mtime-compare: git does not preserve modification times, so
    a fresh clone would give mtimes an arbitrary order and make an mtime check meaningless."""
    packaged = _wheel_sources()[f"enclose/{module}"]
    assert packaged == (ROOT / "enclose" / module).read_bytes(), (
        f"pyodide wheel's {module} differs from enclose/{module} -- {REBUILD}"
    )
