import io
import PIL

from matplotlib import font_manager
from PIL import ImageColor, ImageDraw, ImageFont

from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance


# https://en.wikipedia.org/wiki/X11_color_names
X11_COLORS = [
    "#F0F8FF",
    "#FAEBD7",
    "#00FFFF",
    "#7FFFD4",
    "#F0FFFF",
    "#F5F5DC",
    "#FFE4C4",
    "#000000",
    "#FFEBCD",
    "#0000FF",
    "#8A2BE2",
    "#A52A2A",
    "#DEB887",
    "#5F9EA0",
    "#7FFF00",
    "#D2691E",
    "#FF7F50",
    "#6495ED",
    "#FFF8DC",
    "#DC143C",
    "#00FFFF",
    "#00008B",
    "#008B8B",
    "#B8860B",
    "#A9A9A9",
    "#006400",
    "#BDB76B",
    "#8B008B",
    "#556B2F",
    "#FF8C00",
    "#9932CC",
    "#8B0000",
    "#E9967A",
    "#8FBC8F",
    "#483D8B",
    "#2F4F4F",
    "#00CED1",
    "#9400D3",
    "#FF1493",
    "#00BFFF",
    "#696969",
    "#1E90FF",
    "#B22222",
    "#FFFAF0",
    "#228B22",
    "#FF00FF",
    "#DCDCDC",
    "#F8F8FF",
    "#FFD700",
    "#DAA520",
    "#BEBEBE",
    "#808080",
    "#00FF00",
    "#008000",
    "#ADFF2F",
    "#F0FFF0",
    "#FF69B4",
    "#CD5C5C",
    "#4B0082",
    "#FFFFF0",
    "#F0E68C",
    "#E6E6FA",
    "#FFF0F5",
    "#7CFC00",
    "#FFFACD",
    "#ADD8E6",
    "#F08080",
    "#E0FFFF",
    "#FAFAD2",
    "#D3D3D3",
    "#90EE90",
    "#FFB6C1",
    "#FFA07A",
    "#20B2AA",
    "#87CEFA",
    "#778899",
    "#B0C4DE",
    "#FFFFE0",
    "#00FF00",
    "#32CD32",
    "#FAF0E6",
    "#FF00FF",
    "#B03060",
    "#800000",
    "#66CDAA",
    "#0000CD",
    "#BA55D3",
    "#9370DB",
    "#3CB371",
    "#7B68EE",
    "#00FA9A",
    "#48D1CC",
    "#C71585",
    "#191970",
    "#F5FFFA",
    "#FFE4E1",
    "#FFE4B5",
    "#FFDEAD",
    "#000080",
    "#FDF5E6",
    "#808000",
    "#6B8E23",
    "#FFA500",
    "#FF4500",
    "#DA70D6",
    "#EEE8AA",
    "#98FB98",
    "#AFEEEE",
    "#DB7093",
    "#FFEFD5",
    "#FFDAB9",
    "#CD853F",
    "#FFC0CB",
    "#DDA0DD",
    "#B0E0E6",
    "#A020F0",
    "#800080",
    "#663399",
    "#FF0000",
    "#BC8F8F",
    "#4169E1",
    "#8B4513",
    "#FA8072",
    "#F4A460",
    "#2E8B57",
    "#FFF5EE",
    "#A0522D",
    "#C0C0C0",
    "#87CEEB",
    "#6A5ACD",
    "#708090",
    "#FFFAFA",
    "#00FF7F",
    "#4682B4",
    "#D2B48C",
    "#008080",
    "#D8BFD8",
    "#FF6347",
    "#40E0D0",
    "#EE82EE",
    "#F5DEB3",
    "#FFFFFF",
    "#F5F5F5",
    "#FFFF00",
    "#9ACD32",
]

LIGHT_COLORS = [
    "#F0F8FF",
    "#F0FFFF",
    "#F5F5DC",
    "#FFE4C4",
    "#FFEBCD",
    "#FFF8DC",
    "#FFFAF0",
    "#F8F8FF",
    "#F0FFF0",
    "#FFFFF0",
    "#FFF0F5",
    "#E0FFFF",
    "#FFFFE0",
    "#FAF0E6",
    "#F5FFFA",
    "#FDF5E6",
    "#FFF5EE",
    "#FFFAFA",
    "#FFFFFF",
    "#F5F5F5",
]

DARK_COLORS = [
    "#000000",
    "#00008B",
    "#191970",
    "#483D8B",
    "#2F4F4F",
    "#4B0082",
    "#191970",
    "#000080",
]


DEFAULT_FONT_FAMILY = "sans\\-serif"


