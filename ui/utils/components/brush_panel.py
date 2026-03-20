import tkinter as tk
from services.brushes.presets import (
    create_airbrush,
    create_hard_brush,
    create_eraser
)

class BrushPanel(tk.Frame):
    """Brush selection panel with icons and sliders."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#666")
        self.controller = controller
        self._build()

    def _build(self):
        """Build the panel."""

        tk.Label(self, text="Brushes", bg="#666", fg="white").pack(pady=5)

        brushes = [
            {"factory": create_hard_brush, "name": "Hard"},
            {"factory": create_airbrush, "name": "Airbrush"},
            {"factory": create_eraser, "name": "Eraser"},
        ]

        for b in brushes:
            btn = tk.Button(
                self,
                text=b["name"],
                command=lambda f=b["factory"]: self._select_brush(f)
            )
            btn.pack(pady=3, fill="x")

    def _select_brush(self, factory):
        """Select a brush from the services."""

        color = (0, 0, 0, 255)

        brush = factory(color) if factory != create_eraser else factory()
        self.controller.state.set_brush(brush)
