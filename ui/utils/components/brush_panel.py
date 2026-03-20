# ui/utils/components/brush_panel.py
import tkinter as tk
from services.brushes.normal_brush import NormalBrush
from services.brushes.eraser_brush import EraserBrush
from services.brushes.opacity_brush import OpacityBrush

class BrushPanel(tk.Frame):
    """Brush selection panel with icons and sliders."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#666")
        self.controller = controller
        self._build()

    def _build(self):
        tk.Label(self, text="Brushes", bg="#666", fg="white").pack(pady=5)

        # Brush buttons
        brushes = [
            {"class": NormalBrush, "name": "Normal", "icon": None},
            {"class": EraserBrush, "name": "Eraser", "icon": None},
            {"class": OpacityBrush, "name": "Opacity", "icon": None},
        ]

        for b in brushes:
            btn = tk.Button(
                self,
                text=b["name"],
                command=lambda cls=b["class"]: self._select_brush(cls)
            )
            btn.pack(pady=3, fill="x")

    def _select_brush(self, brush_class):
        brush = brush_class()
        self.controller.state.set_brush(brush)
