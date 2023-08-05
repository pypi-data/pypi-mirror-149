from typing import Type

from wai.annotations.core.domain import DomainSpecifier

from ._LabelDistributionOutputFormatSpecifier import LabelDistributionOutputFormatSpecifier


class LabelDistributionICOutputFormatSpecifier(LabelDistributionOutputFormatSpecifier):
    """
    Specifier for the label-dist in the image-classification domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier
