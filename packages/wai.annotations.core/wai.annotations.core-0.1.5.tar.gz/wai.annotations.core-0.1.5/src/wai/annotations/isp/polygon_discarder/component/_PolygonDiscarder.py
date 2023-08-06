from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli.options import TypedOption, FlagOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionInstance


class PolygonDiscarder(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
    """
    Stream processor which removes annotations with polygons that fall outside
    certain point limits (skips annotations that have no polygons).
    """
    MIN_POINTS = TypedOption(
        "--min-points",
        type=int,
        help="the minimum number of points in the polygon"
    )

    MAX_POINTS = TypedOption(
        "--max-points",
        type=int,
        help="the maximum number of points in the polygon"
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

        if not located_object.has_polygon():
            if log:
                self.logger.info("No polygon, skipping")
            return False

        poly = located_object.get_actual_polygon()
        num_points = len(poly.points)

        # Min points check
        if self.MIN_POINTS is not None and num_points < self.MIN_POINTS:
            if log:
                self.logger.info("too few points: %d < %d" % (num_points, self.MIN_POINTS))
            return True

        # Max points check
        if self.MAX_POINTS is not None and num_points > self.MAX_POINTS:
            if log:
                self.logger.info("too many points: %d > %d" % (num_points, self.MAX_POINTS))
            return True

        return False
