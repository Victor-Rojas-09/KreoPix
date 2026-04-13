import tkinter as tk
from tkinter import colorchooser

from ui.utils.tools.custom_slider import DarkRangeSlider
from ui.utils.tools.icon_button import IconButton
from services.filters.filter_service import FILTER_REGISTRY


class ColorTabFrame(tk.Frame):
    """
    Color and threshold filter control panel.

    Responsibilities:
    - Render sliders dynamically
    - Handle preview
    - Apply/reset filters
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#444")

        self.controller = controller
        self._bound_state = None
        self._adjustment_sliders = {}
        self._snapshot = None
        self._current_filters = None

        self.icons = {
            "reset": "assets/icons/reset.png",
            "settings": "assets/icons/settings.png",
            "picker": "assets/icons/piker.png"
        }

        self._build()
        self.rebind_state_listener()

        # FIRST RENDER
        self._on_state_change(self.controller.state)

    # ==================================================
    # STATE
    # ==================================================

    def rebind_state_listener(self):
        if self._bound_state is not None:
            self._bound_state.remove_listener(self._on_state_change)

        self._bound_state = self.controller.state
        self._bound_state.add_listener(self._on_state_change)

    # ==================================================
    # UI
    # ==================================================

    def _build(self):
        self._sliders_container = tk.Frame(self, bg="#444")
        self._sliders_container.pack(fill="x", pady=5)

        # =========================
        # BUTTON ROW
        # =========================
        button_row = tk.Frame(self, bg="#444")
        button_row.pack(fill="x", padx=10, pady=5)

        center_frame = tk.Frame(button_row, bg="#444")
        center_frame.pack(side="left", expand=True)

        inner = tk.Frame(center_frame, bg="#444")
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
            button_row,
            image_path=self.icons["settings"],
            size=(18, 18),
            command=self._open_advanced_dialog
        ).pack(side="left", padx=5)

        # Color bar
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

        # RESTORE DEFAULT COLORS
        if not self.controller.state.get_recent_colors():
            default_colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]
            for c in default_colors:
                r, g, b = self._hex_to_rgb(c)
                self.controller.state.set_color((r, g, b, 255))

        self._refresh_color_bar()

    # ==================================================
    # SLIDERS
    # ==================================================

    def _rebuild_sliders(self, filters):
        for widget in self._sliders_container.winfo_children():
            widget.destroy()

        self._adjustment_sliders.clear()

        for fid in filters:
            self._create_filter_sliders(fid)

    def _create_filter_sliders(self, fid):
        meta = FILTER_REGISTRY.get(fid, {})
        name = meta.get("name", fid)
        params = meta.get("params", {})

        for pname, rules in params.items():

            if pname == "dummy":
                frame = tk.Frame(self._sliders_container, bg="#444")
                frame.pack(fill="x", padx=10, pady=4)

                tk.Label(frame, text=f"{name} (Auto)", fg="#aaa", bg="#444").pack(anchor="w")
                continue

            frame = tk.Frame(self._sliders_container, bg="#444")
            frame.pack(fill="x", padx=10, pady=4)

            label = f"{name} ({pname})" if len(params) > 1 else name

            tk.Label(frame, text=label, bg="#444", fg="white", width=18, anchor="w").pack(side="left")

            slider = DarkRangeSlider(
                frame,
                min_value=rules["min"],
                max_value=rules["max"],
                initial_value=rules["default"],
                width=240,
                command=lambda v, f=fid, p=pname: self._on_slider_change(f, p, v)
            )

            slider.pack(side="left")

            slider.set_value(rules["default"], trigger=False)

            self._adjustment_sliders[(fid, pname)] = slider

    # ==================================================
    # LOGIC
    # ==================================================

    def _on_slider_change(self, fid, param, value):
        if not self._snapshot:
            layer = self.controller.state.get_selected_layer()
            if layer:
                self._snapshot = layer.image.copy()

        self.controller.state.set_threshold_param(fid, param, int(value))
        self._preview()

    def _preview(self):
        params = self.controller.state.get_threshold_params()
        filters = self.controller.state.get_active_threshold_filters()

        self.controller.request_threshold_stack_preview(
            self._snapshot,
            filters,
            params
        )

    def _apply_changes(self):
        layer = self.controller.state.get_selected_layer()

        if layer and self._snapshot:
            self.controller.request_threshold_stack_commit(
                self._snapshot,
                layer.image.copy()
            )

        self._reset_all()

    def _reset_changes(self):
        if self._snapshot:
            self.controller.request_threshold_stack_cancel(self._snapshot)

        self._reset_all()

    def _reset_all(self):
        self._snapshot = None
        self.controller.state.reset_threshold_params()

        for (fid, pname), slider in self._adjustment_sliders.items():
            default = FILTER_REGISTRY[fid]["params"][pname]["default"]
            slider.set_value(default, trigger=False)

    # ==================================================
    # STATE LISTENER
    # ==================================================

    def _on_state_change(self, state):
        filters = state.get_active_threshold_filters()

        if filters != self._current_filters:
            self._current_filters = list(filters)
            self._rebuild_sliders(filters)

        self._refresh_color_bar()

    # ==================================================
    # COLOR
    # ==================================================

    def _open_color_picker(self):
        result = colorchooser.askcolor()
        if result and result[0]:
            r, g, b = map(int, result[0])
            color = (r, g, b, 255)

            self.controller.state.set_color(color)
            self.controller.request_update_brush_color(color)
            self._refresh_color_bar()

    def _refresh_color_bar(self):
        for widget in self.color_bar.winfo_children():
            widget.destroy()

        colors = self.controller.state.get_recent_colors()

        for c in colors:
            hex_color = f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}"

            tk.Button(
                self.color_bar,
                bg=hex_color,
                width=2,
                command=lambda col=c: self._select_color(col)
            ).pack(side="left", padx=2)

    def _select_color(self, color):
        self.controller.state.set_color(color)
        self.controller.request_update_brush_color(color)

    def _open_advanced_dialog(self):
        top = self.winfo_toplevel()
        self.controller.open_threshold_settings_dialog(top)

    # ==================================================
    # UTILS
    # ==================================================

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))