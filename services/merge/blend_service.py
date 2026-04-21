from PIL import Image
from services.merge.blend_adapter import BlendAdapter


class BlendService:
    """High-level service for image merging."""

    def __init__(self):
        self._adapter = BlendAdapter()

    def merge(self, base: Image.Image, overlay: Image.Image, position=(0, 0)) -> Image.Image:
        """Merge two images using additive blending."""

        return self._adapter.blend_add(base, overlay, position)

    def merge_average(self, base: Image.Image, overlay: Image.Image, position=(0, 0)) -> Image.Image:
        """Merge two images using average blending."""

        return self._adapter.blend_average(base, overlay, position)

    def merge_layers(self, layers, mode="add") -> Image.Image:
        """Merge a list of layers into a single image."""

        if not layers:
            return None

        result = layers[0]

        for layer_img in layers[1:]:
            if mode == "add":
                result = self.merge(result, layer_img)

            elif mode == "average":
                result = self.merge_average(result, layer_img)

            else:
                raise ValueError(f"Unsupported merge mode: {mode}")

        return result