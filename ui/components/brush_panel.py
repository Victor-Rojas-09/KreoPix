import tkinter as tk


class BrushPanel(tk.Frame):
    """Brush selection panel."""

    def __init__(self, parent):
        super().__init__(parent, bg="#666")

        self._build()

    def _build(self):

        tk.Label(
            self,
            text="Brushes",
            bg="#666",
            fg="white"
        ).pack(pady=5)

        tk.Button(self, text="Round").pack(pady=3)
        tk.Button(self, text="Soft").pack(pady=3)
        tk.Button(self, text="Hard").pack(pady=3)