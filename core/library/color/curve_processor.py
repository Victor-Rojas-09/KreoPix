import numpy as np


class CurveProcessor:
    """
    Build an entry LUT from control points and apply it to RGB channels.

    Control points are (x, y) in 0-255; x must be strictly increasing.
    Endpoints at x=0 and x=255 are required (inserted if missing).
    """

    @staticmethod
    def normalize_points(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Sort by x, clamp to 0-255, ensure endpoints at 0 and 255."""

        if not points:
            return [(0, 0), (255, 255)]

        cleaned = []
        for x, y in points:
            xi = int(max(0, min(255, x)))
            yi = int(max(0, min(255, y)))
            cleaned.append((xi, yi))

        cleaned.sort(key=lambda p: p[0])

        merged: list[tuple[int, int]] = []

        for p in cleaned:
            if merged and merged[-1][0] == p[0]:
                merged[-1] = p
            else:
                merged.append(p)

        if merged[0][0] != 0:
            merged.insert(0, (0, merged[0][1]))

        if merged[-1][0] != 255:
            merged.append((255, merged[-1][1]))

        return merged

    @staticmethod
    def build_lut(points: list[tuple[int, int]]) -> np.ndarray:
        """Return uint8 LUT of length 256."""

        pts = CurveProcessor.normalize_points(points)

        xs = np.array([p[0] for p in pts], dtype=np.float64)
        ys = np.array([p[1] for p in pts], dtype=np.float64)

        idx = np.arange(256, dtype=np.float64)
        lut = np.interp(idx, xs, ys)

        return np.clip(np.round(lut), 0, 255).astype(np.uint8)

    @staticmethod
    def apply_lut_to_rgb(img: np.ndarray, lut: np.ndarray) -> np.ndarray:
        """Apply the same LUT to R, G, B (uint8 HxWx3)."""

        if img.ndim != 3 or img.shape[2] < 3:
            raise ValueError("Expected RGB image (H, W, 3)")

        base = img.astype(np.uint8)
        out = np.empty_like(base)

        for c in range(3):
            out[:, :, c] = lut[base[:, :, c]]

        return out
