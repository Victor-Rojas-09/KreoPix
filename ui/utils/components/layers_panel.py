import tkinter as tk
from ui.utils.tools.custom_slider import BlueSlider
from ui.utils.components.layer_row import LayerRow

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

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    def _configure_grid(self):
        """Configure grid of the panel."""

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _build_header(self):
        """Build the header of the panel."""

        header = tk.Frame(self, bg="#555")
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header.columnconfigure(1, weight=1)

        # Selection a mode
        self.mode_var = tk.StringVar(value="Normal")
        self.mode_button = tk.Menubutton(header, textvariable=self.mode_var, bg="#666", fg="white", relief="raised")
        self.mode_button.grid(row=0, column=0, padx=(5, 15))

        menu = tk.Menu(self.mode_button, tearoff=0)
        for mode in ["Normal", "grayscale_avg", "grayscale_lum", "laplacian", "canny"]:
            menu.add_command(label=mode, command=lambda m=mode: self._on_mode_change(m))
        self.mode_button.config(menu=menu)

        # Slider for the opacity manage
        self.opacity_slider = BlueSlider(header, width=100, height=16, command=self._on_opacity_change)
        self.opacity_slider.grid(row=0, column=1, sticky="ew", padx=(0, 5))

        # Button for add a new layer
        add_btn = tk.Button(header, text="+", bg="#777", fg="white", padx=5, pady=2, command=self._on_add_layer)
        add_btn.grid(row=0, column=2, padx=(5, 2))

        # Button for remove selected layer
        remove_btn = tk.Button(header, text="-", bg="#777", fg="white", padx=5, pady=2, command=self._on_remove_layer)
        remove_btn.grid(row=0, column=3, padx=(2, 5))

    def _build_layers_area(self):
        """Build the layers part in the grid."""

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
            row = LayerRow(self.layers_container, layer, index=i, controller=self.controller)
            row.pack(fill="x", padx=5, pady=2)
            self.layer_rows.append(row)

    # --------------------------------------------------
    # Layer controls
    # --------------------------------------------------
    def _on_opacity_change(self, value):
        """Change the opacity of the layer."""

        layer = self.controller.state.get_selected_layer()

        if layer:
            self.controller.state.update_layer_opacity(layer, value)

    def _on_add_layer(self):
        """Request controller to add new layer."""

        if self.controller:
            self.controller.add_new_layer()

    def _update_layers(self, layers, selected_index):
        """Efficient diff-based update (no full re-render)."""

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

    def _on_remove_layer(self):
        """Request controller to remove selected layer."""

        if self.controller:
            self.controller.remove_selected_layer()

    def _on_mode_change(self, mode):
        """Change the mode of the layer."""

        layer = self.controller.state.get_selected_layer()
        if layer:
            self.controller.request_set_layer_mode(layer, mode)
            self.mode_var.set(mode)
