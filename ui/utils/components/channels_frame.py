import tkinter as tk

class ChannelsTabFrame(tk.Frame):
    """Frame for channel selection (RGB/CMYK)."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self.channels = {}
        self.mode_var = tk.StringVar(value="RGB")
        self._build()

    def _build(self):
        """Build mode selector and channel checkboxes."""

        # Mode selector
        mode_frame = tk.Frame(self, bg="#444")
        mode_frame.pack(fill="x", pady=5)
        tk.Label(mode_frame, text="Mode:", bg="#444", fg="white").pack(side="left", padx=5)
        option = tk.OptionMenu(mode_frame, self.mode_var, "RGB", "CMYK", command=self._on_mode_change)
        option.pack(side="left")

        # Channel checkboxes container
        self.channels_frame = tk.Frame(self, bg="#444")
        self.channels_frame.pack(fill="x", pady=5)

        self._build_channel_checkboxes("RGB")

    def _build_channel_checkboxes(self, mode):
        """Build checkboxes for channels depending on mode."""

        for widget in self.channels_frame.winfo_children():
            widget.destroy()
        self.channels.clear()

        if mode == "RGB":
            channel_list = ["R", "G", "B"]
        else:  # CMYK
            channel_list = ["C", "M", "Y", "K"]

        for channel in channel_list:
            var = tk.BooleanVar(value=True)
            button = tk.Checkbutton(self.channels_frame, text=channel, variable=var, bg="#444", fg="white")
            button.pack(anchor="w", padx=10)
            self.channels[channel] = var

    def _on_mode_change(self, mode):
        """Handle mode change and rebuild channel checkboxes."""

        self._build_channel_checkboxes(mode)
