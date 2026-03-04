import tkinter as tk


class HomeScreen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.recent_files = []

        self._configure_grid()
        self._create_header()
        self._create_actions_panel()
        self._create_recent_panel()

    # ==================================================
    # Home Layout
    # ==================================================

    def _configure_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def _create_header(self):
        tk.Label(
            self,
            text="Welcome to KreoPix",
            font=("Arial", 26)
        ).grid(row=0, column=0, columnspan=2, pady=30)

    def _create_actions_panel(self):
        frame = tk.Frame(self)
        frame.grid(row=1, column=0, sticky="nsew", padx=40)

        tk.Button(
            frame,
            text="New Project",
            width=20,
            height=2,
            command=self.controller.request_new_project
        ).pack(pady=15)

        tk.Button(
            frame,
            text="Open Project",
            width=20,
            height=2,
            command=self.controller.request_open
        ).pack(pady=15)

    # ==================================================
    # Recent Files Panel
    # ==================================================

    def _create_recent_panel(self):
        self.recent_frame = tk.Frame(self, bd=1, relief="solid")
        self.recent_frame.grid(row=1, column=1, sticky="nsew", padx=40)

        tk.Label(
            self.recent_frame,
            text="Recent Projects",
            font=("Arial", 16)
        ).pack(pady=10)

        self.listbox = tk.Listbox(self.recent_frame)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    # -------------------------
    # PUBLIC API
    # -------------------------

    def set_recent(self, recent_files):
        self.recent_files = recent_files
        self._refresh_list()

    def _refresh_list(self):
        self.listbox.delete(0, "end")

        for path in self.recent_files:
            self.listbox.insert("end", path)

    def _on_select(self, event):
        selection = self.listbox.curselection()

        if selection:
            path = self.listbox.get(selection[0])
            self.controller.request_open_recent(path)