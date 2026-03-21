import numpy as np
from PIL import Image

def pil_to_numpy(img: Image.Image) -> np.ndarray:
    """Convert a PIL image to a numpy image."""
    return np.array(img.convert("RGB"))

def numpy_to_pil(arr: np.ndarray) -> Image.Image:
    """Convert a numpy image to a PIL image"""
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
