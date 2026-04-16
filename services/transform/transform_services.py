from services.transform.transform_adapter import (
    CropAdapter,
    TranslationAdapter,
    RotationAdapter,
    ResizeAdapter
)

class TransformSession:
    def __init__(self, image_np, position):
        self.original = image_np
        self.current = image_np.copy()

        self.x, self.y = position

        self.scale = 1
        self.rotation = 0

class TransformToolService:

    def __init__(self):
        self.crop = CropAdapter()
        self.translate = TranslationAdapter()
        self.resize = ResizeAdapter()
        self.rotate = RotationAdapter()

    def create_session(self, pil_image, bbox):

        img_np = self.crop.from_selection(pil_image, bbox)

        return TransformSession(img_np, (bbox[0], bbox[1]))

    def apply_all(self, session):
        img = session.original.copy()

        # Escale
        img = self.resize.apply(img, session.scale)

        # Rotate
        img = self.rotate.apply(img, session.rotation)

        # Translate
        img = self.translate.apply(img, session.x, session.y)

        return img