import tkinter as tk

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
        if self.controller:
            self.controller.state.current_tool = "brush"

            from services.brushes.normal_brush import NormalBrush
            self.controller.state.set_brush(NormalBrush())

    def _select_eraser(self):
        if self.controller:
            self.controller.state.current_tool = "brush"

            from services.brushes.eraser_brush import EraserBrush
            self.controller.state.set_brush(EraserBrush())

    def _select_select(self):
        if self.controller:
            self.controller.state.current_tool = "select"
