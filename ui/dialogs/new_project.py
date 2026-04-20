import tkinter as tk

from ui.widgets.helpers import WindowPositioner


class NewProjectDialog(tk.Toplevel):
    """Dialog for creating a new project with name and canvas size."""

    def __init__(self, parent, on_confirm):
        """Initialize dialog."""

        super().__init__(parent)

        self.parent = parent
        self.on_confirm = on_confirm

        self.title("New Project")
        self.resizable(False, False)

        try:
            self.iconbitmap("assets/app/LOGO.ico")
        except tk.TclError:
            pass

        WindowPositioner.center_to_parent(self, parent, 380, 280)

        self.transient(parent)
        self.grab_set()

        self._build()

    def _build(self):
        """Build dialog UI."""

        outer = tk.Frame(self, bg="#2b2b2b")
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg="#2b2b2b")
        header.pack(fill="x", padx=20, pady=(20, 8))

        tk.Label(
            header,
            text="New project",
            font=("Segoe UI", 16, "bold"),
            bg="#2b2b2b",
            fg="#f0f0f0",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Choose a name and canvas size",
            font=("Segoe UI", 9),
            bg="#2b2b2b",
            fg="#aaaaaa",
        ).pack(anchor="w", pady=(4, 0))

        form = tk.Frame(outer, bg="#2b2b2b")
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Project name", bg="#2b2b2b", fg="#e0e0e0").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )
        self.name_var = tk.StringVar(value="Untitled")
        name_entry = tk.Entry(
            form,
            textvariable=self.name_var,
            width=32,
            font=("Segoe UI", 10),
            bg="#3c3c3c",
            fg="#f0f0f0",
            insertbackground="#ffffff",
            relief="flat",
        )
        name_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 14))

        tk.Label(form, text="Width", bg="#2b2b2b", fg="#e0e0e0").grid(row=2, column=0, sticky="w")
        tk.Label(form, text="Height", bg="#2b2b2b", fg="#e0e0e0").grid(row=3, column=0, sticky="w")

        self.width_var = tk.IntVar(value=800)
        self.height_var = tk.IntVar(value=600)

        tk.Entry(
            form,
            textvariable=self.width_var,
            width=12,
            bg="#3c3c3c",
            fg="#f0f0f0",
            insertbackground="#ffffff",
            relief="flat",
        ).grid(row=2, column=1, padx=(12, 4), pady=4, sticky="w")

        tk.Entry(
            form,
            textvariable=self.height_var,
            width=12,
            bg="#3c3c3c",
            fg="#f0f0f0",
            insertbackground="#ffffff",
            relief="flat",
        ).grid(row=3, column=1, padx=(12, 4), pady=4, sticky="w")

        tk.Label(form, text="px", bg="#2b2b2b", fg="#888888").grid(row=2, column=2, sticky="w")
        tk.Label(form, text="px", bg="#2b2b2b", fg="#888888").grid(row=3, column=2, sticky="w")

        buttons = tk.Frame(outer, bg="#2b2b2b")
        buttons.pack(fill="x", padx=20, pady=(8, 20))

        tk.Button(
            buttons,
            text="Cancel",
            command=self.destroy,
            bg="#404040",
            fg="#f0f0f0",
            activebackground="#505050",
            relief="flat",
            padx=16,
            pady=6,
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            buttons,
            text="Create",
            command=self._confirm,
            bg="#0e639c",
            fg="#ffffff",
            activebackground="#1177bb",
            relief="flat",
            padx=16,
            pady=6,
        ).pack(side="right")

    def _confirm(self):
        """Confirm project creation."""

        width = self.width_var.get()
        height = self.height_var.get()
        name = (self.name_var.get() or "").strip() or "Untitled"

        if width <= 0 or height <= 0:
            return

        self.on_confirm(width, height, name)

        self.destroy()
