import numpy as np


class BrightnessAdjust:
    """
    Adjusts overall image brightness.
    """

    def __init__(self, value: int = 0):
        self.value = value

    def apply(self, img: np.ndarray) -> np.ndarray:

        imgf = img.astype(np.int32)

        result = np.clip(imgf + self.value, 0, 255)

        return result.astype(np.uint8)


class RedAdjust:
    """
    Adjusts the red channel intensity.
    """

    def __init__(self, value: int = 0):
        self.value = value

    def apply(self, img: np.ndarray) -> np.ndarray:

        result = img.astype(np.int32).copy()

        result[:, :, 0] = np.clip(result[:, :, 0] + self.value, 0, 255)

        return result.astype(np.uint8)


class GreenAdjust:
    """
    Adjusts the green channel intensity.
    """

    def __init__(self, value: int = 0):
        self.value = value

    def apply(self, img: np.ndarray) -> np.ndarray:

        result = img.astype(np.int32).copy()

        result[:, :, 1] = np.clip(result[:, :, 1] + self.value, 0, 255)

        return result.astype(np.uint8)


class BlueAdjust:
    """
    Adjusts the blue channel intensity.
    """

    def __init__(self, value: int = 0):
        self.value = value

    def apply(self, img: np.ndarray) -> np.ndarray:

        result = img.astype(np.int32).copy()

        result[:, :, 2] = np.clip(result[:, :, 2] + self.value, 0, 255)

        return result.astype(np.uint8)