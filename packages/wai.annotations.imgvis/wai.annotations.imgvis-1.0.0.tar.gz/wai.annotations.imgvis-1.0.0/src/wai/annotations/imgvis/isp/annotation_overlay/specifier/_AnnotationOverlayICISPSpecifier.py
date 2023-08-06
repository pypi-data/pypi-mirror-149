from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class AnnotationOverlayICISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the annotation_overlay image ISP (IC).
    """
    @classmethod
    def description(cls) -> str:
        return "Adds the image classification label on top of images passing through."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        if input_domain is ImageClassificationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"AnnotationOverlayIC only handles the following domains: "
                f"{ImageClassificationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.imgvis.isp.annotation_overlay.component import AnnotationOverlayIC
        return AnnotationOverlayIC,
