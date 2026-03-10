from core.image.image_format import ImageFormat

class AppState:
    """
    Global application state compatible con ImageFormat.
    Mantiene compatibilidad con el código antiguo usando current_project.
    """

    def __init__(self):
        """Initialize the AppState with no document and the first layer selected."""
        # Nuevo núcleo
        self.current_format: ImageFormat | None = None

        # Para compatibilidad con código antiguo
        self.current_project = None

        # Índice de capa seleccionada
        self.selected_layer_index: int = 0

        # (Opcional) herramienta activa
        self.current_tool = None

    # ==========================================================
    # Document / Project
    # ==========================================================

    def set_format(self, image_format: ImageFormat):
        """Set the current ImageFormat and reset the selected layer."""
        self.current_format = image_format
        self.selected_layer_index = 0

        # Mantener compatibilidad con current_project
        self.current_project = image_format

    def get_format(self) -> ImageFormat | None:
        """Return the current ImageFormat."""
        return self.current_format

    def set_project(self, project):
        """Compatibilidad: se comporta igual que set_format."""
        self.set_format(project)

    def get_project(self):
        """Compatibilidad: devuelve current_format."""
        return self.get_format()

    # ==========================================================
    # Layers
    # ==========================================================

    def get_layers(self):
        """Return list of layers, empty list if no document."""
        if not self.current_format:
            return []
        return self.current_format.layers

    def get_selected_layer(self):
        """Return the currently selected layer, or None if no document."""
        layers = self.get_layers()
        if not layers:
            return None
        index = max(0, min(self.selected_layer_index, len(layers)-1))
        return layers[index]

    def set_selected_layer(self, index: int):
        """Set selected layer by index, clamped to valid range."""
        layers = self.get_layers()
        if not layers:
            self.selected_layer_index = 0
        else:
            self.selected_layer_index = max(0, min(index, len(layers)-1))

    # ==========================================================
    # Extras
    # ==========================================================

    def has_format(self) -> bool:
        return self.current_format is not None

    def has_project(self) -> bool:
        """Compatibilidad: True si hay current_format"""
        return self.has_format()

    def clear_format(self):
        """Clear the current ImageFormat."""
        self.current_format = None
        self.selected_layer_index = 0
        self.current_project = None

    def clear_project(self):
        """Compatibilidad: limpiar proyecto antiguo."""
        self.clear_format()