# services/brushes/base_brush.py
from abc import ABC, abstractmethod

class BaseBrush(ABC):
    """Abstract base class for brushes."""

    def __init__(self, name="Brush", size=100, opacity=100, color=(0,0,0,255), icon=None):
        self.name = name
        self.size = size
        self.opacity = opacity
        self.color = color
        self.icon = icon

    @abstractmethod
    def apply_stroke(self, layer_image, points):
        """
        Apply stroke to the given layer image.
        """
        pass
