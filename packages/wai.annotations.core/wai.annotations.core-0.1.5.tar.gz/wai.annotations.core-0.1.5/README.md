# wai-annotations-core
wai.annotations core module.

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins

### CHECK-DUPLICATE-FILENAMES
Causes the conversion stream to halt when multiple dataset items have the same filename

#### Domain(s)
- Speech Domain
- Image Segmentation Domain
- Image Object-Detection Domain
- Image Classification Domain

#### Options
```
    CHECK-DUPLICATE-FILENAMES:
      Causes the conversion stream to halt when multiple dataset items have the same filename

      Domain(s): Speech Domain, Image Segmentation Domain, Image Object-Detection Domain, Image Classification Domain

      usage: check-duplicate-filenames
```

### COERCE-BOX
Converts all annotation bounds into box regions

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    COERCE-BOX:
      Converts all annotation bounds into box regions

      Domain(s): Image Object-Detection Domain

      usage: coerce-box
```

### COERCE-MASK
Converts all annotation bounds into polygon regions

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    COERCE-MASK:
      Converts all annotation bounds into polygon regions

      Domain(s): Image Object-Detection Domain

      usage: coerce-mask
```

### CONVERT-IMAGE-FORMAT
Converts images from one format to another

#### Domain(s)
- Image Segmentation Domain
- Image Object-Detection Domain
- Image Classification Domain

#### Options
```
    CONVERT-IMAGE-FORMAT:
      Converts images from one format to another

      Domain(s): Image Segmentation Domain, Image Object-Detection Domain, Image Classification Domain

      usage: convert-image-format -f FORMAT

      optional arguments:
        -f FORMAT, --format FORMAT
                        format to convert images to
```

### DIMENSION-DISCARDER
Removes annotations which fall outside certain size constraints

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    DIMENSION-DISCARDER:
      Removes annotations which fall outside certain size constraints

      Domain(s): Image Object-Detection Domain

      usage: dimension-discarder [--max-area MAX_AREA] [--max-height MAX_HEIGHT] [--max-width MAX_WIDTH] [--min-area MIN_AREA] [--min-height MIN_HEIGHT] [--min-width MIN_WIDTH] [--verbose]

      optional arguments:
        --max-area MAX_AREA
                        the maximum area of annotations to convert
        --max-height MAX_HEIGHT
                        the maximum height of annotations to convert
        --max-width MAX_WIDTH
                        the maximum width of annotations to convert
        --min-area MIN_AREA
                        the minimum area of annotations to convert
        --min-height MIN_HEIGHT
                        the minimum height of annotations to convert
        --min-width MIN_WIDTH
                        the minimum width of annotations to convert
        --verbose       outputs information when discarding annotations
```

### DISCARD-NEGATIVES
Discards negative examples (those without annotations) from the stream

#### Domain(s)
- Speech Domain
- Image Segmentation Domain
- Image Object-Detection Domain
- Image Classification Domain

#### Options
```
    DISCARD-NEGATIVES:
      Discards negative examples (those without annotations) from the stream

      Domain(s): Speech Domain, Image Segmentation Domain, Image Object-Detection Domain, Image Classification Domain

      usage: discard-negatives
```

### FILTER-LABELS
Filters detected objects down to those with specified labels.

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    FILTER-LABELS:
      Filters detected objects down to those with specified labels.

      Domain(s): Image Object-Detection Domain

      usage: filter-labels [-l LABELS [LABELS ...]] [-r regexp]

      optional arguments:
        -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        labels to use
        -r regexp, --regexp regexp
                        regular expression for using only a subset of labels
```


