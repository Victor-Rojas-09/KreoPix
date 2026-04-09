from collections import deque
import numpy as np
from PIL import Image


class SelectionService:
    """Selection helper service for region-based and rectangle masks."""

    def create_rect_mask(self, size, x0: int, y0: int, x1: int, y1: int) -> Image.Image:
        """Create a binary selection mask for the inclusive rectangle bounds."""

        width, height = size

        # Normalize coordinates
        left = max(0, min(x0, x1))
        right = min(width - 1, max(x0, x1))
        top = max(0, min(y0, y1))
        bottom = min(height - 1, max(y0, y1))

        # Create empty mask
        mask_array = np.zeros((height, width), dtype=np.uint8)

        # Fill rectangle
        if right >= left and bottom >= top:
            mask_array[top:bottom + 1, left:right + 1] = 255

        return Image.fromarray(mask_array, "L")

    def create_magic_wand_mask(self, image: Image.Image, x: int, y: int, tolerance: int = 40) -> Image.Image | None:
        """Create a contiguous color-similarity mask from a seed pixel."""

        rgba = np.array(image.convert("RGBA"), dtype=np.int16)
        height, width, _ = rgba.shape

        # Check bounds
        if not (0 <= x < width and 0 <= y < height):
            return None

        # Get seed color
        seed = rgba[y, x, :3]

        squared_tolerance = int(tolerance) * int(tolerance)

        # Helper arrays for result mask and avoids infinite loops
        selected = np.zeros((height, width), dtype=np.uint8)
        visited = np.zeros((height, width), dtype=bool)

        # Initialize queue (BFS)
        queue = deque([(x, y)])
        visited[y, x] = True

        # Flood Fill
        while queue:

            # Compare color distance
            px, py = queue.popleft()
            pixel_rgb = rgba[py, px, :3]
            diff = pixel_rgb.astype(np.float64) - seed.astype(np.float64)
            dist2 = np.dot(diff, diff)

            # Check tolerance
            if dist2 > squared_tolerance:
                continue

            # Mark as selected
            selected[py, px] = 255

            # Add neighbors
            for nx, ny in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((nx, ny))

        return Image.fromarray(selected, "L")