from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class ImageViewerODSinkSpecifier(SinkStageSpecifier):
    """
    Specifies the image viewer sink.
    """
    @classmethod
    def description(cls) -> str:
        return "Displays object detection images."

    """
    Specifier for label-dist in the object-detection domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.imgvis.sink.image_viewer.component import ImageViewer
        return ImageViewer,
