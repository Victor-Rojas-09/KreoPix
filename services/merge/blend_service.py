from PIL import Image
from services.merge.blend_adapter import BlendAdapter


class BlendService:
    """High-level service for image merging."""

    def __init__(self):
        self._adapter = BlendAdapter()

    def blend(self, base_image: Image.Image, top_image: Image.Image) -> Image.Image:
        """Standard alpha compositing."""

        if base_image is None:
            return top_image

        if top_image is None:
            return base_image

        return Image.alpha_composite(base_image, top_image)

    def blend_average(self, base_image: Image.Image, top_image: Image.Image) -> Image.Image:
        """Blend using average."""

        return self._adapter.blend_average(base_image, top_image)
