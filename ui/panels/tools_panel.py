import tkinter as tk
from PIL import Image, ImageTk

from core.brush.presets import (
    create_hard_brush,
    create_eraser
)


class ToolsPanel(tk.Frame):
    """Tools panel with icon-only buttons."""

    def __init__(self, parent, controller=None):
        """Initialize panel."""
        super().__init__(parent, width=80, bg="#2c2c2c")

        self.controller = controller
        self.icons = self._load_icons()
        self.buttons = {}

        self._build()

    def _load_icon(self, path):
        """Load and resize icon."""

        img = Image.open(path)
        img = img.resize((42, 42), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def _load_icons(self):
        """Load all icons."""

        return {
            "Brush": self._load_icon("assets/icons/brush.png"),
            "Eraser": self._load_icon("assets/icons/eraser.png"),
            "Select": self._load_icon("assets/icons/select.png"),
            "Paint Bucket": self._load_icon("assets/icons/paint_bucket.png"),
            "Eyedropper": self._load_icon("assets/icons/eyedropper.png"),
            "Magic Wand": self._load_icon("assets/icons/magic_wand.png"),
        }

    def _build(self):
        """Create tool buttons."""

        tools = [
            ("Brush", lambda: self._select_tool("brush", create_hard_brush((0, 0, 0, 255)))),
            ("Eraser", lambda: self._select_tool("eraser", create_eraser())),
            ("Select", lambda: self._select_tool("select")),
            ("Paint Bucket", lambda: self._select_tool("paint_bucket")),
            ("Eyedropper", lambda: self._select_tool("eyedropper")),
            ("Magic Wand", lambda: self._select_tool("magic_wand")),
        ]

        for name, command in tools:
            btn = tk.Button(
                self,
                image=self.icons[name],
                command=command,
                bg="#2c2c2c",
                activebackground="#2c2c2c",
                bd=0,
                highlightthickness=0,
                relief="flat",
                cursor="hand2"
            )

            btn.pack(pady=6)

            # Hover effect
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#3a3a3a"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#2c2c2c"))

            self.buttons[name] = btn

    def _select_tool(self, tool_name, brush=None):
        """Set active tool."""

        if not self.controller:
            return

        self.controller.request_set_tool(tool_name)

        if brush:
            self.controller.state.set_brush(brush)

        self._highlight(tool_name)

    def _highlight(self, tool_name):
        """Highlight selected tool."""

        mapping = {
            "brush": "Brush",
            "eraser": "Eraser",
            "select": "Select",
            "paint_bucket": "Paint Bucket",
            "eyedropper": "Eyedropper",
            "magic_wand": "Magic Wand",
        }

        selected = mapping.get(tool_name)

        for name, btn in self.buttons.items():
            if name == selected:
                btn.config(bg="#505050")
            else:
                btn.config(bg="#2c2c2c")