# ui/screens/home_screen.py
import tkinter as tk


class HomeScreen(tk.Frame):
    """Home screen view."""

    def __init__(self, parent, controller=None):
        """Initialize home layout."""
        super().__init__(parent)

        self.controller = controller

        self._configure_grid()
        self._create_header()
        self._create_actions_panel()
        self._create_recent_panel()

    def _configure_grid(self):
        """Configure base grid."""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def _create_header(self):
        """Create title label."""
        tk.Label(
            self,
            text="Welcome to KreoPix",
            font=("Arial", 26)
        ).grid(row=0, column=0, columnspan=2, pady=30)

    def _create_actions_panel(self):
        """Create actions panel."""
        self.actions_panel = ActionsPanel(
            self,
            on_create=self._handle_create,
            on_open=self._handle_open
        )
        self.actions_panel.grid(row=1, column=0, sticky="nsew", padx=40)

    def _create_recent_panel(self):
        """Create recent projects panel."""
        self.recent_panel = RecentProjectsPanel(
            self,
            on_select=self._handle_recent
        )
        self.recent_panel.grid(row=1, column=1, sticky="nsew", padx=40)

    def _handle_create(self):
        """Handle create action."""
        print("Project created")
        if self.controller:
            self.controller.show_editor()

    def _handle_open(self):
        """Handle open action."""
        print("Project opened")
        if self.controller:
            self.controller.show_editor()

    def _handle_recent(self, project_name):
        """Handle recent selection."""
        print(f"Opening recent: {project_name}")
        if self.controller:
            self.controller.show_editor()


class ActionsPanel(tk.Frame):
    """Primary actions panel."""

    def __init__(self, parent, on_create, on_open):
        """Initialize actions panel."""
        super().__init__(parent)

        self.on_create = on_create
        self.on_open = on_open

        self._build()

    def _build(self):
        """Build action buttons."""
        tk.Button(
            self,
            text="New Project",
            width=20,
            height=2,
            command=self.on_create
        ).pack(pady=15)

        tk.Button(
            self,
            text="Open Project",
            width=20,
            height=2,
            command=self.on_open
        ).pack(pady=15)


class RecentProjectsPanel(tk.Frame):
    """Recent projects panel."""

    def __init__(self, parent, on_select):
        """Initialize recent panel."""
        super().__init__(parent, bd=1, relief="solid")

        self.on_select = on_select

        self._build()

    def _build(self):
        """Build list widget."""
        tk.Label(
            self,
            text="Recent Projects",
            font=("Arial", 16)
        ).pack(pady=10)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self._load_mock_data()
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def _load_mock_data(self):
        """Insert sample data."""
        self.listbox.insert("end", "Project_1.kreo")
        self.listbox.insert("end", "Illustration_final.kreo")
        self.listbox.insert("end", "Concept_art.kreo")

    def _on_select(self, event):
        """Handle list selection."""
        selection = self.listbox.curselection()
        if selection:
            project = self.listbox.get(selection[0])
            self.on_select(project)