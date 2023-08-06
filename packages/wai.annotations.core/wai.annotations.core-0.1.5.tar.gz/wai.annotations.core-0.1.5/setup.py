from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.core",
    description="Python library for converting between deep-learning annotation formats.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-datamining/wai-annotations-core",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations"
    ],
    version="0.1.5",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "wai.common>=0.0.35",
        "wai.json>=0.0.4,<0.1",
        "wai.bynning>=0.0.2,<0.1",
        "Pillow",
        "contextlib2",
        "numpy>=1.16",
        "planar",
        "scikit-image",
        "wai.pycocotools",
        "opencv-python",
    ],
    entry_points={
        "console_scripts": ["wai-annotations=wai.annotations.main:sys_main"],
        "wai.annotations.plugins": [
            # Formats
            "from-images-ic=wai.annotations.format.image.specifier:ImagesICInputFormatSpecifier",
            "from-images-is=wai.annotations.format.image.specifier:ImagesISInputFormatSpecifier",
            "from-images-od=wai.annotations.format.image.specifier:ImagesODInputFormatSpecifier",
            "to-images-ic=wai.annotations.format.image.specifier:ImagesICOutputFormatSpecifier",
            "to-images-is=wai.annotations.format.image.specifier:ImagesISOutputFormatSpecifier",
            "to-images-od=wai.annotations.format.image.specifier:ImagesODOutputFormatSpecifier",
            "to-void-ic=wai.annotations.format.void.specifier:VoidICOutputFormatSpecifier",
            "to-void-is=wai.annotations.format.void.specifier:VoidISOutputFormatSpecifier",
            "to-void-od=wai.annotations.format.void.specifier:VoidODOutputFormatSpecifier",
            "to-void-sp=wai.annotations.format.void.specifier:VoidSPOutputFormatSpecifier",

            # ISPs
            "coerce-box=wai.annotations.isp.coercions.specifier:BoxBoundsCoercionISPSpecifier",
            "coerce-mask=wai.annotations.isp.coercions.specifier:MaskBoundsCoercionISPSpecifier",
            "convert-image-format=wai.annotations.isp.convert_image_format.specifier:ConvertImageFormatISPSpecifier",
            "dimension-discarder=wai.annotations.isp.dimension_discarder.specifier:DimensionDiscarderISPSpecifier",
            "discard-negatives=wai.annotations.isp.discard_negatives.specifier:DiscardNegativesISPSpecifier",
            "check-duplicate-filenames=wai.annotations.isp.duplicate_filenames.specifier:DuplicateFileNamesISPSpecifier",
            "filter-labels=wai.annotations.isp.filter_labels.specifier:FilterLabelsISPSpecifier",
            "map-labels=wai.annotations.isp.map_labels.specifier:MapLabelsISPSpecifier",
            "passthrough=wai.annotations.isp.passthrough.specifier:PassThroughISPSpecifier",
            "polygon-discarder=wai.annotations.isp.polygon_discarder.specifier:PolygonDiscarderISPSpecifier",
            "remove-classes=wai.annotations.isp.remove_classes.specifier:RemoveClassesISPSpecifier",
            "strip-annotations=wai.annotations.isp.strip_annotations.specifier:StripAnnotationsISPSpecifier",

            # XDCs
            "od-to-is=wai.annotations.xdc.od_to_is.specifier:OD2ISXDCSpecifier",
            "od-to-ic=wai.annotations.xdc.od_to_ic.specifier:OD2ICXDCSpecifier",
        ]
    }
)
