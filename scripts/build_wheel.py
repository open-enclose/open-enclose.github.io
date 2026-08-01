"""Rebuild the Pyodide wheel that the interactive page runs in the browser.

`content/05-explore.md` does not execute this repository's source. It downloads
`pyodide/enclose-0.1.0-py3-none-any.whl` and installs it into the browser's Python. So the
wheel is a *published artifact*, exactly like `Figures/`, and it goes stale the moment any
module under `enclose/` changes. It shipped a superseded `wedge_panel` once already — the
interactive page told readers "no combined threshold is derived" for a threshold that had
been derived, verified and written into the appendix two commits earlier.

Run this after changing anything in `enclose/`, or just run `pytest tests/test_wheel.py`,
which fails with the command to run.

    python scripts/build_wheel.py

CI runs this before the test suite, so what the site serves is always what the tests then
pass against.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "pyodide"

#: `content/05-explore.md` hardcodes this name, and GitHub Pages serves no directory index
#: for the page to discover it from. A version bump in pyproject.toml therefore silently
#: 404s the explore page unless that constant moves too, so assert the name here.
EXPECTED = "enclose-0.1.0-py3-none-any.whl"


def main():
    OUTDIR.mkdir(exist_ok=True)
    for stale in OUTDIR.glob("*.whl"):
        stale.unlink()

    subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(OUTDIR), str(ROOT)],
        check=True,
    )

    # `build` leaves the source tree's egg-info behind; it is not ours to publish.
    shutil.rmtree(ROOT / "enclose.egg-info", ignore_errors=True)

    built = sorted(p.name for p in OUTDIR.glob("*.whl"))
    if built != [EXPECTED]:
        raise SystemExit(
            f"Built {built}, expected ['{EXPECTED}'].\n"
            f"content/05-explore.md hardcodes WHEEL_NAME = \"{EXPECTED}\". If the package "
            f"version changed in pyproject.toml, update WHEEL_NAME and EXPECTED together, "
            f"or the explore page will 404 on the wheel."
        )
    print(f"wrote {OUTDIR / EXPECTED}")


if __name__ == "__main__":
    main()
