import io
import PIL

from PIL import ImageDraw

from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.imgvis.isp.annotation_overlay.component._colors import default_colors, text_color
from wai.annotations.imgvis.isp.annotation_overlay.component._fonts import DEFAULT_FONT_FAMILY, load_font


class AnnotationOverlayOD(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
    """
    Stream processor which adds object detections overlays to images.
    """

    labels: str = TypedOption(
        "--labels",
        type=str,
        default="",
        help="the comma-separated list of labels of annotations to overlay, leave empty to overlay all"
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
        default=DEFAULT_FONT_FAMILY,
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

    colors: str = TypedOption(
        "--colors",
        type=str,
        default="",
        help="the blank-separated list of RGB triplets (R,G,B) of custom colors to use, leave empty for default colors"
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
        help="the alpha value to use for the outline (0: transparent, 255: opaque)."
    )

    fill: bool = FlagOption(
        "--fill",
        help="whether to fill the bounding boxes/polygons"
    )

    fill_alpha: str = TypedOption(
        "--fill-alpha",
        type=int,
        default=128,
        help="the alpha value to use for the filling (0: transparent, 255: opaque)."
    )

    vary_colors: bool = FlagOption(
        "--vary-colors",
        help="whether to vary the colors of the outline/filling regardless of label"
    )

    force_bbox: bool = FlagOption(
        "--force-bbox",
        help="whether to force a bounding box even if there is a polygon available"
    )

    def _initialize(self):
        """
        Initializes colors etc.
        """
        self._colors = dict()
        self._default_colors = default_colors()
        self._default_colors_index = 0
        self._custom_colors = []
        if len(self.colors) > 0:
            for color in self.colors.split(" "):
                self._custom_colors.append([int(x) for x in color.split(",")])
        self._label_mapping = dict()
        self._font = load_font(self.logger, self.font_family, self.font_size)
        self._text_vertical, self._text_horizontal = self.text_placement.upper().split(",")
        self._accepted_labels = None
        if len(self.labels) > 0:
            self._accepted_labels = set(self.labels.split(","))

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
            has_custom = False
            if label in self._label_mapping:
                index = self._label_mapping[label]
                if index < len(self._custom_colors):
                    has_custom = True
                    self._colors[label] = self._custom_colors[index]
            if not has_custom:
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
            label = "object"
            if self.label_key in lobj.metadata:
                label = lobj.metadata[self.label_key]
            if self._accepted_labels is not None:
                if label not in self._accepted_labels:
                    continue
            if label not in self._label_mapping:
                self._label_mapping[label] = len(self._label_mapping)
            if self.vary_colors:
                color_label = "object-%d" % i
            else:
                color_label = label

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
                draw.polygon(tuple(points), outline=self._get_outline_color(color_label), fill=self._get_fill_color(color_label), width=self.outline_thickness)
            else:
                draw.polygon(tuple(points), outline=self._get_outline_color(color_label), width=self.outline_thickness)

            # output text
            if len(self.text_format) > 0:
                text = self._expand_label(label, lobj.metadata)
                rect = lobj.get_rectangle()
                x, y, w, h = self._text_coords(draw, text, rect)
                draw.rectangle((x, y, x+w, y+h), fill=self._get_outline_color(color_label))
                draw.text((x, y), text, font=self._font, fill=text_color(self._get_color(color_label)))

        img_pil.paste(overlay, (0, 0), mask=overlay)

        # convert back to PIL bytes
        pil_img_bytes = io.BytesIO()
        img_pil.save(pil_img_bytes, format=img_in.format.pil_format_string)
        img_out = Image(img_in.filename, pil_img_bytes.getvalue(), img_in.format, img_in.size)

        # new element
        then(element.__class__(img_out, element.annotations))
