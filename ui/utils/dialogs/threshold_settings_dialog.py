import tkinter as tk

from services.color.threshold_stack_service import ThresholdStackService
from services.filters.filter_service import FILTER_REGISTRY
from ui.utils.tools.custom_slider import DarkRangeSlider
from ui.utils.tools.window_positioner import WindowPositioner


class ThresholdSettingsDialog(tk.Toplevel):
    """Up to five simultaneous threshold-type filters with sliders and live preview."""

    MAX_ACTIVE = 5

    FILTER_ORDER = ThresholdStackService.ORDERED_FILTER_IDS

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.title("Threshold filters")
        self.resizable(False, False)

        try:
            self.iconbitmap("assets/app/LOGO.ico")
        except tk.TclError:
            pass

        layer = self.controller.state.get_selected_layer()
        if not layer:
            self.destroy()
            return

        self._snapshot = layer.image.copy()
        self._vars: dict[str, tk.BooleanVar] = {}
        self._param_widgets: dict[str, dict] = {}
        self._slider_row_frames: dict[str, tk.Frame] = {}
        self._checkbuttons: dict[str, tk.Checkbutton] = {}
        self._after_id = None

        self._defaults = self._build_default_params()

        WindowPositioner.center_to_parent(self, parent, 420, 520)

        self.transient(parent)
        self.grab_set()

        self._build()

    # ==========================================================
    # Defaults
    # ==========================================================

    def _build_default_params(self) -> dict[str, dict]:
        out = {}
        for fid in self.FILTER_ORDER:
            meta = FILTER_REGISTRY.get(fid, {})
            params = {}
            for name, rules in meta.get("params", {}).items():
                params[name] = rules.get("default", 0)
            out[fid] = params
        return out

    def _current_params(self) -> dict[str, dict]:
        """Read slider-backed values into dict copies."""

        result = {}
        for fid in self.FILTER_ORDER:
            base = dict(self._defaults.get(fid, {}))
            widgets = self._param_widgets.get(fid, {})
            for key, w in widgets.items():
                if isinstance(w, DarkRangeSlider):
                    base[key] = int(round(w.value))
                elif isinstance(w, tk.Scale):
                    base[key] = int(round(float(w.get())))
            if fid in ("adaptive_gaussian", "adaptive_mean") and "block_size" in base:
                bs = base["block_size"]
                if bs % 2 == 0:
                    bs += 1
                base["block_size"] = max(3, min(99, bs))
            result[fid] = base
        return result

    def _active_ids(self) -> list[str]:
        return [fid for fid in self.FILTER_ORDER if self._vars[fid].get()]

    # ==========================================================
    # UI
    # ==========================================================

    def _build(self):
        outer = tk.Frame(self, bg="#2b2b2b")
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg="#2b2b2b")
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="Threshold filters",
            font=("Segoe UI", 14, "bold"),
            bg="#2b2b2b",
            fg="#f0f0f0",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Select up to five filters. Order follows the list. Preview updates live.",
            font=("Segoe UI", 8),
            bg="#2b2b2b",
            fg="#aaaaaa",
            wraplength=380,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        list_frame = tk.Frame(outer, bg="#2b2b2b")
        list_frame.pack(fill="both", expand=True, padx=20, pady=8)

        for fid in self.FILTER_ORDER:
            meta = FILTER_REGISTRY.get(fid, {})
            name = meta.get("name", fid)
            row = tk.Frame(list_frame, bg="#2b2b2b")
            row.pack(fill="x", pady=4)

            var = tk.BooleanVar(value=False)
            self._vars[fid] = var

            cb = tk.Checkbutton(
                row,
                text=name,
                variable=var,
                bg="#2b2b2b",
                fg="#e0e0e0",
                activebackground="#2b2b2b",
                activeforeground="#ffffff",
                selectcolor="#3c3c3c",
                highlightthickness=0,
                command=lambda f=fid: self._on_toggle(f),
            )
            cb.pack(anchor="w")
            self._checkbuttons[fid] = cb

            slider_parent = tk.Frame(list_frame, bg="#2b2b2b")
            slider_parent.pack(fill="x", padx=(24, 0), pady=(0, 6))
            self._slider_row_frames[fid] = slider_parent
            self._param_widgets[fid] = {}
            self._build_param_sliders(fid, slider_parent)
            slider_parent.pack_forget()

        btn_row = tk.Frame(outer, bg="#2b2b2b")
        btn_row.pack(fill="x", padx=20, pady=(8, 16))

        tk.Button(
            btn_row,
            text="Apply changes",
            bg="#505050",
            fg="white",
            activebackground="#606060",
            padx=12,
            pady=4,
            command=self._on_apply,
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            btn_row,
            text="Cancel",
            bg="#505050",
            fg="white",
            activebackground="#606060",
            padx=12,
            pady=4,
            command=self._on_cancel,
        ).pack(side="right")

        self._update_checkbox_states()
        self._update_slider_visibility()

    def _build_param_sliders(self, fid: str, parent: tk.Frame):
        meta = FILTER_REGISTRY.get(fid, {})
        schema = meta.get("params", {})
        widgets = self._param_widgets[fid]

        if fid == "otsu_binarize":
            tk.Label(
                parent,
                text="No parameters (automatic threshold).",
                bg="#2b2b2b",
                fg="#888888",
                font=("Segoe UI", 8),
            ).pack(anchor="w")
            return

        for pname, rules in schema.items():
            if pname == "dummy":
                continue
            min_v = int(rules.get("min", 0))
            max_v = int(rules.get("max", 255))
            default_v = int(rules.get("default", min_v))

            row = tk.Frame(parent, bg="#2b2b2b")
            row.pack(fill="x", pady=2)

            tk.Label(
                row,
                text=pname.replace("_", " ").title(),
                width=14,
                anchor="w",
                bg="#2b2b2b",
                fg="#cccccc",
                font=("Segoe UI", 9),
            ).pack(side="left")

            if min_v < 0 or (fid in ("adaptive_gaussian", "adaptive_mean") and pname == "C"):
                slider = DarkRangeSlider(
                    row,
                    min_value=min_v,
                    max_value=max_v,
                    initial_value=max(min_v, min(max_v, default_v)),
                    width=220,
                    command=lambda _v, f=fid: self._schedule_preview(),
                )
            else:
                slider = tk.Scale(
                    row,
                    from_=min_v,
                    to=max_v,
                    orient="horizontal",
                    length=220,
                    resolution=1,
                    bg="#2b2b2b",
                    fg="#e0e0e0",
                    troughcolor="#3c3c3c",
                    highlightthickness=0,
                    command=lambda _v, f=fid: self._schedule_preview(),
                )
                slider.set(default_v)

            slider.pack(side="left", padx=(4, 0))
            widgets[pname] = slider

    def _on_toggle(self, fid: str):
        active = self._active_ids()
        if len(active) > self.MAX_ACTIVE:
            self._vars[fid].set(False)

        self._update_checkbox_states()
        self._update_slider_visibility()
        self._schedule_preview()

    def _update_checkbox_states(self):
        active_count = len(self._active_ids())
        at_limit = active_count >= self.MAX_ACTIVE
        for fid in self.FILTER_ORDER:
            cb = self._checkbuttons[fid]
            if not self._vars[fid].get() and at_limit:
                cb.config(state="disabled")
            else:
                cb.config(state="normal")

    def _update_slider_visibility(self):
        for fid in self.FILTER_ORDER:
            frame = self._slider_row_frames[fid]
            if self._vars[fid].get():
                frame.pack(fill="x", padx=(24, 0), pady=(0, 6))
            else:
                frame.pack_forget()

    def _schedule_preview(self):
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(40, self._do_preview)

    def _do_preview(self):
        self._after_id = None
        self.controller.request_threshold_stack_preview(
            self._snapshot,
            self._active_ids(),
            self._current_params(),
        )

    def _on_apply(self):
        layer = self.controller.state.get_selected_layer()
        if layer:
            final_img = layer.image.copy()
            self.controller.request_threshold_stack_commit(self._snapshot, final_img)
        self.grab_release()
        self.destroy()

    def _on_cancel(self):
        self.controller.request_threshold_stack_cancel(self._snapshot)
        self.grab_release()
        self.destroy()
