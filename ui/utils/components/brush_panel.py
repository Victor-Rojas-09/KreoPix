import tkinter as tk
import os

from services.brushes.presets import (
    create_airbrush,
    create_hard_brush,
    create_eraser
)


class BrushPanel(tk.Frame):
    """Brush selection panel with icon-only buttons."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#666")
        self.controller = controller


        self.icons = []

        self._build()

    def _build(self):
        """Build the panel."""

        tk.Label(self, text="Brushes", bg="#666", fg="white").pack(pady=5)

        # Import the image
        base_dir = os.path.dirname(__file__)
        icons_dir = os.path.join(base_dir, "../../../", "assets", "icons")

        brushes = [
            {"factory": create_hard_brush, "icon": "hard.png"},
            {"factory": create_airbrush, "icon": "airbrush.png"},
            {"factory": create_eraser, "icon": "eraser.png"},
        ]

        for b in brushes:
            icon_path = os.path.join(icons_dir, b["icon"])

            icon = tk.PhotoImage(file=icon_path)

            icon = icon.subsample(8)

            self.icons.append(icon)

            btn = tk.Button(
                self,
                image=icon,
                bg="#777",
                activebackground="#999",
                relief="flat",
                command=lambda f=b["factory"]: self._select_brush(f)
            )

            btn.pack(pady=4)

    def _select_brush(self, factory):
        """Select a brush from the services."""

        color = (0, 0, 0, 255)

        brush = factory(color) if factory != create_eraser else factory()

        self.controller.state.set_brush(brush)