import tkinter as tk

from utils.blue_slider import BlueSlider
from ui.components.layer_row import LayerRow


class LayersPanel(tk.Frame):
    """Layers management panel."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#555")

        self.controller = controller
        self.layer_rows = []

        self._configure_grid()
        self._build_header()
        self._build_layers_area()

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    def _configure_grid(self):

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _build_header(self):

        header = tk.Frame(self, bg="#555")
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header.columnconfigure(1, weight=1)

        self.mode_button = tk.Label(
            header,
            text="Normal",
            bg="#666",
            fg="white",
            padx=8,
            pady=4,
            cursor="hand2"
        )
        self.mode_button.grid(row=0, column=0, padx=(5, 15))

        self.opacity_slider = BlueSlider(
            header,
            width=100,
            height=16,
            command=self._on_opacity_change
        )
        self.opacity_slider.grid(row=0, column=1, sticky="ew", padx=(0, 5))

        add_btn = tk.Button(
            header,
            text="+ Capa",
            bg="#777",
            fg="white",
            padx=5,
            pady=2,
            command=self._on_add_layer
        )
        add_btn.grid(row=0, column=2, padx=(5, 5))

        self.opacity_slider = BlueSlider(
            header,
            width=100,
            height=16,
            command=self._on_opacity_change
        )

    def _build_layers_area(self):

        self.layers_container = tk.Frame(self, bg="#555")
        self.layers_container.grid(row=1, column=0, sticky="nsew")

        self.layers_container.columnconfigure(0, weight=1)

    # --------------------------------------------------
    # Layers logic
    # --------------------------------------------------

    def load_layers(self, layers):
        """Render layer list."""

        for row in self.layer_rows:
            row.destroy()

        self.layer_rows.clear()

        for i, layer in reversed(list(enumerate(layers))):

            row = LayerRow(
                self.layers_container,
                layer,
                index=i,
                controller=self.controller
            )

            row.pack(fill="x", padx=5, pady=2)

            self.layer_rows.append(row)

    # --------------------------------------------------
    # Layer controls
    # --------------------------------------------------

    def _on_opacity_change(self, value):

        layer = self.controller.state.get_selected_layer()

        if layer:

            self.controller.image_service.set_layer_opacity(
                layer,
                value
            )

            self.controller.refresh_canvas()

    def _on_add_layer(self):
        """Request controller to add new layer."""

        if self.controller:
            self.controller.add_new_layer()