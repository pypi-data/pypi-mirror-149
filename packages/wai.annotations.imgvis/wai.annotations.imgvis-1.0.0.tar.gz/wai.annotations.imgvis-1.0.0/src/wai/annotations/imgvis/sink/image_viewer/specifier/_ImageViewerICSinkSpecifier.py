from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class ImageViewerICSinkSpecifier(SinkStageSpecifier):
    """
    Specifies the image viewer sink.
    """
    @classmethod
    def description(cls) -> str:
        return "Displays image classification images."

    """
    Specifier for label-dist in the image classification domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.imgvis.sink.image_viewer.component import ImageViewer
        return ImageViewer,
