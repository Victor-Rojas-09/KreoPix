import tkinter as tk

from ui.widgets.helpers import WindowPositioner


class ConfirmExitDialog(tk.Toplevel):
    """Exit confirmation dialog."""

    def __init__(self, parent, on_confirm):
        super().__init__(parent)

        self.on_confirm = on_confirm

        self.title("Exit KreoPix")
        self.resizable(False, False)

        try:
            self.iconbitmap("assets/app/LOGO.ico")
        except tk.TclError:
            pass

        WindowPositioner.center_to_parent(self, parent, 320, 140)

        self.transient(parent)
        self.grab_set()

        self.configure(bg="#2b2b2b")

        outer = tk.Frame(self, bg="#2b2b2b")
        outer.pack(expand=True, fill="both")

        content = tk.Frame(outer, bg="#2b2b2b", padx=10, pady=10)
        content.pack(expand=True)

        tk.Label(
            content,
            text="Are you sure you want to exit?",
            bg="#2b2b2b",
            fg="#f0f0f0",
            font=("Segoe UI", 10),
            anchor="center",
            justify="center",
        ).pack(pady=(0, 16))

        btn_row = tk.Frame(content, bg="#2b2b2b")
        btn_row.pack()

        tk.Button(
            btn_row,
            text=" Exit ",
            command=self._confirm,
            bg="#606060",
            fg="#ffffff",
            relief="flat",
            padx=14,
            pady=6,
        ).pack(side="left", padx=5)

        tk.Button(
            btn_row,
            text="Cancel",
            command=self.destroy,
            bg="#404040",
            fg="#f0f0f0",
            relief="flat",
            padx=14,
            pady=6,
        ).pack(side="left", padx=5)

    def _confirm(self):
        """Confirm exit of the window to destroy."""

        self.on_confirm()
        self.destroy()