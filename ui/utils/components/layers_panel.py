import tkinter as tk
from ui.utils.tools.custom_slider import BlueSlider
from ui.utils.components.layer_row import LayerRow

from services.filters.filter_service import FILTER_REGISTRY


class LayersPanel(tk.Frame):
    """Layers management panel."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#555")
        self.controller = controller
        self.layer_rows = []

        self._configure_grid()
        self._build_header()
        self._build_layers_area()

        # Register listener to AppState
        if self.controller and self.controller.state:
            self.controller.state.add_listener(self.refresh_layers)

    def refresh_layers(self, state):
        """Efficient refresh of layer list."""

        layers = state.get_layers()
        selected_index = state.selected_layer_index

        self._update_layers(layers, selected_index)

        # Update mode UI based on selected layer
        selected_layer = state.get_selected_layer()
        if selected_layer:
            filter_id = getattr(selected_layer, "filter_id", "normal")
            filter_meta = FILTER_REGISTRY.get(filter_id, {})
            self.mode_var.set(filter_meta.get("name", "Normal"))

    # ==================================================
    # Layout
    # ==================================================

    def _configure_grid(self):
        """Configure grid of the panel."""

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _build_header(self):
        """Build the header of the panel."""

        header = tk.Frame(self, bg="#555")
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header.columnconfigure(1, weight=1)

        # FILTER SELECTOR

        self.mode_var = tk.StringVar(value="Normal")

        self.mode_button = tk.Menubutton(
            header,
            textvariable=self.mode_var,
            bg="#666",
            fg="white",
            relief="raised"
        )
        self.mode_button.grid(row=0, column=0, padx=(5, 15))

        menu = tk.Menu(self.mode_button, tearoff=0)

        # List of filters used
        filters_to_show = [
            "normal",
            "grayscale_average",
            "grayscale_luminosity",
            "grayscale_midgray"
        ]

        for filter_id in filters_to_show:
            meta = FILTER_REGISTRY.get(filter_id)

            if not meta:
                continue

            label = meta.get("name", filter_id)

            menu.add_command(
                label=label,
                command=lambda fid=filter_id, name=label: self._on_filter_change(fid, name)
            )

        self.mode_button.config(menu=menu)

        self.opacity_slider = BlueSlider(
            header,
            min_value=0,
            max_value=100,
            initial_value=100,
            command=self._on_opacity_change
        )

        self.opacity_slider.grid(row=0, column=1, sticky="ew", padx=(0, 5))

        add_btn = tk.Button(
            header,
            text="+",
            bg="#777",
            fg="white",
            padx=5,
            pady=2,
            command=self._on_add_layer
        )
        add_btn.grid(row=0, column=2, padx=(5, 2))

        remove_btn = tk.Button(
            header,
            text="-",
            bg="#777",
            fg="white",
            padx=5,
            pady=2,
            command=self._on_remove_layer
        )
        remove_btn.grid(row=0, column=3, padx=(2, 5))

    def _build_layers_area(self):
        """Build the layers part in the grid."""

        self.layers_container = tk.Frame(self, bg="#555")
        self.layers_container.grid(row=1, column=0, sticky="nsew")
        self.layers_container.columnconfigure(0, weight=1)

    # ==================================================
    # Layers logic
    # ==================================================

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

    # ==================================================
    # Layer controls
    # ==================================================

    def _on_opacity_change(self, value):
        """Change the opacity of the layer."""

        layer = self.controller.state.get_selected_layer()

        if layer:
            self.controller.request_update_layer_opacity(layer, value)

    def _on_add_layer(self):
        """Request controller to add new layer."""

        if self.controller:
            self.controller.add_new_layer()

    def _on_remove_layer(self):
        """Request controller to remove selected layer."""

        if self.controller:
            self.controller.remove_selected_layer()

    def _update_layers(self, layers, selected_index):
        """Efficient diff-based update ."""

        current = len(self.layer_rows)
        target = len(layers)

        # Fill in missing rows
        for _ in range(current, target):
            row = LayerRow(self.layers_container, layers[0], 0, self.controller)
            row.pack(fill="x", padx=5, pady=2)
            self.layer_rows.append(row)

        # Remove extra rows
        for _ in range(target, current):
            row = self.layer_rows.pop()
            row.destroy()

        # Update content
        reversed_layers = list(reversed(list(enumerate(layers))))

        for visual_index, (real_index, layer) in enumerate(reversed_layers):
            row = self.layer_rows[visual_index]

            row.update(layer, real_index)
            row.set_selected(real_index == selected_index)

    def _on_filter_change(self, filter_id, display_name):
        """Handle filter change from UI."""

        if not self.controller:
            return

        self.controller.request_set_filter(filter_id)
        self.mode_var.set(display_name)