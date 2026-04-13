import numpy as np
from PIL import Image

from core.library.color.adjustments import (
    BrightnessAdjust,
    RedAdjust,
    GreenAdjust,
    BlueAdjust,
)
from services.filters.utils import pil_to_numpy, numpy_to_pil


class ColorAdjustmentService:
    """Chain brightness and per-channel adjustments (same semantics as Color tab sliders)."""

    @staticmethod
    def scale_brightness_slider_to_value(slider_value: float) -> int:
        """Map DarkRangeSlider -100..100 to brightness delta (gamma curve)."""

        v = slider_value / 100.0
        gamma = 3.0
        if v >= 0:
            return int((abs(v) ** gamma) * 255)
        return int(-(abs(v) ** gamma) * 255)

    @staticmethod
    def scale_channel_slider_to_value(slider_value: float) -> int:
        """Map -100..100 to -255..255 linear."""

        return int(slider_value * 255 / 100)

    def apply_color_adjustments(
        self,
        image: Image.Image,
        brightness_slider: float,
        red_slider: float,
        green_slider: float,
        blue_slider: float,
    ) -> Image.Image:
        """Apply cumulative adjustments; input/output RGBA."""

        if image is None:
            return None

        rgba = image.convert("RGBA")
        np_rgb = pil_to_numpy(rgba)

        b_val = self.scale_brightness_slider_to_value(brightness_slider)
        r_val = self.scale_channel_slider_to_value(red_slider)
        g_val = self.scale_channel_slider_to_value(green_slider)
        bl_val = self.scale_channel_slider_to_value(blue_slider)

        out = np_rgb.astype(np.int32)
        if b_val != 0:
            out = BrightnessAdjust(b_val).apply(out)
        if r_val != 0:
            out = RedAdjust(r_val).apply(out)
        if g_val != 0:
            out = GreenAdjust(g_val).apply(out)
        if bl_val != 0:
            out = BlueAdjust(bl_val).apply(out)

        adjusted_rgb = numpy_to_pil(out)
        r, g, b = adjusted_rgb.split()
        _, _, _, a = rgba.split()
        return Image.merge("RGBA", (r, g, b, a))
