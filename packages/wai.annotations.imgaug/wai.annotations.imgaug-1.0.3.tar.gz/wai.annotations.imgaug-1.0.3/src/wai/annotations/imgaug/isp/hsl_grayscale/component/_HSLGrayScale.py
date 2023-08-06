import cv2
import io
import numpy as np
import PIL

from random import Random
from wai.common.cli.options import TypedOption
from wai.annotations.domain.image import ImageInstance, Image
from wai.annotations.imgaug.isp.base.component import BaseISP


class HSLGrayScale(BaseISP):
    """
    Stream processor which turns RGB images into fake grayscale ones.
    """

    factor_from: float = TypedOption(
        "-f", "--from-factor",
        type=float,
        help="the start of the factor range to apply to the L channel to darken or lighten the image (<1: darker, >1: lighter)"
    )

    factor_to: float = TypedOption(
        "-t", "--to-factor",
        type=float,
        help="the end of the factor range to apply to the L channel to darken or lighten the image (<1: darker, >1: lighter)"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-gray"

    def _augment(self, element: ImageInstance, aug_seed: int):
        """
        Augments the image.

        :param element: the image to augment
        :type element: ImageInstance
        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the potentially updated image
        :rtype: ImageInstance
        """
        img_in = element.data

        # convert to HSL
        img_pil = img_in.pil_image
        img_rgb = np.array(img_pil)
        img_hls = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HLS)
        img_l = img_hls[:, :, 1]

        # determine factor
        factor = None
        if (self.factor_from is not None) and (self.factor_to is not None):
            if self.factor_from == self.factor_to:
                factor = self.factor_from
            else:
                rnd = Random(aug_seed)
                factor = rnd.random() * (self.factor_to - self.factor_from) + self.factor_from

        # adjust brightness?
        if factor is not None:
            img_l = img_l * factor
            img_l = img_l.astype(np.uint8)

        # convert back to PIL bytes
        img_pil = PIL.Image.fromarray(np.uint8(img_l))
        pil_img_bytes = io.BytesIO()
        img_pil.save(pil_img_bytes, format=img_in.format.pil_format_string)
        img_out = Image(img_in.filename, pil_img_bytes.getvalue(), img_in.format, img_in.size)

        # new element
        result = element.__class__(img_out, element.annotations)
        return result
