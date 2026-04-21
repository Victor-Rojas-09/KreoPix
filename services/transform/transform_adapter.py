from PIL import Image
import numpy as np
from core.library.transform.crop import ImageCrop
from core.library.transform.resize import ImageReduction, ImageUpscale
from core.library.transform.rotation import ImageRotator


class CropAdapter:
    """Adapter for cropping a region from a PIL image."""

    def __init__(self):
        self.cropper = ImageCrop()

    def from_selection(self, pil_image: Image.Image, bbox: tuple[int, int, int, int]) -> np.ndarray:
        """Extract a sub-image from a PIL image based on a bounding box."""

        np_img = np.array(pil_image)
        x0, y0, x1, y1 = bbox

        return self.cropper.apply(np_img, x0, x1, y0, y1)


class ResizeAdapter:
    """Adapter for scaling images."""

    def __init__(self):
        self.reducer = ImageReduction()
        self.upscaler = ImageUpscale()

    def apply(self, img_np: np.ndarray, scale: float) -> np.ndarray:
        """Apply scaling transformation."""

        if scale == 1:
            return img_np

        if scale > 1:
            factor = int(round(scale))
            return self.upscaler.apply(img_np, factor)

        # scale < 1 → reduce resolution
        factor = int(round(1 / scale))
        factor = max(1, factor)

        return self.reducer.apply(img_np, factor)


class RotationAdapter:
    """Adapter for rotation using the custom core rotation algorithm."""

    def __init__(self):
        self.rotator = ImageRotator()

    def apply(self, img_np: np.ndarray, angle: float) -> np.ndarray:
        """Apply rotation transformation."""

        return self.rotator.apply(img_np, angle)

