from PIL import Image
from core.image.layer import Layer
from services.history.command_base import DocumentCommand


class ReplaceLayerImageCommand(DocumentCommand):
    """Restore layer.image to before/after snapshots."""

    def __init__(
        self,
        layer: Layer,
        image_before: Image.Image,
        image_after: Image.Image,
        description: str = "Paint",
    ):
        self._layer = layer
        self._before = image_before.copy()
        self._after = image_after.copy()
        self._label = description

    @property
    def description(self) -> str:
        return self._label

    def undo(self) -> None:
        self._layer.image = self._before.copy()
        self._layer.original_image = self._before.copy()

    def redo(self) -> None:
        self._layer.image = self._after.copy()
        self._layer.original_image = self._after.copy()
