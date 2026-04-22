import tkinter as tk


class MenuBar:
    """Application menu bar."""

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self._build()

    def _build(self):
        """
        Builds the File menu for the application's main menu bar and
        separators are added between logical groups of commands.
        """

        file_menu = tk.Menu(self.menu, tearoff=0)

        file_menu.add_command(
            label="New Project",
            command=self.controller.request_new_project,
        )

        file_menu.add_command(
            label="Open",
            command=self.controller.request_open,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Save",
            command=self.controller.request_save,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.controller.request_exit,
        )

        self.menu.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu, tearoff=0)

        edit_menu.add_command(
            label="Undo",
            command=self.controller.request_undo,
            accelerator="Ctrl+Z",
        )

        edit_menu.add_command(
            label="Redo",
            command=self.controller.request_redo,
            accelerator="Ctrl+Y",
        )

        self.menu.add_cascade(label="Edit", menu=edit_menu)

        tools_menu = tk.Menu(self.menu, tearoff=0)

        tools_menu.add_command(
            label="Brush",
            command=lambda: self._activate_tool("brush"),
            accelerator="B",
        )
        tools_menu.add_command(
            label="Eraser",
            command=lambda: self._activate_tool("eraser"),
            accelerator="E",
        )
        tools_menu.add_command(
            label="Select",
            command=lambda: self._activate_tool("select"),
            accelerator="S",
        )
        tools_menu.add_command(
            label="Paint Bucket",
            command=lambda: self._activate_tool("paint_bucket"),
            accelerator="F",
        )
        tools_menu.add_command(
            label="Eyedropper",
            command=lambda: self._activate_tool("eyedropper"),
            accelerator="I",
        )
        tools_menu.add_command(
            label="Magic Wand",
            command=lambda: self._activate_tool("magic_wand"),
            accelerator="W",
        )
        tools_menu.add_command(
            label="Zoom area",
            command=lambda: self._activate_tool("zoom_area"),
            accelerator="Z",
        )

        self.menu.add_cascade(label="Tools", menu=tools_menu)

        layer_menu = tk.Menu(self.menu, tearoff=0)

        layer_menu.add_command(
            label="Merge Visible (Add)",
            command=lambda: self._merge_visible("add"),
            accelerator="Ctrl+E",
        )

        layer_menu.add_command(
            label="Merge Visible (Average)",
            command=lambda: self._merge_visible("average"),
            accelerator="Ctrl+Shift+E",
        )

        self.menu.add_cascade(label="Layer", menu=layer_menu)

    def _activate_tool(self, tool_name: str):
        """Switch tool using the same logic as keyboard shortcuts."""

        if not self.controller.state.has_format():
            return

        from core.brush.presets import create_hard_brush, create_eraser

        self.controller.request_set_tool(tool_name)
        if tool_name == "brush":
            self.controller.request_set_brush_by_preset(
                create_hard_brush, self.controller.state.get_color()
            )
        elif tool_name == "eraser":
            self.controller.request_set_brush_by_preset(create_eraser)
        if hasattr(self.controller, "_sync_tools_highlight"):
            self.controller._sync_tools_highlight()

    def _merge_visible(self, mode: str):
        """Trigger merge visible layers with the given blend mode."""

        if not self.controller.state.has_format():
            return

        self.controller.request_merge_visible(mode=mode)