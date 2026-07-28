# Archive

Superseded material, kept for provenance. Nothing here is part of the site — the project's
table of contents in `myst.yml` lists pages explicitly, so files in this directory are not
published.

## `Model_Construction.ipynb`

The original working notebook: 92 cells (69 markdown, 23 code) in which the model was
actually worked out. It was the site's "Model Construction" page until July 2026.

It was retired because it was a research scratchpad rather than a document — it opens
mid-derivation, follows the order things were discovered rather than the paper's argument,
and trails off unfinished. It also rendered its own baked-in cell outputs, so the figures it
displayed could not be updated without re-executing it by hand.

Where its content went:

| Notebook content | Now |
|---|---|
| The derivation narrative (markdown cells) | `content/01-model.md`, reorganised into the paper's order |
| Figure-producing cells 26, 36, 45, 47, 91 | `enclose/figures.py`, one function per figure |
| The sympy derivations (cells 4–23, 38–43) | `enclose/symbolic.py`, which now also verifies the numeric layer |
| `safe_log_power`, `style_axes`, `common_labels`, `fill_between_sorted` (cell 91) | `enclose/style.py` |
| Cells 85–87 | Dropped — unfinished notes to self ("what to do next?") |

Cells 88–90 were *not* dropped despite sitting after that unfinished passage: they contain
the τ-extended global-games derivation that `loci.ln_gg(th, tau)` and panel (b) of
`trajectories.png` rest on.