def rgb2yiq(r, g, b):
    """
    Generates YIQ perceived brightness from RGB colors.

    :param r: the red value
    :param g: the green value
    :param b: the blue value
    :return: the YIQ value
    """
    return ((r * 299) + (g * 587) + (b * 114)) / 1000


def default_colors(no_light=True, no_dark=True):
    """
    Returns a list of default color tuples.

    :param no_light: skips light colors
    :type no_light: bool
    :param no_dark: skips dark colors
    :type no_dark: bool
    :return: the list of colors
    :rtype: list
    """
    result = []
    skip = set()
    if no_light:
        for c in LIGHT_COLORS:
            skip.add(c)
    if no_dark:
        for c in DARK_COLORS:
            skip.add(c)
    for c in X11_COLORS:
        if c in skip:
            continue
        result.append(ImageColor.getrgb(c))
    return result


def text_color(color, threshold=128):
    """
    Computes the text color to use for the given RGB color.

    :param color: the RGB tuple
    :param threshold: the threshold to use
    :return: the text color tuple
    :rtype: tuple
    """
    r, g, b = color
    if rgb2yiq(r, g, b) >= threshold:
        return 0, 0, 0
    else:
        return 255, 255, 255


class AnnotationOverlay(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
    """
    Stream processor which adds object detections overlays to images.
    """

    labels: float = TypedOption(
        "--labels",
        type=str,
        default="",
        help="the blank-separated list of labels of annotations to overlay, leave empty to overlay all"
    )

    label_key: str = TypedOption(
        "--label-key",
        type=str,
        default="type",
        help="the key in the meta-data that contains the label."
    )

    text_format: str = TypedOption(
        "--text-format",
        type=str,
        default="{label}",
        help="template for the text to print on top of the bounding box or polygon, '{PH}' is a placeholder for the 'PH' value from the meta-data or 'label' for the current label; ignored if empty."
    )

    text_placement: str = TypedOption(
        "--text-placement",
        type=str,
        default="T,L",
        help="comma-separated list of vertical (T=top, C=center, B=bottom) and horizontal (L=left, C=center, R=right) anchoring."
    )

    font_family: str = TypedOption(
        "--font-family",
        type=str,
        default="sans\\-serif",
        help="the name of the TTF font-family to use, note: any hyphens need escaping with backslash."
    )

    font_size: int = TypedOption(
        "--font-size",
        type=int,
        default=14,
        help="the size of the font."
    )

    num_decimals: int = TypedOption(
        "--num-decimals",
        type=int,
        default=3,
        help="the number of decimals to use for float numbers in the text format string."
    )

    outline_thickness: int = TypedOption(
        "--outline-thickness",
        type=int,
        default=3,
        help="the line thickness to use for the outline, <1 to turn off."
    )

    outline_alpha: str = TypedOption(
        "--outline-alpha",
        type=int,
        default=255,
        help="the alpha value to use for the outline."
    )

    fill: bool = FlagOption(
        "--fill",
        help="whether to fill the bounding boxes/polygons"
    )

    fill_alpha: str = TypedOption(
        "--fill-alpha",
        type=int,
        default=128,
        help="the alpha value to use for the filling."
    )

    vary_colors: bool = FlagOption(
        "--vary-colors",
        help="whether to vary the colors of the outline/filling regardless of label"
    )

    force_bbox: bool = FlagOption(
        "--force-bbox",
        help="whether to force a bounding box even if there is a polygon available"
    )

    def _load_font(self, family, size):
        """
        Attempts to instantiate the specified font family.

        :param family: the TTF font family
        :type family: str
        :param size: the size to use
        :type size: int
        :return: the Pillow font
        """
        try:
            mpl_font = font_manager.FontProperties(family=family)
            font_file = font_manager.findfont(mpl_font)
            return ImageFont.truetype(font_file, size)
        except:
            self.logger.warning("Failed to instantiate font family '%s', falling back on '%s'" % (family, DEFAULT_FONT_FAMILY), exc_info=True)
            mpl_font = font_manager.FontProperties(family=DEFAULT_FONT_FAMILY)
            font_file = font_manager.findfont(mpl_font)
            return ImageFont.truetype(font_file, size)

    def _initialize(self):
        """
        Initializes colors etc.
        """
        self._colors = dict()
        self._default_colors = default_colors()
        self._default_colors_index = 0
        self._font = self._load_font(self.font_family, self.font_size)
        self._text_vertical, self._text_horizontal = self.text_placement.upper().split(",")

    def _next_default_color(self):
        """
        Returns the next default color.

        :return: the color tuple
        :rtype: tuple
        """
        if self._default_colors_index >= len(self._default_colors):
            self._default_colors_index = 0
        result = self._default_colors[self._default_colors_index]
        self._default_colors_index += 1
        return result

    def _get_color(self, label):
        """
        Returns the color for the label.

        :param label: the label to get the color for
        :type label: str
        :return: the RGB color tuple
        :rtype: tuple
        """
        if label not in self._colors:
            self._colors[label] = self._next_default_color()
        return self._colors[label]

    def _get_outline_color(self, label):
        """
        Generates the color for the outline.

        :param label: the label to get the color for
        :type label: str
        :return: the RGBA color tuple
        :rtype: tuple
        """
        r, g, b = self._get_color(label)
        return r, g, b, self.outline_alpha

    def _get_fill_color(self, label):
        """
        Generates the color for the filling.

        :param label: the label to get the color for
        :type label: str
        :return: the RGBA color tuple
        :rtype: tuple
        """
        r, g, b = self._get_color(label)
        return r, g, b, self.fill_alpha

    def _expand_label(self, label, metadata):
        """
        Expands the label text.

        :param label: the current label
        :type label: str
        :param metadata: the metadata associated with the label
        :type metadata: dict
        :return: the expanded label text
        :rtype: str
        """
        result = self.text_format.replace("{label}", label)
        for key in metadata:
            value = metadata[key]
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, bool):
                result = result.replace("{%s}" % key, str(value))
            elif isinstance(value, float):
                result = result.replace("{%s}" % key, ("%." + str(self.num_decimals) + "f") % float(value))
        return result

    def _text_coords(self, draw, text, rect):
        """
        Determines the text coordinates in the image.

        :param draw: the ImageDraw instance
        :type draw: ImageDraw
        :param text: the text to output
        :type text: str
        :param rect: the rectangle to use as reference
        :return: the x, y, w, h tuple
        :rtype: tuple
        """
        w, h = draw.textsize(text, font=self._font)

        # x
        if self._text_horizontal == "L":
            x = rect.left()
        elif self._text_horizontal == "C":
            x = rect.left() + (rect.right() - rect.left() - w) // 2
        elif self._text_horizontal == "R":
            x = rect.right() - w
        else:
            raise Exception("Unhandled horizontal text position: %s" % self._text_horizontal)

        # y
        if self._text_vertical == "T":
            y = rect.top()
        elif self._text_vertical == "C":
            y = rect.top() + (rect.bottom() - rect.top() - h) // 2
        elif self._text_vertical == "B":
            y = rect.bottom() - h
        else:
            raise Exception("Unhandled horizontal text position: %s" % self._text_horizontal)

        return x, y, w, h

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        if not hasattr(self, "_colors"):
            self._initialize()

        img_in = element.data
        img_pil = element.data.pil_image

        overlay = PIL.Image.new('RGBA', img_pil.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for i, lobj in enumerate(element.annotations):
            # determine label/color
            if self.vary_colors:
                label = "object-%d" % i
            else:
                label = "object"
                if self.label_key in lobj.metadata:
                    label = lobj.metadata[self.label_key]

            # assemble polygon
            points = []
            if lobj.has_polygon() and not self.force_bbox:
                poly_x = lobj.get_polygon_x()
                poly_y = lobj.get_polygon_y()
                for x, y in zip(poly_x, poly_y):
                    points.append((x, y))
            else:
                rect = lobj.get_rectangle()
                points.append((rect.left(), rect.top()))
                points.append((rect.right(), rect.top()))
                points.append((rect.right(), rect.bottom()))
                points.append((rect.left(), rect.bottom()))
            if self.fill:
                draw.polygon(tuple(points), outline=self._get_outline_color(label), fill=self._get_fill_color(label), width=self.outline_thickness)
            else:
                draw.polygon(tuple(points), outline=self._get_outline_color(label), width=self.outline_thickness)

            # output text
            if len(self.text_format) > 0:
                text = self._expand_label(label, lobj.metadata)
                rect = lobj.get_rectangle()
                x, y, w, h = self._text_coords(draw, text, rect)
                draw.rectangle((x, y, x+w, y+h), fill=self._get_outline_color(label))
                draw.text((x, y), text, font=self._font, fill=text_color(self._get_color(label)))

        img_pil.paste(overlay, (0, 0), mask=overlay)

        # convert back to PIL bytes
        pil_img_bytes = io.BytesIO()
        img_pil.save(pil_img_bytes, format=img_in.format.pil_format_string)
        img_out = Image(img_in.filename, pil_img_bytes.getvalue(), img_in.format, img_in.size)

        # new element
        then(element.__class__(img_out, element.annotations))
