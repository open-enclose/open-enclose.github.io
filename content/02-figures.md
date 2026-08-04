---
title: Reproducing the Paper's Figures
short_title: Figures
---

# Reproducing the Paper's Figures

Every figure in the paper is produced by one function call. This page is deliberately thin —
that it *can* be thin is the point. The model code lives in
[`enclose`](https://github.com/open-enclose/open-enclose.github.io/tree/main/enclose), not
scattered across notebook cells, so reproducing a figure takes a line rather than a
transcription.

## Getting set up

```bash
git clone https://github.com/open-enclose/open-enclose.github.io
cd open-enclose.github.io
pip install -e ".[dev]"
```

To regenerate everything at once:

```bash
python scripts/make_figures.py --outdir Figures
```

That single command writes all seven paper figures plus the four explanatory figures used
elsewhere on this site. It runs in CI on every push, immediately before the site build, so
the figures published here cannot drift from the code that generates them.

## The paper's figures

Each returns a matplotlib `(fig, ax)`; nothing is written to disk unless you save it.

All seven, in the order the paper prints them:

```python
from enclose import figures

fig, ax = figures.social_optimum(cond_opt=False)     # Fig. 1  social_optimum.png
fig, ax = figures.nash_equilibrium(full_diag=False)  # Fig. 2  nash_eq.png
fig, ax = figures.nash_equilibrium(full_diag=True)   # Fig. 3  nash_so_comp.png
fig, ax = figures.social_optimum(cond_opt=True)      # Fig. 4  social_opt_cond.png
fig, ax = figures.comparison()                       # Fig. 5  comparison.png
fig, ax = figures.combined_4x4()                     # Fig. 6  new_comp_fig4x4.png
fig, ax = figures.monopoly()                         # Fig. 7  monopoly.png
```

The `\label` is carried alongside the number because numbers renumber when a figure is
added or moved, and labels do not — if the two ever disagree, trust the label.

| Paper | `\label` | Function | Output | Paper section |
|:---|:---|:---|:---|:---|
| Fig. 1 | `fig-social` | `social_optimum(cond_opt=False)` | `social_optimum.png` | §3.2, Lemma 1 |
| Fig. 2 | `figure_private` | `nash_equilibrium(full_diag=False)` | `nash_eq.png` | §3.3, Props 2–3 |
| Fig. 3 | `fig_compare` | `nash_equilibrium(full_diag=True)` | `nash_so_comp.png` | §4 |
| Fig. 4 | `fig-social-cond` | `social_optimum(cond_opt=True)` | `social_opt_cond.png` | §4.1 |
| Fig. 5 | `figure5` | `comparison()` | `comparison.png` | §4.1 |
| Fig. 6 | `figure4x4` | `combined_4x4()` | `new_comp_fig4x4.png` | §5.4 |
| Fig. 7 | `figure7` | `monopoly()` | `monopoly.png` | §6.3 |

Verified against `main.tex` by `scripts/check_figure_map.py`, which reads the figure
environments in source order — which is what determines the printed number — and compares
them with the table above.

## Explanatory figures

Four more are used on this site but appear **nowhere in the paper**. Two fill placeholders the
[Mathematical Appendix](04-derivations.md) numbers but never had generators for; two support
the [manufacturing extension](03-manufacturing.md).

```python
fig, ax = figures.labor_reaction(te=0.5, th=1.6, alp=0.5, mu=0.5)
fig, ax = figures.labor_misallocation(te=0.5, alp=0.5, th=1.5, mu=0.0)
fig, ax = figures.manufacturing_equilibrium(te_values=(0.0, 1.0), th=1.0, alp=0.4, b=0.7)
fig, ax = figures.structural_transformation(alp=0.5, mu=0.0, b=0.5)
```

## Changing the parameters

Everything is keyword-driven, so exploring is a matter of passing different values. All the
paper's diagrams are drawn at $\alpha = 2/3$ and $c/A = 1$; the loci carry those as
defaults.

```python
from enclose import loci
import numpy as np

theta = np.linspace(1.1, 2.1, 200)
loci.ln_l01(theta)                 # first-best no-enclosure locus, eq. (6)
loci.ln_ld0(theta, tau=0.5)        # decentralized, with partial compensation
loci.ln_ld0(theta, mu=1.0, tau=1.0)  # both wedges closed -- equals the planner's locus
loci.ln_gg(theta, tau=1.0)         # global-games locus under full compensation
```

:::{note} A note on `c` and `A`
Every locus equates a marginal benefit that scales with $A$ to a marginal cost that scales
with $c$, so the two only ever appear as the ratio $c/A$. The package therefore carries no
separate `A`, and `loci.C` **is** the paper's $c/A$. Output and welfare *levels* are
consequently in units of $A$; ratios and thresholds are unaffected.
:::

## How the figures are checked

Two mechanisms, because figures are easy to get quietly wrong:

- **The numeric layer is checked against symbolic derivations.** `enclose/symbolic.py`
  derives every locus from its objective — differentiating, integrating or comparing
  endpoints and solving for $\bar l$ — and the test suite asserts the closed forms in
  `loci.py` match. A mistranscribed formula fails the build.
- **The figures are checked against the paper's own PNGs.** The set generated here was
  compared pixel-by-pixel against the figures the published paper compiles, and agrees to
  within the axis-label wording that was deliberately standardised.

```bash
pytest tests/
```
