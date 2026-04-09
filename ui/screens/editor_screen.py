import os
import tkinter as tk
from ui.panels.tools_panel import ToolsPanel
from ui.panels.canvas_panel import CanvasPanel
from ui.panels.right_sidebar import RightSidebar


class EditorScreen(tk.Frame):
    """Main editor screen layout with tab bar for multiple projects."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)

        self.controller = controller

        self._configure_grid()
        self._create_panels()

    # ==================================================
    # Layout
    # ==================================================

    def _configure_grid(self):
        """Configure main editor proportions."""

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        self.rowconfigure(1, weight=1)

    def _create_panels(self):
        """Create tab bar and UI panels."""

        self.tab_frame = tk.Frame(self, bg="#252526", height=36)
        self.tab_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.tools_panel = ToolsPanel(self, self.controller)
        self.tools_panel.grid(row=1, column=0, sticky="ns")

        self.canvas_panel = CanvasPanel(self, self.controller)
        self.canvas_panel.grid(row=1, column=1, sticky="nsew")

        self.right_sidebar = RightSidebar(self, self.controller)
        self.right_sidebar.grid(row=1, column=2, sticky="ns")

        self.refresh_tabs()

    # ==================================================
    # Multi-tab
    # ==================================================

    def refresh_tabs(self):
        """Rebuild tab buttons from controller sessions."""

        for w in self.tab_frame.winfo_children():
            w.destroy()

        if not self.controller:
            return

        sessions = self.controller.get_sessions()
        active = self.controller.get_active_session_index()

        for i, sess in enumerate(sessions):
            tab_row = tk.Frame(self.tab_frame, bg="#252526")
            tab_row.pack(side="left", padx=(4, 0), pady=4)

            bg = "#3c3c3c" if i == active else "#2d2d30"
            lbl = self._tab_title(sess)
            btn = tk.Button(
                tab_row,
                text=lbl,
                bg=bg,
                fg="#e0e0e0",
                activebackground="#505050",
                bd=0,
                padx=12,
                pady=4,
                font=("Segoe UI", 9),
                command=lambda idx=i: self.controller.activate_session(idx),
            )
            btn.pack(side="left")

            close_btn = tk.Button(
                tab_row,
                text="x",
                bg=bg,
                fg="#cccccc",
                bd=0,
                width=2,
                command=lambda idx=i: self.controller.request_close_tab(idx),
            )
            close_btn.pack(side="left", padx=(2, 0))

    def _tab_title(self, sess):
        """Prefer image filename; fallback to project display name."""

        if getattr(sess, "source_path", None):
            return os.path.basename(sess.source_path)
        return getattr(sess, "display_title", None) or "Untitled"

    def rebind_state_listeners(self):
        """Rebind panels when switching tabs."""

        self.canvas_panel.rebind_state_listener()
        self.right_sidebar.layers_panel.rebind_state_listener()
        self.right_sidebar.color_panel.color_tab.rebind_state_listener()

    # ==================================================
    # APIs
    # ==================================================

    def load_project(self, image_format):
        """Legacy: project load is handled via tab sessions."""

        self.sync_from_controller()

    def sync_from_controller(self):
        """Refresh tab bar and canvas from controller."""

        self.refresh_tabs()
        self.refresh()

    def refresh(self):
        """Refresh the image."""

        if not self.controller.state.has_format():
            return

        image = self.controller.state.current_format.composite()
        self.canvas_panel.display_image(image)

    def refresh_layers(self):
        """Delegate to layers panel."""

        self.right_sidebar.layers_panel.refresh_layers(self.controller.state)
