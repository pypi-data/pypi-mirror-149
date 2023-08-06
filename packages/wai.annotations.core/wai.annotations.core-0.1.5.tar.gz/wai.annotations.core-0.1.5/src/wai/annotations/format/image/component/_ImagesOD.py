from wai.annotations.core.component import SinkComponent
from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.image import Image
from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.common.cli.options import TypedOption


class ImagesReaderOD(AnnotationFileProcessor[ImageObjectDetectionInstance]):
    """
    Dummy reader that turns a list of images into an object detection dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[ImageObjectDetectionInstance]):
        then(
            ImageObjectDetectionInstance(
                Image.from_file(filename),
                LocatedObjects()
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[ImageObjectDetectionInstance]):
        then(
            ImageObjectDetectionInstance(
                Image.from_file(filename),
                None
            )
        )


class ImagesWriterOD(
    SinkComponent[ImageObjectDetectionInstance]
):
    """
    Writes the images to the specified output directory.
    """

    output_dir: str = TypedOption(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="the directory to write the images to"
    )

    def consume_element(self, element: ImageObjectDetectionInstance):
        element.data.write_data_if_present(self.output_dir)

    def finish(self):
        pass

