"""Smoke and structural tests for the figure layer.

Figures are hard to assert on exhaustively; these check the properties that would actually
break silently -- that every figure builds, and that the two explanatory appendix figures
put their curves and marked points where the economics says they belong.
"""
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from enclose import figures, model  # noqa: E402

PAPER_FIGURES = [
    ("social_optimum", dict(cond_opt=False)),
    ("social_optimum", dict(cond_opt=True)),
    ("nash_equilibrium", dict(full_diag=False)),
    ("nash_equilibrium", dict(full_diag=True)),
    ("monopoly", {}),
    ("comparison", {}),
    ("combined_4x4", {}),
    ("trajectories", {}),
]


@pytest.mark.parametrize("name,kwargs", PAPER_FIGURES)
def test_paper_figure_builds(name, kwargs):
    result = getattr(figures, name)(**kwargs)
    fig = result[0] if isinstance(result, tuple) else result
    assert fig is not None
    plt.close(fig)


@pytest.mark.parametrize("fn,kwargs", [
    (figures.labor_reaction, dict(te=0.5, th=1.6, alp=0.5, mu=0.5)),
    (figures.labor_misallocation, dict(te=0.5, alp=0.5, th=1.5, mu=0.0)),
])
def test_appendix_figure_builds(fn, kwargs):
    fig, ax = fn(**kwargs)
    assert fig is not None and ax is not None
    plt.close(fig)


def test_labor_reaction_orders_the_three_regimes():
    """Appendix Fig. 5's economic content: at theta above theta_H the planner puts more
    labor on enclosed land than open access does, with regulated commons in between.

    This is the misallocation wedge the figure exists to show -- if the three curves ever
    came out in the wrong order the figure would be silently misleading.
    """
    te, th, alp, mu = 0.5, 1.6, 0.5, 0.5
    open_access = model.le(te, th, alp, mu=0)
    regulated = model.le(te, th, alp, mu)
    planner = model.le(te, th, alp, mu=1)
    assert open_access < regulated < planner


def test_labor_reaction_curves_start_and_end_pinned():
    """l_e(0)=0 and l_e(1)=1 for every mu -- enclosing no land uses no labor, enclosing all
    land uses all of it. The curves may bow either way between those pins."""
    for mu in (0.0, 0.5, 1.0):
        assert model.le(0.0, 1.6, 0.5, mu) == pytest.approx(0.0)
        assert model.le(1.0, 1.6, 0.5, mu) == pytest.approx(1.0)


def test_labor_reaction_bows_above_45_line_only_when_lambda_exceeds_one():
    """Which side of the 45-degree line the curve sits on is the sign of (Lambda_mu - 1) --
    the same quantity that flips at theta_H."""
    te, alp = 0.5, 0.5
    th_hi = model.theta_H(alp, mu=0) + 0.5      # Lambda > 1
    th_lo = model.theta_H(alp, mu=0) - 0.5      # Lambda < 1
    assert model.Lambda(th_hi, alp, 0) > 1 and model.le(te, th_hi, alp, 0) > te
    assert model.Lambda(th_lo, alp, 0) < 1 and model.le(te, th_lo, alp, 0) < te


def test_labor_misallocation_wedge_is_nonempty_and_correctly_ordered():
    """Appendix Fig. 4: the hatched wedge runs from the decentralized allocation up to the
    efficient one, so l_e* < l_e^o must hold or there is nothing to hatch."""
    te, th, alp = 0.5, 1.5, 0.5
    decentralized = model.le(te, th, alp, mu=0)
    efficient = model.leo(te, th, alp)
    assert decentralized < efficient
