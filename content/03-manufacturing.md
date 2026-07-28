---
title: Manufacturing and Structural Transformation
short_title: Manufacturing
---

# Manufacturing and Structural Transformation

:::{note} Status
This extension goes **beyond the published paper**. A section on structural transformation
was cut from the manuscript during revision, and this page is where that material lives —
developed further than the paper ever carried it. Section 5 below reports a result that is
not in the paper at all.
:::

The benchmark model has one mobile factor moving between enclosed and unenclosed
agriculture. Historically the interesting question is what enclosure did to the *other*
margin: whether it released labor to industry. This page adds a manufacturing sector and
asks exactly that — and finds the answer is not the one the standard narrative assumes.

---

## 1. Three sectors

Labor moves freely between manufacturing and agriculture, and within agriculture between
enclosed and unenclosed land. Capital is specific to manufacturing, land to agriculture —
an augmented specific-factors model, with the twist that land may be enclosed or not, which
changes agricultural labor demand and hence labor supply to industry.

| Technology | Sector |
|:---|:---|
| $p \cdot \theta_M \cdot G(K,L) = K^{1-\beta} L^{\beta}$ | Manufacturing |
| $F(T,L) = T^{1-\alpha} L^{\alpha}$ | Unenclosed agriculture |
| $\theta \cdot F(T,L)$ | Enclosed agriculture |

with labor adding up as $l_e + l_u = 1 - l_m$.

## 2. Labor allocation within agriculture

Given a manufacturing share $l_m$, the within-agriculture allocation is exactly the
benchmark reaction function with the agricultural labor force shrunk to $(1-l_m)$ —
equation (36):

$$
l_e^*(t_e) = \frac{\Lambda t_e}{1+(\Lambda-1)t_e}\cdot(1-l_m)
$$

Nothing about the enclosure margin changes; the whole three-sector extension enters through
that one scaling factor. This is why the benchmark's closed forms survive.

## 3. Where the manufacturing share settles

Labor moves until wages are equal across sectors, $w = p\,MPL_m = MPL_e = APL_u$. Writing
the two sides of the manufacturing/agriculture margin:

$$
\underbrace{p \beta \bar k^{1-\beta}}_{C_m}\, l_m^{-(1-\beta)}
\;=\;
\underbrace{\bar t^{1-\alpha}\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}}_{C_a}\,
(1-l_m)^{-(1-\alpha)}
$$

$MPL_m$ falls in $l_m$ and $MPL_a$ rises in it, so **the two cross exactly once**: the
equilibrium exists and is unique for any admissible parameters. (`enclose.manufacturing`
exploits this — it solves with a *bracketed* root-finder, which is guaranteed to converge,
rather than an initial-guess method that could wander.)

Rearranged, the condition is

$$
\frac{l_m^{1-\beta}}{(1-l_m)^{1-\alpha}} = \frac{C_m}{C_a}
$$

which for $\beta \neq \alpha$ is transcendental — there is no closed form, and the
equilibrium must be found numerically. The one exception is $\beta = \alpha$, where the
exponents coincide and it collapses to

$$
l_m = \frac{R}{1+R}, \qquad R = \left(\frac{C_m}{C_a}\right)^{\frac{1}{1-\alpha}}
$$

That special case is worth keeping in view: it is the only fully solvable version, and it
serves as an exact check on the numerical solver used everywhere else.

## 4. Enclosure without any productivity gain

Set $\theta = 1$, so enclosure yields *no* technological improvement whatever, and compare
an unenclosed economy with a fully enclosed one.

```{figure} ../Figures/manufacturing_equilibrium.png
:name: fig-manuf-equilibrium
:width: 100%

Labor market equilibrium before and after enclosure, at $\theta=1$, $\alpha=0.4$,
$\beta=0.7$. Left: no land enclosed — the open-access and planner curves coincide, because
with no enclosure there is no commons distortion to speak of. Right: all land enclosed. The
planner's allocation is *unchanged* at $l_m=0.20$, while under open access it jumps to
$l_m=0.68$.
```

