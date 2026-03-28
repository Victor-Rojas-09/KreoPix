import numpy as np


class ImageCrop:
    """
    Crop a specific area of the image.
    """

    def apply(
        self,
        img: np.ndarray,
        x_ini: int,
        x_fin: int,
        y_ini: int,
        y_fin: int
    ) -> np.ndarray:

        return img[y_ini:y_fin, x_ini:x_fin]