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

    def set_controller(self, controller):
        """Attach app controller."""

        self.controller = controller

    def show(self, screen_name):
        """Display selected screen. Keeps EditorScreen alive when already on editor."""

        if screen_name == "editor":
            if isinstance(self.current_screen, EditorScreen):
                return
            if self.current_screen:
                self.current_screen.destroy()
            self.current_screen = EditorScreen(self, self.controller)
            self.current_screen.pack(fill="both", expand=True)
            return

        if screen_name == "home":
            if self.current_screen:
                self.current_screen.destroy()
            self.current_screen = HomeScreen(self, self.controller)
            self.current_screen.pack(fill="both", expand=True)
            return

    def load_project_into_editor(self, project):
        """Legacy hook; projects load via tab sessions."""

        if isinstance(self.current_screen, EditorScreen):
            self.current_screen.sync_from_controller()
