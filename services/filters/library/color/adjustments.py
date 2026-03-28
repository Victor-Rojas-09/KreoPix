import numpy as np


class BrightnessAdjust:
    """
    Class for adjusting the brightness of an image.
    """

    def __init__(self, value: int = 0):
        self.value = value

    def apply(self, img: np.ndarray) -> np.ndarray:

        imgf = img.astype(np.int32)

        result = np.clip(imgf + self.value, 0, 255)

        return result.astype(np.uint8)


class ChannelAdjust:
    """
    Adjusts the brightness of a specific channel in the image.
    """

    def __init__(self, value: int = 0):
        self.value = value

    def apply(self, img: np.ndarray, channel: int) -> np.ndarray:

        if channel not in [0, 1, 2]:
            raise ValueError("The channel must be 0 (R), 1 (G), or 2 (B).")

        result = img.astype(np.int32).copy()

        result[:, :, channel] = np.clip(
            result[:, :, channel] + self.value,
            0,
            255
        )

        return result.astype(np.uint8)