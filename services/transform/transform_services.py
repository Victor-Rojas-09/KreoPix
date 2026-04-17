from services.transform.transform_adapter import (
    CropAdapter,
    ResizeAdapter,
    RotationAdapter,
)


class TransformSession:
    """Represents a temporary transformation state."""

    def __init__(self, image_np, position):
        """Initialize a transform session."""

        self.original = image_np

        # Position in the layer (used during composition, NOT inside transform)
        self.x, self.y = position

        # Transformation parameters
        self.scale = 1.0
        self.rotation = 0.0


class TransformToolService:
    """Service responsible for applying transformation pipelines."""

    def __init__(self):
        self.crop = CropAdapter()
        self.resize = ResizeAdapter()
        self.rotate = RotationAdapter()

    def create_session(self, pil_image, bbox):
        """Create a transform session from a selection."""

        img_np = self.crop.from_selection(pil_image, bbox)

        return TransformSession(img_np, (bbox[0], bbox[1]))

    def apply_all(self, session: TransformSession):
        """Apply all transformations to the session image."""

        img = session.original.copy()

        # Apply scaling (may reduce or increase resolution)
        img = self.resize.apply(img, session.scale)

        # Apply rotation
        img = self.rotate.apply(img, session.rotation)

        return img