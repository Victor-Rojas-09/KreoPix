import tkinter as tk
from tkinter import ttk
from utils.window_positioner import WindowPositioner


class NewProjectDialog(tk.Toplevel):
    """Dialog for new project."""

    def __init__(self, parent, on_confirm):
        """Initialize dialog."""

        super().__init__(parent)

        self.parent = parent
        self.on_confirm = on_confirm

        self.title("New Project")
        self.resizable(False, False)

        WindowPositioner.center_to_parent(self, parent, 340, 220)

        self.transient(parent)
        self.grab_set()

        self._build()

    def _build(self):
        """Build dialog UI."""

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Create New Canvas",
            font=("Arial", 14)
        ).pack(pady=(0, 15))
        self._build_inputs(container)
        self._build_buttons(container)


    def _build_inputs(self, parent):
        """Create size inputs."""

        form = ttk.Frame(parent)
        form.pack(fill="x")

        ttk.Label(form, text="Width").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Height").grid(row=1, column=0, sticky="w")

        self.width_var = tk.IntVar(value=800)
        self.height_var = tk.IntVar(value=600)

        ttk.Entry(
            form,
            textvariable=self.width_var,
            width=10
        ).grid(row=0, column=1, pady=5)

        ttk.Entry(
            form,
            textvariable=self.height_var,
            width=10
        ).grid(row=1, column=1, pady=5)

        ttk.Label(form, text="px").grid(row=0, column=2)
        ttk.Label(form, text="px").grid(row=1, column=2)

    def _build_buttons(self, parent):
        """Create dialog buttons."""

        buttons = ttk.Frame(parent)
        buttons.pack(fill="x", pady=(20, 0))

        ttk.Button(
            buttons,
            text="Cancel",
            command=self.destroy
        ).pack(side="right", padx=5)

        ttk.Button(
            buttons,
            text="Create",
            command=self._confirm
        ).pack(side="right")

    def _confirm(self):
        """Confirm project creation."""

        width = self.width_var.get()
        height = self.height_var.get()

        if width <= 0 or height <= 0:
            return

        self.on_confirm(width, height)

        self.destroy()