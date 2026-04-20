import tkinter as tk


class IconButton(tk.Label):
    """Icon button methods."""

    def __init__(
        self,
        parent,
        image_path,
        size=(20, 20),
        bg="#444",
        hover_bg="#666",
        active_bg="#777",
        command=None
    ):
        super().__init__(parent, bg=bg, cursor="hand2")

        self.command = command
        self.default_bg = bg
        self.hover_bg = hover_bg
        self.active_bg = active_bg

        # Load image
        self.image = self._load_image(image_path, size)
        self.config(image=self.image)

        # Bind events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _load_image(self, path, size):
        """Load icon image."""

        img = tk.PhotoImage(file=path)

        # Resize using subsample
        w, h = img.width(), img.height()
        scale_w = max(1, int(w / size[0]))
        scale_h = max(1, int(h / size[1]))

        img = img.subsample(scale_w, scale_h)

        return img

    def _on_enter(self, event):
        """Hover enter mouse event."""

        self.config(bg=self.hover_bg)

    def _on_leave(self, event):
        """Hover leave mouse event."""

        self.config(bg=self.default_bg)

    def _on_press(self, event):
        """Hover press mouse event."""

        self.config(bg=self.active_bg)

    def _on_release(self, event):
        """Release mouse event."""

        self.config(bg=self.hover_bg)
        if self.command:
            self.command()