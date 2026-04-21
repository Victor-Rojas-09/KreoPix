from PIL import Image
import numpy as np
from services.transform.transform_adapter import CropAdapter, ResizeAdapter, RotationAdapter


class TransformSession:
    """
    Pure data object — no service dependencies, no image logic.
    Holds the extracted pixel region and all transformation parameters.
    """

    def __init__(self, image_np: np.ndarray, position: tuple[int, int]):
        self.original: np.ndarray = image_np
        self.x: float = float(position[0])
        self.y: float = float(position[1])
        self.scale: float = 1.0
        self.rotation: float = 0.0

        # Cache state
        self.dirty: bool = True
        self._cache: np.ndarray | None = None

        # Snapshot stored by controller before erasing pixels; used by cancel
        self.layer_snapshot: Image.Image | None = None


class TransformToolService:
    """Centralised transformation pipeline, scale to rotate."""

    _PIPELINE = ("scale", "rotate")

    def __init__(self):
        self.crop   = CropAdapter()
        self.resize = ResizeAdapter()
        self.rotate = RotationAdapter()

    def create_session(
        self,
        pil_image: Image.Image,
        bbox: tuple[int, int, int, int],
    ) -> TransformSession:
        """Crop the bounding-box region from *pil_image* and wrap it in a session."""

        img_np = self.crop.from_selection(pil_image, bbox)
        return TransformSession(img_np, (bbox[0], bbox[1]))

    def erase_selection(
        self,
        image: Image.Image,
        selection_mask: Image.Image,
    ) -> Image.Image:
        """Return a copy of *image* with the masked region made fully transparent."""

        transparent = Image.new("RGBA", image.size, (0, 0, 0, 0))

        return Image.composite(transparent, image.convert("RGBA"), selection_mask)

    def _run_pipeline(self, session: TransformSession) -> np.ndarray:
        """Apply transformations in canonical order."""

        img = session.original.copy()

        for step in self._PIPELINE:
            if step == "scale":
                img = self.resize.apply(img, session.scale)
            elif step == "rotate":
                img = self.rotate.apply(img, session.rotation)

        return img

    def get_preview(self, session: TransformSession) -> np.ndarray:
        """Return the transformed result."""

        if not session.dirty and session._cache is not None:
            return session._cache

        result = self._run_pipeline(session)
        session._cache = result
        session.dirty  = False

        return result

    def apply_final(self, session: TransformSession) -> np.ndarray:
        """Produce the final result without consulting the cache."""

        return self._run_pipeline(session)

    def composite_on_layer(self, layer_pil: Image.Image, session: TransformSession, result_np: np.ndarray) -> Image.Image:
        """Paste result onto layer at the session position."""

        transformed_pil = Image.fromarray(result_np).convert("RGBA")

        base    = layer_pil.convert("RGBA").copy()
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))

        x = int(session.x)
        y = int(session.y)

        overlay.paste(transformed_pil, (x, y))
        return Image.alpha_composite(base, overlay)