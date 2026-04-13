import numpy as np
from PIL import Image

from core.library.color.curve_processor import CurveProcessor
from core.library.color.histogram import compute_rgb_histograms
from services.filters.utils import pil_to_numpy


class HistogramCurveService:
    """Histogram data and curve (LUT) application for RGBA images."""

    def get_histogram(self, image: Image.Image) -> dict[str, object]:
        """
        Return histogram counts and max for UI scaling.

        Keys: R, G, B, luma (each length-256), max_count (int).
        """

        if image is None:
            zero = np.zeros(256, dtype=np.int64)
            return {"R": zero, "G": zero, "B": zero, "luma": zero, "max_count": 1}

        np_rgb = pil_to_numpy(image)
        h = compute_rgb_histograms(np_rgb)
        max_count = max(
            int(h["R"].max()),
            int(h["G"].max()),
            int(h["B"].max()),
            int(h["luma"].max()),
            1,
        )
        return {
            "R": h["R"],
            "G": h["G"],
            "B": h["B"],
            "luma": h["luma"],
            "max_count": max_count,
        }

    def apply_curve(self, image: Image.Image, points: list[tuple[int, int]]) -> Image.Image:
        """Apply master RGB curve; preserve alpha."""

        if image is None:
            return None

        rgba = image.convert("RGBA")
        r, g, b, a = rgba.split()
        rgb = Image.merge("RGB", (r, g, b))
        np_rgb = pil_to_numpy(rgb)
        lut = CurveProcessor.build_lut(points)
        out_rgb = CurveProcessor.apply_lut_to_rgb(np_rgb, lut)
        out = Image.fromarray(out_rgb, "RGB")
        r2, g2, b2 = out.split()
        return Image.merge("RGBA", (r2, g2, b2, a))
