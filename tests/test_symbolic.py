"""The symbolic layer is the source of truth; assert the numeric layer matches it.

Every formula in `enclose.loci` was a hand-transcription until `enclose.symbolic` existed.
The existing cross-checks (loci vs model, loci vs the original notebook/script forms) all
share a blind spot: an error in the *original* derivation propagates into every copy and
every check passes. These tests close that gap by deriving each locus independently from
its objective and comparing.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from enclose import loci, symbolic  # noqa: E402

ALP, C = loci.ALP, loci.C

# theta grids per locus, chosen inside each one's domain of definition
TH_FB = np.array([1.15, 1.3, 1.6, 1.9, 2.1])       # first-best loci
TH_HI = np.array([1.55, 1.7, 1.9, 2.1])            # high-TFP (decentralized, second-best)
TH_LO = np.array([0.85, 1.0, 1.2, 1.4])            # low-TFP (global games)
TH_LS = np.array([1.1, 1.2, 1.35, 1.45])           # second-best full-vs-none


def _sym(name, thv, mu=0.0, tau=0.0):
    """Evaluate the symbolic locus and return it in log units, as loci.py returns."""
    f = symbolic.lambdified(name, ALP, C, mu, tau)
    return np.log(np.asarray(f(thv), dtype=float))


@pytest.mark.parametrize("name,numeric,thv", [
    ("ln_l01", loci.ln_l01, TH_FB),
    ("ln_l11", loci.ln_l11, TH_FB),
    ("ln_ld0", loci.ln_ld0, TH_HI),
    ("ln_ld1", loci.ln_ld1, TH_HI),
    ("ln_lc0", loci.ln_lc0, TH_HI),
    ("ln_ls", loci.ln_ls, TH_LS),
    ("ln_gg", loci.ln_gg, TH_LO),
])
def test_numeric_locus_matches_symbolic_derivation(name, numeric, thv):
    """Each closed form in loci.py equals the expression derived from its objective."""
    np.testing.assert_allclose(numeric(thv), _sym(name, thv), rtol=1e-10)


@pytest.mark.parametrize("tau", [0.0, 0.3, 0.7])
def test_tau_extension_matches_symbolic(tau):
    """The tau-extended decentralized loci, derived from eq. (27)'s payoff."""
    np.testing.assert_allclose(loci.ln_ld0(TH_HI, tau=tau), _sym("ln_ld0", TH_HI, tau=tau), rtol=1e-10)
    np.testing.assert_allclose(loci.ln_ld1(TH_HI, tau=tau), _sym("ln_ld1", TH_HI, tau=tau), rtol=1e-10)


@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
def test_mu_extension_matches_symbolic(mu):
    """The mu extension -- whose algebra previously existed only as hand-written markdown,
    with no symbolic verification anywhere in either codebase."""
    np.testing.assert_allclose(loci.ln_ld0(TH_HI, mu=mu), _sym("ln_ld0", TH_HI, mu=mu), rtol=1e-10)


def test_global_games_tau_extension_matches_symbolic_integration():
    """The gg locus was hand-derived from a hand-computed integral in
    generate_trajectories_figure.py. Here sympy performs the integration itself."""
    th = np.array([1.35, 1.42, 1.48])
    np.testing.assert_allclose(loci.ln_gg(th, tau=1.0), _sym("ln_gg", th, tau=1.0), rtol=1e-10)


def test_wedge_closes_at_mu_tau_one_symbolically():
    """Independent confirmation of the paper's Key Result (5.3): derived symbolically from
    the *decentralized* payoff, the mu=tau=1 loci equal the *planner's* loci.

    tests/test_loci.py asserts this too, but from the numeric closed forms -- which share a
    derivation ancestor. This route starts from the payoff and never touches loci.py's
    planner functions, so it is a genuinely independent check.
    """
    np.testing.assert_allclose(_sym("ln_ld0", TH_FB, mu=1.0, tau=1.0), loci.ln_l01(TH_FB), rtol=1e-10)
    np.testing.assert_allclose(_sym("ln_ld1", TH_FB, mu=1.0, tau=1.0), loci.ln_l11(TH_FB), rtol=1e-10)


def test_second_best_ls_comes_from_endpoint_comparison_not_an_foc():
    """z_0 is convex in t_e below theta_H, so lbar^s compares endpoint values rather than
    solving a first-order condition. Guard that the objective really is convex there, so
    the endpoint comparison is the right derivation and not a shortcut."""
    import sympy as sp
    obj = symbolic.second_best_objective()
    d2 = sp.diff(obj, symbolic.te, 2).subs({
        symbolic.alpha: sp.Rational(2, 3), symbolic.c: 1,
        symbolic.lbar: 1, symbolic.te: sp.Rational(1, 2),
    })
    for thv in (1.1, 1.2, 1.3):          # below theta_H = 1.5
        assert float(sp.N(d2.subs(symbolic.theta, thv))) > 0
