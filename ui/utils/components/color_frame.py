import tkinter as tk
from tkinter import colorchooser
from ui.utils.tools.custom_slider import DarkRangeSlider


class ColorTabFrame(tk.Frame):
    """Color adjustment panel with recent colors from AppState."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self._build()
        self.controller.state.add_listener(self._on_state_change)

    # ==================================================
    # UI BUILD
    # ==================================================

    def _build(self):
        """Build the full UI layout."""

        # Sliders
        self._add_slider("Brightness", self._on_brightness_change)
        self._add_slider("Red", self._on_red_change)
        self._add_slider("Green", self._on_green_change)
        self._add_slider("Blue", self._on_blue_change)

        # Advanced button
        tk.Button(
            self,
            text="Advanced...",
            command=self._open_advanced_dialog
        ).pack(pady=5)

        # Color bar
        self.color_bar = tk.Frame(self, bg="#333")
        self.color_bar.pack(fill="x", padx=10, pady=8)

        # Initialize with default colors if state has none
        if not self.controller.state.get_recent_colors():
            default_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]

            for c in default_colors:
                r, g, b = self._hex_to_rgb(c)
                self.controller.state.set_color((r, g, b, 255))

        self._refresh_color_bar()

        # Color picker button
        tk.Button(
            self,
            text="Pick Color",
            command=self._open_color_picker
        ).pack(pady=5)

    def _add_slider(self, label, command):
        """Create a centered slider row with aligned label."""

        frame = tk.Frame(self, bg="#444")
        frame.pack(fill="x", padx=10, pady=4)

        inner = tk.Frame(frame, bg="#444")
        inner.pack(anchor="center")

        tk.Label(
            inner,
            text=label,
            width=10,
            anchor="w",
            bg="#444",
            fg="white"
        ).pack(side="left", padx=(0, 10))

        slider = DarkRangeSlider(
            inner,
            min_value=-100,
            max_value=100,
            initial_value=0,
            width=240,
            command=command
        )
        slider.pack(side="left")

    # ==================================================
    # SCALING FUNCTIONS
    # ==================================================

    def _scale_linear(self, value):
        """Scale the slider to linear."""

        return int(value * 255 / 100)

    def _scale_gamma(self, value, gamma):
        """Scale the color with a given gamma."""

        v = value / 100
        return int((abs(v) ** gamma) * 255) if v >= 0 else int(-(abs(v) ** gamma) * 255)


    def _on_brightness_change(self, value):
        """Change the brightness of the color."""

        if not self.controller:
            return

        self.controller.request_set_filter("brightness")

        scaled_value = self._scale_gamma(value, gamma=3.0)

        self.controller.request_update_filter_param("value", scaled_value)

    def _on_red_change(self, value):
        """Change the red color of the color."""

        if not self.controller:
            return

        self.controller.request_set_filter("red_adjust")
        self.controller.request_update_filter_param("value", self._scale_linear(value))

    def _on_green_change(self, value):
        """Change the green color of the color."""

        if not self.controller:
            return

        self.controller.request_set_filter("green_adjust")
        self.controller.request_update_filter_param("value", self._scale_linear(value))

    def _on_blue_change(self, value):
        """Change the blue color of the color."""

        if not self.controller:
            return

        self.controller.request_set_filter("blue_adjust")
        self.controller.request_update_filter_param("value", self._scale_linear(value))


    def _open_color_picker(self):
        """Open system color picker and apply selected color."""

        result = colorchooser.askcolor()
        if result and result[0]:
            r, g, b = map(int, result[0])
            color = (r, g, b, 255)

            self.controller.state.set_color(color)
            self.controller.request_update_brush_color(color)
            self._refresh_color_bar()

    def _refresh_color_bar(self):
        """Refresh color buttons from state recent colors."""

        for widget in self.color_bar.winfo_children():
            widget.destroy()

        colors = self.controller.state.get_recent_colors()
        for c in colors:
            self._add_color_button(self._rgba_to_hex(c))

    def _add_color_button(self, hex_color):
        """Create a selectable color button."""

        tk.Button(
            self.color_bar,
            bg=hex_color,
            width=2,
            height=1,
            command=lambda c=hex_color: self._select_color(c)
        ).pack(side="left", padx=2)

    def _select_color(self, hex_color):
        """Apply selected color from palette."""

        r, g, b = self._hex_to_rgb(hex_color)
        color = (r, g, b, 255)

        self.controller.state.set_color(color)
        self.controller.request_update_brush_color(color)

    def _on_state_change(self, state):
        """React to state changes by keeping recent color bar in sync."""

        self._refresh_color_bar()

    def _rgba_to_hex(self, color):
        """Return hex color from rgba tuple."""

        r, g, b, _ = color

        return f"#{r:02x}{g:02x}{b:02x}"

    def _hex_to_rgb(self, hex_color):
        """Return rgb color from hex color."""

        hex_color = hex_color.lstrip("#")

        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        return r, g, b

    def _open_advanced_dialog(self):
        print("Advanced dialog placeholder")