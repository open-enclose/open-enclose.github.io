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


@pytest.mark.parametrize("fn,kwargs", [
    (figures.manufacturing_equilibrium, dict(te_values=(0.0, 1.0), th=1.0, alp=0.4, b=0.7)),
    (figures.structural_transformation, dict(alp=0.5, mu=0.0, b=0.5)),
])
def test_manufacturing_figure_builds(fn, kwargs):
    fig, ax = fn(**kwargs)
    assert fig is not None and ax is not None
    plt.close(fig)


def test_manufacturing_figure_reproduces_the_drafts_headline_example():
    """enclosure_manuf.md's worked example: at theta=1, alpha=0.4, beta=0.7, enclosing all
    land raises manufacturing's labor share from "about 20 percent" to "almost 70 percent"
    while the wage falls -- the Weitzman/Samuelson effect.

    Pinning it guards the port against drifting away from the source material the
    manufacturing page is written around.
    """
    from enclose import manufacturing as mfg
    kw = dict(b=0.7, alp=0.4, th=1.0, tbar=1.0, kb=1.0, p=1.0, mu=0.0)

    lm_open = mfg.labor_share(te=0.0, **kw)
    lm_enclosed = mfg.labor_share(te=1.0, **kw)
    assert lm_open == pytest.approx(0.20, abs=0.01)
    assert lm_enclosed == pytest.approx(0.68, abs=0.01)

    w_open = mfg.mpl_m(lm_open, p=1.0, kb=1.0, b=0.7)
    w_enclosed = mfg.mpl_m(lm_enclosed, p=1.0, kb=1.0, b=0.7)
    assert w_enclosed < w_open, "the Weitzman/Samuelson wage fall"


def test_planner_allocation_is_unmoved_by_enclosure_when_theta_is_one():
    """The sharp version of the same point: at theta=1 the planner's Lambda_o = 1, so
    enclosure shifts no labor at all under mu=1 -- the decentralized shift is the commons
    distortion, not a productivity effect.

    Note where the planner sits, though: flat at ~0.68, which is where the decentralized
    economy *ends up* under full enclosure, not where it starts. So enclosure here moves
    the inter-sectoral allocation toward the optimum, and at te=1 reaches it exactly. (An
    earlier version of the model put the planner flat at ~0.20 and supported the opposite
    reading; that was the missing commons wedge -- see enclose/manufacturing.py.)
    """
    from enclose import manufacturing as mfg
    kw = dict(b=0.7, alp=0.4, th=1.0, tbar=1.0, kb=1.0, p=1.0, mu=1.0)
    assert model.Lambda(1.0, 0.4, 1.0) == pytest.approx(1.0)
    assert mfg.labor_share(te=0.0, **kw) == pytest.approx(mfg.labor_share(te=1.0, **kw))

    planner = mfg.labor_share(te=0.0, **kw)
    decentralized = dict(kw, mu=0.0)
    assert mfg.labor_share(te=0.0, **decentralized) < planner
    assert mfg.labor_share(te=1.0, **decentralized) == pytest.approx(planner)
