import tkinter as tk


class NewProjectDialog(tk.Toplevel):
    """Canvas size dialog."""

    def __init__(self, parent, on_confirm):
        super().__init__(parent)

        self.on_confirm = on_confirm

        self.title("New Project")
        self.transient(parent)
        self.grab_set()

        self._build()

    def _build(self):
        tk.Label(self, text="Width (px):").pack()
        self.width_entry = tk.Entry(self)
        self.width_entry.pack()

        tk.Label(self, text="Height (px):").pack()
        self.height_entry = tk.Entry(self)
        self.height_entry.pack()

        tk.Button(
            self,
            text="Create",
            command=self._confirm
        ).pack(pady=10)

    def _confirm(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.on_confirm(width, height)
            self.destroy()
        except ValueError:
            pass