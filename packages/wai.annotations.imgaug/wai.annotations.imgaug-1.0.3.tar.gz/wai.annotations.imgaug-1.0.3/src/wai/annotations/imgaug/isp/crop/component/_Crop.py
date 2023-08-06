import imgaug.augmenters as iaa

from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.imgaug.isp.base.component import BaseImageAugmentation


class Crop(BaseImageAugmentation):
    """
    Stream processor which crops images.
    """

    percent_from: float = TypedOption(
        "-f", "--from-percent",
        type=float,
        help="the minimum percent to crop from images"
    )

    percent_to: float = TypedOption(
        "-t", "--to-percent",
        type=float,
        help="the maximum percent to crop from images"
    )

    update_size: bool = FlagOption(
        "-u", "--update-size",
        help="whether to update the image size after the crop operation or scale back to original size"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-cropped"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.percent_from is not None) and (self.percent_to is not None)

    def _create_pipeline(self, aug_seed):
        """
        Creates and returns the augmentation pipeline.

        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the pipeline
        :rtype: iaa.Sequential
        """
        keep_size = not self.update_size

        if self.percent_from == self.percent_to:
            return iaa.Sequential([
                iaa.Crop(percent=self.percent_from, keep_size=keep_size)
            ])
        else:
            return iaa.Sequential([
                iaa.Crop(percent=(self.percent_from, self.percent_to), keep_size=keep_size)
            ])
