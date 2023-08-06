# wai-annotations-imgaug
Image augmentation stream processors for the [wai.annotations](https://github.com/waikato-ufdl/wai-annotations) 
conversion library.

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins
### ADD-ANNOTATION-OVERLAY-OD
Adds object detection overlays to images passing through.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: add-annotation-overlay-od [--fill] [--fill-alpha FILL_ALPHA] [--font-family FONT_FAMILY] [--font-size FONT_SIZE] [--force-bbox] [--label-key LABEL_KEY] [--labels LABELS] [--num-decimals NUM_DECIMALS] [--outline-alpha OUTLINE_ALPHA] [--outline-thickness OUTLINE_THICKNESS] [--text-format TEXT_FORMAT] [--text-placement TEXT_PLACEMENT] [--vary-colors]

optional arguments:
  --fill                whether to fill the bounding boxes/polygons
  --fill-alpha FILL_ALPHA
                        the alpha value to use for the filling.
  --font-family FONT_FAMILY
                        the name of the TTF font-family to use, note: any hyphens need escaping with backslash.
  --font-size FONT_SIZE
                        the size of the font.
  --force-bbox          whether to force a bounding box even if there is a polygon available
  --label-key LABEL_KEY
                        the key in the meta-data that contains the label.
  --labels LABELS       the blank-separated list of labels of annotations to overlay, leave empty to overlay all
  --num-decimals NUM_DECIMALS
                        the number of decimals to use for float numbers in the text format string.
  --outline-alpha OUTLINE_ALPHA
                        the alpha value to use for the outline.
  --outline-thickness OUTLINE_THICKNESS
                        the line thickness to use for the outline, <1 to turn off.
  --text-format TEXT_FORMAT
                        template for the text to print on top of the bounding box or polygon, '{PH}' is a placeholder for the 'PH' value from the meta-data or 'label' for the current label; ignored if empty.
  --text-placement TEXT_PLACEMENT
                        comma-separated list of vertical (T=top, C=center, B=bottom) and horizontal (L=left, C=center, R=right) anchoring.
  --vary-colors         whether to vary the colors of the outline/filling regardless of label
```


### CROP
Crops images.

#### Domain(s):
- **Image Classification Domain, Image Object-Detection Domain**

#### Options:
```
    CROP:
      Crops images.

      Domain(s): Image Object-Detection Domain, Image Classification Domain

      usage: crop [-m IMGAUG_MODE] [--suffix IMGAUG_SUFFIX] [-f PERCENT_FROM] [-t PERCENT_TO] [-s SEED] [-a] [-T THRESHOLD] [-u]

      optional arguments:
        -m IMGAUG_MODE, --mode IMGAUG_MODE
                        the image augmentation mode to use, available modes: replace, add
        --suffix IMGAUG_SUFFIX
                        the suffix to use for the file names in case of augmentation mode add
        -f PERCENT_FROM, --from-percent PERCENT_FROM
                        the minimum percent to crop from images
        -t PERCENT_TO, --to-percent PERCENT_TO
                        the maximum percent to crop from images
        -s SEED, --seed SEED
                        the seed value to use for the random number generator; randomly seeded if not provided
        -a, --seed-augmentation
                        whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from 0 to 1000 for the augmentation.
        -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
        -u, --update-size
                        whether to update the image size after the crop operation or scale back to original size
```

### FLIP
Flips images either left-to-right, up-to-down or both.

#### Domain(s):
- **Image Classification Domain, Image Object-Detection Domain**

#### Options:
```
    FLIP:
      Flips images either left-to-right, up-to-down or both.

      Domain(s): Image Object-Detection Domain, Image Classification Domain

      usage: flip [-d DIRECTION] [-m IMGAUG_MODE] [--suffix IMGAUG_SUFFIX] [-s SEED] [-a] [-T THRESHOLD]

      optional arguments:
        -d DIRECTION, --direction DIRECTION
                        the direction to flip, available options: lr, up, lrup
        -m IMGAUG_MODE, --mode IMGAUG_MODE
                        the image augmentation mode to use, available modes: replace, add
        --suffix IMGAUG_SUFFIX
                        the suffix to use for the file names in case of augmentation mode add
        -s SEED, --seed SEED
                        the seed value to use for the random number generator; randomly seeded if not provided
        -a, --seed-augmentation
                        whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from 0 to 1000 for the augmentation.
        -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
```

### GAUSSIAN-BLUR
Applies gaussian blur to images.

#### Domain(s):
- **Image Classification Domain, Image Object-Detection Domain**

#### Options:
```
    GAUSSIAN-BLUR:
      Applies gaussian blur to images.

      Domain(s): Image Object-Detection Domain, Image Classification Domain

      usage: gaussian-blur [-m IMGAUG_MODE] [--suffix IMGAUG_SUFFIX] [-s SEED] [-a] [-f SIGMA_FROM] [-t SIGMA_TO] [-T THRESHOLD]

      optional arguments:
        -m IMGAUG_MODE, --mode IMGAUG_MODE
                        the image augmentation mode to use, available modes: replace, add
        --suffix IMGAUG_SUFFIX
                        the suffix to use for the file names in case of augmentation mode add
        -s SEED, --seed SEED
                        the seed value to use for the random number generator; randomly seeded if not provided
        -a, --seed-augmentation
                        whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from 0 to 1000 for the augmentation.
        -f SIGMA_FROM, --from-sigma SIGMA_FROM
                        the minimum sigma for the blur to apply to the images
        -t SIGMA_TO, --to-sigma SIGMA_TO
                        the maximum sigma for the blur to apply to the images
        -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
```


### HSL-GRAYSCALE
Turns RGB images into fake grayscale ones by converting them to HSL and then using the L channel for all channels. The brightness can be influenced and varied even.

#### Domain(s):
- **Image Classification Domain, Image Object-Detection Domain**

#### Options:
```
    HSL-GRAYSCALE:
      Turns RGB images into fake grayscale ones by converting them to HSL and then using the L channel for all channels. The brightness can be influenced and varied even.

      Domain(s): Image Object-Detection Domain, Image Classification Domain

      usage: hsl-grayscale [-f FACTOR_FROM] [-t FACTOR_TO] [-m IMGAUG_MODE] [--suffix IMGAUG_SUFFIX] [-s SEED] [-a] [-T THRESHOLD]

      optional arguments:
        -f FACTOR_FROM, --from-factor FACTOR_FROM
                        the start of the factor range to apply to the L channel to darken or lighten the image (<1: darker, >1: lighter)
        -t FACTOR_TO, --to-factor FACTOR_TO
                        the end of the factor range to apply to the L channel to darken or lighten the image (<1: darker, >1: lighter)
        -m IMGAUG_MODE, --mode IMGAUG_MODE
                        the image augmentation mode to use, available modes: replace, add
        --suffix IMGAUG_SUFFIX
                        the suffix to use for the file names in case of augmentation mode add
        -s SEED, --seed SEED
                        the seed value to use for the random number generator; randomly seeded if not provided
        -a, --seed-augmentation
                        whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from 0 to 1000 for the augmentation.
        -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
```


### LINEAR-CONTRAST
Applies linear contrast to images.

#### Domain(s):
- **Image Classification Domain, Image Object-Detection Domain**

#### Options:
```
    LINEAR-CONTRAST:
      Applies linear contrast to images.

      Domain(s): Image Object-Detection Domain, Image Classification Domain

      usage: linear-contrast [-f ALPHA_FROM] [-t ALPHA_TO] [-m IMGAUG_MODE] [--suffix IMGAUG_SUFFIX] [-s SEED] [-a] [-T THRESHOLD]

      optional arguments:
        -f ALPHA_FROM, --from-alpha ALPHA_FROM
                        the minimum alpha to apply to the images
        -t ALPHA_TO, --to-alpha ALPHA_TO
                        the maximum alpha to apply to the images
        -m IMGAUG_MODE, --mode IMGAUG_MODE
                        the image augmentation mode to use, available modes: replace, add
        --suffix IMGAUG_SUFFIX
                        the suffix to use for the file names in case of augmentation mode add
        -s SEED, --seed SEED
                        the seed value to use for the random number generator; randomly seeded if not provided
        -a, --seed-augmentation
                        whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from 0 to 1000 for the augmentation.
        -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
```

### ROTATE
Rotates images randomly within a range of degrees or by a specified degree. Specify seed value and force augmentation to be seeded to generate repeatable augmentations.

#### Domain(s):
- **Image Classification Domain, Image Object-Detection Domain**

#### Options:
```
    ROTATE:
      Rotates images randomly within a range of degrees or by a specified degree. Specify seed value and force augmentation to be seeded to generate repeatable augmentations.

      Domain(s): Image Object-Detection Domain, Image Classification Domain

      usage: rotate [-f DEGREE_FROM] [-t DEGREE_TO] [-m IMGAUG_MODE] [--suffix IMGAUG_SUFFIX] [-s SEED] [-a] [-T THRESHOLD]

      optional arguments:
        -f DEGREE_FROM, --from-degree DEGREE_FROM
                        the start of the degree range to use for rotating the images
        -t DEGREE_TO, --to-degree DEGREE_TO
                        the end of the degree range to use for rotating the images
        -m IMGAUG_MODE, --mode IMGAUG_MODE
                        the image augmentation mode to use, available modes: replace, add
        --suffix IMGAUG_SUFFIX
                        the suffix to use for the file names in case of augmentation mode add
        -s SEED, --seed SEED
                        the seed value to use for the random number generator; randomly seeded if not provided
        -a, --seed-augmentation
                        whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from 0 to 1000 for the augmentation.
        -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
```

### SCALE
Scales images randomly within a range of percentages or by a specified percentage. Specify seed value and force augmentation to be seeded to generate repeatable augmentations.

#### Domain(s):
- **Image Classification Domain, Image Object-Detection Domain**

#### Options:
```
    SCALE:
      Scales images randomly within a range of percentages or by a specified percentage. Specify seed value and force augmentation to be seeded to generate repeatable augmentations.

      Domain(s): Image Object-Detection Domain, Image Classification Domain

      usage: scale [-m IMGAUG_MODE] [--suffix IMGAUG_SUFFIX] [-k] [-f PERCENTAGE_FROM] [-t PERCENTAGE_TO] [-s SEED] [-a] [-T THRESHOLD] [-u]

      optional arguments:
        -m IMGAUG_MODE, --mode IMGAUG_MODE
                        the image augmentation mode to use, available modes: replace, add
        --suffix IMGAUG_SUFFIX
                        the suffix to use for the file names in case of augmentation mode add
        -k, --keep-aspect
                        whether to keep the aspect ratio
        -f PERCENTAGE_FROM, --from-percentage PERCENTAGE_FROM
                        the start of the percentage range to use for scaling the images
        -t PERCENTAGE_TO, --to-percentage PERCENTAGE_TO
                        the end of the percentage range to use for scaling the images
        -s SEED, --seed SEED
                        the seed value to use for the random number generator; randomly seeded if not provided
        -a, --seed-augmentation
                        whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from 0 to 1000 for the augmentation.
        -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
        -u, --update-size
                        whether to update the image size after the scaling operation or use original size
```
