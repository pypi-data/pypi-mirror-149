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
