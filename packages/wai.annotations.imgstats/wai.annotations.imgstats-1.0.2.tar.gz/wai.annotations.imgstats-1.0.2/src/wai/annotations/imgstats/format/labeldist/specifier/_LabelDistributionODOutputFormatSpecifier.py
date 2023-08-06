from typing import Type

from wai.annotations.core.domain import DomainSpecifier

from ._LabelDistributionOutputFormatSpecifier import LabelDistributionOutputFormatSpecifier


class LabelDistributionODOutputFormatSpecifier(LabelDistributionOutputFormatSpecifier):
    """
    Specifier for label-dist in the object-detection domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
