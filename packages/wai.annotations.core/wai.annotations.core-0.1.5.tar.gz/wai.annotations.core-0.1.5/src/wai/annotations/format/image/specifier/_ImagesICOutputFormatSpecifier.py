from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class ImagesICOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing images from from an image classification dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy writer that just outputs images from image classification datasets."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.format.image.component import ImagesWriterIC
        return ImagesWriterIC,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier
