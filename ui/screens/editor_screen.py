import tkinter as tk


class EditorScreen(tk.Frame):
    """Editor main screen."""

    def __init__(self, parent, controller=None):
        """Initialize editor layout."""
        super().__init__(parent)

        self.controller = controller

        self._configure_grid()
        self._create_tools_panel()
        self._create_canvas_panel()
        self._create_right_panel()

    def _configure_grid(self):
        """Configure main grid."""
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

    def _create_tools_panel(self):
        """Create tools section."""
        self.tools_panel = ToolsPanel(self)
        self.tools_panel.grid(row=0, column=0, sticky="ns")

    def _create_canvas_panel(self):
        """Create canvas section."""
        self.canvas_panel = CanvasPanel(self)
        self.canvas_panel.grid(row=0, column=1, sticky="nsew")

    def _create_right_panel(self):
        """Create right sidebar."""
        self.right_panel = RightSidebar(self)
        self.right_panel.grid(row=0, column=2, sticky="ns")


class ToolsPanel(tk.Frame):
    """Left tools panel."""

    def __init__(self, parent):
        """Initialize tools panel."""
        super().__init__(parent, width=120, bg="#2c2c2c")

        self._build()

    def _build(self):
        """Build tool buttons."""
        tk.Label(
            self,
            text="Tools",
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        tk.Button(self, text="Brush").pack(fill="x", pady=5)
        tk.Button(self, text="Eraser").pack(fill="x", pady=5)
        tk.Button(self, text="Select").pack(fill="x", pady=5)


class CanvasPanel(tk.Frame):
    """Center canvas panel."""

    def __init__(self, parent):
        """Initialize canvas panel."""
        super().__init__(parent, bg="#1e1e1e")

        self._configure_grid()
        self._build()

    def _configure_grid(self):
        """Configure inner grid."""
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _build(self):
        """Build canvas widget."""
        self.canvas = tk.Canvas(
            self,
            bg="white",
            width=800,
            height=600
        )
        self.canvas.grid(row=0, column=0)

        self._draw_mock_content()

    def _draw_mock_content(self):
        """Draw test rectangle."""
        self.canvas.create_rectangle(
            100, 100, 300, 300,
            fill="blue"
        )


class RightSidebar(tk.Frame):
    """Right composite panel."""

    def __init__(self, parent):
        """Initialize sidebar."""
        super().__init__(parent, width=250, bg="#3a3a3a")

        self._configure_grid()
        self._create_sections()

    def _configure_grid(self):
        """Configure sidebar grid."""
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def _create_sections(self):
        """Create sidebar sections."""
        self.color_panel = ColorPanel(self)
        self.color_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.layers_panel = LayersPanel(self)
        self.layers_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.brush_panel = BrushPanel(self)
        self.brush_panel.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)


class ColorPanel(tk.Frame):
    """Color selection panel."""

    def __init__(self, parent):
        """Initialize color panel."""
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


class LayersPanel(tk.Frame):
    """Layers management panel."""

    def __init__(self, parent):
        """Initialize layers panel."""
        super().__init__(parent, bg="#555")

        tk.Label(
            self,
            text="Layers",
            bg="#555",
            fg="white"
        ).pack(pady=5)

        tk.Listbox(self).pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )


class BrushPanel(tk.Frame):
    """Brush presets panel."""

    def __init__(self, parent):
        """Initialize brush panel."""
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