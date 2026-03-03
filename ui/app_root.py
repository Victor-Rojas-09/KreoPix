# ui/app_root.py
import tkinter as tk

from ui.layout.main_layout import MainLayout
from ui.layout.menubar import MenuBar
from ui.screens.home_screen import HomeScreen
from ui.screens.editor_screen import EditorScreen


class AppRoot:
    def __init__(self):
        """The app root."""

        self.root = tk.Tk()
        self.root.title("KreoPix")
        self.root.geometry("1000x700")

        """Create the main frame."""
        self.menubar = MenuBar(self.root)

        """Main Layout for the screens."""
        self.layout = MainLayout(self.root)

        """Initial Screen."""
        self.show_home()

    def show_home(self):
        """Show the home screen."""
        self.menubar.set_mode("home")
        self.layout.set_screen(HomeScreen, controller=self)

    def show_editor(self):
        """Show the editor screen."""
        self.menubar.set_mode("editor")
        self.layout.set_screen(EditorScreen, controller=self)