"""Regenerate all 8 paper figures in one command.

Writes to Figures_generated/ (not the live Figures/) so this is safe to re-run for
verification without touching what the site currently serves — see
REORGANIZATION_PROPOSAL.md Phase 1's definition of done.

Usage (from the repo root):
    python scripts/make_figures.py [--outdir DIR]
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from enclose import figures  # noqa: E402

# dpi matches each figure's source cell: matplotlib's default (100) for the six ported
# from cells 26/36/45/47, the source's own explicit dpi for the other two.
TARGETS = [
    ("social_optimum.png", figures.social_optimum, dict(cond_opt=False), 100),
    ("social_opt_cond.png", figures.social_optimum, dict(cond_opt=True), 100),
    ("nash_eq.png", figures.nash_equilibrium, dict(full_diag=False), 100),
    ("nash_so_comp.png", figures.nash_equilibrium, dict(full_diag=True), 100),
    ("monopoly.png", figures.monopoly, {}, 100),
    ("comparison.png", figures.comparison, {}, 100),
    ("new_comp_fig4x4.png", figures.combined_4x4, {}, 200),
    ("trajectories.png", figures.trajectories, {}, 120),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", default=str(REPO_ROOT / "Figures_generated"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for filename, fn, kwargs, dpi in TARGETS:
        result = fn(**kwargs)
        fig = result[0] if isinstance(result, tuple) else result
        outfile = outdir / filename
        fig.savefig(outfile, dpi=dpi, facecolor="white")
        print(f"[OK] {filename} -> {outfile}")

    print(f"\nAll {len(TARGETS)} figures written to {outdir}/")


if __name__ == "__main__":
    main()
