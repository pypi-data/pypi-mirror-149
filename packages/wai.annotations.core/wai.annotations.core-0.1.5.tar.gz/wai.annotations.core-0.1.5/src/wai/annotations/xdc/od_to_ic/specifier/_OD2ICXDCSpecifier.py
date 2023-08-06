from typing import Tuple, Type

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class OD2ICXDCSpecifier(ProcessorStageSpecifier):
    """
    Specifies the image object-detection -> image classification
    cross-domain converter.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts image object-detection instances into image classification instances"

    @classmethod
    def domain_transfer_function(cls, input_domain: Type[DomainSpecifier]) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        from ....domain.image.classification import ImageClassificationDomainSpecifier
        if input_domain is ImageObjectDetectionDomainSpecifier:
            return ImageClassificationDomainSpecifier
        else:
            raise Exception("OD -> IC XDC can only handle the image object-detection domain")

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import OD2ICXDC
        return OD2ICXDC,
