import numpy as np


class ColorInverter:
    """
    Inverts the colors of an RGB image.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        return 1 - img


class RedChannel:
    """
    Extract only the red channel from the image.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        result = np.copy(img)
        result[:, :, 0] = 0
        result[:, :, 1] = 0

        return result


class GreenChannel:
    """
    Extract only the green channel from the image.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:
        result = np.copy(img)
        result[:, :, 0] = 0
        result[:, :, 2] = 0
        return result


class BlueChannel:
    """
    Extract only the blue channel from the image.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:
        result = np.copy(img)
        result[:, :, 1] = 0
        result[:, :, 2] = 0
        return result


class MagentaChannel:
    """
    Extract the magenta channel.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:
        result = np.copy(img)
        result[:, :, 1] = 0
        return result


class CyanChannel:
    """
    Extract the cyan channel.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:
        result = np.copy(img)
        result[:, :, 2] = 0
        return result


class YellowChannel:
    """
    Extract the yellow channel.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:
        result = np.copy(img)
        result[:, :, 0] = 0
        return result