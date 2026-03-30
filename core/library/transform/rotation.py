import numpy as np


class ImageRotator:
    """
    Rotate images using inverse mapping
    and the nearest-neighbor method.
    """

    def apply(self, img: np.ndarray, ang_deg: float, fondo=0) -> np.ndarray:

        H, W = img.shape[:2]

        cx = (W - 1) / 2.0
        cy = (H - 1) / 2.0

        ang = np.deg2rad(ang_deg)
        cos_t = np.cos(ang)
        sin_t = np.sin(ang)

        esquinas = np.array([
            [0, 0],
            [W - 1, 0],
            [W - 1, H - 1],
            [0, H - 1]
        ], dtype=np.float32)

        x = esquinas[:, 0] - cx
        y = esquinas[:, 1] - cy

        xr = x * cos_t - y * sin_t
        yr = x * sin_t + y * cos_t

        min_x, max_x = xr.min(), xr.max()
        min_y, max_y = yr.min(), yr.max()

        out_W = int(np.ceil(max_x - min_x + 1))
        out_H = int(np.ceil(max_y - min_y + 1))

        out_cx = (out_W - 1) / 2.0
        out_cy = (out_H - 1) / 2.0

        if img.ndim == 3:
            out = np.full((out_H, out_W, 3), fondo, dtype=img.dtype)
        else:
            out = np.full((out_H, out_W), fondo, dtype=img.dtype)

        for y_out in range(out_H):
            for x_out in range(out_W):

                x2 = x_out - out_cx
                y2 = y_out - out_cy

                x1 = x2 * cos_t + y2 * sin_t
                y1 = -x2 * sin_t + y2 * cos_t

                x_src = x1 + cx
                y_src = y1 + cy

                xi = int(round(x_src))
                yi = int(round(y_src))

                if 0 <= xi < W and 0 <= yi < H:
                    out[y_out, x_out] = img[yi, xi]

        return out