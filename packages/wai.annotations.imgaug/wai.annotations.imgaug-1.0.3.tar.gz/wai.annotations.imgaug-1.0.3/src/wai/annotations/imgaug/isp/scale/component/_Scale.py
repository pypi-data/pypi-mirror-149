import imgaug.augmenters as iaa

from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.imgaug.isp.base.component import BaseImageAugmentation


class Scale(BaseImageAugmentation):
    """
    Stream processor which scales images, either randomly within a range of percentages
    or with a specific percentage when the to/from percentages are the same.
    """

    percentage_from: float = TypedOption(
        "-f", "--from-percentage",
        type=float,
        help="the start of the percentage range to use for scaling the images"
    )

    percentage_to: float = TypedOption(
        "-t", "--to-percentage",
        type=float,
        help="the end of the percentage range to use for scaling the images"
    )

    keep_aspect: bool = FlagOption(
        "-k", "--keep-aspect",
        help="whether to keep the aspect ratio"
    )

    update_size: bool = FlagOption(
        "-u", "--update-size",
        help="whether to update the image size after the scaling operation or use original size"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-scaled"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.percentage_from is not None) and (self.percentage_to is not None)

    def _create_pipeline(self, aug_seed):
        """
        Creates and returns the augmentation pipeline.

        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the pipeline
        :rtype: iaa.Sequential
        """
        if self.percentage_from == self.percentage_to:
            scale = {"x": (self.percentage_from, self.percentage_from),
                     "y": (self.percentage_from, self.percentage_from)}
        else:
            if self.keep_aspect:
                percentage = self._random.random() * (self.percentage_to - self.percentage_from) + self.percentage_from
                scale = {"x": (percentage, percentage),
                         "y": (percentage, percentage)}
            else:
                scale = {"x": (self.percentage_from, self.percentage_to),
                         "y": (self.percentage_from, self.percentage_to)}

        return iaa.Sequential([
            iaa.Affine(
                scale=scale,
                seed=aug_seed,
                fit_output=self.update_size,
            )
        ])
