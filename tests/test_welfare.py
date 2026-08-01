"""The welfare decomposition: orderings, identities, and the results the site page claims.

`build_grid` already asserts the orderings and identities at every grid point, so these tests
are partly a guard on that guard -- they run it at (mu, tau) combinations the site's sliders
reach, including the corners where the assertions are tightest. The rest pin the claims the
explore page makes in prose, so that a refactor which quietly changes a number cannot leave
the page asserting the old one.
"""

import numpy as np
import pytest

from enclose import model, welfare

# Coarse by design: these check theorems and identities, which hold pointwise, not the
# smoothness of a picture. n=25 is 625 points per case and keeps the suite quick.
N = 25
CORNERS = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (0.35, 0.35), (0.5, 0.75)]


def _grid(mu, tau, n=N):
    return welfare.build_grid(n_th=n, n_l=n, mu=mu, tau=tau)


# ---------------------------------------------------------------------------
# Orderings and identities
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mu,tau", CORNERS)
def test_orderings_and_identities_hold(mu, tau):
    """build_grid asserts internally; this makes the failure a named test rather than an
    AssertionError from inside a plotting call."""
    _, _, S = _grid(mu, tau)
    assert np.all(S["W_FB"] >= S["W_SB"] - 1e-9)
    assert np.all(S["W_SB"] >= S["W_P"] - 1e-9)
    assert np.allclose(S["total"], S["misallocation"] + S["enclosure"])
    assert np.allclose(S["total"], S["enclosure_fb"] + S["misallocation_actual"])


@pytest.mark.parametrize("mu,tau", CORNERS)
def test_every_component_is_non_negative(mu, tau):
    _, _, S = _grid(mu, tau)
    for k in ("total", "misallocation", "enclosure", "over_enclosure",
              "under_enclosure", "misallocation_actual", "enclosure_fb"):
        assert S[k].min() >= -1e-9, f"{k} went negative"


@pytest.mark.parametrize("mu,tau", CORNERS)
def test_enclosure_wedge_splits_exactly_into_over_and_under(mu, tau):
    """The two faces partition the wedge: te_d is above, below, or equal to te_sb."""
    _, _, S = _grid(mu, tau)
    assert np.allclose(S["enclosure"], S["over_enclosure"] + S["under_enclosure"])


# ---------------------------------------------------------------------------
# The transfer-neutrality theorem -- the sharpest check that tau is wired correctly
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tau", [0.0, 0.4, 1.0])
def test_planner_regimes_do_not_see_tau(tau):
    """Compensation is a transfer, so it cancels out of total output and cannot move either
    planner. Only the private regime may respond. If tau ever leaked into the planners'
    *objectives* this is what would catch it -- and a bug of exactly that shape (the whole
    surface tau-invariant, because tepvt lacked a tau argument) is why the check exists.

    W^FB is invariant to the bit. W^SB is not, and the reason is not economics: `build_grid`
    feeds the private te_d into both maximisations as an extra candidate (see `_candidates`,
    which needs it for W^SB >= W^P to hold exactly rather than up to mesh), and te_d moves
    with tau. So the candidate *set* carries tau even though the objective does not, and a
    peak that the 401-point grid straddles can be resolved a hair better at one tau than
    another. Measured: one grid point in 625, 5e-7 relative. Bounding it is the honest test;
    asserting exact equality would be asserting something the implementation does not claim.
    """
    _, _, base = _grid(0.3, 0.0)
    _, _, S = _grid(0.3, tau)
    assert np.array_equal(base["W_FB"], S["W_FB"]), "first-best moved with tau"

    rel = np.abs(base["W_SB"] - S["W_SB"]) / np.abs(base["W_SB"])
    assert rel.max() < 1e-5, f"second-best moved with tau by {rel.max():.2e}, beyond mesh"
    assert (rel > 0).sum() <= 2, "tau-dependence is spreading beyond isolated mesh points"

    m = np.abs(base["misallocation"] - S["misallocation"])
    assert m.max() < 1e-5, \
        "planner-side misallocation compares the two planners; it cannot see tau"


def test_private_regime_does_see_tau():
    """The converse: without this, the test above would pass on a surface that ignores tau
    entirely."""
    _, _, a = _grid(0.0, 0.0)
    _, _, b = _grid(0.0, 1.0)
    assert not np.allclose(a["W_P"], b["W_P"])
    assert not np.allclose(a["te_private"], b["te_private"])


# ---------------------------------------------------------------------------
# The Key Result, in welfare units
# ---------------------------------------------------------------------------

def test_both_wedges_shut_gives_exactly_zero_loss():
    """At mu=tau=1 the decentralized allocation *is* the first-best, so the loss is zero --
    not small. The tolerance is floating-point, not economic."""
    _, _, S = _grid(1.0, 1.0)
    assert S["total"].max() < 1e-9


