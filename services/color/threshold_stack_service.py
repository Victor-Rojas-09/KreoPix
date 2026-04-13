from PIL import Image

from services.filters.filter_service import FilterService


class ThresholdStackService:
    """Apply multiple threshold-type filters in fixed registry order."""

    ORDERED_FILTER_IDS = (
        "global_binarize",
        "adaptive_gaussian",
        "adaptive_mean",
        "canny_edge",
        "otsu_binarize",
        "brightness",
        "red_adjust",
        "blue_adjust",
        "green_adjust"
    )

    def __init__(self):
        self._filter_service = FilterService()

    def apply_stack(self, image, active_ids: list[str], params_by_id: dict[str, dict]) -> Image.Image:
        """Run each active filter in ORDERED_FILTER_IDS order."""

        if image is None:
            return None

        result = image.convert("RGBA")
        for fid in self.ORDERED_FILTER_IDS:
            if fid not in active_ids:
                continue
            params = params_by_id.get(fid, {})
            result = self._filter_service.apply(result, fid, params)
        return result
