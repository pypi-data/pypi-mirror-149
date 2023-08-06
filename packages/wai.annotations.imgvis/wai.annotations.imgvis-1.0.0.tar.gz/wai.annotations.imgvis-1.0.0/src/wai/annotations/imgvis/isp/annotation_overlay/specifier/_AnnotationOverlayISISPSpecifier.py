from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class AnnotationOverlayISISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the annotation_overlay image ISP (IS).
    """
    @classmethod
    def description(cls) -> str:
        return "Adds the image segmentation annotations on top of images passing through."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        if input_domain is ImageSegmentationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"AnnotationOverlayIS only handles the following domains: "
                f"{ImageSegmentationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.imgvis.isp.annotation_overlay.component import AnnotationOverlayIS
        return AnnotationOverlayIS,
