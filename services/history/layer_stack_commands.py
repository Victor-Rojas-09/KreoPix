"""Undo/redo for adding or removing layers in the document list."""
from core.image.layer import Layer
from core.state.app_state import AppState
from core.image.image_format import ImageFormat
from services.history.command_base import DocumentCommand
from services.history.layer_clone import clone_layer


class AddLayerCommand(DocumentCommand):
    """Undo removes the added layer at insert_index; redo reinserts a clone."""

    def __init__(
        self,
        state: AppState,
        document: ImageFormat,
        insert_index: int,
        added_layer_snapshot: Layer,
    ):
        self._state = state
        self._document = document
        self._insert_index = insert_index
        self._snapshot = clone_layer(added_layer_snapshot)

    @property
    def description(self) -> str:
        return "Add layer"

    def undo(self) -> None:
        if self._insert_index < len(self._document.layers):
            self._document.layers.pop(self._insert_index)
        self._state.selected_layer_index = max(0, self._insert_index - 1)

    def redo(self) -> None:
        layer = clone_layer(self._snapshot)
        idx = min(self._insert_index, len(self._document.layers))
        self._document.layers.insert(idx, layer)
        self._state.selected_layer_index = self._insert_index


class RemoveLayerCommand(DocumentCommand):
    """Undo reinserts removed layer; redo removes it again at the same index."""

    def __init__(self, state: AppState, removed_index: int, removed_snapshot: Layer):
        self._state = state
        self._index = removed_index
        self._snapshot = clone_layer(removed_snapshot)

    @property
    def description(self) -> str:
        return "Remove layer"

    def undo(self) -> None:
        doc = self._state.current_format
        if not doc:
            return
        idx = min(self._index, len(doc.layers))
        doc.layers.insert(idx, clone_layer(self._snapshot))
        self._state.selected_layer_index = self._index

    def redo(self) -> None:
        doc = self._state.current_format
        if not doc or self._index >= len(doc.layers):
            return
        doc.layers.pop(self._index)
        layers = doc.layers
        if layers:
            self._state.selected_layer_index = max(0, min(self._index, len(layers) - 1))
        else:
            self._state.selected_layer_index = 0


class ReplaceLayerOpacityCommand(DocumentCommand):
    """Undo/redo layer opacity percentage (0–100)."""

    def __init__(self, layer: Layer, opacity_before: int, opacity_after: int):
        self._layer = layer
        self._opacity_before = max(0, min(100, int(opacity_before)))
        self._opacity_after = max(0, min(100, int(opacity_after)))

    @property
    def description(self) -> str:
        return "Layer opacity"

    def undo(self) -> None:
        self._layer.opacity = self._opacity_before

    def redo(self) -> None:
        self._layer.opacity = self._opacity_after


class ReplaceLayerFilterStateCommand(DocumentCommand):
    """Undo/redo filter_id and filter_params on one layer."""

    def __init__(
        self,
        layer: Layer,
        filter_id_before: str,
        filter_params_before: dict,
        filter_id_after: str,
        filter_params_after: dict,
    ):
        self._layer = layer
        self._id_before = filter_id_before
        self._params_before = dict(filter_params_before)
        self._id_after = filter_id_after
        self._params_after = dict(filter_params_after)

    @property
    def description(self) -> str:
        return "Filter"

    def undo(self) -> None:
        self._layer.filter_id = self._id_before
        self._layer.filter_params = dict(self._params_before)

    def redo(self) -> None:
        self._layer.filter_id = self._id_after
        self._layer.filter_params = dict(self._params_after)
