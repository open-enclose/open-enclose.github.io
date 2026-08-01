r"""Foregone output and its decomposition over the $(\theta, \ln\bar l)$ plane.

Ported from `enclosure_paper/welfare/welfare_maps.py`, which computed all of this by
importing `enclose` from outside. Bringing the economics *into* the package means the
browser can run it from the shipped wheel, and means the identities below are checked by
`tests/test_welfare.py` on every push rather than by a script someone remembers to run.

Only the **efficiency** half is here. The distributional half of that analysis is blocked on
`model.weq`, which returns a labor share of 1.0 at every $t_e$ when $\mu=1$; until the
$\mu>0$ wage/rent split is settled there is nothing here to port.

What it computes, for fixed $(\alpha, c/A, \mu, \tau)$, on a grid over $(\theta, \ln\bar l)$:

    W^FB = max_te [ z(te)          - c*te ]   first-best labor rule, optimal enclosure
    W^SB = max_te [ totalq(te, mu) - c*te ]   distorted labor rule, optimal enclosure
    W^P  =         totalq(te_d, mu) - c*te_d  distorted labor rule, private enclosure

and the identity

    W^FB - W^P  =  (W^FB - W^SB)  +  (W^SB - W^P)
    total loss  =  misallocation  +  enclosure error

The second-best planner is the device that makes the split meaningful: it **inherits the
labor distortion it cannot fix** but chooses enclosure freely, so it isolates one failure
from the other. Both terms are non-negative by construction rather than by luck — the
first-best labor rule maximizes output at any $t_e$, so $z \ge z_0^\mu$ pointwise, and
$W^{SB}$ is a maximum over the very objective $W^{P}$ merely evaluates at a point.
`build_grid` asserts both orderings and both identities at every grid point.

**"Enclosure error", not "the race".** $W^{SB}-W^{P}$ is the cost of the enclosure margin
being privately chosen, and it has two faces: over-enclosure ($t_e^d > t_e^{sb}$ — races,
rent grabs) and under-enclosure ($t_e^d < t_e^{sb}$ — transitions compensation deterred). At
$\tau=0$ the mass is almost all over-enclosure, so calling the wedge "the race" nearly held;
at $\tau=1$ it is entirely under-enclosure, where nobody is racing anything. The
`over_enclosure` / `under_enclosure` components split it by $\operatorname{sign}(t_e^d -
t_e^{sb})$ so the trade between them is visible.

**Two orderings, both available.** Sequential decompositions are order-dependent when the
margins interact. The default changes the labor rule first, at each regime's own optimal
$t_e$. The alternative changes the enclosure rate first, evaluating at the *actual* $t_e^d$:

    W^FB - W^P  =  (W^FB - [z(te_d)-c*te_d])  +  ([z(te_d)-c*te_d] - W^P)
                =  enclosure error (FB labor)  +  misallocation at the actual te_d

`misallocation` (the default) answers "what would the labor distortion cost even under
optimal enclosure management" — a counterfactual that never touches the private decision,
and which is $\tau$-invariant by construction. `misallocation_actual` answers "how much
labor misallocation is actually occurring here" — zero wherever the private sector encloses
nothing or everything, however far that is from optimal. Neither is more correct.

Enclosure rates come from a grid search over $t_e \in [0,1]$ rather than from the
first-order conditions. That is deliberate: $z_0$ is convex below $\theta_H$ and concave
above, so an FOC solver needs branch logic that is easy to get subtly wrong, while a bounded
1-D maximum over a fine grid cannot be. The private rate is taken from `model.tepvt_g`
directly, because it is a *selection*, not a maximum, and cannot be gridded for.
"""

import numpy as np

from . import loci, model

ALP = loci.ALP          #: 2/3, the paper's benchmark
C = loci.C              #: 1.0 -- this is c/A, not c (see the package README)
MU = 0.0                #: ungoverned commons; the benchmark case

#: Candidate enclosure rates for both maximisations. 401 points puts the mesh at 0.0025,
#: which is finer than any feature of z_0 at the parameters the site plots.
TE_GRID = np.linspace(0.0, 1.0, 401)


