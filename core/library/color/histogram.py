import numpy as np


class Histogram:
    """RGB and Luma histogram generator."""

    def _normalize(self, img: np.ndarray) -> np.ndarray:
        """Convert image to uint8 RGB."""

        if img.ndim == 2:
            img = np.stack([img, img, img], axis=2)

        if img.dtype != np.uint8:
            if float(img.max()) <= 1.0:
                img = (np.clip(img, 0, 1) * 255).astype(np.uint8)
            else:
                img = np.clip(img, 0, 255).astype(np.uint8)

        return img[:, :, :3]

    def _hist(self, channel: np.ndarray) -> np.ndarray:
        """Compute 256-bin histogram for a single channel."""

        return np.histogram(channel.ravel(), bins=256, range=(0, 256))[0]

    # ==========================================================
    # HISTOGRAMS OF CHANNELS
    # ==========================================================

    def apply_red(self, img: np.ndarray) -> np.ndarray:
        """Compute histogram for red channel."""

        img = self._normalize(img)

        return self._hist(img[:, :, 0])

    def apply_green(self, img: np.ndarray) -> np.ndarray:
        """Compute histogram for green channel."""

        img = self._normalize(img)

        return self._hist(img[:, :, 1])

    def apply_blue(self, img: np.ndarray) -> np.ndarray:
        """Compute histogram for blue channel."""

        img = self._normalize(img)

        return self._hist(img[:, :, 2])

    def apply_luma(self, img: np.ndarray) -> np.ndarray:
        """Compute luminance histogram."""

        img = self._normalize(img)

        luma = (
            0.299 * img[:, :, 0].astype(np.float64)
            + 0.587 * img[:, :, 1].astype(np.float64)
            + 0.114 * img[:, :, 2].astype(np.float64)
        )

        return self._hist(luma)