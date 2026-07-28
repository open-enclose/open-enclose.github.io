r"""Symbolic derivations of every locus, as the source of truth for the numeric layer.

The point of this module is *derivation*, not restatement. Each locus is obtained here by
writing down the relevant objective or payoff, differentiating or integrating it, and
solving for $\bar l$ — the same steps `Model_Construction.ipynb` cells 4-23 and 38-43 do by
hand. `enclose.loci` then carries the closed forms for fast numpy evaluation, and
`tests/test_symbolic.py` asserts the two agree.

That matters because the numeric layer's formulas were, until this module existed, *all*
hand-transcriptions. They were cross-checked against each other and against the original
notebook/script implementations — but a shared error in the original derivation would have
been invisible to those checks, since every copy inherited it. Deriving independently from
the objective is the only check that catches that class of error.

What this verifies that nothing did before:
- the $\mu$ extension, whose algebra existed only as hand-written markdown;
- the joint $(\mu,\tau)$ form, and its collapse onto the planner locus at $\mu=\tau=1$;
- the global-games locus, by actually integrating the payoff over $t_e\in[0,1]$ rather
  than trusting a hand-computed integral.

Note on `A`: absent here as in the rest of the package. Every locus solves "marginal
benefit = marginal cost", and the `A` in the benefit cancels against the `c` in the cost,
so `c` below is the paper's `c/A`. See `enclose.loci`'s module docstring.

Solving and integrating is slow, so results are cached; `lambdified()` is the fast path.
"""

from functools import lru_cache

import sympy as sp

# alpha/theta/c/lbar are strictly positive; mu and tau legitimately take the value 0, so
# they are only nonnegative -- declaring them positive makes sympy refuse to substitute 0.
alpha, theta, te, c, lbar = sp.symbols("alpha theta t_e c lbar", positive=True)
mu, tau = sp.symbols("mu tau", nonnegative=True)

#: Planner's Lambda, $\Lambda_o = \theta^{1/(1-\alpha)}$ (i.e. Lambda_mu at mu=1).
Lambda_o = theta**(1 / (1 - alpha))

#: $\Lambda_\mu$, eq. (23). At mu=0 this is $(\alpha\theta)^{1/(1-\alpha)}$.
Lambda_mu = (alpha * theta / (1 - mu * (1 - alpha)))**(1 / (1 - alpha))

#: $\Lambda$ at mu=0, the baseline decentralized case.
Lambda = Lambda_mu.subs(mu, 0)


# ---------------------------------------------------------------------------
# Objectives and payoffs -- the things we differentiate/integrate
# ---------------------------------------------------------------------------

def planner_objective():
    r"""First-best objective per unit land, $z_1(t_e) - c\,t_e$, eq. (5).

    $$z_1(t_e) = \bar l^\alpha\left(1 + (\Lambda_o - 1)t_e\right)^{1-\alpha}$$
    """
    return lbar**alpha * ((Lambda_o - 1) * te + 1)**(1 - alpha) - c * te


def second_best_objective():
    r"""Second-best objective per unit land, $z_0(t_e) - c\,t_e$, eq. (17).

    Labor is allocated by the decentralized reaction function, so the bracket differs from
    the planner's. Written as notebook cell 12 writes it, with $\Lambda/\alpha$ where
    `enclose.model.zpv` writes the equal $\theta\Lambda^\alpha$.
    """
    return (lbar**alpha * (1 - te + Lambda / alpha * te) / (1 - te + Lambda * te)**alpha
            - c * te)


def private_payoff():
    r"""Encloser's payoff per unit land, net of compensation, eq. (27).

    $$r^e_\mu(t_e) - \tau\, r^c_\mu(t_e)
      = (1-\alpha)\,\bar l^\alpha\,(\theta\Lambda_\mu^\alpha - \tau)\,
        \left(1+(\Lambda_\mu-1)t_e\right)^{-\alpha}$$

    Setting this equal to `c` at an endpoint gives the decentralized loci; integrating it
    over $t_e\in[0,1]$ (Laplacian beliefs) gives the global-games locus.
    """
    return ((1 - alpha) * lbar**alpha * (theta * Lambda_mu**alpha - tau)
            * (1 + (Lambda_mu - 1) * te)**(-alpha))


# ---------------------------------------------------------------------------
# Solved loci (cached: solve/integrate are slow)
# ---------------------------------------------------------------------------

