from core.image.image_format import ImageFormat
from services.brushes.presets import create_hard_brush


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

    # -------------------------
    # Document
    # -------------------------
    def get_format(self) -> ImageFormat | None:
        """Get the active document."""

        return self.current_format

    def set_format(self, image_format: ImageFormat):
        """Set the active document and reset layer selection."""

        self.current_format = image_format
        self.selected_layer_index = 0
        self.current_project = image_format
        self._notify()

    def clear_format(self):
        """Remove the active document."""

        self.current_format = None
        self.selected_layer_index = 0
        self.current_project = None
        self._notify()

    def has_format(self) -> bool:
        """Return True if a document is loaded."""
        return self.current_format is not None

    # -------------------------
    # UI
    # -------------------------
    def add_listener(self, callback):
        """Register a state change listener."""

        self._listeners.append(callback)

    def _notify(self):
        """Notify all listeners."""

        for cb in self._listeners:
            cb(self)

    # -------------------------
    # Tools
    # -------------------------
    def set_tool(self, tool):
        """Get the active tool."""

        self.current_tool = tool
        self._notify()

    def get_tool(self):
        """Set the active tool."""

        return self.current_tool

    # -------------------------
    # Layers
    # -------------------------
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
        self._notify()

    def update_layer_opacity(self, layer, opacity: int):
        """Update the opacity of a layer."""
        layer.opacity = max(0, min(opacity, 100))
        self._notify()

    def update_layer_visibility(self, layer, visible: bool):
        """Set layer visibility."""

        layer.visible = visible
        self._notify()

    def update_layer_name(self, layer, name: str):
        """Set layer name."""

        if layer:
            layer.name = name
            self._notify()

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

        self._notify()

    # -------------------------
    # Brushes
    # -------------------------
    def get_brush(self):
        """Get the active brush."""

        return self.current_brush

    def set_brush(self, brush):
        """Set the active brush."""

        self.current_brush = brush
        self._notify()

    def update_brush_size(self, size: int):
        """Set brush size (min 1)."""

        if self.current_brush:
            self.current_brush.dynamics.base_size = max(1, int(size))
            self._notify()

    def update_brush_opacity(self, opacity: int):
        """Set brush opacity (0–100)."""

        if self.current_brush:
            self.current_brush.dynamics.base_opacity = max(0, min(100, int(opacity)))
            self._notify()

    def update_brush_color(self, color: tuple):
        """Set brush color and clear cache."""

        if self.current_brush:
            self.current_brush.tip.color = color
            self.current_brush.tip._cache.clear()
            self._notify()