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
    silently ignored.

    mu enters twice and in *opposing* directions: it raises Lambda_mu (which raises the
    agricultural curve and pulls labor out of manufacturing) and it lowers the commons
    wedge A_mu (which lowers the curve and pushes labor in). An earlier version of this
    test asserted lm_planner < lm_open, which is what you get if you keep only the first
    channel -- and the module did exactly that. Assert only that mu moves the answer;
    the direction is pinned by the te=0 and te=1 tests below, where one channel or the
    other drops out cleanly.
    """
    kw = dict(te=0.5, b=0.5, alp=0.5, th=1.6)
    shares = [mf.labor_share(mu=m, **kw) for m in (0.0, 0.5, 1.0)]
    assert len(set(shares)) == 3


def test_planner_first_order_conditions_hold_at_the_solution():
    """The load-bearing check on mu=1: the returned allocation must satisfy the planner's
    FOCs written straight from the objective

        max  th*F(te, le) + F(1-te, 1-lm-le) + p*G(kb, lm) - c*te

    i.e. th*F_L(te,le) = F_L(1-te,lu) = p*G_L(kb,lm), using only the primitive derivatives
    -- no Lambda, no C_a, nothing from the module under test. This is what fails by a
    factor of 1/alpha when the commons wedge is dropped.
    """
    for te, th, alp, b, p in [(0.0, 1.0, 0.4, 0.7, 1.0), (0.5, 1.0, 0.4, 0.7, 1.0),
                              (1.0, 1.0, 0.4, 0.7, 1.0), (0.3, 1.6, 0.5, 0.5, 1.0),
                              (0.7, 2.0, 0.6, 0.3, 1.2), (0.9, 1.2, 0.35, 0.8, 0.8)]:
        lm = mf.labor_share(te, b=b, alp=alp, th=th, p=p, mu=1.0)
        le = mf.agricultural_labor(te, th=th, alp=alp, mu=1.0, b=b, p=p)
        lu = (1 - lm) - le

        mpl_m = p * b * 1.0**(1 - b) * lm**-(1 - b)
        mpl_e = alp * th * (te / le)**(1 - alp) if te > 0 else None
        mpl_u = alp * ((1 - te) / lu)**(1 - alp) if te < 1 else None

        for other in (mpl_e, mpl_u):
            if other is not None:
                assert other == pytest.approx(mpl_m, rel=1e-9), \
                    f"planner FOC violated at te={te}, th={th}"


def test_planner_allocation_maximizes_the_actual_objective():
    """Second, cruder check on the same thing: perturbing l_m away from the returned value
    (re-optimizing l_e each time) must lower the planner's objective."""
    from scipy.optimize import brentq

    def value(lm, te, th, alp, b, p):
        """Objective at lm, with le chosen to equate agricultural marginal products."""
        if te <= 0:
            le = 0.0
        elif te >= 1:
            le = 1 - lm
        else:
            le = brentq(lambda x: (th * alp * (te / x)**(1 - alp)
                                   - alp * ((1 - te) / ((1 - lm) - x))**(1 - alp)),
                        1e-14, (1 - lm) - 1e-14)
        lu = (1 - lm) - le
        return ((th * te**(1 - alp) * le**alp if te > 0 else 0.0)
                + ((1 - te)**(1 - alp) * lu**alp if te < 1 else 0.0)
                + p * lm**b)

    for te, th, alp, b, p in [(0.5, 1.0, 0.4, 0.7, 1.0), (0.3, 1.6, 0.5, 0.5, 1.0),
                              (0.7, 2.0, 0.6, 0.3, 1.2)]:
        lm = mf.labor_share(te, b=b, alp=alp, th=th, p=p, mu=1.0)
        best = value(lm, te, th, alp, b, p)
        for d in (-0.05, -0.01, 0.01, 0.05):
            assert value(lm + d, te, th, alp, b, p) < best


def test_open_access_and_planner_differ_by_alpha_when_no_land_is_enclosed():
    """At te=0 the whole economy is the commons and Lambda_mu drops out, so the only
    difference between the two curves is the wedge: open access pays the average product,
    a planner the marginal product, a ratio of exactly alpha.

    They previously coincided, which is what flagged the bug -- overlapping curves in the
    left panel of the manufacturing_equilibrium figure.
    """
    lm = np.array([0.2, 0.5, 0.8])
    for alp in (0.4, 0.5, 0.6):
        open_access = mf.mpl_a(lm, te=0.0, alp=alp, mu=0.0)
        planner = mf.mpl_a(lm, te=0.0, alp=alp, mu=1.0)
        assert planner / open_access == pytest.approx(np.full(3, alp))


