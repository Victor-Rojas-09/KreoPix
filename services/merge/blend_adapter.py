from PIL import Image
import numpy as np

from core.library.transform.blend import ImageBlend, ImageBlendAverage


class BlendAdapter:
    """Adapter layer between PIL images and low-level NumPy blend operations."""

    def __init__(self):
        self._blend_add = ImageBlend()
        self._blend_avg = ImageBlendAverage()

    def _to_numpy(self, img: Image.Image) -> np.ndarray:
        """Convert PIL image to NumPy array."""

        return np.array(img.convert("RGBA"))

    def _to_pil(self, arr: np.ndarray) -> Image.Image:
        """Convert NumPy array to PIL image."""

        arr = np.clip(arr, 0, 255).astype(np.uint8)

        return Image.fromarray(arr, "RGBA")

    def _compute_overlap(self, base, overlay, x, y):
        """Compute overlapping region between base and overlay given position."""

        H, W = base.shape[:2]
        h, w = overlay.shape[:2]

        x_end = min(x + w, W)
        y_end = min(y + h, H)

        if x >= W or y >= H:
            return None  # no overlap

        base_crop = base[y:y_end, x:x_end]
        overlay_crop = overlay[:(y_end - y), :(x_end - x)]

        return base_crop, overlay_crop, (y, y_end, x, x_end)

    def blend_add(self, base_pil: Image.Image, overlay_pil: Image.Image, position=(0, 0)) -> Image.Image:
        """Blend using pixel addition."""

        return self._blend(base_pil, overlay_pil, mode="add", position=position)

    def blend_average(self, base_pil: Image.Image, overlay_pil: Image.Image, position=(0, 0)) -> Image.Image:
        """Blend using pixel averaging."""

        return self._blend(base_pil, overlay_pil, mode="average", position=position)

    def _blend(self, base_pil, overlay_pil, mode, position):
        """Blend using pixel addition."""

        base_np = self._to_numpy(base_pil)
        overlay_np = self._to_numpy(overlay_pil)

        x, y = position
        overlap = self._compute_overlap(base_np, overlay_np, x, y)

        if overlap is None:
            return base_pil  # nothing to blend

        base_crop, overlay_crop, (y1, y2, x1, x2) = overlap

        if mode == "add":
            blended = self._blend_add.apply(base_crop, overlay_crop)

        elif mode == "average":
            blended = self._blend_avg.apply(base_crop, overlay_crop)

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        result = base_np.copy()
        result[y1:y2, x1:x2] = blended

        return self._to_pil(result)