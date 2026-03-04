import tkinter as tk
from PIL import ImageTk


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
        self.right_panel = RightSidebar(self)
        self.right_panel.grid(row=0, column=2, sticky="ns")

    # ==================================================
    # PUBLIC API
    # ==================================================

    def load_project(self, project):
        self.project = project
        self._render_canvas()
        self.right_panel.layers_panel.set_layers(project.get_layers())

    # ==================================================

    def _render_canvas(self):
        image = self.project.composite()
        self.canvas_panel.display_image(image)


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
        self.canvas.delete("all")

        canvas_w = self.winfo_width()
        canvas_h = self.winfo_height()

        img_w, img_h = self.current_image.size

        scale = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        resized = self.current_image.resize((new_w, new_h))
        self.tk_image = ImageTk.PhotoImage(resized)

        x = (canvas_w - new_w) // 2
        y = (canvas_h - new_h) // 2

        self.canvas.create_image(x, y, anchor="nw", image=self.tk_image)


# ======================================================
# RIGHT PANEL
# ======================================================

class RightSidebar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, width=260, bg="#3a3a3a")

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.color_panel = ColorPanel(self)
        self.color_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.layers_panel = LayersPanel(self)
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

class LayersPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#555")

        tk.Label(
            self,
            text="Layers",
            bg="#555",
            fg="white"
        ).pack(pady=5)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

    # PUBLIC API

    def set_layers(self, layers):
        self.listbox.delete(0, "end")

        # Mostrar de arriba hacia abajo (como Photoshop)
        for layer in reversed(layers):
            self.listbox.insert("end", layer.name)


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