@pytest.mark.parametrize("th", [0.8, 1.0, 1.5, 2.5])
@pytest.mark.parametrize("alp,b", [(0.4, 0.7), (0.5, 0.5)])
def test_full_enclosure_leaves_no_commons_so_mu_cannot_matter(th, alp, b):
    """At te=1 every worker is paid a marginal product regardless of how the commons was
    governed, so C_a = alpha*theta*tbar^(1-alpha) and l_m is independent of mu.

    Equivalently: full enclosure implements the planner's inter-sectoral allocation for
    any theta. The pre-fix code made l_m at te=1 depend on mu, which is the same defect
    seen from the other end.
    """
    shares = [mf.labor_share(1.0, b=b, alp=alp, th=th, mu=m) for m in (0.0, 0.5, 1.0)]
    assert shares == pytest.approx([shares[0]] * 3)
    for mu in (0.0, 0.5, 1.0):
        assert mf._c_a(1.0, 1.0, alp, th, mu) == pytest.approx(alp * th)


def test_more_productive_manufacturing_draws_in_labor():
    """Comparative static in p: a better manufacturing price raises its labor share."""
    kw = dict(te=0.5, b=0.5, alp=0.5, th=1.4)
    shares = [mf.labor_share(p=p, **kw) for p in (0.5, 1.0, 2.0)]
    assert shares == sorted(shares)


@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
def test_enclosure_effect_on_manufacturing_flips_sign_at_theta_H(mu):
    """The te comparative static has no single direction -- it flips at theta_H.

    The agricultural constant carries (1 + (Lambda_mu - 1) t_e), so dC_a/dt_e has the sign
    of (Lambda_mu - 1) -- and dl_m/dt_e has the OPPOSITE sign, because the equilibrium
    condition l_m^(1-b)/(1-l_m)^(1-a) = C_m/C_a rises in l_m, so l_m rises when C_a falls.
    Lambda_mu = 1 exactly at theta_H (eq. 24). Below theta_H
    private enclosure *reduces* labor on enclosed land, agricultural MPL falls as te rises,
    and labor flows to manufacturing; above theta_H the reverse. At theta_H enclosure does
    not move labor at all.

    (An earlier version of this test asserted the "falling" branch unconditionally and
    failed at theta=1.8 -- which is below theta_H=2 for alpha=0.5. The code was right.)

    Run across mu because the commons wedge A_mu shifts the *level* of the agricultural
    curve: the point of this result is that it does not touch the *slope*, since A_mu
    carries no te and no lm.
    """
    alp = 0.5
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


@pytest.mark.parametrize("th", [0.8, 1.0, 1.3, 2.0])
@pytest.mark.parametrize("te", [0.2, 0.5, 0.8])
def test_planner_marginal_benefit_matches_a_numerical_derivative(th, te):
    """The envelope claim: dY/dt_e at the planner's allocation is just the land-rent
    differential, because the labor terms drop out. Checked against a central difference
    of the actual value function."""
    kw = dict(b=0.7, alp=0.4, th=th, p=1.0)
    h = 1e-6
    numeric = (mf.total_output(te + h, mu=1.0, **kw)
               - mf.total_output(te - h, mu=1.0, **kw)) / (2 * h)
    assert mf.planner_marginal_benefit(te, **kw) == pytest.approx(numeric, abs=1e-5)


@pytest.mark.parametrize("th,expected", [(0.7, -1), (0.9, -1), (1.0, 0), (1.2, 1), (2.0, 1)])
def test_planner_benefit_of_enclosure_has_the_sign_of_theta_minus_one(th, expected):
    """Not theta_H -- this margin turns at theta = 1, because it involves Lambda_o and not
    Lambda_mu. Confusing the two thresholds is the easy mistake here."""
    vals = [mf.planner_marginal_benefit(te, b=0.7, alp=0.4, th=th) for te in (0.0, 0.5, 1.0)]
    assert all(np.sign(v) == expected for v in vals), vals


@pytest.mark.parametrize("th", [0.7, 0.9, 1.0])
@pytest.mark.parametrize("c", [0.01, 0.05, 0.2])
def test_planner_never_encloses_when_theta_is_at_most_one(th, c):
    """Full enclosure is NOT generally first best. With theta <= 1 the planner's gross
    output is flat or falling in te, so any positive enclosure cost gives t_e^o = 0 --
    however misallocated the decentralized economy's labor is at te=0.
    """
    grid = np.linspace(0, 1, 201)
    value = [mf.total_output(t, b=0.7, alp=0.4, th=th, mu=1.0) - c * t for t in grid]
    assert grid[int(np.argmax(value))] == pytest.approx(0.0)


