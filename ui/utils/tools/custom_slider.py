import tkinter as tk
from tkinter import simpledialog


class BaseSlider(tk.Canvas):
    """
    Base class for custom sliders.

    Handles:
    - Value management (min, max, clamp)
    - Mouse interaction
    - Callback system
    - Value-position conversion
    """

    def __init__(
        self,
        parent,
        width=200,
        height=20,
        min_value=0,
        max_value=100,
        initial_value=None,
        command=None,
        release_command=None,
        bg="#333"
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=bg,
            highlightthickness=0
        )

        # Model
        self.min = min_value
        self.max = max_value
        self.value = initial_value if initial_value is not None else min_value

        # Callbacks
        self.command = command
        self.release_command = release_command

        # Dimensions
        self.width = width
        self.height = height


        # Events
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Double-Button-1>", self._on_double_click)
        self.bind("<Configure>", self._on_resize)

    # ==================================================
    # Conversion methods
    # ==================================================
    def value_to_x(self, value):
        """Convert a value to an x-coordinate."""

        ratio = (value - self.min) / (self.max - self.min)
        return ratio * self.width

    def x_to_value(self, x):
        """Convert an x-coordinate to a value."""

        ratio = x / self.width
        return self.min + ratio * (self.max - self.min)

    # ==================================================
    # Event handlers
    # ==================================================
    def _on_click(self, event):
        """Handle mouse click event."""

        self._update_from_event(event)

    def _on_drag(self, event):
        """Handle mouse drag event."""

        self._update_from_event(event)

    def _update_from_event(self, event):
        """Update slider value based on mouse position."""

        value = self.x_to_value(event.x)
        self.set_value(value)

    def _on_release(self, event):
        """Handle release event."""

        if self.release_command:
            self.release_command(self.value)

    def _on_double_click(self, event):
        """Handle double click event."""

        value = simpledialog.askfloat(
            "Set value",
            f"Enter value ({self.min} to {self.max}):",
            initialvalue=self.value
        )

        if value is not None:
            self.set_value(value, trigger=True)

    def _on_resize(self, event):
        """Handle resize event."""

        self.width = event.width
        self.height = event.height
        self.draw()

    # ==================================================
    # Public API
    # ==================================================
    def set_value(self, value, trigger=True):
        """Set slider value (clamped to range)."""

        clamped = max(self.min, min(self.max, value))
        self.value = clamped
        self.draw()

        if trigger and self.command:
            self.command(self.value)

    def get_value(self):
        """Get slider value."""

        return self.value


class BlueSlider(BaseSlider):
    """Standard linear slider."""

    def __init__(
        self,
        parent,
        bg_empty="#e0e0e0",
        bg_filled="#0078ff",
        **kwargs
    ):

        super().__init__(parent, **kwargs)

        self.bg_empty = bg_empty
        self.bg_filled = bg_filled

        self.draw()

    def draw(self):
        """Draw slider."""

        self.delete("all")

        # Background
        self.create_rectangle(
            0, 0, self.width, self.height,
            fill=self.bg_empty,
            outline=""
        )

        fill_x = self.value_to_x(self.value)

        # Filled bar
        self.create_rectangle(
            0, 0, fill_x, self.height,
            fill=self.bg_filled,
            outline=""
        )


class DarkRangeSlider(BaseSlider):
    """Bipolar dark slider centered."""

    def __init__(
        self,
        parent,
        track_color="#2b2b2b",
        negative_color="#ff5555",
        positive_color="#4aa3ff",
        handle_color="#dddddd",
        **kwargs
    ):
        super().__init__(parent, bg="#1e1e1e", **kwargs)

        self.track_color = track_color
        self.negative_color = negative_color
        self.positive_color = positive_color
        self.handle_color = handle_color

        self.draw()

    def center_x(self):
        """Center x slider."""

        return self.value_to_x(0)

    def draw(self):
        """Draw slider."""

        self.delete("all")

        mid_y = self.height // 2

        # Track
        self.create_line(
            0, mid_y,
            self.width, mid_y,
            fill=self.track_color,
            width=4
        )

        center = self.center_x()
        current = self.value_to_x(self.value)

        # Negative side
        if self.value < 0:
            self.create_line(
                current, mid_y,
                center, mid_y,
                fill=self.negative_color,
                width=4
            )

        # Positive side
        elif self.value > 0:
            self.create_line(
                center, mid_y,
                current, mid_y,
                fill=self.positive_color,
                width=4
            )

        # Handle
        r = self.height // 3
        self.create_oval(
            current - r, mid_y - r,
            current + r, mid_y + r,
            fill=self.handle_color,
            outline=""
        )
