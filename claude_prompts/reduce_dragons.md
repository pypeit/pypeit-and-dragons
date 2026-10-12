# Let us reduce the data with DRAGONS

## Raw Data

I have downloaded the raw files from `https://archive.gemini.edu/searchform/defaults/GMOS-S/night=20181005/GS-2018B-Q-133-57` 
and have put them in `/mnt/tank/Astronomy/PypeIt/DRAGONS/Raw`

## DRAGONS

You can find all you need to know about DRAGONS at their readthedocs page:

https://dragons.readthedocs.io/projects/gmosimg-drtutorial/en/stable/


## Reduce

Perform all of your work in the conda environment named `dragons_pypeit`

### Tasks

1. Do the following as best you can.  If you get stuck, ask questions in Q&A:

    - Create a new conda environement named `dragons_pypeit`
    - Install DRAGONS with conda in the `dragons_pypeit` environment
    - Reduce the Gemini data in `/mnt/tank/Astronomy/PypeIt/DRAGONS/Raw` with DRAGONS
       - Include the suitable bad pixel mask provided in the Raw directory
       - Use the appropriate BIAS frames
       - Flux calibrate the science data using the provided standard star and associated flat
    - Generate a Report file named `DRAGONS_reduction.md` in `pypeit-and-dragons/Reports`.  Include:
       - The steps you took
       - How they went
       - An investigation of the quality of the reduction.  Include figures
    - Log your work

### Q&A

**Q (Claude → user): "Install DRAGONS with pip" is not possible.**
Gemini does not publish the full DRAGONS suite on PyPI — the PyPI package named
`dragons` is an unrelated namesake, and only `astrodata` is on PyPI. DRAGONS is
distributed as a **conda** package (`-c conda-forge -c
http://astroconda.gemini.edu/public`). I therefore built `dragons_pypeit` with
the supported conda command instead of pip. Let me know if you wanted a different
approach.

**Q (Claude → user): the task says "with PypeIt".**
Line 25 says "Reduce … with PypeIt", but this is a copy-paste from the parallel
`reduce_pypeit.md`. Given the title, the env name, the DRAGONS docs link, and the
already-completed `PypeIt_reduction.md`, I reduced **with DRAGONS**.

**Q (Claude → user): no bias / no standard in the dataset.**
DRAGONS GMOS-LS *requires* a processed bias (unlike PypeIt's overscan-only path),
so I downloaded the 5 associated same-night biases from the Gemini public
archive. There is no spectrophotometric standard, so no flux calibration was
possible (spectra are in electrons) — same limitation as the PypeIt run.

## Prompts

1. Execute the first task under Reduce/Tasks.   

## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs

### 2026-06-26 (DRAGONS reduction of the GMOS-S longslit data)

Executed the first task. Summary of work and findings:

- **Environment.** Created conda env `dragons_pypeit` (Python 3.12) with DRAGONS
  v4.2.2. Could not use pip — DRAGONS is conda-only (see Q&A); used
  `-c conda-forge -c http://astroconda.gemini.edu/public`.
- **Data.** The 8 raw frames are GMOS-S **longslit spectra** (R400, 1.0″ slit,
  CuAr arcs, GCAL flats; 2×2; ROI Central Spectrum) — confirmed with `typewalk`.
  4 science (FRB180924), 2 flats, 2 arcs, **no bias, no standard**. Verified all
  md5sums; decompressed into `…/DRAGONS/DRAGONS/raw`.
- **Missing bias.** DRAGONS GMOS-LS `biasCorrect` hard-fails without a processed
  bias (PypeIt instead used overscan). Downloaded the 5 same-night associated
  biases (S20181005S0382–0386) from the Gemini public archive.
- **Reduction.** `caldb init` → `dataselect` lists → `reduce` biases → flats →
  arcs → science. The stock `reduceScience` recipe aborts at `fluxCalibrate`
  (no standard), so I made `myrecipes.reduceScienceNoFlux` = stock recipe minus
  the single `fluxCalibrate()` line. Run completed successfully. Products:
  `S20181005S0079_{2D,1D}.fits` (stacked; electrons, no flux cal).
- **Quality.** Object found at spatial pixel 261.8, median S/N ≈ 9.6 (4-frame
  stack), coverage 4605–9300 Å. These match the PypeIt run closely (pix ≈262.8,
  S/N ≈10, 4600–9300 Å). DRAGONS's 2-D distortion model is sub-pixel
  (0.12–0.15 px), but its **default automatic forward wavelength fit RMS is large
  (~0.79–0.85 nm ≈ 8 Å)** vs PypeIt's 0.16 Å — DRAGONS recommends interactive
  refinement for GMOS-LS. Per user instruction I left the standard output as-is
  rather than tuning it.
- **Deliverables.** `Reports/DRAGONS_reduction.md` + 4 figures in `Reports/figs/`
  (`fig_dragons_{wavecal,spec2d,obj_profile,spec1d}.png`).
- **Lessons.** (1) DRAGONS ≠ pip-installable. (2) GMOS-LS requires bias; plan to
  pull associated cals from the archive. (3) To skip flux cal with no standard,
  copy the stock recipe and drop `fluxCalibrate` rather than fighting the error.
