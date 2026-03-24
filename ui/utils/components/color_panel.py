import tkinter as tk
from ui.utils.components.color_frame import ColorTabFrame
from ui.utils.components.channels_frame import ChannelsTabFrame

class ColorPanel(tk.Frame):
    """Panel for color selection and image adjustments."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self._build()

    def _build(self):
        """Build the tab bar and container for tab frames."""

        # Tab bar
        tab_bar = tk.Frame(self, bg="#222")
        tab_bar.pack(fill="x", side="top")

        self.color_tab_btn = tk.Button(
            tab_bar, text="Color", bg="#666", fg="white",
            relief="raised", command=lambda: self._show_tab("color")
        )
        self.color_tab_btn.pack(side="left", padx=2, pady=2)

        self.channels_tab_btn = tk.Button(
            tab_bar, text="Channels", bg="#444", fg="white",
            relief="flat", command=lambda: self._show_tab("channels")
        )
        self.channels_tab_btn.pack(side="left", padx=2, pady=2)

        # Container for tab frames
        self.tab_container = tk.Frame(self, bg="#333")
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

        # Reset tab button styles
        self.color_tab_btn.config(relief="flat", bg="#444")
        self.channels_tab_btn.config(relief="flat", bg="#444")

        # Show selected tab
        if tab_name == "color":
            self.color_tab.pack(fill="both", expand=True)
            self.color_tab_btn.config(relief="raised", bg="#666")
        elif tab_name == "channels":
            self.channels_tab.pack(fill="both", expand=True)
            self.channels_tab_btn.config(relief="raised", bg="#666")




