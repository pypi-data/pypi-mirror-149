from typing import Type

from wai.annotations.core.domain import DomainSpecifier

from ._LabelDistributionOutputFormatSpecifier import LabelDistributionOutputFormatSpecifier


class LabelDistributionISOutputFormatSpecifier(LabelDistributionOutputFormatSpecifier):
    """
    Specifier for label-dist in the image-segmentation domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier
