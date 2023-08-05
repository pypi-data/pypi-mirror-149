# wai-annotations-imgstats
wai.annotations plugin for generating statistics for image datasets.

## Plugins
### LABEL-DIST-IC
Generates a label distribution.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: label-dist-ic [-o OUTPUT_FILE] [-f OUTPUT_FORMAT] [-p]

optional arguments:
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the statistics to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
  -p, --percentages     whether to output percentages instead of counts.
```

### LABEL-DIST-IS
Generates a label distribution.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: label-dist-is [-o OUTPUT_FILE] [-f OUTPUT_FORMAT] [-p]

optional arguments:
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the statistics to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
  -p, --percentages     whether to output percentages instead of counts.
```

### LABEL-DIST-OD
Generates a label distribution.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: label-dist-od [-o OUTPUT_FILE] [-f OUTPUT_FORMAT] [-p]

optional arguments:
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the statistics to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
  -p, --percentages     whether to output percentages instead of counts.
```

### TO-ANNOTATION-OVERLAY-OD
Generates an image with all the annotation shapes (bbox or polygon) overlayed.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-annotation-overlay-od [-b BACKGROUND_COLOR] [-c COLOR] [-o OUTPUT_FILE] [-s SCALE_TO]

optional arguments:
  -b BACKGROUND_COLOR, --background-color BACKGROUND_COLOR
                        the color to use for the background as RGBA byte-quadruplet, e.g.: 255,255,255,255
  -c COLOR, --color COLOR
                        the color to use for drawing the shapes as RGBA byte-quadruplet, e.g.: 255,0,0,64
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the PNG image to write the generated overlay to
  -s SCALE_TO, --scale-to SCALE_TO
                        the dimensions to scale all images to before overlaying them (format: width,height)
```
