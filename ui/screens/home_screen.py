import tkinter as tk
from PIL import Image, ImageTk

class HomeScreen(tk.Frame):

    # ==================================================
    # Constructor
    # ==================================================
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.recent_files = []

        # Keep references to images to avoid garbage collection
        self._thumbnails = []

        # Create de config of the frame
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
        """
        Creates the Recent Projects panel.

        Uses a scrollable frame where each recent project
        is rendered as a card containing a thumbnail and filename.
        """

        self.recent_frame = tk.Frame(self, bd=1, relief="solid")
        self.recent_frame.grid(row=1, column=1, sticky="nsew", padx=40)

        tk.Label(
            self.recent_frame,
            text="Recent Projects",
            font=("Arial", 16)
        ).pack(pady=10)

        self.canvas = tk.Canvas(self.recent_frame)
        self.scroll_frame = tk.Frame(self.canvas)

        scrollbar = tk.Scrollbar(
            self.recent_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

    # -------------------------
    # PUBLIC API
    # -------------------------

    def set_recent(self, recent_projects):
        """
        Updates the list of recent projects displayed on the Home screen.

        Parameters
        ----------
        recent_projects : list[dict]
            Each dict must contain:
            - path : full file path
            - name : file name with extension
        """

        self.recent_files = recent_projects
        self._refresh_recent()

    def _refresh_recent(self):
        """
        Clears and rebuilds the recent project cards.
        """

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self._thumbnails.clear()

        for project in self.recent_files:
            self._create_recent_card(project)


    def _create_recent_card(self, project):
        """
        Creates a visual card representing a recent project.
        """

        frame = tk.Frame(
            self.scroll_frame,
            bd=1,
            relief="ridge",
            padx=10,
            pady=10
        )

        frame.pack(padx=10, pady=10, fill="x")

        path = project["path"]
        name = project["name"]

        photo = None

        try:
            image = Image.open(path)
            image.thumbnail((120, 120))

            photo = ImageTk.PhotoImage(image)
            self._thumbnails.append(photo)

        except Exception:
            pass

        label = tk.Label(
            frame,
            text=name,
            image=photo,
            compound="top",
            font=("Arial", 11),
            pady = 10
        )
        label.pack(padx=5, pady=5)
        label.bind("<Button-1>", lambda e, p=path: self.controller.request_open_recent(p))
