import cv2

from wai.annotations.core.component import SourceComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.image import Image, ImageFormat
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance

from wai.common.cli.options import TypedOption
from wai.common.adams.imaging.locateobjects import LocatedObjects


class WebCamReader(
    SourceComponent[ImageObjectDetectionInstance]
):

    webcam_id: int = TypedOption(
        "-i", "--webcam-id",
        type=int,
        default=0,
        help="the webcam ID to read from"
    )

    from_frame: int = TypedOption(
        "-f", "--from-frame",
        type=int,
        default=1,
        help="determines with which frame to start the stream (1-based index)"
    )

    to_frame: int = TypedOption(
        "-t", "--to-frame",
        type=int,
        default=-1,
        help="determines after which frame to stop (1-based index); ignored if <=0"
    )

    nth_frame: int = TypedOption(
        "-n", "--nth-frame",
        type=int,
        default=1,
        help="determines whether frames get skipped and only evert nth frame gets forwarded"
    )

    max_frames: int = TypedOption(
        "-m", "--max-frames",
        type=int,
        default=-1,
        help="determines the maximum number of frames to read; ignored if <=0"
    )

    prefix: str = TypedOption(
        "-p", "--prefix",
        type=str,
        default="webcam-",
        help="the prefix to use for the frames"
    )

    """
    The source of elements in a stream.
    """
    def produce(
            self,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        """
        Produces elements and inserts them into the stream. Should call 'then'
        for each element produced, and then call 'done' when finished.

        :param then:    A function which forwards elements into the stream.
        :param done:    A function which closes the stream when called.
        """
        # open video file
        if not hasattr(self, "_cap"):
            self._cap = cv2.VideoCapture(self.webcam_id)
            self._frame_no = 0
            self._frame_count = 0

        # next frame?
        count = 0
        while (self._cap is not None) and self._cap.isOpened():
            # next frame
            self._frame_no += 1
            count += 1
            retval, frame_curr = self._cap.read()

            if retval:
                # within frame window?
                if self.from_frame > 0:
                    if self._frame_no < self.from_frame:
                        continue
                if self.to_frame > 0:
                    if self._frame_no >= self.to_frame:
                        break

                # skip frame?
                if (self.nth_frame > 1) and (count < self.nth_frame):
                    continue

                # max frames reached?
                if (self.max_frames > 0) and (self._frame_count >= self.max_frames):
                    break

                self._frame_count += 1
                count = 0
                data = cv2.imencode(".jpg", frame_curr)[1].tobytes()
                filename = "%s%08d.jpg" % (self.prefix, self._frame_no)
                height, width, _ = frame_curr.shape
                image = Image(filename=filename, data=data, format=ImageFormat.JPG, size=(width, height))
                instance = ImageObjectDetectionInstance(data=image, annotations=LocatedObjects())
                then(instance)
            else:
                self._cap.release()
                self._cap = None
                done()

        # close video file
        if self._cap is not None:
            self._cap.release()
            done()
