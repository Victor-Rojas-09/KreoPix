import tkinter as tk

from core.state.app_state import AppState
from core.recent_manager import RecentManager
from services.file_service import FileService
from controllers.app_controller import AppController
from ui.layout.main_layout import MainLayout
from ui.layout.menubar import MenuBar


class AppRoot:
    """
    Application bootstrapper.
    Responsible for assembling all layers.
    """

    # ==========================================================
    # CLASS CONSTRUCTOR
    # ==========================================================

    def __init__(self):

        # Init the main Window
        self.root = tk.Tk()
        self.root.title("KreoPix")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Core Layer
        self.state = AppState()
        self.recent_manager = RecentManager()

        # Services Layer
        self.file_service = FileService()

        # UI Layer
        self.layout = MainLayout(self.root)

        # Controller Layer
        self.controller = AppController(
            root=self.root,
            layout=self.layout,
            state=self.state,
            file_service=self.file_service,
            recent_manager=self.recent_manager
        )

        # Connect UI with the Controller
        self.layout.set_controller(self.controller)

        MenuBar(self.root, self.controller)

        # Initial Screen Home
        self.controller.load_home()

        # Window close
        self.root.protocol("WM_DELETE_WINDOW", self.controller.request_exit)

    # ==========================================================
    # Public API
    # ==========================================================

    def run(self):
        """Start application loop."""

        self.root.mainloop()