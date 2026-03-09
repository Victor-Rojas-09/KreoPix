import tkinter as tk

class LayerRow(tk.Frame):
    """Single layer row widget."""

    def __init__(self, parent, layer, index, controller):
        super().__init__(parent)

        self.layer = layer
        self.index = index
        self.controller = controller

        self.visible_var = tk.BooleanVar(value=layer.visible)

        self._build()

    def _build(self):

        checkbox = tk.Checkbutton(
            self,
            variable=self.visible_var,
            command=self._toggle_visibility
        )
        checkbox.pack(side="left")

        label = tk.Label(self, text=self.layer.name)
        label.pack(side="left", padx=5)

        label.bind("<Button-1>", self._select_layer)

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------

    def _toggle_visibility(self):

        visible = self.visible_var.get()

        self.controller.image_service.set_layer_visibility(
            self.layer,
            visible
        )

        self.controller.refresh_canvas()

    def _select_layer(self, event):

        self.controller.state.set_selected_layer(self.index)