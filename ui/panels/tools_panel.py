import tkinter as tk

from core.brush.presets import (
    create_hard_brush,
    create_eraser
)


class ToolsPanel(tk.Frame):
    """Left panel containing editor tools."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, width=120, bg="#2c2c2c")
        self.controller = controller
        self._build()

    def _build(self):
        """Create tool buttons."""

        tk.Label(
            self,
            text="Tools",
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        tk.Button(self, text="Brush", command=self._select_brush).pack(fill="x", pady=5)
        tk.Button(self, text="Eraser", command=self._select_eraser).pack(fill="x", pady=5)
        tk.Button(self, text="Select", command=self._select_select).pack(fill="x", pady=5)

    def _select_brush(self):
        """Select painting tool with default brush."""

        if not self.controller:
            return

        # Set as active tool
        self.controller.state.set_tool("brush")

        color = (0, 0, 0, 255)

        brush = create_hard_brush(color)

        # Assign to state
        self.controller.state.set_brush(brush)

    def _select_eraser(self):
        """Select eraser tool."""

        if not self.controller:
            return

        self.controller.state.set_tool("brush")

        brush = create_eraser()

        self.controller.state.set_brush(brush)

    def _select_select(self):
        """Select selection tool."""

        if not self.controller:
            return

        self.controller.state.set_tool("select")
