r"""Pure-numpy numeric helpers shared by the model and locus layers.

This module exists to keep the *computation* path free of matplotlib. `safe_log_power` lived
in `enclose.style` until 2026-07-29, which meant `import enclose.loci` pulled in
`matplotlib.patches` transitively and no locus could be evaluated without a plotting stack.
That is load-bearing under Pyodide, where matplotlib is a large download the explore page
should not pay for just to evaluate a curve. `tests/test_imports.py` guards the property.

Nothing here may import matplotlib.
"""

import numpy as np


def safe_log_power(expr, power=1.0, shift=0.0):
    """Return log((expr)**power) + shift, masking expr<=0 as NaN.

    Every locus has the form l_bar = [expr]^(1/alpha), where expr changes sign as theta
    crosses 1 or 1/alpha. This lets one theta grid carry every curve instead of hand-slicing
    the domain into pieces per branch.

    `shift` is also how the small hand-tuned offsets in the monopoly and comparison figures
    (previously buried literals like `- .03`) are applied — see the named constants in
    `enclose.figures`.
    """
    expr = np.asarray(expr, dtype=float)
    out = np.full_like(expr, np.nan, dtype=float)
    mask = np.isfinite(expr) & (expr > 0)
    out[mask] = np.log(expr[mask]**power) + shift
    return out
