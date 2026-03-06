import tkinter as tk
from PIL import Image, ImageTk
from utils.blue_slider import BlueSlider

class EditorScreen(tk.Frame):
    """Editor main screen."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.project = None
        self.tk_image = None

        self._configure_grid()
        self._create_tools_panel()
        self._create_canvas_panel()
        self._create_right_panel()

    # ==================================================
    # Edit Layout
    # ==================================================

    def _configure_grid(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

    def _create_tools_panel(self):
        self.tools_panel = ToolsPanel(self)
        self.tools_panel.grid(row=0, column=0, sticky="ns")

    def _create_canvas_panel(self):
        self.canvas_panel = CanvasPanel(self)
        self.canvas_panel.grid(row=0, column=1, sticky="nsew")

    def _create_right_panel(self):
        self.right_panel = RightSidebar(self, self.controller)
        self.right_panel.grid(row=0, column=2, sticky="ns")

    # ==================================================
    # PUBLIC API
    # ==================================================

    def load_project(self, project):
        """Save the controller state and reder the canvas."""

        self.controller.state.set_project(project)

        self.update()

        self._render_canvas()

        layers = self.controller.state.get_layers()
        self.right_panel.layers_panel.load_layers(layers)

    # ==================================================
    # RENDER LOGIC
    # ==================================================

    def _render_canvas(self):
        """Mix the layers and update the central canvas."""

        project = self.controller.state.get_project()

        if not project or not hasattr(project, 'width'):
            return

        # Make the background layer
        base = Image.new("RGBA", (project.width, project.height), (0, 0, 0, 0))

        # Iteration on the layers
        layers = project.get_layers() if hasattr(project, 'get_layers') else project.layers

        for layer in layers:
            if layer.visible:
                # Use alpha composite combination
                base.alpha_composite(layer.image)

        # Send the final image
        self.canvas_panel.display_image(base)


# ======================================================
# LEFT PANEL
# ======================================================

class ToolsPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, width=120, bg="#2c2c2c")

        tk.Label(
            self,
            text="Tools",
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        tk.Button(self, text="Brush").pack(fill="x", pady=5)
        tk.Button(self, text="Eraser").pack(fill="x", pady=5)
        tk.Button(self, text="Select").pack(fill="x", pady=5)


# ======================================================
# CENTER PANEL
# ======================================================

class CanvasPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")

        self.canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.current_image = None
        self.tk_image = None

        self.bind("<Configure>", self._on_resize)

    def display_image(self, pil_image):
        self.current_image = pil_image
        self._draw_scaled()

    def _on_resize(self, event):
        if self.current_image:
            self._draw_scaled()

    def _draw_scaled(self):
        if self.current_image is None:
            return

        # Geometric update
        self.update_idletasks()

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        # If the canvas is not yet drawn exit to avoid errors.
        if canvas_w < 10: return

        img_w, img_h = self.current_image.size

        # Scale calculate
        scale = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        # Resize for viewing
        resized = self.current_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(resized)
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_w // 2,
            canvas_h // 2,
            image=self.tk_image,
            anchor="center"
        )


# ======================================================
# RIGHT PANEL
# ======================================================

class RightSidebar(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, width=260, bg="#3a3a3a")

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.color_panel = ColorPanel(self)
        self.color_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.layers_panel = LayersPanel(self, controller=controller)
        self.layers_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.brush_panel = BrushPanel(self)
        self.brush_panel.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)


# ======================================================
# COLOR PANEL
# ======================================================

class ColorPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#444")

        tk.Label(
            self,
            text="Color",
            bg="#444",
            fg="white"
        ).pack(pady=5)

        tk.Canvas(self, bg="white").pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


# ======================================================
# LAYERS PANEL
# ======================================================

class LayerRow(tk.Frame):

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

    def _toggle_visibility(self):

        visible = self.visible_var.get()

        self.controller.image_service.set_layer_visibility(
            self.layer,
            visible
        )

        self.controller.refresh_canvas()

    def _select_layer(self, event):

        self.controller.state.set_selected_layer(self.index)

class LayersPanel(tk.Frame):
    """Layers management panel."""

    def __init__(self, parent, controller=None):
        """Initialize layers panel."""
        super().__init__(parent, bg="#555")

        self.controller = controller
        self.layer_rows = []

        self._configure_grid()
        self._build_header()
        self._build_layers_area()

    def _configure_grid(self):
        """Configure base grid."""
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _build_header(self):
        """Build top controls."""

        header = tk.Frame(self, bg="#555")
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        header.columnconfigure(1, weight=1)

        # Layer mode button
        self.mode_button = tk.Label(
            header,
            text="Normal",
            bg="#666",
            fg="white",
            padx=8,
            pady=4,
            cursor="hand2"
        )
        self.mode_button.grid(row=0, column=0, padx=5)

        self.mode_button.bind("<Button-1>", self._show_mode_menu)

        # Opacity slider
        self.opacity_slider = BlueSlider(
            header,
            width=180,
            height=16,
            command=self._on_opacity_change
        )

        self.opacity_slider.grid(row=0, column=1, sticky="ew")

    def _build_layers_area(self):
        """Build layers container."""

        self.layers_container = tk.Frame(self, bg="#555")
        self.layers_container.grid(row=1, column=0, sticky="nsew")

        self.layers_container.columnconfigure(0, weight=1)

    def load_layers(self, layers):
        """Render layer list."""

        # Clean the layers
        for row in self.layer_rows:
            row.destroy()
        self.layer_rows.clear()

        # We reverse the list so that the top layer appears at the top of the UI.
        for i, layer in reversed(list(enumerate(layers))):
            row = LayerRow(
                self.layers_container,
                layer,
                index=i,
                controller=self.controller
            )
            row.pack(fill="x", padx=5, pady=2)
            self.layer_rows.append(row)

    def _show_mode_menu(self, event):
        """Display blend menu."""

        menu = tk.Menu(self, tearoff=0)

        modes = [
            "Normal",
            "Multiply",
            "Overlay",
            "Screen"
        ]

        for m in modes:
            menu.add_command(
                label=m,
                command=lambda v=m: self._set_mode(v)
            )

        menu.tk_popup(event.x_root, event.y_root)

    def _set_mode(self, mode):
        """Set layer blend mode."""
        self.mode_button.config(text=f"{mode}")

    def _on_opacity_change(self, value):
        layer = self.controller.state.get_selected_layer()
        if layer:
            # The service changes the data in the layer object.
            self.controller.image_service.set_layer_opacity(layer, value)
            # The controller instructs the screen to refresh.
            self.controller.refresh_canvas()

# ======================================================
# BRUSH PANEL
# ======================================================

class BrushPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#666")

        tk.Label(
            self,
            text="Brushes",
            bg="#666",
            fg="white"
        ).pack(pady=5)

        tk.Button(self, text="Round").pack(pady=3)
        tk.Button(self, text="Soft").pack(pady=3)
        tk.Button(self, text="Hard").pack(pady=3)