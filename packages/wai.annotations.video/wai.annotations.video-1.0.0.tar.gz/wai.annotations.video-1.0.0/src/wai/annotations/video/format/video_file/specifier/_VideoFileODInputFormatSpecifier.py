from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class VideoFileODInputFormatSpecifier(SourceStageSpecifier):
    """
    Base specifier for the label-dist in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads frames from a video file."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.video.format.video_file.component import VideoFileReader
        return VideoFileReader,

    """
    Specifier for from-video-file-od in the object-detection domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
