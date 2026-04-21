import numpy as np


class ImageBlend:
    """
    Merge two images by summing their pixel values.
    """

    def apply(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:

        h = min(img1.shape[0], img2.shape[0])
        w = min(img1.shape[1], img2.shape[1])

        img1_rec = img1[:h, :w]
        img2_rec = img2[:h, :w]

        blended = img1_rec.astype(np.float32) + img2_rec.astype(np.float32)

        # Safety clip (does not change core logic, only prevents overflow issues)
        blended = np.clip(blended, 0, 255)

        return blended.astype(img1.dtype)


class ImageBlendAverage:
    """
    Merge two images by averaging their pixel values.
    Produces smoother transitions than direct addition.
    """

    def apply(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:

        h = min(img1.shape[0], img2.shape[0])
        w = min(img1.shape[1], img2.shape[1])

        img1_rec = img1[:h, :w]
        img2_rec = img2[:h, :w]

        blended = (img1_rec.astype(np.float32) + img2_rec.astype(np.float32)) / 2.0

        blended = np.clip(blended, 0, 255)

        return blended.astype(img1.dtype)