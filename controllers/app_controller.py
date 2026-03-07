from tkinter import messagebox
from core.project import Project
from ui.dialogs.confirm_exit import ConfirmExitDialog
from services.image_service import ImageService
from ui.dialogs.new_project import NewProjectDialog

class AppController:
    """
    Main application controller.

    Responsibilities:
    - Orchestrate the UI, Core, Services
    - Handle navigation
    - Manage state transitions
    - Coordinate file operations
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
        """
        Load home screen and inject recent projects.
        """
        recent_files = self.recent_manager.get_recent()

        self.layout.show("home")

        # current_screen is HomeScreen at this point
        if hasattr(self.layout.current_screen, "set_recent"):
            self.layout.current_screen.set_recent(recent_files)

    # ==========================================================
    # UI REQUESTS
    # ==========================================================

    def request_new_project(self):
        """
        Trigger new project dialog.
        """
        NewProjectDialog(self.root, self._create_project)

    def request_open(self):
        """
        Open project via file dialog.
        """
        project, path = self.file_service.open_image()

        if not project:
            return

        self.state.set_project(project)
        self.recent_manager.add_recent(path)

        self._go_to_editor(project)



    def request_open_recent(self, path):
        """
        Open a project from recent list.
        """

        try:
            project = self.file_service.open_from_path(path)
            self.state.set_project(project)
            self.recent_manager.add_recent(path)
            self._go_to_editor(project)

        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo no existe en la ruta:\n{path}")
            self.recent_manager.remove_recent(path)

        except Exception as e:
            messagebox.showerror("Error inesperado", f"No se pudo abrir el proyecto: {e}")

    def request_save(self):
        """
        Save current project.
        """
        if not self.state.has_project():
            return

        path = self.file_service.save_project(
            self.state.current_project
        )

        if path:
            self.recent_manager.add_recent(path)

    def request_exit(self):
        """
        Handle exit request.
        """
        if self.state.has_project():
            ConfirmExitDialog(self.root, self.root.destroy)
        else:
            self.root.destroy()

    def request_back_home(self):
        """
        Optional: return to home screen.
        """
        self.state.clear_project()
        self.load_home()

    # ==========================================================
    # INTERNAL LOGIC
    # ==========================================================

    def _create_project(self, width, height):
        """
        Internal project creation.
        """
        project = Project(width=width, height=height)

        self.state.set_project(project)
        self._go_to_editor(project)

    def _go_to_editor(self, project):
        """
        Navigate to editor and render project.
        """
        self.layout.show("editor")
        self.layout.load_project_into_editor(project)

    def refresh_canvas(self):
        """
        In the current screen refresh canvas,
        only if is the edit screen.
        """

        screen = self.layout.current_screen

        if screen and hasattr(screen, "refresh"):
            screen.refresh()