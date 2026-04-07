"""Stacks of commands for undo and redo."""
from __future__ import annotations

from collections import deque

from services.history.command_base import DocumentCommand


class CommandHistory:
    """
    Keeps undo and redo stacks with a maximum depth to cap memory use.
    Pushing a new command clears the redo stack.
    """

    def __init__(self, max_steps: int = 50):
        self._max_steps = max(1, int(max_steps))
        self._undo_stack: deque[DocumentCommand] = deque(maxlen=self._max_steps)
        self._redo_stack: list[DocumentCommand] = []

    def clear(self) -> None:
        """Drop all undo/redo history (e.g. when loading a new document)."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def push(self, command: DocumentCommand) -> None:
        """Record a command that has already been applied to the document."""
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0

    def undo(self) -> bool:
        """Pop last command, undo it, push onto redo. Returns False if empty."""
        if not self._undo_stack:
            return False
        cmd = self._undo_stack.pop()
        cmd.undo()
        self._redo_stack.append(cmd)
        return True

    def redo(self) -> bool:
        """Pop redo stack, redo it, push back onto undo. Returns False if empty."""
        if not self._redo_stack:
            return False
        cmd = self._redo_stack.pop()
        cmd.redo()
        self._undo_stack.append(cmd)
        return True
