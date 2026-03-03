import tkinter as tk


class MenuBar:
    """Application menu manager."""

    MODE_HOME = "home"
    MODE_EDITOR = "editor"

    def __init__(self, root, controller=None):
        """Initialize menu system."""
        self.root = root
        self.controller = controller

        self._create_root_menu()
        self._create_submenus()
        self._create_variables()

        self.set_mode(self.MODE_HOME)

    # ---------- Setup ----------

    def _create_root_menu(self):
        """Attach menu to root."""
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

    def _create_submenus(self):
        """Create base submenus."""
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.edit_menu = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)

    def _create_variables(self):
        """Initialize state variables."""
        self.snap_var = tk.BooleanVar(value=False)

    # ---------- Public API ----------

    def set_mode(self, mode):
        """Switch menu mode."""
        self._clear_menus()

        if mode == self.MODE_HOME:
            self._build_home_menu()

        elif mode == self.MODE_EDITOR:
            self._build_editor_menu()

    # ---------- Menu Builders ----------

    def _build_home_menu(self):
        """Build home menu."""
        self.file_menu.add_command(
            label="New Project",
            command=self._on_new_project
        )
        self.file_menu.add_command(
            label="Open Project",
            command=self._on_open_project
        )

    def _build_editor_menu(self):
        """Build editor menu."""
        self.file_menu.add_command(
            label="Save",
            command=self._on_save
        )
        self.file_menu.add_command(
            label="Save As",
            command=self._on_save_as
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Exit",
            command=self._on_exit
        )

        self.edit_menu.add_checkbutton(
            label="Snap to Grid",
            variable=self.snap_var,
            command=self._on_toggle_snap
        )

    # ---------- Helpers ----------

    def _clear_menus(self):
        """Clear submenu items."""
        self.file_menu.delete(0, tk.END)
        self.edit_menu.delete(0, tk.END)

    # ---------- Event Handlers ----------

    def _on_new_project(self):
        """Handle new project."""
        print("Menu: New Project")
        if self.controller:
            self.controller.show_editor()

    def _on_open_project(self):
        """Handle open project."""
        print("Menu: Open Project")

    def _on_save(self):
        """Handle save action."""
        print("Menu: Save")

    def _on_save_as(self):
        """Handle save as."""
        print("Menu: Save As")

    def _on_exit(self):
        """Handle exit action."""
        print("Menu: Exit")
        self.root.quit()

    def _on_toggle_snap(self):
        """Handle snap toggle."""
        state = self.snap_var.get()
        print(f"Snap to Grid: {state}")