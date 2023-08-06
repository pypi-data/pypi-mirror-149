from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class VideoFileODOutputFormatSpecifier(SinkStageSpecifier):
    """
    Base specifier for the label-dist in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes frames to a MJPG video file."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.video.format.video_file.component import VideoFileWriter
        return VideoFileWriter,

    """
    Specifier for to-video-file-od in the object-detection domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
