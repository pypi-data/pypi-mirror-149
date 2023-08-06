import cv2
import io
import numpy as np

from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import ImageInstance
from wai.annotations.video.util.change_detection import detect_change


class SkipSimilarFrames(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Stream processor which skips similar frames.
    """

    conversion: str = TypedOption(
        "-c", "--conversion",
        type=str,
        default="gray",
        help="how to convert the BGR image to a single channel image (gray/r/g/b)"
    )

    bw_threshold: int = TypedOption(
        "-b", "--bw-threshold",
        type=int,
        default=128,
        help="the threshold to use for converting a gray-scale like image to black and white (0-255)"
    )

    change_threshold: float = TypedOption(
        "-t", "--change-threshold",
        type=float,
        default=0.01,
        help="the percentage of pixels that changed relative to size of image (0-1)"
    )

    verbose: bool = FlagOption(
        "-v", "--verbose",
        help="whether to output some debugging output."
    )

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        if not hasattr(self, "_last_image"):
            self._last_image = None

        # read image
        img_array = np.fromstring(io.BytesIO(element.data.data).read(), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # nothing to compare against?
        if self._last_image is None:
            # shift state
            self._last_image = img
            # forward frame
            then(element)
            return

        # detect change
        ratio, changed = detect_change(self._last_image, img,
                                       self.conversion, self.bw_threshold, self.change_threshold)
        if self.verbose:
            self.logger.info("%s (ratio/changed): %f -> %s" % (element.data.filename, ratio, str(changed)))

        if changed:
            # shift state
            self._last_image = img
            # forward frame
            then(element)