def test_regulating_the_commons_dominates_enclosing_it_at_theta_one():
    """At theta=1 the first best is te=0 with an efficient labor allocation. Full enclosure
    reaches the same output but pays c for it, so it is second best for any c > 0."""
    kw = dict(b=0.7, alp=0.4, th=1.0, p=1.0)
    first_best = mf.total_output(0.0, mu=1.0, **kw)
    enclosed = mf.total_output(1.0, mu=0.0, **kw)
    distorted = mf.total_output(0.0, mu=0.0, **kw)
    assert enclosed == pytest.approx(first_best)      # same allocation, gross of cost
    assert distorted < first_best                     # the commons distortion is real
    for c in (0.01, 0.05, 0.16):
        assert enclosed - c < first_best


@pytest.mark.parametrize("th", [0.9, 1.0, 1.6])
@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("tau", [0.0, 0.5, 1.0])
def test_private_marginal_return_matches_rentals_computed_from_scratch(th, mu, tau):
    """Eq (42) factorizes r^e - tau*r^c into a manufacturing scale factor and a bracket
    carrying tau alone. Check it against the two rentals built from marginal products,
    with no factorization anywhere."""
    te, alp, b = 0.4, 0.4, 0.7
    lm = mf.labor_share(te, b=b, alp=alp, th=th, mu=mu)
    le = mf.agricultural_labor(te, th=th, alp=alp, mu=mu, b=b)
    lc = (1 - lm) - le
    r_e = th * (1 - alp) * (le / te)**alp
    r_c = (1 - alp) * (lc / (1 - te))**alp
    expected = r_e - tau * r_c
    got = mf.private_marginal_return(te, tau=tau, b=b, alp=alp, th=th, mu=mu)
    assert got == pytest.approx(expected, rel=1e-9)


def test_private_and_social_margins_coincide_only_at_mu_and_tau_both_one():
    """Sec 5.3's claim, with manufacturing: efficiency needs BOTH instruments. The private
    bracket is [theta*Lambda_mu^alpha - tau], the social one [Lambda_o - 1]."""
    kw = dict(b=0.7, alp=0.4, th=1.6)
    for te in (0.2, 0.6):
        social = mf.planner_marginal_benefit(te, **kw)
        assert mf.private_marginal_return(te, tau=1.0, mu=1.0, **kw) == pytest.approx(social)
        # either instrument alone is not enough
        assert mf.private_marginal_return(te, tau=1.0, mu=0.0, **kw) != pytest.approx(social)
        assert mf.private_marginal_return(te, tau=0.0, mu=1.0, **kw) != pytest.approx(social)


@pytest.mark.parametrize("alp", [0.3, 0.4, 0.5])
@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
def test_full_compensation_binds_exactly_below_theta_H_to_the_alpha(alp, mu):
    """tau* = 1 exactly at theta = (theta_H^mu)^alpha -- a threshold strictly between 1 and
    theta_H, collapsing to 1 at mu=1. Above it no admissible tau deters enclosure."""
    cut = model.theta_H(alp, mu)**alp
    assert mf.compensation_threshold(cut, alp, mu) == pytest.approx(1.0)
    assert 1.0 - 1e-12 <= cut <= model.theta_H(alp, mu) + 1e-12
    assert mf.compensation_threshold(cut * 0.9, alp, mu) < 1.0
    assert mf.compensation_threshold(cut * 1.1, alp, mu) > 1.0


@pytest.mark.parametrize("alp", [0.4, 0.5])
def test_compensation_threshold_rises_with_governance(alp):
    """The second-best tension: better governance raises Lambda_mu and hence the enclosed
    rent, so a *higher* compensation rate is needed to deter enclosure."""
    taus = [mf.compensation_threshold(0.9, alp, mu) for mu in (0.0, 0.25, 0.5, 0.75, 1.0)]
    assert taus == sorted(taus)
    assert taus[0] < taus[-1]


def test_agricultural_labor_is_reaction_function_scaled_by_labor_left_in_agriculture():
    """Eq. (36): the usual l_e(t_e) times (1 - l_m)."""
    from enclose.model import Lambda, le
    te, th, alp, mu = 0.6, 1.5, 0.5, 0.0
    lm = mf.labor_share(te, alp=alp, th=th, mu=mu)
    expected = le(te, th, alp, mu) * (1 - lm)
    assert mf.agricultural_labor(te, th=th, alp=alp, mu=mu) == pytest.approx(expected)
    # and it must be strictly below the no-manufacturing allocation
    assert mf.agricultural_labor(te, th=th, alp=alp, mu=mu) < le(te, th, alp, mu)
