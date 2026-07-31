"""Model code for "A Model of Enclosures" (Baker and Conning).

- `enclose.model` — pure economics (numpy only): Lambda, le, req, weq, z, teopt, ...
- `enclose.numerics` — pure-numpy helpers shared by model and loci (safe_log_power).
- `enclose.loci` — named, equation-tagged boundary loci, including the tau-extended ones.
- `enclose.style` — shared plotting conventions (colors, hatching, axis cosmetics).
- `enclose.figures` — one function per paper figure.

`model`, `numerics` and `loci` are matplotlib-free by design, so the computation path can run
under Pyodide without a plotting stack. See `tests/test_imports.py`.
"""

__version__ = "0.1.0"
