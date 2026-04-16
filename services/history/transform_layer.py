from PIL import Image
from core.image.layer import Layer
from services.history.command_base import DocumentCommand


class TransformLayerCommand(DocumentCommand):
    """Record layer transformation for undo/redo support."""

    def __init__(self, layer: Layer, image_before: Image.Image, image_after: Image.Image, description: str = "Transform"):
        self._layer = layer
        self._before = image_before.copy()
        self._after = image_after.copy()
        self._label = description

    @property
    def description(self) -> str:
        """Return description of the transformation."""

        return self._label

    def undo(self) -> None:
        """Undo the transformation."""

        self._layer.image = self._before.copy()
        self._layer.original_image = self._before.copy()

    def redo(self) -> None:
        """Redo the transformation."""

        self._layer.image = self._after.copy()
        self._layer.original_image = self._after.copy()
