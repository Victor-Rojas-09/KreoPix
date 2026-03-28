import numpy as np


class ImageBlendAverage:
    """
    Merge two images by averaging
    their pixels.
    """

    def apply(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:

        h = min(img1.shape[0], img2.shape[0])
        w = min(img1.shape[1], img2.shape[1])

        img1_rec = img1[:h, :w]
        img2_rec = img2[:h, :w]

        blended = (img1_rec.astype(np.float32) + img2_rec.astype(np.float32)) / 2

        return blended.astype(img1.dtype)