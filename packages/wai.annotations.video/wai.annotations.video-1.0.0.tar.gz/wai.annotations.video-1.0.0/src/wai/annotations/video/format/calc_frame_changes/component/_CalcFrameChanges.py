import csv
import cv2
import io
import json
import numpy as np
import sys
import termplotlib as tpl

from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.video.util.change_detection import detect_change


class CalcFrameChanges(
    SinkComponent[ImageObjectDetectionInstance]
):

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

    num_bins: int = TypedOption(
        "-B", "--num-bins",
        type=int,
        default=20,
        help="the number of bins to use for the histogram"
    )

    output_format: str = TypedOption(
        "-f", "--output-format",
        type=str,
        default="text",
        help="how to output the statistics (text/csv/json)"
    )

    output_file: str = TypedOption(
        "-o", "--output",
        type=str,
        default="",
        help="the file to write to statistics to, stdout if not provided"
    )

    verbose: bool = FlagOption(
        "-v", "--verbose",
        help="whether to output some debugging output."
    )

    def output_stats(self):
        """
        Calculates and outputs the statistics.
        """
        if not hasattr(self, "_ratios"):
            self.logger.error("Not data collected for statistics!")
            return

        use_stdout = len(self.output_file) == 0
        counts, bin_edges = np.histogram(self._ratios, bins=self.num_bins)

        # text
        if self.output_format == "text":
            fig = tpl.figure()
            fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False)
            if use_stdout:
                fig.show()
            else:
                with open(self.output_file, "w") as fp:
                    fp.write(fig.get_string())
                    fp.write("\n")

        # csv
        elif self.output_format == "csv":
            data = [["bin", "from", "to", "count"]]
            for i in range(self.num_bins):
                data.append([i, bin_edges[i], bin_edges[i+1], counts[i]])
            if use_stdout:
                writer = csv.writer(sys.stdout)
                writer.writerows(data)
            else:
                with open(self.output_file, "w") as fp:
                    writer = csv.writer(fp)
                    writer.writerows(data)

        # json
        elif self.output_format == "json":
            data = []
            for i in range(self.num_bins):
                data.append({
                    "bin": i,
                    "from": float(bin_edges[i]),
                    "to": float(bin_edges[i+1]),
                    "count": int(counts[i])
                })
            if use_stdout:
                print(json.dumps(data, indent=2))
            else:
                with open(self.output_file, "w") as fp:
                    json.dump(data, fp, indent=2)

    def consume_element(self, element: ImageObjectDetectionInstance):
        """
        Consumes instances.
        """
        if not hasattr(self, "_last_image"):
            self._last_image = None
            self._ratios = []

        # read image
        img_array = np.fromstring(io.BytesIO(element.data.data).read(), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # nothing to compare against?
        if self._last_image is None:
            # shift state
            self._last_image = img
            return

        # detect change
        ratio, changed = detect_change(self._last_image, img,
                                       self.conversion, self.bw_threshold, self.change_threshold)
        if self.verbose:
            self.logger.info("%s (ratio/changed): %f -> %s" % (element.data.filename, ratio, str(changed)))

        if changed:
            # shift state
            self._last_image = img
            self._ratios.append(ratio)

    def finish(self):
        self.output_stats()
