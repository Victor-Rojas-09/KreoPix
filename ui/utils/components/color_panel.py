import tkinter as tk
from tkinter import colorchooser
from ui.utils.tools.custom_slider import BlueSlider

class ColorPanel(tk.Frame):
    """Panel for color selection and image adjustments."""

    MAX_COLORS = 9

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")
        self.controller = controller
        self.colors = []
        self._build()

    def _build(self):
        """Build the color selection panel."""

        # Top section sliders
        top_frame = tk.Frame(self, bg="#444")
        top_frame.pack(fill="x", pady=5)

        tk.Label(top_frame, text="Adjustments", bg="#444", fg="white").pack(pady=5)

        self._add_slider(top_frame, "Brightness", self._on_brightness_change)
        self._add_slider(top_frame, "Contrast", self._on_contrast_change)
        self._add_slider(top_frame, "Saturation", self._on_saturation_change)
        self._add_slider(top_frame, "Gamma", self._on_gamma_change)

        # Button for the dialog
        tk.Button(top_frame, text="More", command=self._open_advanced_dialog).pack(pady=5)

        # Bottom section to color bar
        bottom_frame = tk.Frame(self, bg="#333")
        bottom_frame.pack(fill="x", side="bottom", pady=5)

        tk.Label(bottom_frame, text="Colors", bg="#333", fg="white").pack(anchor="w", padx=5)

        self.color_bar = tk.Frame(bottom_frame, bg="#333")
        self.color_bar.pack(fill="x", padx=5, pady=5)

        # Initialize with default colors
        default_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]
        self.colors = default_colors.copy()
        self._refresh_color_bar()

        # Button for color picker
        tk.Button(bottom_frame, text="Pick Color", command=self._open_color_picker).pack(pady=5)

    # -------------------------
    # Slider helpers
    # -------------------------
    def _add_slider(self, parent, label, command):
        """Add a slider to the panel."""

        frame = tk.Frame(parent, bg="#444")
        frame.pack(fill="x", padx=10, pady=2)

        frame.columnconfigure(0, weight=0, minsize=80)  # fixed label width
        frame.columnconfigure(1, weight=1)              # slider expands

        tk.Label(frame, text=label, bg="#444", fg="white").grid(row=0, column=0, sticky="w")
        slider = BlueSlider(frame, command=command)
        slider.grid(row=0, column=1, sticky="ew")

    def _on_brightness_change(self, value):
        """Change the brightness of the color."""

        if self.controller:
            self.controller.request_update_brightness(value)

    def _on_contrast_change(self, value):
        """Change the contrast of the color."""

        if self.controller:
            self.controller.request_update_contrast(value)

    def _on_saturation_change(self, value):
        """Change the saturation of the color."""

        if self.controller:
            self.controller.request_update_saturation(value)

    def _on_gamma_change(self, value):
        """Change the gamma of the color."""
        if self.controller:
            self.controller.request_update_gamma(value)

    def _open_advanced_dialog(self):
        """Open an advanced dialog."""

        print("Advanced dialog will be implemented here.")

    # -------------------------
    # Color picker and history
    # -------------------------
    def _open_color_picker(self):
        """Open a color picker."""

        result = colorchooser.askcolor(initialcolor="#000000")
        if result and result[1]:
            hex_color = result[1]
            r, g, b = map(int, result[0])
            a = 255
            color = (r, g, b, a)

            if self.controller:
                self.controller.request_update_brush_color(color)

            self._add_recent_color(hex_color)

    def _add_recent_color(self, hex_color):
        """Add a recent color."""

        if hex_color in self.colors:
            self.colors.remove(hex_color)
        self.colors.insert(0, hex_color)

        # Limit total colors
        if len(self.colors) > self.MAX_COLORS:
            self.colors = self.colors[:self.MAX_COLORS]

        self._refresh_color_bar()

    def _refresh_color_bar(self):
        """Refresh the color bar."""

        for widget in self.color_bar.winfo_children():
            widget.destroy()
        for c in self.colors:
            self._add_color_button(c)

    def _add_color_button(self, hex_color):
        """Add a color button."""

        btn = tk.Button(self.color_bar, bg=hex_color, width=2, height=1,
                        command=lambda c=hex_color: self._select_color(c))
        btn.pack(side="left", padx=2)

    def _select_color(self, hex_color):
        """Select a color."""

        r, g, b = self.winfo_rgb(hex_color)
        r, g, b = r//256, g//256, b//256
        color = (r, g, b, 255)
        if self.controller:
            self.controller.request_update_brush_color(color)
