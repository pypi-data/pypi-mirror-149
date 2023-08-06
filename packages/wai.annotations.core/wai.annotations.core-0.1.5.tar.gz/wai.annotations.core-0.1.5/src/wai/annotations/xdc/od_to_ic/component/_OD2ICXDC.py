from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.classification import Classification
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label
from ....domain.image.classification import ImageClassificationInstance


class OD2ICXDC(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageClassificationInstance]
):
    """
    Cross-domain converter from the image object-detection domain to the
    image classification domain.
    """
    multiplicity_method: str = TypedOption(
        "-m", "--multiplicity",
        type=str,
        choices=["error", "majority", "single", "skip"],
        default="error",
        help="how to handle instances with more than one located object",
        metavar="HANDLER"
    )

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageClassificationInstance],
            done: DoneFunction
    ):
        # Get the located objects from the instance
        objects = element.annotations

        # If the instance is a negative, leave it as one
        if objects is None or len(objects) == 0:
            return then(ImageClassificationInstance(element.data, None))

        if len(objects) > 1:
            if self.multiplicity_method == "error":
                raise Exception(f"More than one detected object for {element.data.filename}")
            elif self.multiplicity_method == "skip":
                return
            elif self.multiplicity_method == "single":
                labels = set(map(get_object_label, objects))
                if len(labels) > 1:
                    raise Exception(f"More than one type of detected object for {element.data.filename}")
                label = labels.pop()
            else:  # self.multiplicity_method == "majority"
                labels = {}
                for label in map(get_object_label, objects):
                    if label in labels:
                        labels[label] += 1
                    else:
                        labels[label] = 1
                label = max(labels.keys(), key=labels.get)
        else:
            label = get_object_label(objects[0])

        then(ImageClassificationInstance(element.data, Classification(label)))
