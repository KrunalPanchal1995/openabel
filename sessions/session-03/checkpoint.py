"""Checkpoint for Session 3. Prints PASS or FAIL."""
import numpy as np


def run_checks(L):
    """L is the lesson module (or notebook namespace). Returns a list of (label, passed)."""
    checks = []
    # worked example: three rings, R = 3 mm, measured I = (12, 9.121, 4.472)
    got = L.onion_peel(np.array([12.0, 9.121, 4.472]), 3.0)
    checks.append((f"worked example: onion peeling of (12, 9.121, 4.472) gives eps = (3, 2, 1) (got {np.round(got, 2)})",
                   np.allclose(got, [3.0, 2.0, 1.0], atol=0.01)))
    W = L.ring_matrix(3, 3.0)
    checks.append(("worked example: forward model of eps = (3, 2, 1) gives I = (12, 9.121, 4.472)",
                   np.allclose(W @ np.array([3.0, 2.0, 1.0]), [12.0, 9.1206, 4.4721], atol=1e-3)))
    # exact pair, no noise
    N = 40
    r = L.radii(N)
    truth = L.gauss_eps(r, 1.0)
    e0 = L.onion_peel(L.photo_profile(lambda q: L.gauss_eps(q, 1.0), N))
    err = float(np.max(np.abs(e0 - truth)))
    checks.append((f"exact pair: noise-free onion peeling recovers the Gaussian to within 0.02 of its peak (worst {err:.3f})", err < 0.02))
    checks.append(("edge case: an all-zero photo gives zero emission", np.allclose(L.onion_peel(np.zeros(10)), 0.0) and np.allclose(L.smooth_invert(np.zeros(10), 0.5), 0.0)))
    I0 = L.photo_profile(lambda q: L.gauss_eps(q, 1.0), 20)
    checks.append(("lam = 0 smoothing equals onion peeling", np.allclose(L.smooth_invert(I0, 0.0), L.onion_peel(I0), atol=1e-5)))
    # noise gain
    g = L.noise_gain(N)
    checks.append((f"noise gain is largest at the axis: {g[0]:.1f} per mm there against {g[-1]:.2f} per mm at the edge", g[0] > 5 * g[-1] and g[0] > 5.0))
    rng = np.random.default_rng(0)
    Winv = np.linalg.inv(L.ring_matrix(N))
    sim = np.std(np.array([Winv @ rng.standard_normal(N) for _ in range(4000)]), axis=0)
    checks.append(("measured noise in ring 0 matches the predicted gain within 10%", abs(sim[0] / g[0] - 1) < 0.10))
    # bias / noise trade-off
    gauss = lambda q: L.gauss_eps(q, 1.0)
    lo = L.bias_noise_total(gauss, 40, 1e-4, 0.01, 60)
    mid = L.bias_noise_total(gauss, 40, 0.5, 0.01, 60)
    hi = L.bias_noise_total(gauss, 40, 30.0, 0.01, 60)
    checks.append(("more smoothing: bias rises (%.3f < %.3f < %.3f)" % (lo[0], mid[0], hi[0]), lo[0] < mid[0] < hi[0]))
    checks.append(("more smoothing: noise falls (%.3f > %.3f > %.3f)" % (lo[1], mid[1], hi[1]), lo[1] > mid[1] > hi[1]))
    checks.append(("there is a best smoothing in between: total error is smallest at lam = 0.5", mid[2] < lo[2] and mid[2] < hi[2]))
    checks.append((f"smoothing helps: 1% noise total error {lo[2]:.3f} (lam ~ 0) falls to {mid[2]:.3f}", mid[2] < lo[2] / 2))
    ex = L.bias_noise_exact(gauss, 40, 0.5, 0.01)
    checks.append(("the exact (no random draws) bias and noise agree with the Monte Carlo values within 15%",
                   abs(ex[0] / mid[0] - 1) < 0.15 and abs(ex[1] / mid[1] - 1) < 0.15))
    # design check: ring flame, 1% noise, three smoothing strengths
    ringg = lambda q: L.ring_eps(q, 1.5, 0.4)
    tot = [L.bias_noise_exact(ringg, 40, lam, 0.01)[2] for lam in (0.01, 0.1, 10.0)]
    checks.append(("design: ring flame at 1% noise, total error for lam = 0.01, 0.1, 10 is about 2.7%, 2.0%, 7.7% (best: 0.1)",
                   [round(100 * t, 1) for t in tot] == [2.7, 2.0, 7.7]))
    tot3 = [L.bias_noise_exact(gauss, 40, lam, 0.03)[2] for lam in (0.316, 1.0, 3.16)]
    checks.append(("design: Gaussian at 3% noise stays below 2.5% total error for lam >= 1 but not at lam = 0.3",
                   tot3[0] > 0.025 > max(tot3[1], tot3[2])))
    # limit case: over-smoothing fills the hole of a ring-shaped flame
    ringf = lambda q: L.ring_eps(q, 1.5, 0.4)
    Ir = L.photo_profile(ringf, 40)
    hole_ok = float(L.smooth_invert(Ir, 1e-4)[0])
    hole_bad = float(L.smooth_invert(Ir, 30.0)[0])
    checks.append((f"limit: heavy smoothing corrupts the dark hole of a ring flame (axis value {hole_ok:.2f} -> {hole_bad:.2f}, negative light is unphysical)", abs(hole_ok) < 0.05 and abs(hole_bad) > 0.2))
    # mini-project
    img = L.candle_photo(N=40, frac=0.03)
    worst = {lam: L.worst_row_error(img, lam) for lam in L.LAM_GRID}
    best = min(worst, key=worst.get)
    checks.append((f"mini-project: onion peeling on the 3% noise photo has a worst-row error above 0.25 (got {worst[0.0]:.3f})", worst[0.0] > 0.25))
    checks.append((f"mini-project: smallest worst-row error is at lam = 3 and is below 0.05 (got lam = {best}, {worst[best]:.3f})", best == 3.0 and worst[best] < 0.05))
    checks.append(("mini-project: the candle is hollow at z = 4 mm and filled at z = 12 mm",
                   float(L.candle_emission(0.0, 4)) < 0.6 * float(L.candle_emission(1.2, 4)) and float(L.candle_emission(0.0, 12)) == max(L.candle_emission(np.linspace(0, 5, 100), 12))))
    return checks


# --- runner ---
if __name__ == "__main__":
    import importlib.util
    import pathlib
    import sys

    path = pathlib.Path(__file__).resolve().parent / "lesson.py"
    spec = importlib.util.spec_from_file_location("lesson3", path)
    lesson = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lesson)
    ok = True
    for label, passed in run_checks(lesson):
        print(("PASS  " if passed else "FAIL  ") + label)
        ok &= bool(passed)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