def test_unilateral_reform_is_worse_than_doing_nothing():
    """The paper's 'neither alone suffices' sharpened: at the limit either reform alone
    leaves the economy worse off than no reform at all. This is the explore page's headline,
    so it is pinned here."""
    def mean_total(mu, tau):
        return 100 * _grid(mu, tau)[2]["total"].mean()

    nothing = mean_total(0.0, 0.0)
    gov_only = mean_total(1.0, 0.0)
    comp_only = mean_total(0.0, 1.0)
    both = mean_total(1.0, 1.0)

    assert gov_only > nothing, "governance alone should overshoot"
    assert comp_only > nothing, "compensation alone should overshoot"
    assert both < 1e-9
    assert comp_only > gov_only, "compensation alone is the worse of the two"


def test_full_compensation_makes_the_wedge_entirely_under_enclosure():
    """At tau=1 nothing is racing: every bit of the enclosure wedge is a transition
    compensation deterred. This is the correction that retired the name 'the race'."""
    _, _, S = _grid(0.0, 1.0)
    assert S["over_enclosure"].max() < 1e-9
    assert S["under_enclosure"].max() > 0.0


# ---------------------------------------------------------------------------
# output_mu corners, and the NaN it exists to prevent
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("th,lbar", [(0.9, 2.0), (1.5, 10.0), (2.2, 0.5)])
def test_output_corners_are_exact(mu, th, lbar):
    """Y(0) = lbar^alpha and Y(1) = theta*lbar^alpha for every mu -- with all land in one
    state there is no allocation left for governance to affect."""
    a = welfare.ALP
    assert welfare.output_mu(0.0, th, lbar, mu)[0] == pytest.approx(lbar**a, rel=1e-12)
    assert welfare.output_mu(1.0, th, lbar, mu)[0] == pytest.approx(th * lbar**a, rel=1e-12)


def test_output_mu_survives_the_full_enclosure_corner():
    """`model.totalq` can return NaN at te=1 through a float artifact in `le`; a single NaN
    there poisons np.max over a whole grid. Guarding the corner is what output_mu is for."""
    te = np.linspace(0.0, 1.0, 401)
    y = welfare.output_mu(te, 1.0, 3.0, 0.4)
    assert np.all(np.isfinite(y))


# ---------------------------------------------------------------------------
# Normalizations
# ---------------------------------------------------------------------------

def test_the_three_normalizations_are_not_rescalings_of_each_other():
    """Per-worker output falls in density while per-land output rises, so dividing by lbar
    moves the worst-affected economy to the opposite corner of the plane. If these ever
    agreed, the choice would not need to be explicit -- and the page says it does."""
    th, lnl, S = welfare.build_grid(n_th=41, n_l=41, mu=0.0, tau=0.0)
    worst = {}
    for norm in ("ratio", "per_land", "per_worker"):
        M = welfare.loss_surface(S, lnl, "total", norm)
        i, j = np.unravel_index(np.nanargmax(M), M.shape)
        worst[norm] = (round(th[j], 3), round(lnl[i], 3))
    assert worst["per_worker"] != worst["ratio"], "per_worker should disagree with ratio"
    assert worst["per_worker"][0] > worst["ratio"][0], "per_worker favours high theta"
    assert worst["per_worker"][1] < worst["ratio"][1], "per_worker favours low density"


def test_ratio_is_invariant_to_the_level_normalization():
    """The ratio's defence as the default: rescaling numerator and denominator by the same
    factor leaves it unchanged."""
    th, lnl, S = welfare.build_grid(n_th=21, n_l=21, mu=0.0, tau=0.0)
    r = welfare.loss_surface(S, lnl, "total", "ratio")
    per_land = welfare.loss_surface(S, lnl, "total", "per_land")
    assert np.allclose(r, 100 * per_land / S["W_FB"])


def test_unknown_normalize_is_rejected():
    th, lnl, S = welfare.build_grid(n_th=11, n_l=11)
    with pytest.raises(ValueError, match="unknown normalize"):
        welfare.loss_surface(S, lnl, "total", "per_hectare")


# ---------------------------------------------------------------------------
# The grid dodges theta_H rather than producing a NaN column
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mu", [0.0, 0.5])
def test_grid_avoids_the_theta_H_singularity(mu):
    """tepvt carries a 1/(Lambda-1), removable at theta_H but not to floating point. The
    grid is nudged off it; the surfaces must be finite everywhere regardless."""
    th, _, S = welfare.build_grid(n_th=N, n_l=N, mu=mu, tau=0.0)
    # rtol=0: the nudge is +1e-6, and np.isclose's default rtol of 1e-5 is larger than that,
    # so the default would report the nudged point as still "close" and fail a correct grid.
    assert not np.any(np.isclose(th, model.theta_H(welfare.ALP, mu), atol=1e-12, rtol=0))
    assert np.all(np.isfinite(S["total"]))
