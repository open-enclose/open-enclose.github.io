"""Tests for the three-sector manufacturing extension.

The load-bearing test is `test_solver_matches_closed_form_when_beta_equals_alpha`: the
equilibrium has no elementary closed form for beta != alpha, but it does at beta == alpha,
and that gives an independent oracle for the numerical solver. Everything else here guards
properties the solve relies on (single crossing) or the comparative statics the narrative
will claim.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from enclose import manufacturing as mf, model  # noqa: E402

# (te, alp, th, tbar, kb, p, mu) covering both governance regimes and a range of te
CASES = [
    (1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0),
    (0.3, 0.4, 1.6, 1.2, 0.8, 1.5, 0.0),
    (0.7, 0.6, 2.0, 1.0, 1.4, 0.7, 1.0),
    (0.0, 0.5, 1.2, 1.0, 1.0, 1.0, 0.5),
]


@pytest.mark.parametrize("te,alp,th,tbar,kb,p,mu", CASES)
def test_solver_matches_closed_form_when_beta_equals_alpha(te, alp, th, tbar, kb, p, mu):
    """The one case with an exact answer -- an independent check on the numerical root."""
    numeric = mf.labor_share(te, b=alp, alp=alp, th=th, tbar=tbar, kb=kb, p=p, mu=mu)
    exact = mf.labor_share_closed_form(te, alp=alp, th=th, tbar=tbar, kb=kb, p=p, mu=mu)
    assert numeric == pytest.approx(exact, rel=1e-10)


@pytest.mark.parametrize("b", [0.3, 0.5, 0.7])
@pytest.mark.parametrize("alp", [0.4, 0.5, 0.6])
def test_returned_root_actually_zeroes_the_residual(b, alp):
    """Whatever the solver returns must satisfy MPL_m = MPL_a."""
    lm = mf.labor_share(0.5, b=b, alp=alp, th=1.4)
    assert 0.0 < lm < 1.0
    assert mf.excess_mpl(lm, 0.5, b=b, alp=alp, th=1.4) == pytest.approx(0.0, abs=1e-9)


@pytest.mark.parametrize("b,alp", [(0.7, 0.4), (0.3, 0.6), (0.8, 0.5), (0.5, 0.5)])
def test_equilibrium_is_unique_single_crossing(b, alp):
    """The bracketed solve is only justified if the residual crosses zero exactly once.

    MPL_m falls in lm and MPL_a rises in it, so this should hold everywhere; verifying it
    rather than assuming it is what makes brentq's bracket safe.
    """
    grid = np.linspace(1e-6, 1 - 1e-6, 20001)
    resid = mf.excess_mpl(grid, 0.5, b=b, alp=alp, th=1.4)
    assert int(np.sum(np.diff(np.sign(resid)) != 0)) == 1


def test_manufacturing_mpl_falls_and_agricultural_mpl_rises():
    """The monotonicity that produces the single crossing."""
    lm = np.linspace(0.05, 0.95, 50)
    assert np.all(np.diff(mf.mpl_m(lm)) < 0)
    assert np.all(np.diff(mf.mpl_a(lm, te=0.5)) > 0)


def test_mu_is_threaded_through():
    """Guard against the failure mode that bit tepvt_g: a mu parameter accepted and then
    silently ignored. Higher mu raises Lambda_mu, raising agricultural MPL, which should
    pull labor out of manufacturing."""
    kw = dict(te=0.5, b=0.5, alp=0.5, th=1.6)
    lm_open = mf.labor_share(mu=0.0, **kw)
    lm_planner = mf.labor_share(mu=1.0, **kw)
    assert lm_open != pytest.approx(lm_planner)
    assert lm_planner < lm_open


def test_more_productive_manufacturing_draws_in_labor():
    """Comparative static in p: a better manufacturing price raises its labor share."""
    kw = dict(te=0.5, b=0.5, alp=0.5, th=1.4)
    shares = [mf.labor_share(p=p, **kw) for p in (0.5, 1.0, 2.0)]
    assert shares == sorted(shares)


def test_enclosure_effect_on_manufacturing_flips_sign_at_theta_H():
    """The te comparative static has no single direction -- it flips at theta_H.

    Agricultural MPL carries (1 + (Lambda_mu - 1) t_e), so the sign of dl_m/dt_e is the
    sign of (Lambda_mu - 1), and Lambda_mu = 1 exactly at theta_H (eq. 24). Below theta_H
    private enclosure *reduces* labor on enclosed land, agricultural MPL falls as te rises,
    and labor flows to manufacturing; above theta_H the reverse. At theta_H enclosure does
    not move labor at all.

    (An earlier version of this test asserted the "falling" branch unconditionally and
    failed at theta=1.8 -- which is below theta_H=2 for alpha=0.5. The code was right.)
    """
    alp, mu = 0.5, 0.0
    th_H = model.theta_H(alp, mu)
    te_grid = (0.0, 0.3, 0.6, 1.0)

    def shares(th):
        return [mf.labor_share(te=te, b=0.5, alp=alp, th=th, mu=mu) for te in te_grid]

    below = shares(th_H - 0.2)
    assert below == sorted(below), "below theta_H, l_m should rise with te"

    above = shares(th_H + 0.5)
    assert above == sorted(above, reverse=True), "above theta_H, l_m should fall with te"

    at = shares(th_H)
    assert model.Lambda(th_H, alp, mu) == pytest.approx(1.0)
    assert at == pytest.approx([at[0]] * len(te_grid)), \
        "at theta_H, Lambda=1 and enclosure should not shift labor at all"


def test_agricultural_labor_is_reaction_function_scaled_by_labor_left_in_agriculture():
    """Eq. (36): the usual l_e(t_e) times (1 - l_m)."""
    from enclose.model import Lambda, le
    te, th, alp, mu = 0.6, 1.5, 0.5, 0.0
    lm = mf.labor_share(te, alp=alp, th=th, mu=mu)
    expected = le(te, th, alp, mu) * (1 - lm)
    assert mf.agricultural_labor(te, th=th, alp=alp, mu=mu) == pytest.approx(expected)
    # and it must be strictly below the no-manufacturing allocation
    assert mf.agricultural_labor(te, th=th, alp=alp, mu=mu) < le(te, th, alp, mu)
