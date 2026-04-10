import tkinter as tk
from ui.utils.components.color_frame import ColorTabFrame
from ui.utils.components.channels_frame import ChannelsTabFrame

class ColorPanel(tk.Frame):
    """Panel for color selection and image adjustments."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2b2b2b")
        self.controller = controller
        self._build()

    def _build(self):
        """Build the tab bar and container for tab frames."""

        # Tab bar
        self.tab_bar = tk.Frame(self, bg="#1f1f1f")
        self.tab_bar.pack(fill="x", side="top")


        self.color_tab_btn = tk.Button(
            self.tab_bar, text="Color",
            bg="#3a3a3a", fg="white",
            bd=0, relief="flat",
            activebackground="#3a3a3a",
            command=lambda: self._show_tab("color")
        )
        self.color_tab_btn.pack(side="left", padx=(4, 2), pady=(4, 0))

        self.channels_tab_btn = tk.Button(
            self.tab_bar, text="Channels",
            bg="#2a2a2a", fg="#cccccc",
            bd=0, relief="flat",
            activebackground="#3a3a3a",
            command=lambda: self._show_tab("channels")
        )
        self.channels_tab_btn.pack(side="left", padx=2, pady=(4, 0))

        # Container
        self.tab_container = tk.Frame(self, bg="#3a3a3a")
        self.tab_container.pack(fill="both", expand=True)

        # Create tab frames
        self.color_tab = ColorTabFrame(self.tab_container, self.controller)
        self.channels_tab = ChannelsTabFrame(self.tab_container, self.controller)

        # Show default tab
        self._show_tab("color")

    def _show_tab(self, tab_name):
        """Switch between tab frames and update tab button styles."""

        # Hide all frames
        for child in self.tab_container.winfo_children():
            child.pack_forget()

        # Reset
        self.color_tab_btn.config(bg="#2a2a2a", fg="#cccccc")
        self.channels_tab_btn.config(bg="#2a2a2a", fg="#cccccc")

        # Active
        if tab_name == "color":
            self.color_tab.pack(fill="both", expand=True)
            self.color_tab_btn.config(bg="#3a3a3a", fg="white")
        elif tab_name == "channels":
            self.channels_tab.pack(fill="both", expand=True)
            self.channels_tab_btn.config(bg="#3a3a3a", fg="white")