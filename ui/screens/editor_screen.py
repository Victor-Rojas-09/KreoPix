import tkinter as tk

from ui.panels.tools_panel import ToolsPanel
from ui.panels.canvas_panel import CanvasPanel
from ui.panels.right_sidebar import RightSidebar


class EditorScreen(tk.Frame):
    """Main editor layout."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)

        self.controller = controller

        self._configure_grid()
        self._create_panels()

    # ==================================================
    # Layout
    # ==================================================

    def _configure_grid(self):
        """Configure main editor proportions."""

        # Layout igual al original
        self.columnconfigure(0, weight=0)  # tools
        self.columnconfigure(1, weight=1)  # canvas
        self.columnconfigure(2, weight=0)  # sidebar

        self.rowconfigure(0, weight=1)

    def _create_panels(self):
        """Create UI panels."""

        # Tools
        self.tools_panel = ToolsPanel(self, self.controller)
        self.tools_panel.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        # Canvas
        self.canvas_panel = CanvasPanel(self, self.controller)
        self.canvas_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # Sidebar
        self.right_sidebar = RightSidebar(self, self.controller)
        self.right_sidebar.grid(
            row=0,
            column=2,
            sticky="ns"
        )

    # ==================================================
    # API
    # ==================================================

    def load_project(self, image_format):
        self.controller.state.set_format(image_format)
        # No need to call load_layers manually, listeners handle it
        self.refresh()

    # ==================================================
    # Refresh
    # ==================================================

    def refresh(self):
        if not self.controller.state.has_format():
            return

        image = self.controller.state.current_format.composite()
        self.canvas_panel.display_image(image)

