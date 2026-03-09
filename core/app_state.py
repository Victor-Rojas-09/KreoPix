class AppState:
    """
    Global application state.
    Stores the currently opened project and editor state.
    """

    def __init__(self):
        self.current_project = None
        self.selected_layer_index = 0

    # ==========================================================
    #  Project
    # ==========================================================

    def set_project(self, project):
        self.current_project = project
        self.selected_layer_index = 0

    def get_project(self):
        return self.current_project

    # ==========================================================
    #  Layers
    # ==========================================================

    def get_layers(self):
        if not self.current_project:
            return []
        return self.current_project.layers

    def get_selected_layer(self):
        if not self.current_project:
            return None
        return self.current_project.layers[self.selected_layer_index]

    def set_selected_layer(self, index):
        self.selected_layer_index = index

    # ==========================================================
    #  Extra
    # ==========================================================

    def has_project(self):
        return self.current_project is not None

    def clear_project(self):
        self.current_project = None