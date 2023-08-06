from abc import ABC
from typing import Type, Tuple

from ....core.component import Component
from ....core.specifier import SinkStageSpecifier


class VoidOutputFormatSpecifier(SinkStageSpecifier, ABC):
    """
    Base specifier for the void-writer in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Consumes instances without writing them."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import VoidWriter
        return VoidWriter,
