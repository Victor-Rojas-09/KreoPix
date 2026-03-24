from .brush_utils import BrushUtils

class BrushCache:
    """Caches brush masks to avoid recomputing them for the same size and type."""

    _mask_cache = {}

    @classmethod
    def get_mask(cls, size: int, soft: bool = True):
        """Retrieve a cached brush mask or generate it if not available."""

        key = (size, soft)

        if key not in cls._mask_cache:
            cls._mask_cache[key] = (
                BrushUtils.create_soft_mask(size)
                if soft
                else BrushUtils.create_hard_mask(size)
            )

        return cls._mask_cache[key]