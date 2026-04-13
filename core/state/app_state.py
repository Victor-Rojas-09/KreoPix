from core.image.image_format import ImageFormat
from core.brush.presets import create_hard_brush
from PIL import Image


class AppState:
    """
    Centralized application state manager.

    This class is responsible for maintaining and coordinating the current
    document, layers, tools, brushes, and UI listeners. It acts as a single
    source of truth for the application state and notifies registered listeners
    whenever relevant changes occur.
    """

    def __init__(self):

        self.current_format: ImageFormat | None = None
        self.current_project = None
        self.selected_layer_index: int = 0
        self.current_tool = None
        self._listeners = []

        self.current_brush = create_hard_brush((0, 0, 0, 255))
        self.current_color = (0, 0, 0, 255)
        self.recent_colors = []
        self.selection_mask: Image.Image | None = None
        # Threshold filters (UI-driven selection)
        self._active_threshold_filters = [
            "brightness",
            "red_adjust",
            "green_adjust",
            "blue_adjust"
        ]

        # Parámetros actuales de sliders (opcional pero útil)
        self._threshold_params: dict[str, dict] = {}

    # ==========================================================
    # Document
    # ==========================================================

    def get_format(self) -> ImageFormat | None:
        """Get the active document."""

        return self.current_format

    def set_format(self, image_format: ImageFormat):
        """Set the active document and reset layer selection."""

        self.current_format = image_format
        self.selected_layer_index = 0
        self.current_project = image_format
        self.selection_mask = None
        self.notify()

    def clear_format(self):
        """Remove the active document."""

        self.current_format = None
        self.selected_layer_index = 0
        self.current_project = None
        self.selection_mask = None
        self.notify()

    def has_format(self) -> bool:
        """Return True if a document is loaded."""
        return self.current_format is not None

    # ==========================================================
    # UI
    # ==========================================================

    def add_listener(self, callback):
        """Register a state change listener."""

        self._listeners.append(callback)

    def remove_listener(self, callback):
        """Unregister a state change listener."""

        try:
            self._listeners.remove(callback)
        except ValueError:
            pass

    def notify(self):
        """Notify all listeners."""

        for callback in self._listeners:
            callback(self)

    # ==========================================================
    # Tools
    # ==========================================================

    def set_tool(self, tool):
        """Get the active tool."""

        self.current_tool = tool
        self.notify()

    def get_tool(self):
        """Set the active tool."""

        return self.current_tool

    # ==========================================================
    # Layers
    # ==========================================================

    def get_layers(self):
        """Get all layers or an empty list."""

        if not self.current_format:
            return []

        return self.current_format.layers

    def get_selected_layer(self):
        """Get the currently selected layer."""

        layers = self.get_layers()

        if not layers:
            return None

        index = max(0, min(self.selected_layer_index, len(layers) - 1))

        return layers[index]

    def set_selected_layer(self, index: int):
        """Get the selected layer index."""

        layers = self.get_layers()

        if not layers:
            self.selected_layer_index = 0
        else:
            self.selected_layer_index = max(0, min(index, len(layers) - 1))
        self.notify()

    def update_layer_opacity(self, layer, opacity: int):
        """Update the opacity of a layer."""

        layer.opacity = max(0, min(opacity, 100))
        self.notify()

    def update_layer_visibility(self, layer, visible: bool):
        """Set layer visibility."""

        layer.visible = visible
        self.notify()

    def update_layer_name(self, layer, name: str):
        """Set layer name."""

        if layer:
            layer.name = name
            self.notify()

    def remove_selected_layer(self):
        """Remove the selected layer and adjust index."""

        layers = self.get_layers()

        if not layers:
            return

        index = self.selected_layer_index

        # Delete layer
        layers.pop(index)

        # Adjust selection index
        if layers:
            self.selected_layer_index = max(0, min(index, len(layers) - 1))
        else:
            self.selected_layer_index = 0

        self.notify()

    # ==========================================================
    # Brushes
    # ==========================================================

    def get_brush(self):
        """Get the current brush."""

        return self.current_brush

    def set_brush(self, brush):
        """Set the current brush."""

        self.current_brush = brush
        if self.current_brush:
            self.current_brush.brush_color = self.current_color
        self.notify()

    def update_brush_size(self, size: int):
        """Update the current brush size."""

        if self.current_brush:
            self.current_brush.brush_type.base_size = max(1, int(size))
            self.notify()

    def update_brush_opacity(self, opacity: int):

        """Update the current brush opacity."""

        if self.current_brush:
            self.current_brush.brush_type.base_opacity = max(0, min(100, int(opacity)))
            self.notify()

    def update_brush_color(self, color: tuple):
        """Update the current brush color."""

        if self.current_brush:
            # Save the color for the brush
            self.current_brush.brush_color = color
            self.notify()

    # ==========================================================
    # Filters
    # ==========================================================

    def update_layer_filter_param(self, param_name, value):
        """Update the current layer filter parameter."""

        layer = self.get_selected_layer()

        if not layer:
            return

        if not hasattr(layer, "filter_params"):
            layer.filter_params = {}

        layer.filter_params[param_name] = value
        self.notify()


    def set_layer_filter(self, filter_id: str):
        """Set the filter ID for the currently selected layer."""

        layer = self.get_selected_layer()

        if layer:
            layer.filter_id = filter_id

            # Ensure filter_params exists
            if not hasattr(layer, "filter_params") or layer.filter_params is None:
                layer.filter_params = {}
            self.notify()

    # ==========================================================
    # Color
    # ==========================================================
    def set_color(self, color: tuple):
        """Set active color and update history."""

        self.current_color = color
        self._push_recent_color(color)

        # Sync with brush automatically
        if self.current_brush:
            self.current_brush.brush_color = color

        self.notify()

    def get_color(self):
        """Get active color."""

        return self.current_color

    def get_recent_colors(self):
        """Get all recent colors."""

        return self.recent_colors

    def _push_recent_color(self, color):
        """Push recent color if the color is set."""

        if color in self.recent_colors:
            self.recent_colors.remove(color)

        self.recent_colors.insert(0, color)
        self.recent_colors = self.recent_colors[:10]

    # ==========================================================
    # Selection
    # ==========================================================
    def clear_selection(self):
        """Clear the active selection mask."""

        self.selection_mask = None
        self.notify()

    def has_selection(self) -> bool:
        """Return True when there is an active non-empty selection."""

        if self.selection_mask is None:
            return False
        return self.selection_mask.getbbox() is not None

    def get_selection_mask(self, size=None):
        """Return the current selection mask, optionally resized to the given size."""

        if self.selection_mask is None:
            return None

        if size is None or self.selection_mask.size == size:
            return self.selection_mask

        return self.selection_mask.resize(size, Image.NEAREST)

    def set_selection_mask(self, mask: Image.Image | None):
        """Set the current selection mask as a binary L image."""

        if mask is None:
            self.selection_mask = None
            self.notify()
            return

        self.selection_mask = mask.convert("L")
        self.notify()

    # ==========================================================
    # Threshold Filters
    # ==========================================================

    def set_active_threshold_filters(self, filters: list[str]):
        """Set active threshold filters selected from dialog."""

        self._active_threshold_filters = filters

        # Inicializar parámetros si no existen
        for fid in filters:
            if fid not in self._threshold_params:
                self._threshold_params[fid] = {"value": 127}

        # limpiar los que ya no están activos
        for fid in list(self._threshold_params.keys()):
            if fid not in filters:
                del self._threshold_params[fid]

        self.notify()

    def get_active_threshold_filters(self) -> list[str]:
        """Return currently active threshold filters."""

        return self._active_threshold_filters

    def set_threshold_param(self, filter_id: str, param: str, value: int):
        """Update a parameter for a threshold filter."""

        if filter_id not in self._threshold_params:
            self._threshold_params[filter_id] = {}

        self._threshold_params[filter_id][param] = value
        self.notify()

    def get_threshold_params(self) -> dict[str, dict]:
        """Return all threshold parameters."""

        return self._threshold_params

    def reset_threshold_params(self):
        """Reset all threshold params to default values."""

        for fid in self._threshold_params:
            self._threshold_params[fid] = {"value": 127}

        self.notify()

