import tkinter as tk
from ui.utils.components.color_panel import ColorPanel
from ui.utils.components.layers_panel import LayersPanel
from ui.utils.components.brush_panel import BrushPanel

class RightSidebar(tk.Frame):
    """Right sidebar containing color, layers and brush panels."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, width=260, bg="#3a3a3a")
        self.controller = controller

        self._configure_grid()
        self._build_panels()

    def _configure_grid(self):
        """Configure sidebar layout."""

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def _build_panels(self):
        """Create sidebar panels."""

        self.color_panel = ColorPanel(self, self.controller)
        self.color_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.layers_panel = LayersPanel(self, controller=self.controller)
        self.layers_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.brush_panel = BrushPanel(self, self.controller)
        self.brush_panel.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
