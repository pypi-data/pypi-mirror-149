from ....core.component import SinkComponent
from ....core.domain import Instance


class VoidWriter(
    SinkComponent[Instance]
):
    """
    Consumes instances by discarding them.
    """
    def consume_element(self, element: Instance):
        pass

    def finish(self):
        pass
