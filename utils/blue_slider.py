import tkinter as tk


class BlueSlider(tk.Canvas):
    """The slider configuration for handling the opacity of the layer"""

    def __init__(
        self,
        parent,
        width=200,
        height=18,
        bg_empty="#e0e0e0",
        bg_filled="#0078ff",
        command=None
    ):

        super().__init__(
            parent,
            width=width,
            height=height,
            bg="#555",
            highlightthickness=0
        )

        self.width = width
        self.height = height

        self.bg_empty = bg_empty
        self.bg_filled = bg_filled

        self.command = command

        self.value = 100

        self.draw()

        self.bind("<Button-1>", self.update_value)
        self.bind("<B1-Motion>", self.update_value)
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        """update the width on widget went change."""
        self.width = event.width
        self.draw()

    def draw(self):

        self.delete("all")

        # Gray background
        self.create_rectangle(
            0, 0,
            self.width,
            self.height,
            fill=self.bg_empty,
            outline=""
        )

        # Blue width
        fill_width = (self.value / 100) * self.width

        # Blue part
        self.create_rectangle(
            0, 0,
            fill_width,
            self.height,
            fill=self.bg_filled,
            outline=""
        )

    def update_value(self, event):

        raw = (event.x / self.width) * 100

        self.value = int(max(0, min(100, raw)))

        self.draw()

        if self.command:
            self.command(self.value)

    def set_value(self, value):

        self.value = int(max(0, min(100, value)))

        self.draw()

    def get_value(self):

        return self.value