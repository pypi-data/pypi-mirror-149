import cv2
import io
import numpy as np

from wai.common.cli.options import TypedOption
from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.image import ImageInstance


class ImageViewer(
    SinkComponent[ImageInstance]
):
    """
    Sink for displaying images.
    """

    title: str = TypedOption(
        "--title",
        type=str,
        default="wai.annotations",
        help="the title for the window"
    )

    position: str = TypedOption(
        "--position",
        type=str,
        default="0,0",
        help="the position of the window on screen (X,Y)"
    )

    size: str = TypedOption(
        "--size",
        type=str,
        default="640,480",
        help="the maximum size for the image: WIDTH,HEIGHT"
    )

    delay: int = TypedOption(
        "--delay",
        type=int,
        default=500,
        help="the delay in milli-seconds between images, use 0 to wait for keypress, ignored if <0"
    )

    def consume_element(self, element: ImageInstance):
        """
        Consumes instances by displaying them.
        """
        # read image
        img_array = np.fromstring(io.BytesIO(element.data.data).read(), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # resize image, if necessary
        if not hasattr(self, "_width"):
            self._width, self._height = [int(x) for x in self.size.split(",")]
            self._ratio = self._width / self._height
        h, w, _ = img.shape
        if (h > self._height) or (w > self._width):
            img_ratio = w / h
            if img_ratio > self._ratio:
                w_new = self._width
                h_new = w_new / img_ratio
            else:
                h_new = self._height
                w_new = h_new * img_ratio
            img = cv2.resize(img, (int(w_new), int(h_new)))

        cv2.imshow(self.title, img)

        # position window
        if not hasattr(self, "_x"):
            self._x, self._y = [int(x) for x in self.position.split(",")]
            cv2.moveWindow(self.title, self._x, self._y)

        # delay
        if self.delay >= 0:
            cv2.waitKey(self.delay)

    def finish(self):
        cv2.destroyAllWindows()
