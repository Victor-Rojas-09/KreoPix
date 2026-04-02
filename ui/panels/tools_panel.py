import tkinter as tk
from core.brush.presets import (
    create_hard_brush,
    create_eraser
)


class ToolsPanel(tk.Frame):
    """Left panel containing editor tools with icons."""

    def __init__(self, parent, controller=None):
        """Initialize the tools panel."""

        super().__init__(parent, width=120, bg="#2c2c2c")
        self.controller = controller
        self.icons = self._load_icons()
        self._build()

    def _load_icons(self):
        """Load tool icons from assets/icons folder."""

        return {
            "Brush": tk.PhotoImage(file="assets/icons/brush.png"),
            "Eraser": tk.PhotoImage(file="assets/icons/eraser.png"),
            "Select": tk.PhotoImage(file="assets/icons/select.png"),
            "Paint Bucket": tk.PhotoImage(file="assets/icons/paint_bucket.png"),
            "Eyedropper": tk.PhotoImage(file="assets/icons/eyedropper.png"),
            "Magic Wand": tk.PhotoImage(file="assets/icons/magic_wand.png"),
        }

    def _build(self):
        """Create tool buttons dynamically with icons."""

        tk.Label(
            self,
            text="Tools",
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        # Tool definitions: name, callback
        tools = [
            ("Brush", self._select_brush),
            ("Eraser", self._select_eraser),
            ("Select", self._select_select),
            ("Paint Bucket", self._select_paint_bucket),
            ("Eyedropper", self._select_eyedropper),
            ("Magic Wand", self._select_magic_wand),
        ]

        for name, command in tools:
            icon = self.icons.get(name)
            tk.Button(
                self,
                text=name,
                image=icon,
                compound="left",  # icon + text
                command=command
            ).pack(fill="x", pady=5)

    def _select_brush(self):
        """Select painting tool with default brush."""
        if not self.controller:
            return

        self.controller.state.set_tool("brush")
        color = (0, 0, 0, 255)
        brush = create_hard_brush(color)
        self.controller.state.set_brush(brush)

    def _select_eraser(self):
        """Select eraser tool."""
        if not self.controller:
            return

        self.controller.state.set_tool("eraser")
        brush = create_eraser()
        self.controller.state.set_brush(brush)

    def _select_select(self):
        """Select selection tool (not yet implemented)."""

        if not self.controller:
            return

        self.controller.state.set_tool("select")

    def _select_paint_bucket(self):
        """Select paint bucket tool (not yet implemented)."""

        if not self.controller:
            return

        self.controller.state.set_tool("paint_bucket")

    def _select_eyedropper(self):
        """Select eyedropper tool (not yet implemented)."""

        if not self.controller:
            return

        self.controller.state.set_tool("eyedropper")

    def _select_magic_wand(self):
        """Select magic wand tool (not yet implemented)."""

        if not self.controller:
            return

        self.controller.state.set_tool("magic_wand")
