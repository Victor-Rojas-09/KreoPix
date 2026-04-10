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

        option = tk.OptionMenu(
            mode_frame,
            self.mode_var,
            "RGB",
            "CMYK",
            command=self._on_mode_change
        )
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
        else:
            channel_list = ["C", "M", "Y"]

        for channel in channel_list:
            var = tk.BooleanVar(value=False)

            button = tk.Checkbutton(
                self.channels_frame,
                text=channel,
                variable=var,
                bg="#666",
                fg="white",
                activebackground="#666",
                selectcolor="#666",
                highlightthickness=0,
                bd=0,
                width=2,
                anchor="w",
                command=lambda ch=channel: self._on_channel_toggle(ch)
            )
            button.pack(anchor="w", padx=10)

            self.channels[channel] = var

    def _on_mode_change(self, mode):
        """Handle mode change and rebuild channel checkboxes."""

        self._build_channel_checkboxes(mode)

        # Reset filter when mode changes
        self.controller.request_set_filter("normal")


    def _on_channel_toggle(self, selected_channel):
        """Enforce single selection behavior."""

        selected_var = self.channels[selected_channel]

        # If user unchecks the active one
        if not selected_var.get():
            self.controller.request_set_filter("normal")
            return

        # Enforce exclusive selection
        for ch, var in self.channels.items():
            if ch != selected_channel:
                var.set(False)

        # Apply corresponding filter
        filter_id = self._map_channel_to_filter(selected_channel)

        if filter_id and self.controller:
            self.controller.request_set_filter(filter_id)

    def _map_channel_to_filter(self, channel):
        """Map for the channels label in FILTER_REGISTRY."""

        mode = self.mode_var.get()

        mapping_rgb = {
            "R": "red_channel",
            "G": "green_channel",
            "B": "blue_channel"
        }

        mapping_cmy = {
            "C": "cyan_channel",
            "M": "magenta_channel",
            "Y": "yellow_channel"
        }

        if mode == "RGB":
            return mapping_rgb.get(channel)
        else:
            return mapping_cmy.get(channel)