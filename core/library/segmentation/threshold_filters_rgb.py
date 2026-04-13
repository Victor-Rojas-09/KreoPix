"""
RGB-sized threshold-style filters for use with FilterService (HxWx3 uint8 output).
Input images are RGB (as from pil_to_numpy).
"""

import cv2
import numpy as np

from core.library.segmentation.threshold import ImageBinarization
from core.library.segmentation.adaptive_threshold import AdaptiveThreshold
def _gray_to_rgb(gray: np.ndarray) -> np.ndarray:
    """Stack single channel to HxWx3 uint8."""

    g = gray.astype(np.uint8)
    return np.stack([g, g, g], axis=2)


class GlobalBinarizeRgb:
    """Global grayscale threshold → RGB."""

    def __init__(self, threshold: int = 127):
        self.threshold = int(threshold)

    def apply(self, img: np.ndarray) -> np.ndarray:
        binarizer = ImageBinarization()
        binary = binarizer.apply(img, self.threshold)
        return _gray_to_rgb(binary)


class AdaptiveGaussianRgb:
    """Adaptive Gaussian threshold → RGB."""

    def __init__(self, block_size: int = 11, C: int = 2):
        self.block_size = int(block_size)
        self.C = int(C)

    def apply(self, img: np.ndarray) -> np.ndarray:
        adapt = AdaptiveThreshold()
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        binary = adapt.apply(gray, self.block_size, self.C, method="gaussian")
        return _gray_to_rgb(binary)


class AdaptiveMeanRgb:
    """Adaptive mean threshold → RGB."""

    def __init__(self, block_size: int = 11, C: int = 2):
        self.block_size = int(block_size)
        self.C = int(C)

    def apply(self, img: np.ndarray) -> np.ndarray:
        adapt = AdaptiveThreshold()
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        binary = adapt.apply(gray, self.block_size, self.C, method="mean")
        return _gray_to_rgb(binary)


class CannyEdgeRgb:
    """Canny edges → RGB (uses RGB luminance, not BGR)."""

    def __init__(self, threshold1: int = 80, threshold2: int = 160):
        self.threshold1 = int(threshold1)
        self.threshold2 = int(threshold2)

    def apply(self, img: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, self.threshold1, self.threshold2)
        return _gray_to_rgb(edges)


class OtsuBinarizeRgb:
    """Otsu auto threshold on luminance → RGB."""

    def __init__(self, dummy: int = 0):
        """dummy satisfies FilterService param validation when unused."""

        self.dummy = int(dummy)

    def apply(self, img: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return _gray_to_rgb(binary)
