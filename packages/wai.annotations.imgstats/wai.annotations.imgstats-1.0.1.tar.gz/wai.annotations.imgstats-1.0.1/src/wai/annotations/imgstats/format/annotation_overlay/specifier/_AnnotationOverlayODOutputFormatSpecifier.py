from abc import ABC
from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class AnnotationOverlayODOutputFormatSpecifier(SinkStageSpecifier, ABC):
    """
    Base specifier for the label-dist in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Generates an image with all the annotation shapes (bbox or polygon) overlayed."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.imgstats.format.annotation_overlay.component import AnnotationOverlay
        return AnnotationOverlay,

    """
    Specifier for annotation-overlay-od in the object-detection domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