### FROM-IMAGES-IC
Dummy reader that turns images into an image classification dataset.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: from-images-ic [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME] [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into
  --seed SEED           the seed to use for randomisation
```


### FROM-IMAGES-IS
Dummy reader that turns images into an image segmentation dataset.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: from-images-is [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME] [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into
  --seed SEED           the seed to use for randomisation
```


### FROM-IMAGES-OD
Dummy reader that turns images into an object detection dataset.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-images-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME] [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into
  --seed SEED           the seed to use for randomisation
```


### MAP-LABELS
Maps object-detection labels from one set to another

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    MAP-LABELS:
      Maps object-detection labels from one set to another

      Domain(s): Image Object-Detection Domain

      usage: map-labels [-m old=new]

      optional arguments:
        -m old=new, --mapping old=new
                        mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)
```

### OD-TO-IC
Converts image object-detection instances into image classification instances

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    OD-TO-IC:
      Converts image object-detection instances into image classification instances

      Domain(s): Image Object-Detection Domain

      usage: od-to-ic [-m HANDLER]

      optional arguments:
        -m HANDLER, --multiplicity HANDLER
                        how to handle instances with more than one located object
```

### OD-TO-IS
Converts image object-detection instances into image segmentation instances

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    OD-TO-IS:
      Converts image object-detection instances into image segmentation instances

      Domain(s): Image Object-Detection Domain

      usage: od-to-is [--label-error] --labels LABEL [LABEL ...]

      optional arguments:
        --label-error   whether to raise errors when an unspecified label is encountered (default is to ignore)
        --labels LABEL [LABEL ...]
                        specifies the labels for each index
```

### PASSTHROUGH
Dummy ISP which has no effect on the conversion stream

#### Domain(s)
- Speech Domain
- Image Segmentation Domain
- Image Object-Detection Domain
- Image Classification Domain

#### Options
```
    PASSTHROUGH:
      Dummy ISP which has no effect on the conversion stream

      Domain(s): Speech Domain, Image Segmentation Domain, Image Object-Detection Domain, Image Classification Domain

      usage: passthrough
```

### POLYGON-DISCARDER
Removes annotations with polygons which fall outside certain point limit constraints

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    POLYGON-DISCARDER:
      Removes annotations with polygons which fall outside certain point limit constraints

      Domain(s): Image Object-Detection Domain

      usage: polygon-discarder [--max-points MAX_POINTS] [--min-points MIN_POINTS] [--verbose]

      optional arguments:
        --max-points MAX_POINTS
                        the maximum number of points in the polygon
        --min-points MIN_POINTS
                        the minimum number of points in the polygon
        --verbose       outputs information when discarding annotations
```

### REMOVE-CLASSES
Removes classes from classification/image-segmentation instances

#### Domain(s)
- Image Segmentation Domain
- Image Classification Domain

#### Options
```
    REMOVE-CLASSES:
      Removes classes from classification/image-segmentation instances

      Domain(s): Image Segmentation Domain, Image Classification Domain

      usage: remove-classes -c CLASS [CLASS ...]

      optional arguments:
        -c CLASS [CLASS ...], --classes CLASS [CLASS ...]
                        the classes to remove
```

### STRIP-ANNOTATIONS
ISP which removes annotations from instances

#### Domain(s)
- Speech Domain
- Image Segmentation Domain
- Image Object-Detection Domain
- Image Classification Domain

#### Options
```
    STRIP-ANNOTATIONS:
      ISP which removes annotations from instances

      Domain(s): Speech Domain, Image Segmentation Domain, Image Object-Detection Domain, Image Classification Domain

      usage: strip-annotations
```

### TO-IMAGES-IC
Dummy writer that just outputs images from image classification datasets.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: to-images-ic [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the images to
```

### TO-IMAGES-IS
Dummy writer that just outputs images from image segmentation datasets.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: to-images-is [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the images to
```


### TO-IMAGES-OD
Dummy writer that just outputs images from object detection datasets.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-images-od [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the images to
```


### TO-VOID-IC
Consumes instances without writing them.

#### Domain(s)
- Image Classification Domain

#### Options
```
    TO-VOID-IC:
      Consumes instances without writing them.

      Domain(s): Image Classification Domain

      usage: to-void-ic
```

### TO-VOID-IS
Consumes instances without writing them.

#### Domain(s)
- Image Segmentation Domain

#### Options
```
    TO-VOID-IS:
      Consumes instances without writing them.

      Domain(s): Image Segmentation Domain

      usage: to-void-is
```

### TO-VOID-OD
Consumes instances without writing them.

#### Domain(s)
- Image Object-Detection Domain

#### Options
```
    TO-VOID-OD:
      Consumes instances without writing them.

      Domain(s): Image Object-Detection Domain

      usage: to-void-od
```

### TO-VOID-SP
Consumes instances without writing them.

#### Domain(s)
- Speech Domain

#### Options
```
    TO-VOID-SP:
      Consumes instances without writing them.

      Domain(s): Speech Domain

      usage: to-void-sp
```
