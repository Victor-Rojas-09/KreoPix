import tkinter as tk

class ToolsPanel(tk.Frame):
    """Left panel containing editor tools."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, width=120, bg="#2c2c2c")

        self._build()

    def _build(self):
        """Create tool buttons."""

        tk.Label(
            self,
            text="Tools",
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        tk.Button(self, text="Brush").pack(fill="x", pady=5)
        tk.Button(self, text="Eraser").pack(fill="x", pady=5)
        tk.Button(self, text="Select").pack(fill="x", pady=5)