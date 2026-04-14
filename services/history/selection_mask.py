from PIL import Image
from services.history.command_base import DocumentCommand


class ReplaceSelectionMaskCommand(DocumentCommand):
    """Restore selection mask between two snapshots."""

    def __init__(self,state, mask_before: Image.Image | None, mask_after: Image.Image | None, description: str = "Selection"):

        self._state = state
        self._before = mask_before.copy() if mask_before is not None else None
        self._after = mask_after.copy() if mask_after is not None else None
        self._label = description

    @property
    def description(self) -> str:
        """Return description of the mask."""

        return self._label

    def undo(self) -> None:
        """Undo the mask."""

        self._state.set_selection_mask(self._before)

    def redo(self) -> None:
        """Redo the mask."""

        self._state.set_selection_mask(self._after)
