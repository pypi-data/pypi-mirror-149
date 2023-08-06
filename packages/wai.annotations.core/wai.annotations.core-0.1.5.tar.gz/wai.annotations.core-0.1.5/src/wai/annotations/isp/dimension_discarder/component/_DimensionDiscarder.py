from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli.options import TypedOption, FlagOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionInstance


class DimensionDiscarder(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
    """
    Stream processor which removes annotations which fall outside
    certain dimensional limits.
    """
    MIN_WIDTH = TypedOption(
        "--min-width",
        type=int,
        help="the minimum width of annotations to convert"
    )

    MAX_WIDTH = TypedOption(
        "--max-width",
        type=int,
        help="the maximum width of annotations to convert"
    )

    MIN_HEIGHT = TypedOption(
        "--min-height",
        type=int,
        help="the minimum height of annotations to convert"
    )

    MAX_HEIGHT = TypedOption(
        "--max-height",
        type=int,
        help="the maximum height of annotations to convert"
    )

    MIN_AREA = TypedOption(
        "--min-area",
        type=int,
        help="the minimum area of annotations to convert"
    )

    MAX_AREA = TypedOption(
        "--max-area",
        type=int,
        help="the maximum area of annotations to convert"
    )

    VERBOSE = FlagOption(
        "--verbose",
        help="outputs information when discarding annotations"
    )

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        # Unpack the format
        image_info, located_objects = element

        # Create a new set of located objects with only non-zero-area annotations
        located_objects = LocatedObjects((located_object
                                          for located_object in located_objects
                                          if not self._should_discard_located_object(located_object)))

        then(ImageObjectDetectionInstance(image_info, located_objects))

    def _should_discard_located_object(self, located_object: LocatedObject) -> bool:
        """
        Decides if the located object should be discarded.

        :param located_object:  The located object.
        :return:                True if it should be discarded,
                                False if it should be kept.
        """
        log = self.VERBOSE is not None and self.VERBOSE

        # Min width check
        if self.MIN_WIDTH is not None and located_object.width < self.MIN_WIDTH:
            if log:
                self.logger.info("Width too small: %d < %d" % (located_object.width, self.MIN_WIDTH))
            return True

        # Max width check
        if self.MAX_WIDTH is not None and located_object.width > self.MAX_WIDTH:
            if log:
                self.logger.info("Width too large: %d > %d" % (located_object.width, self.MAX_WIDTH))
            return True

        # Min height check
        if self.MIN_HEIGHT is not None and located_object.height < self.MIN_HEIGHT:
            if log:
                self.logger.info("Height too small: %d < %d" % (located_object.height, self.MIN_HEIGHT))
            return True

        # Max height check
        if self.MAX_HEIGHT is not None and located_object.height > self.MAX_HEIGHT:
            if log:
                self.logger.info("Height too large: %d > %d" % (located_object.height, self.MAX_HEIGHT))
            return True

        # Return before calculating the area if there are no area bounds
        if self.MIN_AREA is None and self.MAX_AREA is None:
            return False

        # Calculate the area of the object
        area = (
            located_object.get_actual_polygon().area()
            if located_object.has_polygon()
            else located_object.get_actual_rectangle().area()
        )

        # Min area check
        if self.MIN_AREA is not None and area < self.MIN_AREA:
            if log:
                self.logger.info("Area too small: %d < %d" % (area, self.MIN_AREA))
            return True

        # Max area check
        if self.MAX_AREA is not None and area > self.MAX_AREA:
            if log:
                self.logger.info("Area too large: %d > %d" % (area, self.MAX_AREA))
            return True

        return False
