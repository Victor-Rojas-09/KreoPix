import tkinter as tk
from tkinter import colorchooser
from ui.utils.tools.custom_slider import DarkRangeSlider
from ui.utils.tools.icon_button import IconButton


class ColorTabFrame(tk.Frame):
    """Color adjustment panel with recent colors from AppState."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self._bound_state = None

        # Configuración de iconos (editable fácilmente)
        self.icons = {
            "reset": "assets/icons/reset.png",
            "settings": "assets/icons/settings.png",
            "picker": "assets/icons/piker.png"
        }

        self._build()
        self.rebind_state_listener()

    def rebind_state_listener(self):
        """Attach to the active tab's AppState."""

        if self._bound_state is not None:
            self._bound_state.remove_listener(self._on_state_change)

        self._bound_state = self.controller.state
        self._bound_state.add_listener(self._on_state_change)

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

        # =========================
        # BUTTON ROW
        # =========================
        button_row = tk.Frame(self, bg="#444")
        button_row.pack(fill="x", padx=10, pady=5)

        inner = tk.Frame(button_row, bg="#444")
        inner.pack(anchor="center")

        IconButton(
            inner,
            image_path=self.icons["reset"],
            size=(18, 18),
            command=self._reset_changes
        ).pack(side="left", padx=5)

        tk.Button(
            inner,
            text="Apply",
            bg="#777",
            fg="white",
            padx=5,
            pady=2,
            command=self._apply_changes
        ).pack(side="left", padx=6)

        IconButton(
            inner,
            image_path=self.icons["settings"],
            size=(18, 18),
            command=self._open_advanced_dialog
        ).pack(side="left", padx=5)

        # =========================
        # COLOR ROW
        # =========================
        color_row = tk.Frame(self, bg="#333")
        color_row.pack(fill="x", padx=10, pady=8)

        IconButton(
            color_row,
            image_path=self.icons["picker"],
            size=(20, 20),
            command=self._open_color_picker
        ).pack(side="left", padx=(0, 5))

        self.color_bar = tk.Frame(color_row, bg="#333")
        self.color_bar.pack(side="left", fill="x")

        # Initialize default colors
        if not self.controller.state.get_recent_colors():
            default_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]

            for c in default_colors:
                r, g, b = self._hex_to_rgb(c)
                self.controller.state.set_color((r, g, b, 255))

        self._refresh_color_bar()

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
    # ACTIONS
    # ==================================================

    def _apply_changes(self):
        """Apply the changes."""

        print("Apply changes")
        # self.controller.apply_filters()

    def _reset_changes(self):
        """Reset the changes."""

        print("Reset changes")
        # reset sliders / estado

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

    # ==================================================
    # COLOR HANDLING
    # ==================================================

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

        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _open_advanced_dialog(self):
        print("Advanced dialog placeholder")