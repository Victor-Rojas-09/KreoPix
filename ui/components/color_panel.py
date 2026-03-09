import tkinter as tk

class ColorPanel(tk.Frame):
    """Color selection panel."""

    def __init__(self, parent):
        super().__init__(parent, bg="#444")

        self._build()

    def _build(self):

        tk.Label(
            self,
            text="Color",
            bg="#444",
            fg="white"
        ).pack(pady=5)

        tk.Canvas(
            self,
            bg="white"
        ).pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )