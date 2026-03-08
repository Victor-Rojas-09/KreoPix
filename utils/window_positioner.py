class WindowPositioner:
    """Window positioning utilities."""

    @staticmethod
    def center_to_parent(window, parent, width, height):
        """Center window relative parent."""

        parent.update_idletasks()

        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()

        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        pos_x = parent_x + (parent_w // 2) - (width // 2)
        pos_y = parent_y + (parent_h // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")


    @staticmethod
    def center_to_screen(window, width, height):
        """Center window on screen."""

        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()

        pos_x = (screen_w // 2) - (width // 2)
        pos_y = (screen_h // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")