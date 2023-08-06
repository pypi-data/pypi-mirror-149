from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class ImagesODOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing images from from an object detection dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy writer that just outputs images from object detection datasets."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.format.image.component import ImagesWriterOD
        return ImagesWriterOD,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
