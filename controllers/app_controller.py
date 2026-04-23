from tkinter import messagebox
import os
from PIL import Image

from core.state.app_state import AppState
from controllers.app_editor import EditorSession
from ui.dialogs.confirm_exit import ConfirmExitDialog
from ui.dialogs.new_project import NewProjectDialog
from services.images.image_service import ImageService
from services.brushes.color_picker_service import ColorPickerService
from services.brushes.fill_service import FillService
from services.selection import SelectionService
from services.merge.blend_service import BlendService
from services.color import (
    HistogramCurveService,
    ColorAdjustmentService,
    ThresholdStackService,
)
from services.transform.transform_services import TransformToolService
from services.history.merge_layers import MergeLayersCommand
from services.history import (
    AddLayerCommand,
    CommandHistory,
    RemoveLayerCommand,
    ReplaceLayerFilterStateCommand,
    ReplaceLayerImageCommand,
    ReplaceLayerOpacityCommand,
    ReplaceSelectionMaskCommand,
)
from core.brush.brush_core import BrushPoint


class AppController:
    """
    Main application controller.

    Responsibilities:
    - Orchestrate UI, Core and Services
    - Handle navigation between screens
    - Manage application state
    - Coordinate file operations (open, save, recent)
    - Delegate layer operations to AppState and Services
    - Manage the transform tool lifecycle (start, update, apply, cancel)
    """

    # ==========================================================
    # CLASS CONSTRUCTOR
    # ==========================================================

    def __init__(self, root, layout, file_service, recent_manager):
        self.root = root
        self.layout = layout
        self.file_service = file_service
        self.recent_manager = recent_manager
        self.image_service = ImageService()
        self.color_picker_service = ColorPickerService()
        self.fill_service = FillService()
        self.selection_service = SelectionService()
        self.histogram_curve_service = HistogramCurveService()
        self.color_adjustment_service = ColorAdjustmentService()
        self.threshold_stack_service = ThresholdStackService()
        self.transform_service = TransformToolService()
        self.blend_service = BlendService()
        self._empty_state = AppState()
        self._sessions: list[EditorSession] = []
        self._active_index = 0
        self._bind_edit_shortcuts()
        self._bind_tool_shortcuts()

    # ==========================================================
    # Active session / state
    # ==========================================================

    @property
    def state(self) -> AppState:
        """Active tab state, or an empty state when no editor tab exists."""

        if not self._sessions:
            return self._empty_state

        return self._sessions[self._active_index].state

    def _get_history(self) -> CommandHistory:
        """Get history commands."""

        return self._sessions[self._active_index].history

    def _active_session(self) -> EditorSession | None:
        """Active editor session, or None if no editor session exists."""

        if not self._sessions:
            return None

        return self._sessions[self._active_index]

    def get_sessions(self) -> list[EditorSession]:
        """Return all editor sessions (tabs)."""

        return list(self._sessions)

    def get_active_session_index(self) -> int:
        """Return the active editor session index."""

        return self._active_index

    def activate_session(self, index: int):
        """Switch active tab and sync viewport."""

        if index < 0 or index >= len(self._sessions):
            return
        self._active_index = index
        self._rebind_editor_listeners()
        self.state.notify()
        self.refresh_layers()
        self.refresh_canvas()
        self.sync_tools_highlight()
        self._notify_editor_tabs()

    def sync_tools_highlight(self):
        """Keep tools panel button highlight in sync after tab switch."""

        if not self._is_editor_screen():
            return
        screen = self.layout.current_screen
        if hasattr(screen, "tools_panel") and hasattr(screen.tools_panel, "_highlight"):
            tool = self.state.get_tool()
            if tool:
                screen.tools_panel._highlight(tool)

    def _notify_editor_tabs(self):
        """Notify editor tab changes."""

        if self._is_editor_screen():
            screen = self.layout.current_screen
            if hasattr(screen, "refresh_tabs"):
                screen.refresh_tabs()

    # ==========================================================
    # UNDO / REDO
    # ==========================================================

    def _clear_history(self):
        """Reset undo/redo when the document is replaced or closed."""

        if self._sessions:
            self._get_history().clear()

    def can_undo(self) -> bool:
        """Valid undo command."""

        if not self._sessions:
            return False

        return self._get_history().can_undo()

    def can_redo(self) -> bool:
        """Valid redo command."""

        if not self._sessions:
            return False

        return self._get_history().can_redo()

    def request_undo(self):
        """Undo the last document change."""

        if not self.state.has_format():
            return

        if self._get_history().undo():
            self.state.notify()
            self.refresh_layers()
            self.refresh_canvas()

    def request_redo(self):
        """Redo the last undone change."""

        if not self.state.has_format():
            return

        if self._get_history().redo():
            self.state.notify()
            self.refresh_layers()
            self.refresh_canvas()

    def _is_editor_screen(self) -> bool:
        """Import the editor screen."""

        from ui.screens.editor_screen import EditorScreen

        return isinstance(self.layout.current_screen, EditorScreen)

    def _bind_edit_shortcuts(self):
        """Global shortcuts; only act while the editor screen is active."""

        self.root.bind_all("<Control-z>", self._shortcut_undo)
        self.root.bind_all("<Control-y>", self._shortcut_redo)
        self.root.bind_all("<Control-Shift-Z>", self._shortcut_redo)
        self.root.bind_all("<Control-e>", self._shortcut_merge)
        self.root.bind_all("<Control-E>", self._shortcut_merge)
        self.root.bind_all("<Control-Shift-e>", self._shortcut_merge_avg)
        self.root.bind_all("<Control-Shift-E>", self._shortcut_merge_avg)

    def _shortcut_undo(self, event=None):
        """Valid undo shortcut."""

        if self._is_editor_screen() and self.state.has_format():
            self.request_undo()
            return "break"

    def _shortcut_redo(self, event=None):
        """Valid redo shortcut."""

        if self._is_editor_screen() and self.state.has_format():
            self.request_redo()
            return "break"

    def _shortcut_merge(self, event=None):
        if self._is_editor_screen() and self.state.has_format():
            self.request_merge_two_layers(use_average=False)
            return "break"

    def _shortcut_merge_avg(self, event=None):
        if self._is_editor_screen() and self.state.has_format():
            self.request_merge_two_layers(use_average=True)
            return "break"

    def _bind_tool_shortcuts(self):
        """Letter shortcuts for tools (editor only)."""

        bindings = (
            ("<b>", "brush"),
            ("<B>", "brush"),
            ("<e>", "eraser"),
            ("<E>", "eraser"),
            ("<i>", "eyedropper"),
            ("<I>", "eyedropper"),
            ("<s>", "select"),
            ("<S>", "select"),
            ("<f>", "paint_bucket"),
            ("<F>", "paint_bucket"),
            ("<w>", "magic_wand"),
            ("<W>", "magic_wand"),
            ("<t>", "transform"),
            ("<T>", "transform"),
            ("<z>", "zoom_area"),
            ("<Z>", "zoom_area"),
        )
        for seq, tool in bindings:
            self.root.bind_all(seq, self._make_tool_shortcut_handler(tool))

    def _make_tool_shortcut_handler(self, tool_name: str):
        """Create a handler for tool shortcuts."""

        def handler(event=None):

            if not self._is_editor_screen() or not self.state.has_format():
                return

            self.request_set_tool(tool_name)

            from core.brush.presets import create_hard_brush, create_eraser

            if tool_name == "brush":
                self.request_set_brush_by_preset(create_hard_brush, self.state.get_color())
            elif tool_name == "eraser":
                self.request_set_brush_by_preset(create_eraser)

            self.sync_tools_highlight()
            return "break"

        return handler

    def _push_layer_pixel_command(self, layer, image_before, image_after, description: str):
        """Record brush/fill/eraser if pixels actually changed."""

        if image_before.tobytes() == image_after.tobytes():
            return

        cmd = ReplaceLayerImageCommand(layer, image_before, image_after, description=description)

        self._get_history().push(cmd)

    def _apply_selection_constraint(self, image_before, image_after):
        """Apply selection mask so only selected pixels can be edited."""

        selection_mask = self.state.get_selection_mask(image_before.size)

        if selection_mask is None:
            return image_after

        return Image.composite(image_after, image_before, selection_mask)

    # ==========================================================
    # HOME
    # ==========================================================

    def load_home(self):
        """Load Home screen and show recent projects."""

        recent_paths = self.recent_manager.get_recent()

        recent_projects = [
            {"path": path, "name": os.path.basename(path)}
            for path in recent_paths
        ]

        self.layout.show("home")
        home_screen = self.layout.current_screen
        home_screen.set_recent(recent_projects)

    # ==========================================================
    # UI REQUESTS
    # ==========================================================

    def request_new_project(self):
        """Open dialog to create a new blank project."""

        NewProjectDialog(self.root, self._create_project)

    def request_open(self):
        """Open project using file dialog."""

        document, path = self.file_service.open_image()
        if not document:
            return

        title = os.path.basename(path) if path else "Untitled"
        self._add_session(document, title, path)
        if path:
            self.recent_manager.add_recent(path)

        self._go_to_editor()

    def request_open_recent(self, path):
        """Open a project from recent list."""

        try:
            document = self.file_service.open_from_path(path)
            if not document:
                return
            title = os.path.basename(path)
            self._add_session(document, title, path)
            self.recent_manager.add_recent(path)
            self._go_to_editor()

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found:\n{path}")
            self.recent_manager.remove_recent(path)

        except Exception as e:
            messagebox.showerror("Error", f"The project could not be opened:\n{e}")

    def request_save(self):
        """Save current project."""

        document = self.state.get_format()
        if not document:
            return

        path = self.file_service.save_project(document)

        if path:
            self.recent_manager.add_recent(path)

    def request_exit(self):
        """Handle exit request."""

        if self.state.has_format():
            ConfirmExitDialog(self.root, self.root.destroy)
        else:
            self.root.destroy()

    def request_back_home(self):
        """Return to home screen."""

        self._sessions.clear()
        self._empty_state.clear_format()
        self.load_home()

    # ==========================================================
    # INTERNAL LOGIC
    # ==========================================================

    def _add_session(self, document, display_title: str, source_path: str | None):
        """Append a new tab with a fresh AppState and history."""

        st = AppState()
        st.set_format(document)
        st.set_selected_layer(len(document.get_layers()) - 1)
        sess = EditorSession(
            state=st,
            display_title=display_title,
            source_path=source_path,
        )
        self._sessions.append(sess)
        self._active_index = len(self._sessions) - 1

    def _create_project(self, width, height, project_name: str = "Untitled"):
        """
        Create a new blank document and open editor.
        Always includes a background layer and an initial editable layer.
        """

        document = self.image_service.create_blank_format(width, height)

        # Add initial editable transparent layer
        document.add_layer(name="Layer 1")

        title = (project_name or "").strip() or "Untitled"
        self._add_session(document, title, None)
        self._go_to_editor()

    def request_close_tab(self, index: int):
        """Close a tab by index; closing the last tab prompts app exit."""

        if index < 0 or index >= len(self._sessions):
            return

        if len(self._sessions) == 1:
            ConfirmExitDialog(self.root, self.root.destroy)
            return

        prev_active = self._active_index
        self._sessions.pop(index)

        if prev_active == index:
            self._active_index = min(index, len(self._sessions) - 1)
        elif prev_active > index:
            self._active_index -= 1

        self._rebind_editor_listeners()
        self.state.notify()
        self.refresh_layers()
        self.refresh_canvas()
        self.sync_tools_highlight()
        self._notify_editor_tabs()

    def _sync_viewport_from_session(self):
        """Apply stored zoom/pan to canvas panel."""

        sess = self._active_session()
        if not sess or not self._is_editor_screen():
            return

        screen = self.layout.current_screen

        if hasattr(screen, "canvas_panel") and hasattr(screen.canvas_panel, "set_viewport_from_session"):
            screen.canvas_panel.set_viewport_from_session(sess)

    def _rebind_editor_listeners(self):
        """Rebind UI listeners when active tab changes."""

        if not self._is_editor_screen():
            return

        screen = self.layout.current_screen

        if hasattr(screen, "rebind_state_listeners"):
            screen.rebind_state_listeners()

        self._sync_viewport_from_session()

    def _go_to_editor(self):
        """Navigate to editor and refresh UI."""

        self.layout.show("editor")
        self.layout.load_project_into_editor(None)
        self._rebind_editor_listeners()
        self.refresh_layers()
        self.refresh_canvas()
        self.sync_tools_highlight()
        self._notify_editor_tabs()

    # ==========================================================
    # UI REFRESH
    # ==========================================================

    def refresh_canvas(self):
        """Refresh canvas if current screen supports it."""

        screen = self.layout.current_screen

        if screen and hasattr(screen, "refresh"):
            screen.refresh()

    def refresh_layers(self):
        """Refresh layer panel if current screen supports it."""

        screen = self.layout.current_screen

        if screen and hasattr(screen, "refresh_layers"):
            screen.refresh_layers()

    # ==========================================================
    # DOCUMENT HELPERS
    # ==========================================================

    def get_document(self):
        """Return current document."""

        return self.state.get_format()

    def get_layers(self):
        """Return document layers."""

        document = self.get_document()

        if not document:
            return []

        return document.get_layers()

    def normalize_value(self, value, max_value=255):
        """Convert a UI percentage value (0–100) into an internal range."""

        try:
            return int(float(value) * max_value / 100)
        except (ValueError, TypeError):
            return 0

    # ==========================================================
    # LAYER OPERATIONS
    # ==========================================================

    def add_new_layer(self, name=None):
        """Add a new layer by position and index."""

        document = self.get_document()

        if not document:
            return

        if name is None:
            name = f"Layer {len(document.get_layers())}"

        # Insert new layer after selected index
        index = self.state.selected_layer_index
        insert_at = index + 1
        document.add_layer(name=name, insert_at=insert_at)

        self.state.set_selected_layer(insert_at)

        added = document.layers[insert_at]
        self._get_history().push(
            AddLayerCommand(self.state, document, insert_at, added)
        )

        # Refresh the canvas after adding
        self.refresh_layers()
        self.refresh_canvas()

    def select_layer(self, index):
        """Select layer by index."""

        self.state.set_selected_layer(index)
        self.refresh_layers()
        self.refresh_canvas()

    def request_update_layer_opacity(self, layer, opacity: int):
        """Update layer opacity with undo support."""

        if not layer:
            return

        before = layer.opacity
        self.state.update_layer_opacity(layer, opacity)
        after = layer.opacity

        if before != after:
            self._get_history().push(
                ReplaceLayerOpacityCommand(layer, before, after)
            )

    def remove_selected_layer(self):
        """Remove currently selected layer via state."""

        if not self.state:
            return

        layers = self.state.get_layers()
        if not layers:
            return

        idx = self.state.selected_layer_index
        removed_snapshot = layers[idx]

        cmd = RemoveLayerCommand(self.state, idx, removed_snapshot)

        self.state.remove_selected_layer()
        self._get_history().push(cmd)

        self.refresh_layers()
        self.refresh_canvas()

    # ==========================================================
    # BRUSH OPERATIONS
    # ==========================================================

    def handle_paint_stroke(self, points):
        """Select pixels from the canvas and apply the stroke."""

        document = self.state.get_format()
        if not document:
            return

        layer = self.state.get_selected_layer()
        if not layer:
            return

        brush = self.state.get_brush()
        if not brush:
            return

        image_before = layer.image.copy()

        # Convert raw points to BrushPoint
        brush_points = [BrushPoint(x=p[0], y=p[1], pressure=1.0) for p in points]

        brush.apply_stroke(layer.image, brush_points, getattr(brush, "brush_color", (0, 0, 0, 255)))

        image_after = layer.image.copy()
        image_after = self._apply_selection_constraint(image_before, image_after)
        layer.image = image_after.copy()
        stroke_label = "Eraser" if self.state.get_tool() == "eraser" else "Brush"
        self._push_layer_pixel_command(layer, image_before, image_after, stroke_label)

        self.state.notify()
        self.refresh_canvas()

    def request_update_brush_size(self, size: int):
        """Update brush size."""

        self.state.update_brush_size(size)

    def request_update_brush_opacity(self, opacity: int):
        """Update the brush opacity."""

        self.state.update_brush_opacity(opacity)

    def request_update_brush_color(self, color_tuple: tuple):
        """Update the brush color."""

        self.state.update_brush_color(color_tuple)

    def request_set_tool(self, tool_name: str):
        """Change active tool."""

        # Cancel active transform gracefully when switching away
        if self.state.has_active_transform() and tool_name != "transform":
            self.cancel_transform()

        self.state.set_tool(tool_name)

    def request_set_brush_by_preset(self, preset_factory, color=None):
        """Create a brush from a preset and assign it to the state."""

        brush_color = color if color is not None else self.state.get_color()

        brush = preset_factory(brush_color) if preset_factory.__name__ != "create_eraser" else preset_factory()

        self.state.set_brush(brush)

    # ==========================================================
    # FILTER REQUESTS
    # ==========================================================

    def request_set_filter(self, filter_id: str):
        """Set the active filter for the selected layer."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        before_id = layer.filter_id
        before_params = dict(layer.filter_params or {})

        self.state.set_layer_filter(filter_id)

        after_id = layer.filter_id
        after_params = dict(layer.filter_params or {})

        if before_id != after_id or before_params != after_params:
            self._get_history().push(
                ReplaceLayerFilterStateCommand(
                    layer, before_id, before_params, after_id, after_params
                )
            )

        self.refresh_canvas()

    def request_update_filter_param(self, param_name: str, value):
        """Update a parameter of the current filter for the selected layer."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        before_id = layer.filter_id
        before_params = dict(layer.filter_params or {})

        normalized_value = self.normalize_value(value)

        self.state.update_layer_filter_param(param_name, normalized_value)

        after_id = layer.filter_id
        after_params = dict(layer.filter_params or {})

        if (before_id != after_id) or (before_params != after_params):

            self._get_history().push(
                ReplaceLayerFilterStateCommand(
                    layer, before_id, before_params, after_id, after_params
                )
            )

        self.refresh_canvas()

    # ==========================================================
    # HISTOGRAM & CURVES
    # ==========================================================

    def get_histogram_for_image(self, image: Image.Image):
        """Return histogram data dict for a PIL image (R, G, B, luma, max_count)."""

        return self.histogram_curve_service.get_histogram(image)

    def open_histogram_curves_dialog(self, parent):
        """Open histogram and curves editor for the selected layer."""

        if not self.state.get_selected_layer():
            return

        from ui.dialogs.histogram_curves import HistogramCurvesDialog

        HistogramCurvesDialog(parent, self)

    def request_histogram_curve_preview(self, snapshot: Image.Image, points: list):
        """Apply curve transformation for live preview."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        base = snapshot.convert("RGBA")
        out = self.histogram_curve_service.apply_curve(base, points)

        layer.image = out.convert("RGBA")

        self.state.notify()
        self.refresh_canvas()

    def request_histogram_curve_commit(self, snapshot: Image.Image, final_image: Image.Image):
        """Commit histogram curve changes to history system."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        self._push_layer_pixel_command(layer, snapshot, final_image, "Curves")

        self.state.notify()
        self.refresh_canvas()

    def request_histogram_curve_cancel(self, snapshot: Image.Image):
        """Revert image back to the original snapshot taken when dialog opened."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        layer.image = snapshot.copy()
        self.state.notify()
        self.refresh_canvas()

    # ==========================================================
    # COLOR ADJUSTMENTS
    # ==========================================================

    def request_preview_color_adjustments(self, snapshot, brightness_slider: float, red_slider: float, green_slider: float, blue_slider: float):
        """Apply real-time color adjustment preview."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        base = snapshot.convert("RGBA")

        out = self.color_adjustment_service.apply_color_adjustments(
            base,
            brightness_slider,
            red_slider,
            green_slider,
            blue_slider
        )

        layer.image = out.convert("RGBA")

        self.state.notify()
        self.refresh_canvas()

    def request_apply_color_adjustments(self):
        """Commit color adjustment changes permanently."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        before = layer.original_image.copy().convert("RGBA")
        after = layer.image.copy().convert("RGBA")

        self._push_layer_pixel_command(layer, before, after, "Color adjust")

        # Persist changes as new baseline
        layer.original_image = after.copy()

        self.state.notify()
        self.refresh_canvas()

    def request_reset_color_adjustments(self):
        """Reset all color adjustments back to original image state."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        layer.image = layer.original_image.copy().convert("RGBA")
        layer.filter_id = "normal"
        layer.filter_params = {}

        self.state.notify()
        self.refresh_canvas()

    # ==========================================================
    # THRESHOLD STACK DIALOG
    # ==========================================================

    def open_threshold_settings_dialog(self, parent):
        """Open threshold stack configuration dialog."""

        if not self.state.get_selected_layer():
            return

        from ui.dialogs.threshold_settings import ThresholdSettingsDialog
        ThresholdSettingsDialog(parent, self)

    def request_threshold_stack_preview(
            self,
            snapshot: Image.Image,
            active_ids: list[str],
            params_by_id: dict[str, dict],
    ):
        """Apply threshold filter stack for live preview."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        base = snapshot.convert("RGBA")

        out = self.threshold_stack_service.apply_stack(
            base,
            active_ids,
            params_by_id
        )

        layer.image = out.convert("RGBA")

        self.state.notify()
        self.refresh_canvas()

    def request_threshold_stack_commit(self, snapshot: Image.Image, final_image: Image.Image):
        """Commit threshold stack changes to history system."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        before = snapshot.copy().convert("RGBA")
        after = final_image.copy().convert("RGBA")

        self._push_layer_pixel_command(layer, before, after, "Threshold stack")

        # Persist new baseline image
        layer.original_image = after.copy()

        self.state.notify()
        self.refresh_canvas()

    def request_threshold_stack_cancel(self, snapshot: Image.Image):
        """Cancel threshold editing and restore snapshot state."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        layer.image = snapshot.copy().convert("RGBA")

        self.state.notify()
        self.refresh_canvas()

    # ==========================================================
    # TOOLS
    # ==========================================================

    def handle_eyedropper(self, x, y):
        """Pick color from image at given coordinates."""

        layer = self.state.get_selected_layer()

        if not layer:
            return None

        color = self.color_picker_service.pick_color(layer, x, y)

        if color:
            self.state.set_color(color)
            return color

        return None

    def handle_fill(self, x, y):
        """Perform flood fill operation on selected layer."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        image = layer.image
        width, height = image.size

        # Validate bounds
        if not (0 <= x < width and 0 <= y < height):
            return

        color = self.state.get_color()

        image_before = layer.image.copy()
        self.fill_service.fill(layer, x, y, color)

        image_after = layer.image.copy()

        # Ensure selection constraints are preserved
        image_after = self._apply_selection_constraint(image_before, image_after)

        layer.image = image_after.copy()

        self._push_layer_pixel_command(layer, image_before, image_after, "Fill")

        self.state.notify()
        self.refresh_canvas()

    def _push_selection_mask_command(self, mask_before, mask_after, label: str = "Selection"):
        """Push selection mask change into history if it is meaningful."""

        if mask_before is None and mask_after is None:
            return

        if (
                mask_before is not None
                and mask_after is not None
                and mask_before.size == mask_after.size
                and mask_before.tobytes() == mask_after.tobytes()
        ):
            return

        cmd = ReplaceSelectionMaskCommand(self.state, mask_before, mask_after, label)
        self._get_history().push(cmd)

    def handle_rect_selection(self, x0, y0, x1, y1):
        """Rectangle selection (geometry-based)."""

        layer = self.state.get_selected_layer()

        if not layer:
            return

        mask_new = self.selection_service.create_rect_mask(
            layer.image.size, x0, y0, x1, y1
        )

        self._apply_selection_with_toggle(mask_new)

    def handle_magic_wand(self, x, y, tolerance=40):
        """Magic wand selection."""

        layer = self.state.get_selected_layer()

        if not layer:
            return

        mask_new = self.selection_service.create_magic_wand_mask(
            layer.image, x, y, tolerance=tolerance
        )

        self._apply_selection_with_toggle(mask_new)

    def _apply_selection_with_toggle(self, mask_new):
        """Apply selection with toggle and undo/redo."""

        if mask_new is None or mask_new.getbbox() is None:
            return

        mask_old = self.state.selection_mask

        same_mask = (
                mask_old is not None and
                mask_old.size == mask_new.size and
                mask_old.tobytes() == mask_new.tobytes()
        )

        if same_mask:
            # Toggle OFF
            self._push_selection_mask_command(mask_old, None, "Clear selection")
            self.state.set_selection_mask(None)
        else:
            # New selection
            self._push_selection_mask_command(mask_old, mask_new, "Selection")
            self.state.set_selection_mask(mask_new)

        self.refresh_canvas()

    def handle_zoom_to_rect(self, x0, y0, x1, y1):
        """Viewport zoom to fit the given image rectangle."""

        if not self._is_editor_screen():
            return

        screen = self.layout.current_screen

        if hasattr(screen, "canvas_panel") and hasattr(screen.canvas_panel, "zoom_to_image_rect"):
            screen.canvas_panel.zoom_to_image_rect(x0, y0, x1, y1)

    def update_active_session_viewport(self, zoom_factor: float, offset_x: float, offset_y: float):
        """Persist viewport on the active tab."""

        session = self._active_session()

        if session:
            session.zoom_factor = zoom_factor
            session.offset_x = offset_x
            session.offset_y = offset_y

    # ==========================================================
    # TRANSFORM TOOL
    # ==========================================================

    def start_transform_from_selection(self):
        """Extract the selected region and begin a floating-transform session."""

        if not self.state.has_selection():
            return

        layer = self.state.get_selected_layer()
        if not layer:
            return

        selection_mask = self.state.get_selection_mask(layer.image.size)
        bbox = selection_mask.getbbox()
        if not bbox:
            return

        image_before = layer.image.copy()

        # Service creates the session (no image logic in controller)
        session = self.transform_service.create_session(layer.image, bbox)

        # Snapshot the layer BEFORE erasing, stored on the session for cancel
        session.layer_snapshot = image_before.copy()

        # Erase the selected region from the layer via the service
        image_after = self.transform_service.erase_selection(image_before, selection_mask)
        layer.image = image_after

        # Store session in state — this triggers notify() → refresh_canvas()
        # so the session must be fully ready before this call
        self.state.set_transform_params(session)

        # Record the pixel removal for undo
        self._push_layer_pixel_command(layer, image_before, image_after, "Transform start")

        self.refresh_canvas()

    def get_transform_preview(self) -> "Image.Image | None":
        """Return a composited PIL image with the floating transform applied."""

        if not self.state.has_active_transform():
            return None

        session = self.state.transform_session
        document = self.state.get_format()
        base_image = document.composite()

        # Cached fast path
        result_np = self.transform_service.get_preview(session)

        return self.transform_service.composite_on_layer(base_image, session, result_np)

    def update_transform(self, dx: float = 0, dy: float = 0, scale=None, rotation=None):
        """Update session parameters and invalidate the preview cache."""

        self.state.update_transform(dx, dy, scale, rotation)
        self.refresh_canvas()

    def apply_transform(self):
        """Commit the floating region onto the active layer."""

        if not self.state.has_active_transform():
            return

        layer = self.state.get_selected_layer()
        if not layer:
            return

        session = self.state.transform_session

        # Produce the final transformed image
        result_np = self.transform_service.apply_final(session)
        transformed_pil = Image.fromarray(result_np).convert("RGBA")

        # Build a full-canvas RGBA overlay positioned
        canvas_size = layer.image.size
        overlay = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

        x = int(session.x)
        y = int(session.y)
        tw, th = transformed_pil.size

        # Clip to canvas bounds so paste never raises
        paste_x = max(0, x)
        paste_y = max(0, y)
        src_x = paste_x - x
        src_y = paste_y - y
        clip_w = min(tw - src_x, canvas_size[0] - paste_x)
        clip_h = min(th - src_y, canvas_size[1] - paste_y)

        if clip_w > 0 and clip_h > 0:
            region = transformed_pil.crop((src_x, src_y, src_x + clip_w, src_y + clip_h))
            overlay.paste(region, (paste_x, paste_y))

        # Alpha-composite the overlay onto the layer
        image_before = layer.image.copy()
        image_after = Image.alpha_composite(layer.image.convert("RGBA"), overlay)
        layer.image = image_after

        # Record in undo history
        self._push_layer_pixel_command(layer, image_before, image_after, "Transform apply")

        self.state.clear_transform_session()
        self.state.clear_selection()

        self.refresh_canvas()

    def cancel_transform(self):
        """Cancel the session and restore the layer WITHOUT touching undo history."""

        if not self.state.has_active_transform():
            return

        layer = self.state.get_selected_layer()
        session = self.state.transform_session

        if layer is not None and session is not None and session.layer_snapshot is not None:
            layer.image = session.layer_snapshot.copy()

        self.state.clear_transform_session()
        self.refresh_canvas()

    def handle_deselect(self):
        """Clear the active selection mask and record it in history."""

        mask_before = self.state.selection_mask
        if mask_before is None:
            return

        self._push_selection_mask_command(mask_before, None, "Deselect")
        self.state.set_selection_mask(None)
        self.refresh_canvas()

    # ==========================================================
    # MERGE OPERATIONS
    # ==========================================================

    def request_merge_two_layers(self, use_average: bool = False):
        """Merge top 2 visible layers and create a new layer."""

        document = self.state.get_format()
        if not document:
            return

        layers = document.get_layers()
        visible_layers = [l for l in layers if l.visible]

        if len(visible_layers) < 2:
            return

        # Top layers visible
        top = visible_layers[-1]
        below = visible_layers[-2]

        base = below.image.convert("RGBA")
        overlay = top.image.convert("RGBA")

        # Select the blend services use
        if use_average:
            merged = self.blend_service.blend_average(base, overlay)
        else:
            merged = self.blend_service.blend(base, overlay)

        # Add the merge in the top
        top_index = layers.index(top)
        insert_index = top_index + 1

        name = "Merged (Average)" if use_average else "Merged"

        document.add_layer(name=name, insert_at=insert_index)
        new_layer = document.layers[insert_index]
        new_layer.image = merged

        self.state.set_selected_layer(insert_index)

        cmd = AddLayerCommand(self.state, document, insert_index, new_layer)
        self._get_history().push(cmd)

        self.refresh_layers()
        self.refresh_canvas()