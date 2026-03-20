from tkinter import messagebox
import os

from ui.utils.dialogs.confirm_exit import ConfirmExitDialog
from ui.utils.dialogs.new_project import NewProjectDialog
from services.images.image_service import ImageService
from services.brushes.stroke import BrushPoint

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

        self.state.set_format(document)
        if path:
            self.recent_manager.add_recent(path)

        self._go_to_editor(document)

    def request_open_recent(self, path):
        """Open a project from recent list."""

        try:
            document = self.file_service.open_from_path(path)
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
    # CANVAS / UI REFRESH
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

    # ==========================================================
    # LAYER OPERATIONS
    # ==========================================================

    def add_new_layer(self, name=None):
        """Add a new layer by position and index."""

        document = self.get_document()

        if not document:
            return

        if name is None:
            name = f"Layer {len(document.get_layers()) + 1}"

        # Insert new layer after selected index
        index = self.state.selected_layer_index
        document.add_layer(name=name)

        self.state.set_selected_layer(index + 1)

        # Refresh the canvas after adding
        self.refresh_layers()
        self.refresh_canvas()

    def select_layer(self, index):
        """Select layer by index."""

        self.state.set_selected_layer(index)
        self.refresh_layers()
        self.refresh_canvas()

    def remove_selected_layer(self):
        """Remove currently selected layer via state."""

        if self.state:
            self.state.remove_selected_layer()

    # ==========================================================
    # BRUSH OPERATIONS
    # ==========================================================
    def handle_paint_stroke(self, points):
        """To handle paint strokes."""

        document = self.state.get_format()
        if not document:
            return

        layer = self.state.get_selected_layer()
        if not layer:
            return

        brush = self.state.get_brush()
        if not brush:
            return

        brush_points = [
            BrushPoint(x=p[0], y=p[1], pressure=1.0)
            for p in points
        ]

        brush.apply_stroke(layer.image, brush_points)

        self.state._notify()
        self.refresh_canvas()

    def request_update_brush_size(self, size: int):
        """Update brush size via AppState."""

        self.state.update_brush_size(size)

    def request_update_brush_opacity(self, opacity: int):
        """Update brush opacity via AppState."""

        self.state.update_brush_opacity(opacity)

    def request_update_brush_color(self, color_tuple: tuple):
        """Update brush color via AppState."""

        self.state.update_brush_color(color_tuple)
