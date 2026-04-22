from PIL import Image
from services.filters.utils import pil_to_numpy, numpy_to_pil

from core.library.color.channels import (
    RedChannel,
    GreenChannel,
    BlueChannel,
    CyanChannel,
    MagentaChannel,
    YellowChannel,
    ColorInverter
)

from core.library.color.grayscale import (
    GrayscaleAverage,
    GrayscaleLuminosity,
    GrayscaleMidgray
)

from core.library.color.adjustments import (
    BrightnessAdjust,
    RedAdjust,
    GreenAdjust,
    BlueAdjust
)

from core.library.segmentation.threshold_filters_rgb import (
    GlobalBinarizeRgb,
    AdaptiveGaussianRgb,
    AdaptiveMeanRgb,
    CannyEdgeRgb,
    OtsuBinarizeRgb,
)


"""
The FILTER_REGISTRY is a centralized dictionary that defines all 
available image filters. It works with a configuration map of filter 
identifier to its corresponding implementation and parameter rules.
"""

FILTER_REGISTRY = {
    "normal": {
        "name": "Normal",
        "class": None,
        "params": {}
    },
    "invert": {
        "name": "Invert Color",
        "class": ColorInverter,
        "params": {}
    },
    "red_channel": {
        "name": "Red Channel",
        "class": RedChannel,
        "params": {}
    },
    "green_channel": {
        "name": "Green Channel",
        "class": GreenChannel,
        "params": {}
    },
    "blue_channel": {
        "name": "Blue Channel",
        "class": BlueChannel,
        "params": {}
    },
    "cyan_channel": {
        "name": "Cyan Channel",
        "class": CyanChannel,
        "params": {}
    },
    "magenta_channel": {
        "name": "Magenta Channel",
        "class": MagentaChannel,
        "params": {}
    },
    "yellow_channel": {
        "name": "Yellow Channel",
        "class": YellowChannel,
        "params": {}
    },
    "grayscale_average": {
        "name": "Grayscale Average",
        "class": GrayscaleAverage,
        "params": {}
    },
    "grayscale_luminosity": {
        "name": "Grayscale Luminosity",
        "class": GrayscaleLuminosity,
        "params": {}
    },
    "grayscale_midgray": {
        "name": "Grayscale Midgray",
        "class": GrayscaleMidgray,
        "params": {}
    },
    "brightness": {
        "name": "Brightness",
        "class": BrightnessAdjust,
        "params": {
            "value": {"min": -255, "max": 255, "default": 0}
        }
    },

    "red_adjust": {
        "name": "Red Adjust",
        "class": RedAdjust,
        "params": {
            "value": {"min": -255, "max": 255, "default": 0}
        }
    },

    "green_adjust": {
        "name": "Green Adjust",
        "class": GreenAdjust,
        "params": {
            "value": {"min": -255, "max": 255, "default": 0}
        }
    },

    "blue_adjust": {
        "name": "Blue Adjust",
        "class": BlueAdjust,
        "params": {
            "value": {"min": -255, "max": 255, "default": 0}
        }
    },

    "global_binarize": {
        "name": "Global Binarize",
        "class": GlobalBinarizeRgb,
        "params": {
            "threshold": {"min": 0, "max": 255, "default": 127}
        }
    },
    "adaptive_gaussian": {
        "name": "Adaptive Gaussian",
        "class": AdaptiveGaussianRgb,
        "params": {
            "block_size": {"min": 3, "max": 99, "default": 11},
            "C": {"min": -50, "max": 50, "default": 2}
        }
    },
    "adaptive_mean": {
        "name": "Adaptive Mean",
        "class": AdaptiveMeanRgb,
        "params": {
            "block_size": {"min": 3, "max": 99, "default": 11},
            "C": {"min": -50, "max": 50, "default": 2}
        }
    },
    "canny_edge": {
        "name": "Canny Edge",
        "class": CannyEdgeRgb,
        "params": {
            "threshold1": {"min": 0, "max": 255, "default": 80},
            "threshold2": {"min": 0, "max": 255, "default": 160}
        }
    },
    "otsu_binarize": {
        "name": "Otsu Binarize",
        "class": OtsuBinarizeRgb,
        "params": {
            "dummy": {"min": 0, "max": 0, "default": 0}
        }
    },
}


class FilterService:
    """Service responsible for applying filters to images."""

    def apply(self, image: Image.Image, filter_id: str, params: dict = None) -> Image.Image:
        """Apply a filter to an image safely."""

        if image is None:
            return None

        params = params or {}

        # Validate filter existence
        filter_meta = FILTER_REGISTRY.get(filter_id)
        if not filter_meta:
            return image

        filter_class = filter_meta.get("class")

        if filter_class is None:
            return image

        safe_params = self._validate_params(filter_meta, params)

        try:
            np_image = pil_to_numpy(image)

            filter_instance = filter_class(**safe_params)
            array = filter_instance.apply(np_image)

            return numpy_to_pil(array)

        except Exception:
            return image

    def _validate_params(self, filter_meta: dict, input_params: dict) -> dict:
        """Validate and sanitize filter parameters."""

        validated_params = {}

        param_schema = filter_meta.get("params", {})

        for param_name, rules in param_schema.items():

            raw_value = input_params.get(param_name, rules.get("default"))

            if raw_value is None:
                validated_params[param_name] = rules.get("default")
                continue

            try:
                value = int(raw_value)
            except (ValueError, TypeError):
                value = rules.get("default")

            # Clamp values
            min_val = rules.get("min", value)
            max_val = rules.get("max", value)

            value = max(min_val, min(max_val, value))

            validated_params[param_name] = value

        return validated_params

class BlendService:
    """Service responsible for blending two images."""

    def blend(self, base_image: Image.Image, top_image: Image.Image) -> Image.Image:
        """Blend two images using alpha compositing."""

        if base_image is None:
            return top_image

        if top_image is None:
            return base_image

        return Image.alpha_composite(base_image, top_image)