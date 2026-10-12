# Let us compare the PypeIt and DRAGONS reductions

## Goals

We will first generate a doc to plan the analysis of the PypeIt and DRAGONS outputs
and generate a report comparing the two.  We will then execute that plan.

## Context

1. The prompt docs in this folder
2. The Reports in `PypeIt/pypeit-and-dragons/Reports/`

## Prompts

1. Perform the 1st task under Plan/Tasks.

## Plan


### Tasks

1. Examine the existing prompt docs, Reports, and also the folders of reduction outputs for PypeIt and
DRAGONS.  Our next goal is to quantitatively compare the two sets of outputs. Do the following:
   - Compare the 1D stacked science spectra
   - Compare the 2D stacked science spectra
   - Examine the S/N for each output spectrum
   - Compare the wavelength solutions
   - Compare the response curves 
   - Provide any other comparions you think are relevant
   - Log your work

### Q&A

**Context gathered (2026-06-27).** I examined the prompt docs, both Reports, and
the on-disk reduction outputs:

- **PypeIt** (`…/DRAGONS/PypeIt/gemini_gmos_south_ham_A/`): 4 individual
  `spec1d_*.fits` (OPT + BOX extractions, counts, 3134-pix grid ≈1.50 Å/pix) and
  4 individual `spec2d_*.fits` (3-CCD mosaic). **No formal coadd product** — the
  Report's combined 1D was a quick inverse-variance average inside `make_figs.py`.
  Calibrations: WaveCalib, Flat, Tilts, Edges/Slits.
- **DRAGONS** (`…/DRAGONS/DRAGONS/`): a single **stacked** `S20181005S0079_1D.fits`
  (6 apertures, SCI/VAR/DQ each, electrons, 3254-pix grid ≈1.45 Å/pix) and
  `S20181005S0079_2D.fits` (stacked). Processed bias/flat/arc in `calibrations/`.

**Implications for a quantitative comparison:**

1. **Product asymmetry.** DRAGONS delivers one stacked 1D/2D; PypeIt delivers four
   per-frame products + a quick (non-canonical) combine. A fair single-spectrum
   comparison needs a matched PypeIt coadd (`pypeit_coadd_1dspec`).
2. **Different wavelength grids/sampling** (3134 vs 3254 pix; 1.50 vs 1.45 Å/pix)
   → must resample to a common grid before differencing/ratioing.
3. **No flux calibration in either** and different count units (per-frame counts
   vs stacked electrons) → flux comparison only meaningful after normalization;
   absolute throughput not directly comparable.
4. **Wavelength reference frame may differ.** PypeIt applied heliocentric +
   spectral-flexure corrections; DRAGONS's frame/alignment must be checked. The
   known headline difference is the default wavelength-solution RMS (0.16 Å vs
   ~8 Å). Independent sky emission lines in the data are the natural ground truth.

**Candidate comparison axes** (to be prioritized per answers below): wavelength
solution accuracy (sky-line centroids), 1D spectral-shape agreement after
resampling+normalization (ratio/difference, cross-correlation lag), per-pixel and
median S/N, object spatial position / trace / FWHM, spectral resolution (line
FWHM), telluric A-band, and optionally calibration-frame (flat/bias) comparison.

**Questions for the user (Q → user):**

1. **PypeIt coadd.** Should I run PypeIt's formal `pypeit_coadd_1dspec` (and
   possibly `pypeit_coadd_2dspec`) so there is a single stacked PypeIt spectrum to
   compare against DRAGONS's stack? (My recommendation: yes — it is the only
   apples-to-apples option. It is a reduction step, not a git operation.)
2. **Scope.** How wide should the comparison be: (a) 1D extracted spectrum only;
   (b) 1D + 2D + wavelength solution; (c) full — also flats/bias/throughput?
3. **Wavelength alignment.** When comparing the 1D spectra, should I first
   cross-correlate and remove any overall wavelength offset (compare *shapes*), or
   keep them on their native solutions to *expose* absolute wavelength differences
   (relevant to the 8 Å vs 0.16 Å gap)? I propose: report the measured offset,
   then also overlay shape-aligned.
4. **Deliverable & code home.** Output a new `Reports/PypeIt_vs_DRAGONS.md` +
   figures in `Reports/figs/`. Should the comparison code live as a reusable
   module under `pypeit_and_dragons/` with a pytest (the repo has `setup.py` /
   `pytest.ini`), or as a standalone analysis script?

## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs

### 2026-06-27 (Planning the PypeIt-vs-DRAGONS quantitative comparison)

Executed Task 1: examined the prompt docs, both Reports, and the on-disk
reduction outputs for each pipeline, then posed questions (see Q&A above).

What I learned by inspecting the products directly (not just the Reports):

- **PypeIt** outputs are **per-frame**: 4 `spec1d_*.fits` (each with OPT + BOX
  extraction columns: `OPT_WAVE`, `OPT_COUNTS`, `OPT_COUNTS_IVAR`, …, on a
  3134-pix grid ≈1.50 Å/pix) and 4 `spec2d_*.fits` mosaics. There is **no formal
  coadd** on disk — the Report's "combined" 1D was a quick inverse-variance
  average computed inside `make_figs.py`.
- **DRAGONS** outputs are a **single stack**: `S20181005S0079_1D.fits` holds 6
  apertures as SCI/VAR/DQ image triplets (aperture 1 = target, in electrons, on a
  3254-pix grid ≈1.45 Å/pix) and `S20181005S0079_2D.fits` is the stacked 2-D.

Key consequences for a *quantitative* comparison, and why each drives a question:
(1) the products are asymmetric (4 per-frame vs 1 stacked) → need a matched
PypeIt coadd; (2) different wavelength grids/sampling → resample to a common grid;
(3) no flux cal + different count units → compare only after normalization;
(4) possibly different wavelength reference frames + the known 0.16 Å vs ~8 Å
default-RMS gap → sky emission lines are the natural independent ground truth.

No reductions were re-run and nothing was modified beyond this prompt doc.
Awaiting answers to the four Q&A questions before building the comparison.
