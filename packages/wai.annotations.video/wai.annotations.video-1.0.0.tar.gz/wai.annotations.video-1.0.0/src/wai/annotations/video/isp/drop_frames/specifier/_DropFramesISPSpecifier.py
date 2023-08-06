from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class DropFramesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the drop_frames ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Drops frames from the stream."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        if input_domain is ImageClassificationDomainSpecifier:
            return input_domain
        elif input_domain is ImageObjectDetectionDomainSpecifier:
            return input_domain
        elif input_domain is ImageSegmentationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Crop only handles the following domains: "
                f"{ImageClassificationDomainSpecifier.name()}, "
                f"{ImageObjectDetectionDomainSpecifier.name()}, "
                f"{ImageSegmentationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.video.isp.drop_frames.component import DropFrames
        return DropFrames,
