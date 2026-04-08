from core.image.layer import Layer


def clone_layer(layer: Layer) -> Layer:
    """Return a new Layer with copied pixels and copied metadata."""

    dup = Layer( image=layer.image.copy(), name=layer.name, opacity=layer.opacity)

    dup.visible = layer.visible
    dup.filter_id = layer.filter_id

    dup.filter_params = dict(layer.filter_params) if layer.filter_params else {}
    dup.original_image = layer.original_image.copy()

    return dup
