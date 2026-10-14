# Roadmap: the path to the openabel Target

This is the path, not the code. Each milestone says what you learn, what you build, and how you know it works. Pick one and open a pull request. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## Session 4: Choose the smoothing from the photo alone

**You will learn:** Generalised cross-validation or the discrepancy principle: picking lam without knowing the truth.

**You will build:** A function that selects lam from a single noisy photo, replacing the grid search that peeks at the true profile.

**Checkpoint (not met by the shipped code):** On the 3 percent noise candle photo, a truth-free choice keeps the worst-row error at or below 0.05 for 20 different noise draws (the shipped project picks lam by comparing with the truth).

**Difficulty:** intermediate

## Session 5: Find the flame axis

**You will learn:** Estimating the symmetry axis from the photo (centroid, or matching left and right halves).

**You will build:** An axis finder with sub-pixel accuracy, used before the inversion.

**Checkpoint (not met by the shipped code):** With the true axis shifted by 1 pixel (0.15 mm) the worst-row error stays at or below 0.045 (the shipped code, which assumes a known axis, gives 0.064 at lam = 3).

**Difficulty:** intermediate

## Session 6: Use both sides and neighbouring rows

**You will learn:** Averaging the left and right halves and smoothing along the flame height before inverting.

**You will build:** A whole-image inversion of all 20 rows with less noise than row-by-row inversion.

**Checkpoint (not met by the shipped code):** RMS error over the full 20-row slice at or below 0.025 of the peak at 3 percent noise (the shipped row-by-row inversion gives 0.039 at lam = 3).

**Difficulty:** advanced

## Session 7: Keep the hollow base hollow

**You will learn:** Constraints (non-negative emission) and penalties that preserve sharp structure better than a second-difference penalty.

**You will build:** An inversion that keeps the dark core of the candle base without negative values.

**Checkpoint (not met by the shipped code):** At z = 4 mm the recovered axis-to-peak ratio is within 0.03 of the true value 0.60 and no emission is negative (the shipped smoothed row gives 0.66 and small negative values appear for heavy smoothing).

**Difficulty:** advanced

## Session 8: Render it in 3D and animate

**You will learn:** Spinning an axisymmetric slice into a 3D volume and showing a cut-away.

**You will build:** A looping 3D cut-away animation of the recovered flame.

**Checkpoint (not met by the shipped code):** A 48-frame loop of one full turn whose first and last frames differ by less than 1e-6 and whose title shows the RMS error against the true emission.

**Difficulty:** advanced

## The final step

Combine the milestones: from one noisy side-view photo, find the axis, choose the smoothing automatically, invert the whole image and render a rotating 3D cut-away of the flame. If your result looks like the Target animation, open a pull request and tell us how you did it.
