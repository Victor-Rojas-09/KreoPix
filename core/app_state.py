class AppState:
    """
    Global application state.
    """

    def __init__(self):
        """Initialize the AppState with no project and the first layer selected."""

        self.current_project = None
        self.selected_layer_index = 0

    # ==========================================================
    #  Project
    # ==========================================================

    def set_project(self, project):
        """Set the current project and reset the selected layer to the first one."""

        self.current_project = project
        self.selected_layer_index = 0

    def get_project(self):
        """Return the current project."""

        return self.current_project

    # ==========================================================
    #  Layers
    # ==========================================================

    def get_layers(self):
        """Return the list of layers in the current project, or an empty list if no project."""

        if not self.current_project:
            return []
        return self.current_project.layers

    def get_selected_layer(self):
        """Return the currently selected layer, or None if no project."""

        if not self.current_project:
            return None
        return self.current_project.layers[self.selected_layer_index]

    def set_selected_layer(self, index):
        """Set the selected layer by index."""

        self.selected_layer_index = index

    # ==========================================================
    #  Extra
    # ==========================================================

    def has_project(self):
        """Return True if a project is loaded, False otherwise."""

        return self.current_project is not None

    def clear_project(self):
        """Clear the current project."""

        self.current_project = None