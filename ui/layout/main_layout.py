import tkinter as tk

from ui.screens.home_screen import HomeScreen
from ui.screens.editor_screen import EditorScreen


class MainLayout(tk.Frame):
    """Main screen container."""

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.controller = None
        self.current_screen = None

    # ---------- Public API ----------

    def set_controller(self, controller):
        """Attach app controller."""
        self.controller = controller

    def show(self, screen_name):
        """Display selected screen."""
        if self.current_screen:
            self.current_screen.destroy()

        if screen_name == "home":
            self.current_screen = HomeScreen(self, self.controller)

        elif screen_name == "editor":
            self.current_screen = EditorScreen(self, self.controller)

        self.current_screen.pack(fill="both", expand=True)

    def load_project_into_editor(self, project):
        """Pass project to editor."""
        if isinstance(self.current_screen, EditorScreen):
            self.current_screen.load_project(project)