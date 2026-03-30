import numpy as np
import matplotlib.pyplot as plt

class Histogram:
    """"
    This Class is for make a histogram of the canal image
    """
    def applyRed(self, img: np.ndarray) -> None:

        if img.max() <= 1.0:
            img = (img * 255).astype(np.uint8)

        channel = img[:, :, 0]

        plt.figure(figsize=(12,6))
        plt.hist(channel.ravel(), bins=256, color='red')
        plt.title('Red Channel Histogram')
        plt.show()

    def applyGreen(self, img: np.ndarray) -> None:

        if img.max() <= 1.0:
            img = (img * 255).astype(np.uint8)

        channel = img[:, :, 1]

        plt.figure(figsize=(12,6))
        plt.hist(channel.ravel(), bins=256, color='green')
        plt.title('Green Channel Histogram')
        plt.show()

    def applyBlue(self, img: np.ndarray) -> None:

        if img.max() <= 1.0:
            img = (img * 255).astype(np.uint8)

        channel = img[:, :, 2]

        plt.figure(figsize=(12,6))
        plt.hist(channel.ravel(), bins=256, color='blue')
        plt.title('Blue Channel Histogram')
        plt.show()
