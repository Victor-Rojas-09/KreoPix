from PIL import Image
import numpy as np
from core.library.transform.crop import ImageCrop
from core.library.transform.resize import ImageReduction, ImageUpscale
from core.library.transform.translation import ImageTranslation

class CropAdapter:

    def __init__(self):
        self.cropper = ImageCrop()

    def from_selection(self, pil_image, bbox):
        np_img = np.array(pil_image)

        x0, y0, x1, y1 = bbox

        cropped = self.cropper.apply(np_img, x0, x1, y0, y1)

        return cropped



class TranslationAdapter:

    def __init__(self):
        self.translator = ImageTranslation()

    def apply(self, img_np, dx, dy):
        return self.translator.apply(img_np, dx, dy)



class ResizeAdapter:

    def __init__(self):
        self.reducer = ImageReduction()
        self.upscaler = ImageUpscale()

    def apply(self, img_np, factor):
        if factor > 1:
            return self.upscaler.apply(img_np, int(factor))
        elif factor < 1:
            return self.reducer.apply(img_np, int(1/factor))
        return img_np

class RotationAdapter:

    def apply(self, img_np, angle):
        pil = Image.fromarray(img_np)
        rotated = pil.rotate(angle, expand=True)
        return np.array(rotated)
