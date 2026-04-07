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
            command=self.controller.request_new_project
        )

        file_menu.add_command(
            label="Open",
            command=self.controller.request_open
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Save",
            command=self.controller.request_save
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.controller.request_exit
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