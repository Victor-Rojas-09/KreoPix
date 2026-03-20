import tkinter as tk
from tkinter import colorchooser

class ColorPanel(tk.Frame):
    """Color selection panel."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self._build()

    def _build(self):
        tk.Label(self, text="Color", bg="#444", fg="white").pack(pady=5)

        self.color_display = tk.Canvas(self, bg="black", width=50, height=50)
        self.color_display.pack(pady=10)

        tk.Button(self, text="Pick Color", command=self._open_color_picker).pack(pady=5)

    def _open_color_picker(self):
        result = colorchooser.askcolor(initialcolor="#000000")
        if result and result[0]:
            r, g, b = map(int, result[0])
            a = 255
            color = (r, g, b, a)
            self.color_display.config(bg=result[1])
            if self.controller:
                self.controller.request_update_brush_color(color)
