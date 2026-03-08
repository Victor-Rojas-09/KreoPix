import tkinter as tk
from PIL import Image

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

    def load_project(self, project):
        """Load project into editor."""

        self.controller.state.set_project(project)

        layers = self.controller.state.get_layers()

        self.right_sidebar.layers_panel.load_layers(layers)

        self.refresh()

    # ==================================================
    # Refresh
    # ==================================================

    def refresh(self):
        """Mix layers and update the canvas."""
        project = self.controller.state.get_project()
        if not project or not hasattr(project, 'width'):
            return

        # Background
        base = Image.new("RGBA", (project.width, project.height), (0, 0, 0, 0))

        # Mix layers
        layers = project.get_layers() if hasattr(project, 'get_layers') else project.layers
        for layer in layers:
            if layer.visible:
                base.alpha_composite(layer.image)

        # Update canvas
        self.canvas_panel.display_image(base)