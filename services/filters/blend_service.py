from PIL import Image
from services.filters.utils import pil_to_numpy, numpy_to_pil
from services.filters.filter_library import (
    GrayscaleAverage,
    GrayscaleLuminosity,
    LaplacianEdge,
    CannyEdge,
    GaussianBlur
)

class BlendService:
    """Service for loading image blending modes."""

    def blend(self, bottom: Image.Image, top: Image.Image, mode: str) -> Image.Image:
        """Nested IFs for filter selection."""

        if mode == "normal":
            return Image.alpha_composite(bottom, top)

        elif mode == "grayscale_avg":
            arr = pil_to_numpy(top)
            out = GrayscaleAverage().apply(arr)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "grayscale_lum":
            arr = pil_to_numpy(top)
            out = GrayscaleLuminosity().apply(arr)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "laplacian":
            arr = pil_to_numpy(top)
            out = LaplacianEdge().apply(arr)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "canny":
            arr = pil_to_numpy(top)
            out = CannyEdge().apply(arr)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        elif mode == "gaussian_blur":
            arr = pil_to_numpy(top)
            out = GaussianBlur().apply(arr)
            return Image.alpha_composite(bottom, numpy_to_pil(out))

        else:
            return Image.alpha_composite(bottom, top)