# ---------------------------------------------------------------------------
# The three regimes
# ---------------------------------------------------------------------------

def output_mu(te, th, lbar, mu, alp=ALP):
    r"""`model.totalq`, with the two corners evaluated in closed form.

    Necessary, not defensive. `model.le` computes $1+(\Lambda_\mu-1)t_e$, which at $t_e=1$
    need not equal $\Lambda_\mu$ exactly in floating point — for $\Lambda=0.216$,
    `1 + (0.216 - 1)` is `0.21600000000000003`. `le` then lands a few ulps *above* 1, so
    `1 - le` is a small negative and `(1-le)**alpha` is NaN. One NaN at the full-enclosure
    corner silently poisons `np.max` over the whole grid.

    The corners are exact: $Y(0)=\bar l^\alpha$ (all land commons, allocation trivial) and
    $Y(1)=\theta\bar l^\alpha$ (all land enclosed, no commons), for every $\mu$. Substituting
    them is *more* accurate than what `totalq` returns there, not merely safer.
    """
    te = np.atleast_1d(np.asarray(te, dtype=float))
    with np.errstate(invalid="ignore"):
        y = model.totalq(te, th, alp, lbar, mu)
    y = np.where(te == 0.0, lbar**alp, y)
    y = np.where(te == 1.0, th * lbar**alp, y)
    if not np.all(np.isfinite(y)):
        raise FloatingPointError(
            f"non-finite output away from the corners at theta={th}, lbar={lbar}, mu={mu}")
    return y


def _candidates(extra=()):
    """The te grid plus any extra points, shared by both maximisations.

    Both regimes must search the *same* set. At mu=1 the two objectives coincide exactly
    (Lambda_mu = Lambda_o), so any asymmetry in the candidate sets shows up directly as an
    apparent W^SB > W^FB -- a theorem violation, and one that tripped the ordering assertion
    at mu=tau=1 by ~2e-6 when only the second-best saw the private rate.
    """
    if len(extra) == 0:
        return TE_GRID
    return np.concatenate([TE_GRID, np.atleast_1d(np.asarray(extra, dtype=float))])


def w_first_best(th, lbar, alp=ALP, c=C, extra=()):
    """max over te of z(te) - c*te, with the first-best labor rule.

    `model.z` is a closed form with no `le` call, so it needs no corner patching; it agrees
    with `totalq(..., mu=1)` to machine precision, which is the cross-check that it really
    is the first-best labor rule.
    """
    te = _candidates(extra)
    obj = model.z(te, th, alp, lbar) - c * te
    k = int(np.argmax(obj))
    return obj[k], te[k]


def w_second_best(th, lbar, mu=MU, alp=ALP, c=C, extra=()):
    """max over te of Y^mu(te) - c*te: optimal enclosure, but labor allocated as the
    decentralized market allocates it.

    `extra` adds candidate enclosure rates to the grid. The private rate `te_d` must be
    passed in: it is a feasible te, so the second-best maximum is by definition at least the
    private value -- but a grid that happens to straddle a peaked optimum can miss it by a
    fraction and invert the inequality. Including the point makes W^SB >= W^P exact by
    construction rather than true-up-to-mesh.
    """
    te = _candidates(extra)
    obj = output_mu(te, th, lbar, mu, alp) - c * te
    k = int(np.argmax(obj))
    return obj[k], te[k]


def w_private(th, lbar, mu=MU, alp=ALP, c=C, tau=0.0):
    r"""Y^mu(te_d) - c*te_d at the privately chosen enclosure rate, global-games selected.

    Not a maximum of anything — that is the whole point. The gap to `w_second_best` is
    output lost to the enclosure decision itself, holding the labor distortion fixed.

    **This is the only one of the three that sees $\tau$.** Compensation is a transfer, so it
    cancels out of total output and cannot move the first-best or the second-best; it changes
    the privately chosen $t_e$ and nothing else. That single channel is why the whole loss
    surface is $\tau$-invariant except through the private regime — a property
    `tests/test_welfare.py` asserts directly, and the sharpest available check that the
    implementation is right.

    One qualification, since it is easy to over-claim. $W^{FB}$ is $\tau$-invariant to the
    bit, but $W^{SB}$ is not *quite*: `build_grid` passes this function's $t_e^d$ into both
    maximisations as an extra candidate, so the candidate set carries $\tau$ even though the
    objective does not, and a peak the 401-point grid straddles can be resolved marginally
    better at one $\tau$ than another. Measured at $\mu=0.3$: one grid point in 625, $5\times
    10^{-7}$ relative. It is a mesh artifact, not a channel.
    """
    te_d = model.tepvt_g(th, alp, c, lbar, mu, tau)
    return float(output_mu(te_d, th, lbar, mu, alp)[0]) - c * te_d, te_d


