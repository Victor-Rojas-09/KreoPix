from collections import deque


class FillService:

    def fill(self, layer, x, y, new_color):
        image = layer.image

        if image is None:
            return

        if image.mode != "RGBA":
            image = image.convert("RGBA")
            layer.image = image

        w, h = image.size

        if not (0 <= x < w and 0 <= y < h):
            return

        if isinstance(new_color, (list, tuple)):
            if len(new_color) >= 4:
                fill_rgba = tuple(int(c) for c in new_color[:4])
            else:
                fill_rgba = tuple(int(c) for c in new_color[:3]) + (255,)
        else:
            return

        target_color = image.getpixel((x, y))
        if target_color == fill_rgba:
            return

        queue = deque([(x, y)])

        while queue:
            cx, cy = queue.popleft()

            if not (0 <= cx < w and 0 <= cy < h):
                continue

            if image.getpixel((cx, cy)) != target_color:
                continue

            image.putpixel((cx, cy), fill_rgba)

            queue.extend([
                (cx + 1, cy),
                (cx - 1, cy),
                (cx, cy + 1),
                (cx, cy - 1),
            ])
