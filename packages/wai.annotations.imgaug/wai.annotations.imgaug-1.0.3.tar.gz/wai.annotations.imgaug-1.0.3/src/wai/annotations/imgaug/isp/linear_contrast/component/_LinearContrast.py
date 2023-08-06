import imgaug.augmenters as iaa

from wai.common.cli.options import TypedOption
from wai.annotations.imgaug.isp.base.component import BaseImageAugmentation


class LinearContrast(BaseImageAugmentation):
    """
    Stream processor which applies linear contrast to images.
    """

    alpha_from: float = TypedOption(
        "-f", "--from-alpha",
        type=float,
        help="the minimum alpha to apply to the images"
    )

    alpha_to: float = TypedOption(
        "-t", "--to-alpha",
        type=float,
        help="the maximum alpha to apply to the images"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-contrasted"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.alpha_from is not None) and (self.alpha_to is not None)

    def _create_pipeline(self, aug_seed):
        """
        Creates and returns the augmentation pipeline.

        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the pipeline
        :rtype: iaa.Sequential
        """
        if self.alpha_from == self.alpha_to:
            return iaa.Sequential([
                iaa.LinearContrast(self.alpha_from)
            ])
        else:
            return iaa.Sequential([
                iaa.LinearContrast((self.alpha_from, self.alpha_to))
            ])
