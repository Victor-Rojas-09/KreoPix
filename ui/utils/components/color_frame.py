import tkinter as tk
from tkinter import colorchooser
from ui.utils.tools.custom_slider import DarkRangeSlider


class ColorTabFrame(tk.Frame):
    """Color adjustment panel."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self.colors = []
        self._build()

    # ==================================================
    # UI BUILD
    # ==================================================

    def _build(self):
        """Build the full UI layout."""

        self._add_slider("Brightness", self._on_brightness_change)
        self._add_slider("Red", self._on_red_change)
        self._add_slider("Green", self._on_green_change)
        self._add_slider("Blue", self._on_blue_change)

        tk.Button(
            self,
            text="Advanced...",
            command=self._open_advanced_dialog
        ).pack(pady=5)

        self.color_bar = tk.Frame(self, bg="#333")
        self.color_bar.pack(fill="x", padx=10, pady=8)

        default_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]
        self.colors = default_colors.copy()
        self._refresh_color_bar()

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
        """Linear scaling."""

        return int(value * 255 / 100)

    def _scale_gamma(self, value, gamma):
        """Gamma-based non-linear scaling."""

        v = value / 100

        if v >= 0:
            return int((v ** gamma) * 255)
        else:
            return int(-(abs(v) ** gamma) * 255)

    # ==================================================
    # FILTER CALLBACKS
    # ==================================================

    def _on_brightness_change(self, value):
        """Apply brightness filter using gamma scaling."""

        if not self.controller:
            return

        self.controller.request_set_filter("brightness")

        scaled_value = self._scale_gamma(value, gamma=3.0)

        self.controller.request_update_filter_param(
            "value",
            scaled_value
        )

    def _on_red_change(self, value):
        """Apply red channel adjustment."""

        if not self.controller:
            return

        self.controller.request_set_filter("red_adjust")

        self.controller.request_update_filter_param(
            "value",
            self._scale_linear(value)
        )

    def _on_green_change(self, value):
        """Apply green channel adjustment."""

        if not self.controller:
            return

        self.controller.request_set_filter("green_adjust")

        self.controller.request_update_filter_param(
            "value",
            self._scale_linear(value)
        )

    def _on_blue_change(self, value):
        """Apply blue channel adjustment."""

        if not self.controller:
            return

        self.controller.request_set_filter("blue_adjust")

        self.controller.request_update_filter_param(
            "value",
            self._scale_linear(value)
        )

    # ==================================================
    # COLOR PICKER
    # ==================================================

    def _open_color_picker(self):
        """Open system color picker and apply selected color."""

        result = colorchooser.askcolor(initialcolor="#000000")

        if result and result[1]:
            r, g, b = map(int, result[0])
            color = (r, g, b, 255)

            if self.controller:
                self.controller.request_update_brush_color(color)

            self._add_recent_color(result[1])

    def _add_recent_color(self, hex_color):
        """Maintain a list of recent colors."""

        if hex_color in self.colors:
            self.colors.remove(hex_color)

        self.colors.insert(0, hex_color)

        if len(self.colors) > 9:
            self.colors = self.colors[:9]

        self._refresh_color_bar()

    def _refresh_color_bar(self):
        """Refresh color buttons."""

        for widget in self.color_bar.winfo_children():
            widget.destroy()

        for c in self.colors:
            self._add_color_button(c)

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

        r, g, b = self.winfo_rgb(hex_color)
        r, g, b = r // 256, g // 256, b // 256

        color = (r, g, b, 255)

        if self.controller:
            self.controller.request_update_brush_color(color)

    def _open_advanced_dialog(self):
        """Placeholder for future advanced tools."""

        print("Advanced dialog placeholder")