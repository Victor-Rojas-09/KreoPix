
import tkinter as tk


class MainLayout(tk.Frame):
    """Main Layout for the screen control."""

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True)

    def set_screen(self, screen_class, controller=None):
        """Destroy the last window."""
        for widget in self.content.winfo_children():
            widget.destroy()

        """Create a new window."""
        screen = screen_class(self.content, controller=controller)
        screen.pack(fill="both", expand=True)