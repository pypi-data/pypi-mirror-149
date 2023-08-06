import cv2
import io
import numpy as np

from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance

from wai.common.cli.options import TypedOption


class VideoFileWriter(
    SinkComponent[ImageObjectDetectionInstance]
):

    output_file: str = TypedOption(
        "-o", "--output",
        type=str,
        default="",
        help="the MJPG video file to write to"
    )

    fps: int = TypedOption(
        "-f", "--fps",
        type=int,
        default=25,
        help="the frames per second to use"
    )

    def consume_element(self, element: ImageObjectDetectionInstance):
        """
        Consumes instances.
        """

        img_array = np.fromstring(io.BytesIO(element.data.data).read(), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # open video file
        if not hasattr(self, "_out"):
            h, w, _ = img.shape
            self._out = cv2.VideoWriter(self.output_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, (w, h))

        self._out.write(img)

    def finish(self):
        if hasattr(self, "_out"):
            self._out.release()
