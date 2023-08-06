import io
from PIL import Image, ImageDraw

from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance

from wai.common.cli.options import TypedOption


class AnnotationOverlay(
    SinkComponent[ImageObjectDetectionInstance]
):

    color: str = TypedOption(
        "-c", "--color",
        type=str,
        default="255,0,0,64",
        help="the color to use for drawing the shapes as RGBA byte-quadruplet, e.g.: 255,0,0,64"
    )

    background_color: str = TypedOption(
        "-b", "--background-color",
        type=str,
        default="255,255,255,255",
        help="the color to use for the background as RGBA byte-quadruplet, e.g.: 255,255,255,255"
    )

    scale_to: str = TypedOption(
        "-s", "--scale-to",
        type=str,
        default="",
        help="the dimensions to scale all images to before overlaying them (format: width,height)"
    )

    output_file: str = TypedOption(
        "-o", "--output",
        type=str,
        default="./overlay.png",
        help="the PNG image to write the generated overlay to"
    )

    def output_overlay(self):
        """
        Outputs the overlay image.
        """
        if hasattr(self, "_overlay"):
            self._overlay.save(self.output_file, format="PNG")
        else:
            print("No overlay generated!")

    def consume_element(self, element: ImageObjectDetectionInstance):
        """
        Consumes instances.
        """
        img = Image.open(io.BytesIO(element.data.data))

        if not hasattr(self, "_overlay"):
            self._scale_to = None
            if len(self.scale_to) > 0:
                self._scale_to = [int(x) for x in self.scale_to.split(",")]
                if len(self._scale_to) != 2:
                    self.logger.error("'--scale-to' option requires format 'width,height' but received: %s" % self.scale_to)
                    self._scale_to = None
            # initialize overlay
            self._color = tuple([int(x) for x in self.color.split(",")])
            self._background_color = tuple([int(x) for x in self.background_color.split(",")])
            self._overlay = Image.new('RGBA', img.size if (self._scale_to is None) else self._scale_to, self._background_color)
        else:
            # do we have to make the overlay larger?
            if self._scale_to is None:
                if (img.size[0] > self._overlay.size[0]) or (img.size[1] > self._overlay.size[1]):
                    new_size = (max(img.size[0], self._overlay.size[0]), max(img.size[1], self._overlay.size[1]))
                    tmp = Image.new('RGBA', new_size, self._background_color)
                    tmp.paste(self._overlay, (0, 0))
                    self._overlay = tmp

        if self._scale_to is None:
            scale_x = 1.0
            scale_y = 1.0
        else:
            scale_x = self._overlay.size[0] / img.size[0]
            scale_y = self._overlay.size[1] / img.size[1]

        for lobj in element.annotations:
            points = []
            if lobj.has_polygon():
                poly_x = lobj.get_polygon_x()
                poly_y = lobj.get_polygon_y()
                for x, y in zip(poly_x, poly_y):
                    points.append((int(x * scale_x), int(y * scale_y)))
            else:
                rect = lobj.get_rectangle()
                points.append((int(rect.left() * scale_x), int(rect.top() * scale_y)))
                points.append((int(rect.right() * scale_x), int(rect.top() * scale_y)))
                points.append((int(rect.right() * scale_x), int(rect.bottom() * scale_y)))
                points.append((int(rect.left() * scale_x), int(rect.bottom() * scale_y)))

            draw = ImageDraw.Draw(self._overlay)
            draw.polygon(tuple(points), outline=self._color)

    def finish(self):
        self.output_overlay()