# ---------------------------------------------------------------------------
# Grid
# ---------------------------------------------------------------------------

def build_grid(n_th=161, n_l=161, th_lo=0.90, th_hi=2.30, lnl_lo=-1.0, lnl_hi=4.0,
               mu=MU, tau=0.0, alp=ALP, c=C):
    """Returns (theta, ln lbar, dict of surfaces). Losses are fractions of W^FB."""
    # theta_H^mu is a removable singularity in `tepvt` (a 1/(Lambda-1)), so nudge the grid
    # off it rather than special-casing a NaN column afterwards.
    th = np.linspace(th_lo, th_hi, n_th)
    th_H = model.theta_H(alp, mu)
    th[np.isclose(th, th_H, atol=1e-9)] += 1e-6
    lnl = np.linspace(lnl_lo, lnl_hi, n_l)

    fb = np.empty((n_l, n_th))
    sb = np.empty_like(fb)
    pv = np.empty_like(fb)
    ted = np.empty_like(fb)
    tesb = np.empty_like(fb)
    # W^FB evaluated at the *private* te_d: z(te_d) - c*te_d. The pivot of the alternative
    # ordering -- see the module docstring.
    wfbd = np.empty_like(fb)

    for j, t in enumerate(th):
        for i, x in enumerate(lnl):
            lbar = np.exp(x)
            pv[i, j], ted[i, j] = w_private(t, lbar, mu, alp, c, tau=tau)
            # Same candidate set for both, or mu=1 breaks the ordering -- see `_candidates`.
            fb[i, j], _ = w_first_best(t, lbar, alp, c, extra=(ted[i, j],))
            sb[i, j], tesb[i, j] = w_second_best(t, lbar, mu, alp, c, extra=(ted[i, j],))
            wfbd[i, j] = model.z(ted[i, j], t, alp, lbar) - c * ted[i, j]

    # The decompositions are identities and the orderings are theorems. Check all of it
    # here so a later refactor cannot quietly break them.
    tol = 1e-9
    assert np.all(fb - sb >= -tol), "W^FB < W^SB somewhere: first-best labor rule is optimal"
    assert np.all(sb - pv >= -tol), "W^SB < W^P somewhere: second-best is a max over the same objective"
    assert np.all(fb - wfbd >= -tol), "W^FB < z(te_d)-c*te_d somewhere: W^FB is the max of that objective"
    assert np.all(wfbd - pv >= -tol), "z(te_d) < Y^mu(te_d) somewhere: FB labor rule is optimal at any te"
    assert np.allclose((fb - pv), (fb - sb) + (sb - pv)), "planner-side decomposition is not an identity"
    assert np.allclose((fb - pv), (fb - wfbd) + (wfbd - pv)), "actual-te decomposition is not an identity"

    over_mask = ted > tesb + 1e-9
    under_mask = ted < tesb - 1e-9
    return th, lnl, {
        "total": (fb - pv) / fb,
        "misallocation": (fb - sb) / fb,
        "enclosure": (sb - pv) / fb,
        "over_enclosure": np.where(over_mask, sb - pv, 0.0) / fb,
        "under_enclosure": np.where(under_mask, sb - pv, 0.0) / fb,
        "misallocation_actual": (wfbd - pv) / fb,
        "enclosure_fb": (fb - wfbd) / fb,
        "te_private": ted, "te_second_best": tesb,
        "W_FB": fb, "W_SB": sb, "W_P": pv, "W_FB_ted": wfbd,
    }


