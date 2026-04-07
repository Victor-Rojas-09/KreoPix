"""Base abstraction for undoable document commands (Command Pattern)."""
from abc import ABC, abstractmethod


class DocumentCommand(ABC):
    """
    Undoable change to the document.

    Implementations store enough data to restore prior state on undo()
    and re-apply changes on redo().
    """

    @property
    def description(self) -> str:
        """Short label for UI (e.g. future granular undo menu)."""
        return self.__class__.__name__

    @abstractmethod
    def undo(self) -> None:
        """Revert the change."""
        raise NotImplementedError

    @abstractmethod
    def redo(self) -> None:
        """Re-apply the change after an undo."""
        raise NotImplementedError
