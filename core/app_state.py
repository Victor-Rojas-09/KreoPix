class AppState:
    """Application state container."""

    def __init__(self):
        self.current_project = None

    def has_project(self):
        return self.current_project is not None

    def set_project(self, project):
        self.current_project = project

    def clear_project(self):
        self.current_project = None