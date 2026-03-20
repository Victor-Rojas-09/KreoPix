from core.image.image_format import ImageFormat
from services.brushes.normal_brush import NormalBrush

class AppState:
    """Global application state managing document, layers and tools."""

    def __init__(self):
        """Initialize with no document and no selected layer."""

        self.current_format: ImageFormat | None = None
        self.current_project = None
        self.selected_layer_index: int = 0
        self.current_tool = None
        self._listeners = []

        self.current_brush = NormalBrush()

    # -------------------------
    # Document
    # -------------------------
    def set_format(self, image_format: ImageFormat):
        """Set current document and reset selected layer."""

        self.current_format = image_format
        self.selected_layer_index = 0
        self.current_project = image_format
        self._notify()

    def get_format(self) -> ImageFormat | None:
        """Return current document."""

        return self.current_format

    def clear_format(self):
        """Clear current document."""

        self.current_format = None
        self.selected_layer_index = 0
        self.current_project = None
        self._notify()

    # -------------------------
    # Layers
    # -------------------------
    def get_layers(self):
        """Return all layers, empty list if none."""
        if not self.current_format:
            return []
        return self.current_format.layers

    def get_selected_layer(self):
        """Return selected layer or None."""
        layers = self.get_layers()
        if not layers:
            return None
        index = max(0, min(self.selected_layer_index, len(layers)-1))
        return layers[index]

    def set_selected_layer(self, index: int):
        """Set selected layer index (clamped)."""
        layers = self.get_layers()
        if not layers:
            self.selected_layer_index = 0
        else:
            self.selected_layer_index = max(0, min(index, len(layers)-1))
        self._notify()

    # -------------------------
    # Tools
    # -------------------------
    def set_tool(self, tool):
        """Set active tool."""

        self.current_tool = tool
        self._notify()

    def get_tool(self):
        """Return active tool."""

        return self.current_tool

    # -------------------------
    # Helpers
    # -------------------------
    def has_format(self) -> bool:
        """True if a document is loaded."""
        return self.current_format is not None

    # -------------------------
    # UI
    # -------------------------
    def add_listener(self, callback):
        """Register a UI listener for state changes."""
        self._listeners.append(callback)

    def _notify(self):
        """Notify all listeners of state change."""
        for cb in self._listeners:
            cb(self)

    def update_layer_opacity(self, layer, opacity: int):
        """Update opacity of a layer and notify UI."""
        layer.opacity = max(0, min(opacity, 100))
        self._notify()

    def update_layer_visibility(self, layer, visible: bool):
        """Update visibility of a layer and notify UI."""
        layer.visible = visible
        self._notify()

    def update_layer_name(self, layer, name: str):
        """Update layer name and notify UI."""
        if layer:
            layer.name = name
            self._notify()

    def remove_selected_layer(self):
        """Remove the currently selected layer and update selection."""

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

    def set_brush(self, brush):
        self.current_brush = brush
        self._notify()

    def get_brush(self):
        return self.current_brush

    def update_brush_size(self, size: int):
        if self.current_brush:
            self.current_brush.size = max(1, int(size))
            self._notify()

    def update_brush_opacity(self, opacity: int):
        if self.current_brush:
            self.current_brush.opacity = max(0, min(100, int(opacity)))
            self._notify()

    def update_brush_color(self, color: tuple):
        if self.current_brush:
            self.current_brush.color = color
            self._notify()