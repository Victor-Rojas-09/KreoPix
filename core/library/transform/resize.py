import numpy as np

class ImageReduction:
    """
    Resolution reduction by reducing the number of pixels .
    """

    def apply(self, img: np.ndarray, f: int) -> np.ndarray:

        if not isinstance(f, int) or f <= 0:
            raise ValueError("f must be a positive integer")

        reduction = img[::f , ::f]

        return reduction

class ImageUpscale:
    """
    Upscale by pixel replication.
    """

    def apply(self, img: np.ndarray, f: int) -> np.ndarray:

        if not isinstance(f, int) or f <= 0:
            raise ValueError("f must be a positive integer")

        return np.repeat(np.repeat(img, f, axis=0), f, axis=1)