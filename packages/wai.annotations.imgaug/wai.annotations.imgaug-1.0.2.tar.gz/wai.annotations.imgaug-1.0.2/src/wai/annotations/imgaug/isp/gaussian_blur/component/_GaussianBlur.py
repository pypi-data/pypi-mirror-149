import imgaug.augmenters as iaa

from wai.common.cli.options import TypedOption
from wai.annotations.imgaug.isp.base.component import BaseImageAugmentation


class GaussianBlur(BaseImageAugmentation):
    """
    Stream processor which applies gaussian blur to images.
    """

    sigma_from: float = TypedOption(
        "-f", "--from-sigma",
        type=float,
        help="the minimum sigma for the blur to apply to the images"
    )

    sigma_to: float = TypedOption(
        "-t", "--to-sigma",
        type=float,
        help="the maximum sigma for the blur to apply to the images"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-blurred"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.sigma_from is not None) and (self.sigma_to is not None)

    def _create_pipeline(self, aug_seed):
        """
        Creates and returns the augmentation pipeline.

        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the pipeline
        :rtype: iaa.Sequential
        """
        if self.sigma_from == self.sigma_to:
            return iaa.Sequential([
                iaa.GaussianBlur(sigma=self.sigma_from)
            ])
        else:
            return iaa.Sequential([
                iaa.GaussianBlur(sigma=(self.sigma_from, self.sigma_to))
            ])
