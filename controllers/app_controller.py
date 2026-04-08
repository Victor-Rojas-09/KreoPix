from tkinter import messagebox
import os
from PIL import Image

from ui.utils.dialogs.confirm_exit import ConfirmExitDialog
from ui.utils.dialogs.new_project import NewProjectDialog
from services.images.image_service import ImageService
from services.brushes.color_picker_service import ColorPickerService
from services.brushes.fill_service import FillService
from services.selection import SelectionService
from services.history import (
    AddLayerCommand,
    CommandHistory,
    RemoveLayerCommand,
    ReplaceLayerFilterStateCommand,
    ReplaceLayerImageCommand,
    ReplaceLayerOpacityCommand,
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
    """

    # ==========================================================
    # CLASS CONSTRUCTOR
    # ==========================================================

    def __init__(self, root, layout, state, file_service, recent_manager):
        self.root = root
        self.layout = layout
        self.state = state
        self.file_service = file_service
        self.recent_manager = recent_manager
        self.image_service = ImageService()
        self.color_picker_service = ColorPickerService()
        self.fill_service = FillService()
        self.selection_service = SelectionService()
        self._history = CommandHistory(max_steps=50)
        self._bind_edit_shortcuts()

    # ==========================================================
    # UNDO / REDO
    # ==========================================================

    def _clear_history(self):
        """Reset undo/redo when the document is replaced or closed."""

        self._history.clear()

    def can_undo(self) -> bool:
        return self._history.can_undo()

    def can_redo(self) -> bool:
        return self._history.can_redo()

    def request_undo(self):
        """Undo the last document change."""

        if not self.state.has_format():
            return
        if self._history.undo():
            self.state.notify()
            self.refresh_layers()
            self.refresh_canvas()

    def request_redo(self):
        """Redo the last undone change."""

        if not self.state.has_format():
            return
        if self._history.redo():
            self.state.notify()
            self.refresh_layers()
            self.refresh_canvas()

    def _is_editor_screen(self) -> bool:
        from ui.screens.editor_screen import EditorScreen

        return isinstance(self.layout.current_screen, EditorScreen)

    def _bind_edit_shortcuts(self):
        """Global shortcuts; only act while the editor screen is active."""

        self.root.bind_all("<Control-z>", self._shortcut_undo)
        self.root.bind_all("<Control-y>", self._shortcut_redo)
        self.root.bind_all("<Control-Shift-Z>", self._shortcut_redo)

    def _shortcut_undo(self, event=None):
        if self._is_editor_screen() and self.state.has_format():
            self.request_undo()
            return "break"

    def _shortcut_redo(self, event=None):
        if self._is_editor_screen() and self.state.has_format():
            self.request_redo()
            return "break"

    def _push_layer_pixel_command(self, layer, image_before, image_after, description: str):
        """Record brush/fill/eraser if pixels actually changed."""

        if image_before.tobytes() == image_after.tobytes():
            return
        cmd = ReplaceLayerImageCommand(layer, image_before, image_after, description=description)
        self._history.push(cmd)

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

        self._clear_history()
        self.state.set_format(document)
        if path:
            self.recent_manager.add_recent(path)

        self._go_to_editor(document)

    def request_open_recent(self, path):
        """Open a project from recent list."""

        try:
            document = self.file_service.open_from_path(path)
            self._clear_history()
            self.state.set_format(document)
            self.recent_manager.add_recent(path)
            self._go_to_editor(document)

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

        self._clear_history()
        self.state.clear_format()
        self.load_home()

    # ==========================================================
    # INTERNAL LOGIC
    # ==========================================================

    def _create_project(self, width, height):
        """
        Create a new blank document and open editor.
        Always includes a background layer and an initial editable layer.
        """

        document = self.image_service.create_blank_format(width, height)

        # Add initial editable transparent layer
        document.add_layer(name="Layer 1")

        self._clear_history()
        self.state.set_format(document)
        self.state.set_selected_layer(len(document.get_layers()) - 1)

        self._go_to_editor(document)

    def _go_to_editor(self, document):
        """Navigate to editor and load project."""

        self.layout.show("editor")
        self.layout.load_project_into_editor(document)

        # Initial refresh
        self.refresh_layers()
        self.refresh_canvas()

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
        self._history.push(
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
            self._history.push(
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
        self._history.push(cmd)

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
            self._history.push(
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
        if before_id != after_id or before_params != after_params:
            self._history.push(
                ReplaceLayerFilterStateCommand(
                    layer, before_id, before_params, after_id, after_params
                )
            )

        self.refresh_canvas()

    # ==========================================================
    # Tools
    # ==========================================================

    def handle_eyedropper(self, x, y):
        """Handle eyedropper."""

        layer = self.state.get_selected_layer()
        if not layer:
            return None

        color = self.color_picker_service.pick_color(layer, x, y)

        if color:
            self.state.set_color(color)
            return color
        return None

    def handle_fill(self, x, y):
        """Apply flood fill on selected layer."""

        layer = self.state.get_selected_layer()
        if not layer:
            return

        image = layer.image
        width, height = image.size

        if not (0 <= x < width and 0 <= y < height):
            return

        color = self.state.get_color()

        image_before = layer.image.copy()
        self.fill_service.fill(layer, x, y, color)
        image_after = layer.image.copy()
        image_after = self._apply_selection_constraint(image_before, image_after)
        layer.image = image_after.copy()
        self._push_layer_pixel_command(layer, image_before, image_after, "Fill")

        self.state.notify()
        self.refresh_canvas()

    def handle_rect_selection(self, x0, y0, x1, y1):
        """Create a rectangular selection mask in document space."""

        layer = self.state.get_selected_layer()
        if not layer:
            return
        mask = self.selection_service.create_rect_mask(layer.image.size, x0, y0, x1, y1)
        self.state.set_selection_mask(mask)
        self.refresh_canvas()

    def handle_magic_wand(self, x, y, tolerance=40):
        """Create a contiguous color-similarity selection from active layer."""

        layer = self.state.get_selected_layer()
        if not layer:
            return
        mask = self.selection_service.create_magic_wand_mask(layer.image, x, y, tolerance=tolerance)
        if mask is not None:
            self.state.set_selection_mask(mask)
            self.refresh_canvas()
