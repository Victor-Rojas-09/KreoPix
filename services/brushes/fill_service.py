from collections import deque

class FillService:

    def fill(self, layer, x, y, new_color):
        image = layer.image

        h, w = image.shape[:2]

        target_color = tuple(image[y, x])

        if target_color == new_color:
            return

        queue = deque([(x, y)])

        while queue:
            cx, cy = queue.popleft()

            if not (0 <= cx < w and 0 <= cy < h):
                continue

            if tuple(image[cy, cx]) != target_color:
                continue

            image[cy, cx] = new_color

            queue.extend([
                (cx + 1, cy),
                (cx - 1, cy),
                (cx, cy + 1),
                (cx, cy - 1),
            ])