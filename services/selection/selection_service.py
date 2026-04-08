from collections import deque
import numpy as np
from PIL import Image


class SelectionService:
    """Selection helper service for region-based and rectangle masks."""

    def create_rect_mask(self, size, x0: int, y0: int, x1: int, y1: int) -> Image.Image:
        """Create a binary selection mask for the inclusive rectangle bounds."""

        width, height = size
        left = max(0, min(x0, x1))
        right = min(width - 1, max(x0, x1))
        top = max(0, min(y0, y1))
        bottom = min(height - 1, max(y0, y1))

        mask_array = np.zeros((height, width), dtype=np.uint8)
        if right >= left and bottom >= top:
            mask_array[top:bottom + 1, left:right + 1] = 255
        return Image.fromarray(mask_array, "L")

    def create_magic_wand_mask(self, image: Image.Image, x: int, y: int, tolerance: int = 40) -> Image.Image | None:
        """Create a contiguous color-similarity mask from a seed pixel."""

        rgba = np.array(image.convert("RGBA"), dtype=np.int16)
        height, width, _ = rgba.shape

        if not (0 <= x < width and 0 <= y < height):
            return None

        seed = rgba[y, x, :3]
        squared_tolerance = int(tolerance) * int(tolerance)

        selected = np.zeros((height, width), dtype=np.uint8)
        visited = np.zeros((height, width), dtype=bool)
        queue = deque([(x, y)])
        visited[y, x] = True

        while queue:
            px, py = queue.popleft()
            pixel_rgb = rgba[py, px, :3]
            diff = pixel_rgb - seed
            if int(diff[0] * diff[0] + diff[1] * diff[1] + diff[2] * diff[2]) > squared_tolerance:
                continue

            selected[py, px] = 255

            for nx, ny in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((nx, ny))

        return Image.fromarray(selected, "L")

