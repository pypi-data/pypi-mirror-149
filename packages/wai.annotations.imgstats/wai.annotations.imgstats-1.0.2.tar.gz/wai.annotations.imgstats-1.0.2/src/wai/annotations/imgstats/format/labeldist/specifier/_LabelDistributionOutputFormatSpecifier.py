from abc import ABC
from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.specifier import SinkStageSpecifier


class LabelDistributionOutputFormatSpecifier(SinkStageSpecifier, ABC):
    """
    Base specifier for the label-dist in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Generates a label distribution."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.imgstats.format.labeldist.component import LabelDistribution
        return LabelDistribution,
