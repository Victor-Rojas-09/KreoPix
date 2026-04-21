import cv2
import numpy as np


class ImageRotator:
    """Rotate images around their centre using cv2.warpAffine."""

    def apply(self, img: np.ndarray, ang_deg: float, fondo: int = 0) -> np.ndarray:
        """
        Rotate images by degrees counter-clockwise around the centre.
        The output canvas expands to contain the full rotated image.
        """

        H, W = img.shape[:2]
        cx, cy = (W - 1) / 2.0, (H - 1) / 2.0

        M = cv2.getRotationMatrix2D((cx, cy), ang_deg, 1.0)

        cos_t = abs(M[0, 0])
        sin_t = abs(M[0, 1])
        out_W = int(np.ceil(H * sin_t + W * cos_t))
        out_H = int(np.ceil(H * cos_t + W * sin_t))

        # Shift centre to the expanded canvas
        M[0, 2] += (out_W - W) / 2.0
        M[1, 2] += (out_H - H) / 2.0

        # RGBA: rotate RGB and alpha separately to preserve transparency
        if img.ndim == 3 and img.shape[2] == 4:
            rgb   = img[..., :3]
            alpha = img[...,  3]

            rgb_rot = cv2.warpAffine(
                rgb, M, (out_W, out_H),
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(fondo, fondo, fondo),
            )
            alpha_rot = cv2.warpAffine(
                alpha, M, (out_W, out_H),
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            )

            return np.dstack([rgb_rot, alpha_rot])

        # Grayscale or RGB
        border_val = (fondo, fondo, fondo) if img.ndim == 3 else fondo

        return cv2.warpAffine(
            img, M, (out_W, out_H),
            flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=border_val,
        )