def _generic_branch(expr):
    r"""Drop the economically-void $\alpha=1$ branch of a Piecewise.

    `sp.integrate` splits the global-games integral on `Ne(alpha, 1)`, because at
    $\alpha=1$ the antiderivative becomes logarithmic. But $\alpha$ is the labor share and
    the model maintains $\alpha\in(0,1)$ throughout — land would not be a factor of
    production at $\alpha=1$ — so that branch is meaningless here. sympy cannot infer the
    upper bound from a `positive=True` assumption, hence selecting it explicitly rather
    than letting `solve` return both branches.
    """
    if not isinstance(expr, sp.Piecewise):
        return expr
    for piece, cond in expr.args:
        if cond == sp.Ne(alpha, 1):
            return piece
    raise ValueError(f"no Ne(alpha, 1) branch found in {expr}")


def _solve_for_lbar(equation):
    """Solve `equation` for lbar and return the single positive branch."""
    sols = sp.solve(equation, lbar)
    if len(sols) != 1:
        raise ValueError(f"expected exactly one solution for lbar, got {len(sols)}")
    return sols[0]


@lru_cache(maxsize=None)
def l01():
    """First-best no-enclosure locus, eq. (6): where z_1'(0) = c."""
    return _solve_for_lbar(sp.Eq(sp.diff(planner_objective(), te).subs(te, 0), 0))


@lru_cache(maxsize=None)
def l11():
    """First-best full-enclosure locus, eq. (7): where z_1'(1) = c."""
    return _solve_for_lbar(sp.Eq(sp.diff(planner_objective(), te).subs(te, 1), 0))


@lru_cache(maxsize=None)
def ld0():
    """Decentralized r(0)=c locus, eq. (14), carrying both mu and tau."""
    return _solve_for_lbar(sp.Eq(private_payoff().subs(te, 0), c))


@lru_cache(maxsize=None)
def ld1():
    """Decentralized r(1)=c locus, eq. (15), carrying both mu and tau."""
    return _solve_for_lbar(sp.Eq(private_payoff().subs(te, 1), c))


@lru_cache(maxsize=None)
def gg():
    r"""Global-games risk-dominance locus, eq. (17), carrying both mu and tau.

    Derived by integrating the payoff over $t_e\in[0,1]$ — the Laplacian-beliefs condition
    $E[r^e - \tau r^c - c] = 0$ — rather than by restating a hand-computed integral.
    """
    integral = _generic_branch(sp.integrate(private_payoff(), (te, 0, 1)))
    return _solve_for_lbar(sp.Eq(integral, c))


@lru_cache(maxsize=None)
def lc0():
    """Second-best no-enclosure locus (high-TFP side), eq. (19): where z_0'(0) = c."""
    return _solve_for_lbar(sp.Eq(sp.diff(second_best_objective(), te).subs(te, 0), 0))


@lru_cache(maxsize=None)
def ls():
    r"""Second-best full-vs-none locus (low-TFP side), eq. (18).

    Not a first-order condition: below $\theta_H$ the objective is convex in $t_e$, so the
    optimum is at a corner and the relevant comparison is of *endpoint values*,
    $z_0(1) = z_0(0)$. (Notebook cells 22-23 do the same.)
    """
    obj = second_best_objective()
    return _solve_for_lbar(sp.Eq(obj.subs(te, 1) - obj.subs(te, 0), 0))


#: Every locus this module derives, by the name `enclose.loci` uses.
LOCI = {
    "ln_l01": l01,
    "ln_l11": l11,
    "ln_ld0": ld0,
    "ln_ld1": ld1,
    "ln_gg": gg,
    "ln_lc0": lc0,
    "ln_ls": ls,
}


@lru_cache(maxsize=None)
def lambdified(name, alp_value, c_value, mu_value=0.0, tau_value=0.0):
    """Return a fast numpy callable f(theta) for locus `name` at fixed parameters.

    Substitutes alpha/c/mu/tau first so the returned function takes theta alone, matching
    how the loci are actually used (swept over a theta grid at a fixed calibration).
    """
    if name not in LOCI:
        raise KeyError(f"unknown locus {name!r}; known: {sorted(LOCI)}")
    expr = LOCI[name]().subs({
        alpha: sp.Rational(alp_value).limit_denominator(10**6),
        c: sp.Rational(c_value).limit_denominator(10**6),
        mu: sp.Rational(mu_value).limit_denominator(10**6),
        tau: sp.Rational(tau_value).limit_denominator(10**6),
    })
    return sp.lambdify(theta, expr, "numpy")
