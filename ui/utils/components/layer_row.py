import tkinter as tk


class LayerRow(tk.Frame):
    """Single layer row widget with visibility toggle, selection highlight, and renaming."""

    def __init__(self, parent, layer, index, controller):
        super().__init__(parent, bg="#666", height=26)

        self.controller = controller
        self.layer = layer
        self.index = index

        self.visible_var = tk.BooleanVar(value=layer.visible)

        # Checkbox for visibility manage
        self.check = tk.Checkbutton(
            self,
            text="",
            variable=self.visible_var,
            command=self._toggle_visibility,
            bg="#666",
            fg="white",
            activebackground="#666",
            selectcolor="#666",
            highlightthickness=0,
            bd=0
        )

        self.check.place(relx=0.0, rely=0.0, relwidth=0.15, relheight=1.0)

        # Button for select a layer
        self.name_btn = tk.Button(
            self,
            text=self.layer.name,
            relief="flat",
            bg="#666",
            fg="white",
            activebackground="#555",
            command=self._select_layer
        )

        self.name_btn.place(relx=0.15, rely=0.0, relwidth=0.85, relheight=1.0)

        # rename
        self.name_btn.bind("<Double-Button-1>", self._rename_layer)

        self.bind("<Destroy>", self._on_destroy)

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------

    def _toggle_visibility(self):
        """Toggle layer visibility."""
        self.controller.state.update_layer_visibility(
            self.layer,
            self.visible_var.get()
        )

    def _select_layer(self):
        """Select this layer and update UI highlight."""

        # Evitar error si el widget ya fue destruido
        if not str(self):
            return

        self.controller.select_layer(self.index)

        # Reset the background
        for row in self.master.winfo_children():
            if isinstance(row, LayerRow):
                row.configure(bg="#666")
                if hasattr(row, "name_btn"):
                    row.name_btn.configure(bg="#666")

        # To underline
        self.configure(bg="#444")
        self.name_btn.configure(bg="#444")

    def _rename_layer(self, event):
        """Enable renaming of the layer on double click."""

        self.entry = tk.Entry(
            self,
            bg="#555",
            fg="white",
            insertbackground="white",
            bd=0
        )

        self.entry.insert(0, self.layer.name)

        self.entry.place(
            relx=0.15,
            rely=0.0,
            relwidth=0.85,
            relheight=1.0
        )

        self.entry.focus()

        self.entry.bind("<Return>", self._confirm_rename)
        self.entry.bind("<FocusOut>", self._confirm_rename)

    def _confirm_rename(self, event):
        """Confirm renaming and update layer name."""

        new_name = self.entry.get().strip()

        if new_name:
            self.layer.name = new_name

        self.entry.destroy()

        self.name_btn = tk.Button(
            self,
            text=self.layer.name,
            relief="flat",
            bg=self["bg"],
            fg="white",
            activebackground="#555",
            command=self._select_layer
        )

        self.name_btn.place(
            relx=0.15,
            rely=0.0,
            relwidth=0.85,
            relheight=1.0
        )

        self.name_btn.bind("<Double-Button-1>", self._rename_layer)

    def _on_destroy(self, event):
        """Cleanup to avoid invalid command errors when widget is destroyed."""

        self.check = None
        self.name_btn = None
