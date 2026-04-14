import numpy as np
from PIL import Image

from core.library.color.histogram import Histogram
from core.library.color.curve_processor import CurveProcessor
from services.filters.utils import pil_to_numpy


class HistogramCurveService:
    """Histogram data and curve (LUT) application for RGBA images."""

    def __init__(self):
        self.hist = Histogram()

    def get_histogram(self, image: Image.Image) -> dict[str, object]:

        if image is None:
            zero = np.zeros(256, dtype=np.int64)
            return {"R": zero, "G": zero, "B": zero, "luma": zero, "max_count": 1}

        np_img = pil_to_numpy(image)

        # 👉 usamos la nueva clase (no compute_rgb_histograms)
        h = {
            "R": self.hist.apply_red(np_img),
            "G": self.hist.apply_green(np_img),
            "B": self.hist.apply_blue(np_img),
            "luma": self.hist.apply_luma(np_img),
        }

        max_count = max(
            h["R"].max(),
            h["G"].max(),
            h["B"].max(),
            h["luma"].max(),
            1,
        )

        return {
            **h,
            "max_count": max_count,
        }

    def apply_curve(self, image: Image.Image, points: list[tuple[int, int]]) -> Image.Image:
        """Apply master histogram curve; preserve alpha."""

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