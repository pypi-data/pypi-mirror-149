from wai.common.cli.options import TypedOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import ImageInstance


class DropFrames(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Stream processor which drops frames.
    """

    nth_frame: int = TypedOption(
        "-n", "--nth-frame",
        type=int,
        default=0,
        help="which nth frame to drop, e..g, '2' means to drop every 2nd frame; passes frames through if <=1"
    )

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        # nothing to do?
        if self.nth_frame <= 1:
            then(element)
            return

        if not hasattr(self, "_count"):
            self._count = 0

        self._count += 1
        if (self._count % self.nth_frame) != 0:
            then(element)
        else:
            self._count = 0