# ---------------------------------------------------------------------------
# Components and normalizations
# ---------------------------------------------------------------------------

#: Colour ceilings, held fixed across slider settings. An autoscaled colourbar makes a
#: shrinking loss look identical to a constant one, which defeats the purpose of a slider.
#: These are roughly the observed maxima on the default window at benchmark (mu, tau);
#: extreme corners of the (mu, tau) square can exceed them and saturate the colormap. That is
#: accepted — the panel title reports the true max, and a fixed scale is what makes a sweep
#: comparable.
_VMAX_RATIO = {"total": 25.0, "misallocation": 5.0, "enclosure": 25.0,
               "over_enclosure": 25.0, "under_enclosure": 25.0,
               "misallocation_actual": 5.0, "enclosure_fb": 25.0}
_VMAX_LAND = {"total": 2.5, "misallocation": 0.10, "enclosure": 2.5,
              "over_enclosure": 2.5, "under_enclosure": 2.5,
              "misallocation_actual": 0.25, "enclosure_fb": 2.5}
_VMAX_WORKER = {"total": 0.16, "misallocation": 0.08, "enclosure": 0.10,
                "over_enclosure": 0.10, "under_enclosure": 0.10,
                "misallocation_actual": 0.07, "enclosure_fb": 0.16}
VMAX = {**{("ratio", k): v for k, v in _VMAX_RATIO.items()},
        **{("per_land", k): v for k, v in _VMAX_LAND.items()},
        **{("per_worker", k): v for k, v in _VMAX_WORKER.items()}}

NORM_LABEL = {
    "ratio": "% of first-best",
    "per_land": "per unit land (units of A)",
    "per_worker": "per worker (units of A)",
}

COMP_LABEL = {
    "total": "total loss",
    "misallocation": "misallocation (at the planners' $t_e$)",
    "enclosure": "enclosure error (over + under)",
    "over_enclosure": "over-enclosure (the race)",
    "under_enclosure": "under-enclosure (deterred/blocked)",
    "misallocation_actual": "misallocation (at the actual $t_e$)",
    "enclosure_fb": "enclosure error (at first-best labor)",
}


def loss_surface(S, lnl, component="total", normalize="ratio"):
    r"""Pick a loss component out of `build_grid`'s output and normalize it.

    **The three normalizations are not rescalings of one another.** Output per unit land
    scales as $\bar l^{\alpha}$, so per-worker output scales as $\bar l^{\alpha-1}$ and
    *falls* in density. Dividing by $\bar l$ therefore upweights sparse economies hard enough
    to move the worst case to the opposite corner of the plane: at $\mu=\tau=0$ the worst
    economy is poor and crowded under `ratio` and `per_land`, but productive and
    land-abundant under `per_worker`, and the top-five lists do not overlap at all. Which one
    is right depends on the question, so it is chosen explicitly rather than defaulted into.

    The `ratio` is the only one invariant to that choice — rescaling numerator and
    denominator by the same factor leaves it unchanged, so the per-land, per-worker and total
    loss *ratios* are identical. That is why it is the default.
    """
    encl = S["W_SB"] - S["W_P"]
    num = {"total": S["W_FB"] - S["W_P"],
           # planner-side ordering (tau-invariant by construction; compares the two planners)
           "misallocation": S["W_FB"] - S["W_SB"],
           "enclosure": encl,
           # the two faces of the enclosure-error wedge, split by sign(te_d - te_sb)
           "over_enclosure": np.where(S["te_private"] > S["te_second_best"] + 1e-9, encl, 0.0),
           "under_enclosure": np.where(S["te_private"] < S["te_second_best"] - 1e-9, encl, 0.0),
           # actual-te ordering: what is happening in *this* economy, at the private te_d
           "misallocation_actual": S["W_FB_ted"] - S["W_P"],
           "enclosure_fb": S["W_FB"] - S["W_FB_ted"]}[component]
    if normalize == "ratio":
        return 100 * num / S["W_FB"]
    if normalize == "per_land":
        return num
    if normalize == "per_worker":
        return num / np.exp(lnl)[:, None]
    raise ValueError(f"unknown normalize={normalize!r}")
