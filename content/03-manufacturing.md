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

Labor moves until it earns the same everywhere, $w = p\,MPL_m = \theta\,MPL_e = w_u$. Under
open access the last of these is the commons *average* product, $w_u = APL_u$; under perfect
regulation it is the marginal product, $\alpha \cdot APL_u$. In general labor takes home the
fraction

$$
A_\mu = 1 - \mu(1-\alpha)
$$

of the average product — its marginal product $\alpha\,APL_u$, plus the share $(1-\mu)$ of
possession rents it still captures, $(1-\mu)(1-\alpha)\,APL_u$. So $A_0 = 1$ and
$A_1 = \alpha$. Writing the two sides of the manufacturing/agriculture margin:

$$
\underbrace{p \beta \bar k^{1-\beta}}_{C_m}\, l_m^{-(1-\beta)}
\;=\;
\underbrace{A_\mu\,\bar t^{1-\alpha}\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}}_{C_a}\,
(1-l_m)^{-(1-\alpha)}
$$

:::{warning} $\mu$ enters twice, and in opposite directions
$\Lambda_\mu$ carries the governance parameter into the *slope* of the agricultural
allocation, but $A_\mu$ carries it into the *level* of what labor earns — and the two push
$l_m$ opposite ways. It is easy to keep only the first: substituting $l_e^\mu(t_e)$ back
into the agricultural return gives a factor $\alpha\theta\Lambda_\mu^{-(1-\alpha)}$, which
equals exactly $1$ at $\mu=0$ and so *looks* like it can be dropped. It equals $A_\mu$ in
general, and $\alpha$ at $\mu=1$. Dropping it inflates the planner's agricultural labor
demand by $1/\alpha$ and inverts the welfare comparison in §4.
:::

