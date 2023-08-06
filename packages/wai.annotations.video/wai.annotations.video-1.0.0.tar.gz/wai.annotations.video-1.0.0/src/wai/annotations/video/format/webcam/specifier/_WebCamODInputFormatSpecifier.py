from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class WebCamODInputFormatSpecifier(SourceStageSpecifier):
    """
    Base specifier for the label-dist in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads frames from a webcam."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.video.format.webcam.component import WebCamReader
        return WebCamReader,

    """
    Specifier for from-webcam-od in the object-detection domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
