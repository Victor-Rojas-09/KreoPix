import tkinter as tk

from ui.utils.tools.window_positioner import WindowPositioner

class ConfirmExitDialog(tk.Toplevel):
    """Exit confirmation dialog."""

    def __init__(self, parent, on_confirm):
        super().__init__(parent)

        self.on_confirm = on_confirm

        self.title("Exit")
        self.resizable(False, False)

        WindowPositioner.center_to_parent(self, parent, 200, 150)

        self.transient(parent)
        self.grab_set()

        tk.Label(
            self,
            text="Are you sure you want to exit?"
        ).pack(pady=20)

        tk.Button(
            self,
            text="Cancel",
            command=self.destroy
        ).pack(side="left", padx=20, pady=10)

        tk.Button(
            self,
            text="Exit",
            command=self._confirm
        ).pack(side="right", padx=20, pady=10)

    def _confirm(self):
        self.on_confirm()
        self.destroy()