$MPL_m$ falls in $l_m$ and the agricultural return rises in it, so **the two cross exactly once**: the
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
$\beta=0.7$. Left: no land enclosed — the two agricultural curves stand in the ratio
$\alpha$, since open access pays labor the commons average product and a planner its
marginal product. Right: all land enclosed — the curves *coincide*, because there is no
commons left for governance to apply to. The decentralized share moves from $l_m=0.20$ to
$l_m=0.68$; the planner's sits at $0.68$ throughout.
```

Two facts about the right-hand panel generalise beyond this example. At $t_e=1$ there is no
commons, so every worker is paid a marginal product whatever $\mu$ was, and
$C_a = \alpha\theta\,\bar t^{1-\alpha}$ regardless. Hence:

> **Full enclosure implements the planner's inter-sectoral allocation, for any $\theta$** —
> *conditional on $t_e$*. It does not follow that full enclosure is first best; see §5.

What varies with $\theta$ is *where* that allocation is, not whether enclosure reaches it.

So the decentralized economy does shift nearly half its workforce into manufacturing, and
the shift owes nothing to productivity: $\theta=1$ by construction. But it is not a shift
*away* from the optimum. The unenclosed economy was the misallocated one, holding labor on
the land because the commons paid average rather than marginal product; enclosure removes
that wedge and closes the gap exactly. Decentralized output rises 13.0% between the two
panels, purely from reallocation.

Planner output, meanwhile, is *identical* in the two panels — 1.397 either way. That is the
tell, and §5 makes it the argument: at $\theta=1$ enclosure buys a planner nothing at all.
Everything it achieves here is the repair of a distortion, and repairs have alternatives.

The equilibrium wage nonetheless falls, from 1.14 to 0.79 — the Weitzman–Samuelson effect.
It is worth being precise about what those two numbers are. At $t_e=0$ labor captures the
whole average product of the commons; at $t_e=1$ it is paid a marginal product. The fall is
a change in *which of the two* labor receives, not a fall in anyone's productivity. Output
and labor's share move in opposite directions here, and the distributional loss is real —
but it is not evidence that the inter-sectoral allocation got worse.

None of this is a welfare verdict on enclosure. What the example establishes is narrower:
at this margin, in this case, the harm is not misallocation between agriculture and
industry. §5 takes up the verdict itself.

## 5. Is enclosure worth its cost?

§4 held $t_e$ fixed and asked how labor is allocated. The planner also *chooses* $t_e$, and
that is a different margin with a different threshold. Adding it back:

$$
\max_{t_e}\ Y(t_e) - c\,\bar T\,t_e
$$

By the envelope theorem the labor-reallocation terms vanish — the planner has already
equalised marginal products, so shifting labor has no first-order effect — and all that
survives is the land-rent differential $\theta F_T^e - F_T^u$:

$$
\frac{dY}{dt_e}
= (1-\alpha)\,\bar t^{1-\alpha}\,(\Lambda_o - 1)
  \left(\frac{1-l_m(t_e)}{1+(\Lambda_o-1)t_e}\right)^{\alpha}
$$

This is the benchmark model's $z'(t_e)$ with the *agricultural* labor share $(1-l_m)$ in
place of the whole labor force. Manufacturing changes the level and not the structure — and
in particular not the sign, which is the sign of $(\Lambda_o - 1)$, that is, of
$(\theta - 1)$.

:::{important} Two thresholds, easily confused
The labor-allocation reversal of §6 turns at $\theta_H^\mu$, and involves $\Lambda_\mu$.
This margin turns at $\theta = 1$, and involves $\Lambda_o$. They are different questions:
*which way does enclosure push labor* versus *is enclosure worth doing*.
:::

So:

| $\theta$ | $dY/dt_e$ | planner's $t_e^o$ |
|:---|:---|:---|
| $<1$ | negative — enclosure lowers output even at $c=0$ | $0$ |
| $=1$ | exactly zero at every $t_e$ | $0$ for any $c>0$ |
| $>1$ | positive | encloses while $dY/dt_e > c\,\bar t$ |

**Full enclosure is first best only when $\theta > 1$ and $c$ is small enough.** For
$\theta \le 1$ the planner does not enclose at all, no matter how badly the decentralized
economy is misallocating labor at $t_e = 0$. The §4 result — that full enclosure reaches
the planner's *labor* allocation — is a statement about one margin, and does not carry to
the other.

### Enclosure as a second-best instrument

The $\theta=1$ case makes the distinction sharp. Three allocations, at $\alpha=0.4$,
$\beta=0.7$:

| | output |
|:---|---:|
| decentralized, no enclosure ($\mu=0$, $t_e=0$) | 1.236 |
| decentralized, full enclosure ($\mu=0$, $t_e=1$) | 1.397 $-\ c\bar T$ |
| **regulated commons, no enclosure ($\mu=1$, $t_e=0$)** | **1.397** |

Enclosure closes the entire 0.161 gap — and so does regulating the commons, at $t_e=0$, for
no enclosure cost at all. Enclosure is a *second-best* instrument here: it fixes the labor
misallocation by abolishing the institution that caused it, which works, but pays $c\bar T$
for what governance would deliver directly. It beats doing nothing only while
$c\bar T < 0.161$, and it never beats fixing the commons.

That is the reading the model actually supports, and it is not the enclosure-friendly one.
Where enclosure raises output without raising productivity, it is substituting for an
institutional reform, not accomplishing something reform could not.

### Below $\theta = 1$

For $\theta<1$ enclosure destroys land productivity as well as costing $c$, so the planner's
answer is immediate. The decentralized economy is more interesting: the commons distortion
is large enough that full enclosure *still* raises output for a range of $\theta$ below one
— down to $\theta \approx 0.73$ at these parameters — before the productivity loss
overwhelms it. So there is a band, roughly $0.73 < \theta \le 1$, where enclosure raises
decentralized output, lowers planner output, and is worth doing only if both $c$ is small
*and* commons governance is unavailable.

Unlike $\theta_H$, that lower crossover is **not** a clean knife-edge: it moves with
$\alpha$, $\beta$ and $p$ (0.73 at $\alpha=0.4,\beta=0.7,p=1$; 0.89 at
$\alpha=\beta=0.5$; 0.42 at $p=2$). It is a numerical feature of the example, not a
result.

## 6. The effect reverses at $\theta_H$

The example above is not general — and the direction in which it generalises is the
substantive finding on this page.

$C_a$ carries the factor $\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}$, so the sign of
$\partial l_m/\partial t_e$ is simply the sign of $(1 - \Lambda_\mu)$ — note the inversion:
the equilibrium condition's left side rises in $l_m$, so $l_m$ rises exactly when $C_a$
*falls*. (This is the reverse of §5's enclosure margin, which does carry the sign of
$(\Lambda_o-1)$ directly. Two margins, two signs.) The wedge $A_\mu$
does not interfere: it contains neither $t_e$ nor $l_m$, so it moves the level of
agricultural labor demand without touching its slope, and the result below holds for every
$\mu$. And $\Lambda_\mu = 1$ holds exactly at

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

## 7. Socially optimal enclosure with manufacturing

The planner chooses $(T_e, L_e, L_m)$ to maximise

$$
\theta F(T_e,L_e) + F(\bar T - T_e,\ \bar L - L_m - L_e) + p\,G(\bar K, L_m) - c\,T_e
$$

The two labor first-order conditions equate marginal value products across all three
sectors, $p\,MPL_m = \theta\,MPL_e = MPL_u$. The first gives back the benchmark planner's
reaction function scaled by $(1-l_m)$, with $\Lambda_o = \theta^{1/(1-\alpha)}$; the second,
after substituting it, gives the agricultural side of the manufacturing margin as the
general expression of §3 evaluated at $\mu=1$, where $A_1 = \alpha$. Both derivations are in
[online appendix](04-derivations.md) §6.4, equations (36) and (38).

That leading $\alpha$ is not decoration. Without it the planner's labor demand is overstated
by $1/\alpha$, the two curves in the §4 figure coincide in the *left* panel instead of the
right, and the comparison in §4 comes out backwards.

The third first-order condition, in $T_e$, is the enclosure margin — that is §5, where the
envelope theorem reduces it to the land-rent differential alone.

The contrast with the decentralized economy is the same one as in the benchmark model: the
private economy equates the enclosed sector's marginal product to the unenclosed sector's
*average* product. The extra sector does not introduce a new distortion — it gives the
existing one another margin to act on, and, as §4 shows, one that full enclosure happens to
close. Whether closing it *that way* is worth doing is the separate question §5 answers,
and usually the answer is no.

## 8. Status and open questions

- The manufacturing price $p$ is exogenous. Endogenising it is the obvious next step and
  could overturn the partial-equilibrium comparative statics in §6.
- §5 compares output, not welfare. It takes no view on the distributional shift from
  average- to marginal-product pay, which §4 shows moves opposite to output. Any actual
  welfare statement needs a weight on that, and this page does not supply one.
- §5 derives the *planner's* $t_e$. The **decentralized** $t_e$ is still taken as given —
  closing that loop, with enclosers responding to a manufacturing outside option, is what
  would make this a paper rather than an extension. Expect the enclosure loci to move, since
  the outside option changes what the commons is worth.
- §5's second-best reading invites the obvious follow-up: if governance ($\mu$) and
  enclosure ($t_e$) are both costly instruments for the same distortion, what does the
  trade-off between them look like? The appendix's $\tau$ belongs in that comparison too.
- Whether enclosure raises *measured* aggregate TFP is worth computing explicitly. §4
  suggests much of any such gain is composition: labor moving from a low-average-product
  commons into manufacturing, with no technology change anywhere.

The code behind every figure here is in `enclose/manufacturing.py`, with the uniqueness
property, the $\beta=\alpha$ closed form, the $\theta_H$ reversal, the $A_\mu$ wedge and
§5's enclosure margin (`planner_marginal_benefit`, `total_output`) all pinned by tests in
`tests/test_manufacturing.py` — the wedge by checking the planner's first-order conditions
against the primitive derivatives of the objective above, the enclosure margin against a
numerical derivative of the value function.
