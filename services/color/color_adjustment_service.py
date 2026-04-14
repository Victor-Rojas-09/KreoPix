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
    """Chain brightness and per-channel adjustments."""

    @staticmethod
    def scale_brightness_slider_to_value(slider_value: float) -> int:
        """Convert slider into a nonlinear brightness delta."""

        v = slider_value / 100.0

        # Gamma curve to make low values less aggressive and high values stronger
        gamma = 3.0

        # Positive values increase brightness exponentially
        if v >= 0:
            return int((abs(v) ** gamma) * 255)

        # Negative values decrease brightness with same curve
        return int(-(abs(v) ** gamma) * 255)

    @staticmethod
    def scale_channel_slider_to_value(slider_value: float) -> int:
        """Map -100..100 to -255..255 linear."""

        return int(slider_value * 255 / 100)

    def apply_color_adjustments(self,image, brightness_slider: float, red_slider: float, green_slider: float, blue_slider: float) -> Image.Image:
        """Apply brightness and RGB channel adjustments on an RGBA image."""

        # Guard: ensure image exists
        if image is None:
            return None

        # Convert to consistent RGBA format for safe processing
        rgba = image.convert("RGBA")

        # Convert image to NumPy array for vectorized operations
        np_rgb = pil_to_numpy(rgba)

        # Map UI sliders to internal adjustment values
        b_val = self.scale_brightness_slider_to_value(brightness_slider)
        r_val = self.scale_channel_slider_to_value(red_slider)
        g_val = self.scale_channel_slider_to_value(green_slider)
        bl_val = self.scale_channel_slider_to_value(blue_slider)

        # Work in higher precision to avoid overflow during transformations
        out = np_rgb.astype(np.int32)

        # Apply brightness adjustment if needed
        if b_val != 0:
            out = BrightnessAdjust(b_val).apply(out)

        # Apply per-channel RGB adjustments if needed
        if r_val != 0:
            out = RedAdjust(r_val).apply(out)
        if g_val != 0:
            out = GreenAdjust(g_val).apply(out)
        if bl_val != 0:
            out = BlueAdjust(bl_val).apply(out)

        # Convert back to PIL image
        adjusted_rgb = numpy_to_pil(out)

        # Preserve original alpha channel
        r, g, b = adjusted_rgb.split()
        _, _, _, a = rgba.split()

        # Recombine RGB with original alpha
        return Image.merge("RGBA", (r, g, b, a))
