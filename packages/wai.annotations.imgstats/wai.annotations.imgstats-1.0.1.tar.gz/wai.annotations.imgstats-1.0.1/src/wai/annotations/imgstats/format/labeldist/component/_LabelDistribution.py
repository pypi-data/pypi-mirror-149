import csv
import json
import sys
from collections import OrderedDict
import numpy as np

from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.image import ImageInstance
from wai.annotations.domain.image.classification import ImageClassificationInstance
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.domain.image.segmentation import ImageSegmentationInstance

from wai.common.cli.options import TypedOption, FlagOption

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]


class LabelDistribution(
    SinkComponent[ImageInstance]
):
    output_format: str = TypedOption(
        "-f", "--format",
        type=str,
        default=OUTPUT_FORMAT_TEXT,
        help="the format to use for the output, available modes: %s" % ", ".join(OUTPUT_FORMATS)
    )

    output_file: str = TypedOption(
        "-o", "--output",
        type=str,
        default="",
        help="the file to write the statistics to; uses stdout if omitted"
    )

    percentages: bool = FlagOption(
        "-p", "--percentages",
        help="whether to output percentages instead of counts."
    )

    def init_labels(self):
        """
        Initializes the labels.
        """
        if not hasattr(self, "_labels"):
            self._labels = dict()

    def add_label(self, label):
        """
        Increments the count for the label.
        """
        self.init_labels()

        if label not in self._labels:
            self._labels[label] = 0

        self._labels[label] = self._labels[label] + 1

    def output_text(self, dist, keys, use_stdout):
        """
        Outputs the label distribution in simple textual format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            for k in keys:
                if self.percentages:
                    print("%s: %f" % (k, dist[k]))
                else:
                    print("%s: %d" % (k, dist[k]))
        else:
            with open(self.output_file, "w") as f:
                for k in keys:
                    if self.percentages:
                        f.write("%s: %f" % (k, dist[k]))
                    else:
                        f.write("%s: %d" % (k, dist[k]))
                    f.write("\n")

    def output_csv(self, dist, keys, use_stdout):
        """
        Outputs the label distribution in CSV format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            writer = csv.writer(sys.stdout)
            f = None
        else:
            f = open(self.output_file, "w")
            writer = csv.writer(f)

        writer.writerow(["Label", "Percent" if self.percentages else "Count"])
        for k in keys:
            writer.writerow([k, dist[k]])

        if f is not None:
            f.close()

    def output_json(self, dist, use_stdout):
        """
        Outputs the label distribution in json format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            print(json.dumps(dist, indent=2))
        else:
            with open(self.output_file, "w") as f:
                json.dump(dist, f, indent=2)

    def output_label_distribution(self):
        """
        Outputs the distribution.
        """
        keys = list(self._labels.keys())
        sorted(keys)
        dist = OrderedDict()
        for k in keys:
            dist[k] = self._labels[k]

        if self.percentages:
            total = 0
            for k in dist:
                total += dist[k]
            for k in dist:
                dist[k] = dist[k] / total * 100.0

        use_stdout = len(self.output_file) == 0

        if self.output_format == "text":
            self.output_text(dist, keys, use_stdout)
        elif self.output_format == "csv":
            self.output_csv(dist, keys, use_stdout)
        elif self.output_format == "json":
            self.output_json(dist, use_stdout)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

    def consume_element(self, element: ImageInstance):
        """
        Consumes instances by discarding them.
        """
        if isinstance(element, ImageClassificationInstance):
            self.add_label(element.annotations.label)
        elif isinstance(element, ImageObjectDetectionInstance):
            for obj in element.annotations:
                if "type" in obj.metadata:
                    self.add_label(obj.metadata["type"])
        elif isinstance(element, ImageSegmentationInstance):
            unique = np.unique(element.annotations.indices)
            for index in unique:
                # skip background
                if index == 0:
                    continue
                self.add_label(element.annotations.labels[index - 1])

    def finish(self):
        self.init_labels()
        self.output_label_distribution()
