Changelog
=========

0.1.5 (2022-05-09)
------------------

- Added dataset readers that generate dummy datasets from images: `from-images-ic`, `from-images-is`, `from-images-od`
- Added dataset writers that just output the images from datasets: `to-images-ic`, `to-images-is`, `to-images-od`

0.1.4 (2021-11-11)
------------------

- Added ISP for discarding polygons that either have too few or too many points (`polygon-discarder`)
- Added `--verbose` flag to `dimension-discarder` ISP for outputting information when an annotation
  gets discarded.

0.1.3 (2021-06-22)
-------------------

- Added cross-domain converter which reduces object-detection datasets to image classification
  by looking for single/majority objects/labels.

0.1.2 (2021-06-01)
-------------------

- Added void output formats for each domain which discard the conversion results.
- Added option to LocalFilenameSource which tells it to write the files it reads to a list-file.

0.1.1 (2021-05-20)
-------------------

- Fixed build.

0.1.0 (2021-05-20)
-------------------

- Initial release after separation from wai.annotations main repo.
