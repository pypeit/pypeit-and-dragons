# Let us reduce the data with PypeIt

## Raw Data

I have downloaded the raw files from `https://archive.gemini.edu/searchform/defaults/GMOS-S/night=20181005/GS-2018B-Q-133-57` 
and have put them in `/mnt/tank/Astronomy/PypeIt/DRAGONS/Raw`

## PypeIt

You can find all you need to know about PypeIt at their readthedocs page:

https://pypeit.readthedocs.io/en/stable/


## Reduce

Perform all of your work in the conda environment named `pypeit_dragons`

### Tasks

1. Do the following as best you can.  If you get stuck, ask questions in Q&A:

    - Create a new conda environement named `pypeit_dragons`
    - Install PypeIt with pip in the `pypeit_dragons` environment
    - Reduce the Gemini data in `/mnt/tank/Astronomy/PypeIt/DRAGONS/Raw` with PypeIt
    - Generate a Report file named `PypeIt_reduction.md` in `pypeit-and-dragons/Reports`.  Include:
       - The steps you took
       - How they went
       - An investigation of the quality of the reduction.  Include figures
    - Log your work

### Q&A

## Prompts

1. Execute the first task under Reduce/Tasks.   

## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs

### 2026-06-26 (PypeIt reduction of GMOS-S FRB180924 longslit data)

Executed the first task under Reduce/Tasks end-to-end.

**Environment.** Created conda env `pypeit_dragons` (Python 3.12) and
`pip install pypeit` → **PypeIt 2.0.1**. Gotcha: the user's shell profile
auto-activates an existing `pypeit` env, so a plain `conda activate
pypeit_dragons && pip ...` actually installed into the wrong env. Fixed by
calling the env's absolute pip (`/home/xavier/miniconda3/envs/pypeit_dragons/bin/pip`).
Also: running from the PypeIt **source checkout** dir shadows the installed
package, so all reduction commands were run from the working dir
`/mnt/tank/Astronomy/PypeIt/DRAGONS/PypeIt`.

**Data.** 8 archive frames (GS-2018B-Q-133, 2018-10-05), all md5-verified,
decompressed `.fits.bz2` → `.fits` into `raw/`. Configuration: GMOS-S R400,
λc=700nm, GG455, 1.0″ slit, 2×2 binning. Content: 4×700 s science (FRB180924),
2 GCAL flats, 2 CuAr arcs. **No biases, no standard star.**

**Reduction.** `pypeit_setup -s gemini_gmos_south_ham` typed all frames
correctly automatically. First `run_pypeit` aborted: `No frames of type=bias
... use_biasimage`. Fix = add `[baseprocess]\n use_biasimage = False` so GMOS
uses overscan. Re-run finished clean (exit 0), producing spec1d+spec2d for all
4 science frames (3-CCD mosaic MSC01, 1 object each on slit 258).

**Quality (all excellent/expected).** Wavelength RMS 0.110 px (~0.16 Å @
1.500 Å/pix), tilt RMS 0.034 px; coverage ~4600–9300 Å. Object S/N ≈ 5 per
frame at consistent spat≈263; inverse-variance coadd S/N ≈ 10. Clear emission
line near ~8650 Å (plausibly Hα at the host z≈0.32). Sky subtraction flat
except residuals at chip gaps / bright sky lines.

**Deliverables.** Wrote `Reports/PypeIt_reduction.md` with 4 figures in
`Reports/figs/` (1D extraction+coadd, 2D sky-subtracted, wavelength 1D fit,
object-finding profile). Figure scripts: `make_figs.py`, `make_fig2d.py` in the
working dir. Lesson learned for figures: `Spec2DObj.bpmmask` is an
`ImageBitMaskArray` — good pixels are `bpmmask.mask == 0` (the `.mask` attribute
is the *integer* bitmask, not a bool; `~` on it gives garbage).

**Not done (no data for it):** flux calibration (no standard star) and PypeIt's
formal coadd — noted as next steps in the report. Per CLAUDE.md, did not run any
git commands.