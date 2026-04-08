from dataclasses import dataclass, field
from core.state.app_state import AppState
from services.history.command_history import CommandHistory


@dataclass
class EditorSession:
    """One open project tab with its own AppState and command history."""

    state: AppState
    history: CommandHistory = field(default_factory=lambda: CommandHistory(max_steps=50))
    display_title: str = "Untitled"
    source_path: str | None = None
    zoom_factor: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
