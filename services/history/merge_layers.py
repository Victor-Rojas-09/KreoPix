from PIL import Image
from core.image.layer import Layer
from services.history.command_base import DocumentCommand


class MergeLayersCommand(DocumentCommand):
    """Undo and redo command for merging all visible layers into one."""

    def __init__(self, state, document, merged_image: Image.Image):
        self._state    = state
        self._document = document
        self._merged   = merged_image.copy()

        # Full snapshot of every layer before the merge, for undo
        self._before_layers = [
            {
                "image":         l.image.copy(),
                "original":      l.original_image.copy(),
                "name":          l.name,
                "visible":       l.visible,
                "opacity":       l.opacity,
                "filter_id":     l.filter_id,
                "filter_params": dict(l.filter_params or {}),
            }
            for l in document.get_layers()
        ]

    @property
    def description(self) -> str:
        """Description of merging layers."""

        return "Merge visible layers"

    def redo(self) -> None:
        """Replace visible layers with the single merged layer."""

        layers  = self._document.get_layers()
        hidden  = [l for l in layers if not l.visible]

        merged_layer = Layer(self._merged.copy(), name="Merged")

        layers.clear()
        layers.extend(hidden)
        layers.append(merged_layer)

        self._state.selected_layer_index = max(0, len(layers) - 1)
        self._state.notify()

    def undo(self) -> None:
        """Restore all layers from the pre-merge snapshot."""

        layers = self._document.get_layers()
        layers.clear()

        for snap in self._before_layers:
            l = Layer(snap["image"].copy(), name=snap["name"])
            l.original_image = snap["original"].copy()
            l.visible        = snap["visible"]
            l.opacity        = snap["opacity"]
            l.filter_id      = snap["filter_id"]
            l.filter_params  = dict(snap["filter_params"])
            layers.append(l)

        self._state.selected_layer_index = max(0, len(layers) - 1)
        self._state.notify()