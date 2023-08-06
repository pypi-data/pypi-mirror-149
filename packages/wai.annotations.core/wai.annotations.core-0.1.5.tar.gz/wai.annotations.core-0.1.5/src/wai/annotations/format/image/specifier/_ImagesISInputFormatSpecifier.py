from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class ImagesISInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for turning images into an image segmentation dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy reader that turns images into an image segmentation dataset."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util import LocalFilenameSource
        from wai.annotations.format.image.component import ImagesReaderIS
        return LocalFilenameSource, ImagesReaderIS

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier
