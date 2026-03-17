import tkinter as tk


class LayerRow(tk.Frame):
    """
    UI component representing a single row in the layers panel.
    """

    def __init__(self, parent, layer, index, controller):
        super().__init__(parent, bg="#666", height=26)

        self.controller = controller
        self.layer = layer
        self.index = index

        # reference to delayed click callback
        self._click_job = None

        self.visible_var = tk.BooleanVar(value=layer.visible)

        # visibility checkbox
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

        # layer name button
        self.name_btn = tk.Button(
            self,
            text=self.layer.name,
            relief="flat",
            bg="#666",
            fg="white",
            activebackground="#555"
        )

        self.name_btn.place(relx=0.15, rely=0.0, relwidth=0.85, relheight=1.0)

        # events
        self.name_btn.bind("<Button-1>", self._on_click)
        self.name_btn.bind("<Double-Button-1>", self._rename_layer)

    def _on_click(self, event):
        """
        Handles single click selection.
        """

        self._click_job = self.after(200, self._select_layer)

    def _select_layer(self):
        """Select the current layer."""

        try:
            self.controller.select_layer(self.index)
        except tk.TclError:
            pass

    def _rename_layer(self, event):
        """
        Activate inline rename for the layer.
        Cancels any pending single-click selection event.
        """

        if self._click_job:
            self.after_cancel(self._click_job)
            self._click_job = None

        self.entry = tk.Entry(
            self,
            bg="#555",
            fg="white",
            insertbackground="white",
            bd=0
        )

        self.entry.insert(0, self.layer.name)
        self.entry.select_range(0, "end")

        self.entry.place(relx=0.15, rely=0.0, relwidth=0.85, relheight=1.0)
        self.entry.focus()

        self.entry.bind("<Return>", self._confirm_rename)
        self.entry.bind("<FocusOut>", self._confirm_rename)

    def _confirm_rename(self, event):
        """Apply the new layer name."""

        new_name = self.entry.get().strip()

        if new_name:
            self.controller.state.update_layer_name(self.layer, new_name)

        self.entry.destroy()

    def _toggle_visibility(self):
        """Toggle the visibility state of the layer."""

        self.controller.state.update_layer_visibility(
            self.layer,
            self.visible_var.get()
        )

    def update(self, layer, index):
        """Update row content without recreating widget."""

        self.layer = layer
        self.index = index

        # Update name
        self.name_btn.config(text=layer.name)

        # Update visibility without breaking the binding
        self.visible_var.set(layer.visible)

    def set_selected(self, selected: bool):
        """Update visual selection state."""

        color = "#444" if selected else "#666"

        self.configure(bg=color)
        self.name_btn.configure(bg=color)