The planner does not move labor at all, and should not: with $\theta=1$ there is nothing to
gain. But the decentralized economy shifts nearly half its workforce into manufacturing —
and at a **lower** equilibrium wage (it falls from 1.14 to 0.79).

This is the Weitzman–Samuelson effect in the three-sector setting. The "structural
transformation" here is not driven by productivity; it is driven entirely by enclosure
removing the commons that had been absorbing labor at its average product. Industry gains
workers because agriculture expels them, not because industry became more attractive.

## 5. The effect reverses at $\theta_H$

The example above is not general — and the direction in which it generalises is the
substantive finding on this page.

$C_a$ carries the factor $\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}$, so the sign of
$\partial l_m/\partial t_e$ is simply the sign of $(\Lambda_\mu - 1)$. And $\Lambda_\mu = 1$
holds exactly at

$$
\theta_H^\mu = \frac{1}{\alpha} - \mu\frac{1-\alpha}{\alpha}
$$

the same threshold that separates strategic complements from substitutes in the benchmark
model. So:

- **$\theta < \theta_H^\mu$** — enclosure is labor-*extensive*, agricultural labor demand
  falls as $t_e$ rises, and labor is released **into** manufacturing. Enclosure
  *accelerates* structural transformation.
- **$\theta > \theta_H^\mu$** — enclosure is labor-*intensive* and pulls labor **back into**
  agriculture. Enclosure *retards* structural transformation.
- **$\theta = \theta_H^\mu$** — enclosure moves no labor at all.

```{figure} ../Figures/structural_transformation.png
:name: fig-structural
:width: 90%

Manufacturing's labor share as land is enclosed, for $\theta$ either side of
$\theta_H = 1/\alpha = 2$. Below the threshold the curves rise, above it they fall, and at
$\theta_H$ exactly the line is flat — the knife-edge is exact, not approximate.
```

The reading matters for economic history. The familiar account — enclosure freed labor for
industry — is a claim about the *low-TFP branch*. Precisely where enclosure is most
defensible on efficiency grounds, because it delivers a large productivity gain, it is
*least* likely to release labor. The §4 example makes the point sharply: the case with the
biggest labor release is the case with no productivity gain at all.

### Governance moves the threshold

Since $\theta_H^\mu$ falls in $\mu$ — from $1/\alpha$ at $\mu=0$ down to $1$ at $\mu=1$ —
better commons governance *widens* the region in which enclosure retards structural
transformation. Where the commons is already well regulated, enclosure is more likely to
draw labor back into agriculture than to release it.

This follows directly from the above, but its implications have not been worked through. It
is stated here as a lead, not a result.

## 6. Socially optimal enclosure with manufacturing

The planner chooses $(T_e, L_e, L_m)$ to maximise

$$
\theta F(T_e,L_e) + F(\bar T - T_e,\ \bar L - L_m - L_e) + p\,G(\bar K, L_m) - c\,T_e
$$

and equates marginal value products across all three sectors, $p\,MPL_m = MPL_e = MPL_u$.
The contrast with the decentralized economy is the same one as in the benchmark model: the
private economy equates the enclosed sector's marginal product to the unenclosed sector's
*average* product. The extra sector does not introduce a new distortion — it gives the
existing one another margin to act on.

## 7. Status and open questions

- The manufacturing price $p$ is exogenous. Endogenising it is the obvious next step and
  could overturn the partial-equilibrium comparative statics in §5.
- The planner/private distinction enters only through $\mu$ in $\Lambda_\mu$; a full
  welfare comparison with manufacturing has not been done.
- The equilibrium enclosure rate $t_e$ itself is taken as given throughout this page.
  Closing that loop — deriving $t_e$ under decentralized enclosure *with* a manufacturing
  outside option — is what would make this a paper rather than an extension.

The code behind every figure here is in `enclose/manufacturing.py`, with the uniqueness
property, the $\beta=\alpha$ closed form and the $\theta_H$ reversal all pinned by tests in
`tests/test_manufacturing.py`.
