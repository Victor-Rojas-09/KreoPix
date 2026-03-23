import tkinter as tk
from tkinter import colorchooser
from ui.utils.tools.custom_slider import BlueSlider

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


class ColorTabFrame(tk.Frame):
    """Frame for sliders and color picker/history."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self.colors = []
        self._build()

    def _build(self):
        """Build sliders and color bar."""

        # Sliders
        self._add_slider("Brightness", self._on_brightness_change)
        self._add_slider("Contrast", self._on_contrast_change)
        self._add_slider("Saturation", self._on_saturation_change)
        self._add_slider("Gamma", self._on_gamma_change)

        tk.Button(self, text="Advanced...", command=self._open_advanced_dialog).pack(pady=5)

        # Color bar
        self.color_bar = tk.Frame(self, bg="#333")
        self.color_bar.pack(fill="x", padx=5, pady=5)

        default_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]
        self.colors = default_colors.copy()
        self._refresh_color_bar()

        tk.Button(self, text="Pick Color", command=self._open_color_picker).pack(pady=5)

    def _add_slider(self, label, command):
        """Add a labeled slider with proportional layout."""

        frame = tk.Frame(self, bg="#444")
        frame.pack(fill="x", padx=10, pady=2)
        frame.columnconfigure(0, weight=0, minsize=80)
        frame.columnconfigure(1, weight=1)
        tk.Label(frame, text=label, bg="#444", fg="white").grid(row=0, column=0, sticky="w")
        slider = BlueSlider(frame, command=command)
        slider.grid(row=0, column=1, sticky="ew")

    def _on_brightness_change(self, value):
        """Handle brightness slider change."""

        if self.controller:
            self.controller.request_update_brightness(value)

    def _on_contrast_change(self, value):
        """Handle contrast slider change."""

        if self.controller:
            self.controller.request_update_contrast(value)

    def _on_saturation_change(self, value):
        """Handle saturation slider change."""

        if self.controller:
            self.controller.request_update_saturation(value)

    def _on_gamma_change(self, value):
        """Handle gamma slider change."""

        if self.controller:
            self.controller.request_update_gamma(value)

    def _open_advanced_dialog(self):
        """Placeholder for advanced dialog."""

        print("Advanced dialog placeholder")

    def _open_color_picker(self):
        """Open color chooser and add selected color to bar."""

        result = colorchooser.askcolor(initialcolor="#000000")

        if result and result[1]:
            hex_color = result[1]
            r, g, b = map(int, result[0])
            color = (r, g, b, 255)

            if self.controller:
                self.controller.request_update_brush_color(color)
            self._add_recent_color(hex_color)

    def _add_recent_color(self, hex_color):
        """Insert new color at front and limit total colors."""

        if hex_color in self.colors:
            self.colors.remove(hex_color)

        self.colors.insert(0, hex_color)

        if len(self.colors) > 9:
            self.colors = self.colors[:9]

        self._refresh_color_bar()

    def _refresh_color_bar(self):
        """Rebuild color bar with current colors."""

        for widget in self.color_bar.winfo_children():
            widget.destroy()

        for c in self.colors:
            self._add_color_button(c)

    def _add_color_button(self, hex_color):
        """Add a button for a color swatch."""

        btn = tk.Button(self.color_bar, bg=hex_color, width=2, height=1, command=lambda c=hex_color: self._select_color(c))

        btn.pack(side="left", padx=2)

    def _select_color(self, hex_color):
        """Select a color from the bar and update brush."""

        r, g, b = self.winfo_rgb(hex_color)
        r, g, b = r//256, g//256, b//256
        color = (r, g, b, 255)

        if self.controller:
            self.controller.request_update_brush_color(color)


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

        for ch in channel_list:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.channels_frame, text=ch, variable=var, bg="#444", fg="white")
            cb.pack(anchor="w", padx=10)
            self.channels[ch] = var

    def _on_mode_change(self, mode):
        """Handle mode change and rebuild channel checkboxes."""

        self._build_channel_checkboxes(mode)
