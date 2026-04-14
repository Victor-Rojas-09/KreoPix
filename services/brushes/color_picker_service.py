class ColorPickerService:
    """Color picker service class."""

    def pick_color(self, layer, x: int, y: int):
        """Pick color from a given (x, y) coordinate in a layer image."""

        image = layer.image

        # Ensure layer has an image to sample from
        if image is None:
            return None

        w, h = image.size

        # Validate that coordinates are inside image bounds
        if not (0 <= x < w and 0 <= y < h):
            return None

        # Extract pixel value from image
        px = image.getpixel((x, y))

        # Normalize pixel format to tuple
        if not isinstance(px, tuple):
            px = tuple(px)

        # Convert RGB → RGBA by assuming full opacity
        if len(px) == 3:
            return px + (255,)

        # Ensure RGBA is returned consistently
        if len(px) >= 4:
            return tuple(px[:4])

        # Unsupported pixel format
        return None