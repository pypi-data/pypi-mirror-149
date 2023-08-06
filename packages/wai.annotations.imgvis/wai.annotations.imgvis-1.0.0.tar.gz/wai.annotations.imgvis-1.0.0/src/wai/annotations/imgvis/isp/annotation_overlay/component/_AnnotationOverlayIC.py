import io
import PIL

from PIL import ImageDraw

from wai.common.cli.options import TypedOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.classification import ImageClassificationInstance
from wai.annotations.imgvis.isp.annotation_overlay.component._fonts import DEFAULT_FONT_FAMILY, load_font


class AnnotationOverlayIC(
    RequiresNoFinalisation,
    ProcessorComponent[ImageClassificationInstance, ImageClassificationInstance]
):
    """
    Stream processor which adds image classification labels on top of images.
    """

    text_placement: str = TypedOption(
        "--position",
        type=str,
        default="5,5",
        help="the position of the label (X,Y)."
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

    font_color: str = TypedOption(
        "--font-color",
        type=str,
        default="255,255,255",
        help="the RGB color triplet to use for the font."
    )

    def _initialize(self):
        """
        Initializes colors etc.
        """
        self._colors = dict()
        self._font = load_font(self.logger, self.font_family, self.font_size)
        self._font_color = tuple([int(x) for x in self.font_color.split(",")])
        self._text_x, self._text_y = [int(x) for x in self.text_placement.upper().split(",")]

    def process_element(
            self,
            element: ImageClassificationInstance,
            then: ThenFunction[ImageClassificationInstance],
            done: DoneFunction
    ):
        if not hasattr(self, "_colors"):
            self._initialize()

        img_in = element.data
        img_pil = element.data.pil_image

        overlay = PIL.Image.new('RGBA', img_pil.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.text((self._text_x, self._text_y), element.annotations.label, font=self._font, fill=self._font_color)
        img_pil.paste(overlay, (0, 0), mask=overlay)

        # convert back to PIL bytes
        pil_img_bytes = io.BytesIO()
        img_pil.save(pil_img_bytes, format=img_in.format.pil_format_string)
        img_out = Image(img_in.filename, pil_img_bytes.getvalue(), img_in.format, img_in.size)

        # new element
        then(element.__class__(img_out, element.annotations))
