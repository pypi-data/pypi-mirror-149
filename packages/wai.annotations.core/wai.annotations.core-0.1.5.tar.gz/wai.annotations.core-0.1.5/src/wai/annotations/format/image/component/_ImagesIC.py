from wai.annotations.core.component import SinkComponent
from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.classification import Classification
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.classification import ImageClassificationInstance
from wai.common.cli.options import TypedOption


class ImagesReaderIC(AnnotationFileProcessor[ImageClassificationInstance]):
    """
    Dummy reader that turns a list of images into an image classification dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[ImageClassificationInstance]):
        then(
            ImageClassificationInstance(
                Image.from_file(filename),
                Classification("?")
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[ImageClassificationInstance]):
        then(
            ImageClassificationInstance(
                Image.from_file(filename),
                None
            )
        )


class ImagesWriterIC(
    SinkComponent[ImageClassificationInstance]
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

    def consume_element(self, element: ImageClassificationInstance):
        element.data.write_data_if_present(self.output_dir)

    def finish(self):
        pass

