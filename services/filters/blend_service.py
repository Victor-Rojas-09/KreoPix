from PIL import Image
from services.filters.utils import pil_to_numpy, numpy_to_pil
from services.filters.filter_library import (
    GrayscaleAverage,
    GrayscaleLuminosity,
    LaplacianEdge,
    CannyEdge,
    GaussianBlur,
    ThresholdFilter
)

class BlendService:
    """Service for loading image blending modes."""

    def blend(self, bottom: Image.Image, top: Image.Image, mode: str, params=None) -> Image.Image:
        """Nested IFs for filter selection."""
        params = params or {}

        if mode == "normal":
            return Image.alpha_composite(bottom, top)

        elif mode == "grayscale_avg":
            array = pil_to_numpy(top)
            out = GrayscaleAverage().apply(array)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "grayscale_lum":
            array = pil_to_numpy(top)
            out = GrayscaleLuminosity().apply(array)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "laplacian":
            array = pil_to_numpy(top)
            out = LaplacianEdge().apply(array)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "canny":
            array = pil_to_numpy(top)
            out = CannyEdge().apply(array)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "gaussian_blur":
            array = pil_to_numpy(top)
            out = GaussianBlur().apply(array)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "threshold":
            array = pil_to_numpy(top)
            out = ThresholdFilter(**params).apply(array)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        else:
            return Image.alpha_composite(bottom, top)
