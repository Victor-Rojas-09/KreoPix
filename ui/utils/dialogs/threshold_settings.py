import tkinter as tk
from services.filters.filter_service import FILTER_REGISTRY
from ui.utils.tools.window_positioner import WindowPositioner


class ThresholdSettingsDialog(tk.Toplevel):
    """
    Dialog for selecting active threshold filters.

    Responsibilities:
    - Only selects which filters are active
    - Does NOT apply filters
    - Does NOT handle parameters
    """

    MAX_ACTIVE = 5

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.title("Select Threshold Filters")
        self.resizable(False, False)

        WindowPositioner.center_to_parent(self, parent, 350, 800)

        self.transient(parent)
        self.grab_set()

        self._vars = {}
        self._build()

    # ==================================================
    # UI
    # ==================================================

    def _build(self):
        outer = tk.Frame(self, bg="#2b2b2b")
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="Select up to 5 filters",
            bg="#2b2b2b",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        list_frame = tk.Frame(outer, bg="#2b2b2b")
        list_frame.pack(fill="both", expand=True, padx=20)

        current_active = self.controller.state.get_active_threshold_filters()

        # USE ALL FILTERS
        for fid, meta in FILTER_REGISTRY.items():
            name = meta.get("name", fid)

            var = tk.BooleanVar(value=fid in current_active)
            self._vars[fid] = var

            cb = tk.Checkbutton(
                list_frame,
                text=name,
                variable=var,
                bg="#2b2b2b",
                fg="#e0e0e0",
                selectcolor="#3c3c3c",
                command=self._limit_selection
            )
            cb.pack(anchor="w", pady=2)

        btn_row = tk.Frame(outer, bg="#2b2b2b")
        btn_row.pack(fill="x", padx=20, pady=15)

        tk.Button(
            btn_row,
            text="Apply changes",
            bg="#505050",
            fg="white",
            command=self._on_apply
        ).pack(side="right", padx=5)

        tk.Button(
            btn_row,
            text="Cancel",
            bg="#505050",
            fg="white",
            command=self._on_cancel
        ).pack(side="right")

    # ==================================================
    # LOGIC
    # ==================================================

    def _limit_selection(self):
        selected = [fid for fid, var in self._vars.items() if var.get()]

        if len(selected) > self.MAX_ACTIVE:
            for fid in reversed(list(self._vars.keys())):
                if self._vars[fid].get():
                    self._vars[fid].set(False)
                    break

    def _on_apply(self):
        selected = [fid for fid, var in self._vars.items() if var.get()]
        self.controller.state.set_active_threshold_filters(selected)
        self.destroy()

    def _on_cancel(self):
        self.destroy()