class Layer:
    """
    Represents a single image layer.
    """

    def __init__(self, image, name="Layer"):
        self.image = image
        self.name = name

        self.visible = True
        self.opacity = 100

        # layer position inside canvas
        self.x = 0
        self.y = 0