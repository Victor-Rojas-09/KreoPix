import tkinter as tk
from tkinter import colorchooser
from ui.utils.tools.custom_slider import DarkRangeSlider

class ColorTabFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self.colors = []
        self._build()

    def _build(self):

        self._add_slider("Brightness", self._on_brightness_change)
        self._add_slider("Contrast", self._on_contrast_change)
        self._add_slider("Saturation", self._on_saturation_change)
        self._add_slider("channel_R", self._on_red_channel_change)
        self._add_slider("Threshold", self._on_threshold_change)

        tk.Button(self, text="Advanced...", command=self._open_advanced_dialog).pack(pady=5)

        self.color_bar = tk.Frame(self, bg="#333")
        self.color_bar.pack(fill="x", padx=5, pady=5)

        default_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]
        self.colors = default_colors.copy()
        self._refresh_color_bar()

        tk.Button(self, text="Pick Color", command=self._open_color_picker).pack(pady=5)

    def _add_slider(self, label, command):

        frame = tk.Frame(self, bg="#444")
        frame.pack(fill="x", padx=10, pady=2)
        frame.columnconfigure(0, weight=0, minsize=80)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text=label, bg="#444", fg="white").grid(row=0, column=0, sticky="w")

        slider = DarkRangeSlider(
            frame,
            min_value=-100,
            max_value=100,
            initial_value=0,
            command=command
        )

        slider.grid(row=0, column=1, sticky="ew")

    def _on_brightness_change(self, value):

        if self.controller:
            self.controller.request_set_filter("brightness")
            self.controller.request_update_filter_param("value", value)

    def _on_contrast_change(self, value):

        if self.controller:
            self.controller.request_update_contrast(value)

    def _on_saturation_change(self, value):

        if self.controller:
            self.controller.request_update_saturation(value)

    def _on_red_channel_change(self, value):

        if self.controller:
            self.controller.request_set_filter("channel")
            self.controller.request_update_filter_param("channel", 0)
            self.controller.request_update_filter_param("value", value)

    def _on_threshold_change(self, value):

        if self.controller:
            self.controller.request_set_filter("threshold")
            self.controller.request_update_filter_param("threshold", value)

    def _open_advanced_dialog(self):

        print("Advanced dialog placeholder")

    def _open_color_picker(self):

        result = colorchooser.askcolor(initialcolor="#000000")

        if result and result[1]:
            hex_color = result[1]
            r, g, b = map(int, result[0])
            color = (r, g, b, 255)

            if self.controller:
                self.controller.request_update_brush_color(color)

            self._add_recent_color(hex_color)

    def _add_recent_color(self, hex_color):

        if hex_color in self.colors:
            self.colors.remove(hex_color)

        self.colors.insert(0, hex_color)

        if len(self.colors) > 9:
            self.colors = self.colors[:9]

        self._refresh_color_bar()

    def _refresh_color_bar(self):

        for widget in self.color_bar.winfo_children():
            widget.destroy()

        for c in self.colors:
            self._add_color_button(c)

    def _add_color_button(self, hex_color):

        btn = tk.Button(
            self.color_bar,
            bg=hex_color,
            width=2,
            height=1,
            command=lambda c=hex_color: self._select_color(c)
        )

        btn.pack(side="left", padx=2)

    def _select_color(self, hex_color):

        r, g, b = self.winfo_rgb(hex_color)
        r, g, b = r // 256, g // 256, b // 256
        color = (r, g, b, 255)

        if self.controller:
            self.controller.request_update_brush_color(color)