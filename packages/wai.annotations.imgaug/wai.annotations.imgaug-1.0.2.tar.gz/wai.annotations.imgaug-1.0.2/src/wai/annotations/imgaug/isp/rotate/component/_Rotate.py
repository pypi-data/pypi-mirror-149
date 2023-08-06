import imgaug.augmenters as iaa

from wai.common.cli.options import TypedOption
from wai.annotations.imgaug.isp.base.component import BaseImageAugmentation


class Rotate(BaseImageAugmentation):
    """
    Stream processor which rotates images, either randomly within a range of degrees
    (negative/positive) or with a specific degree when the to/from degrees are the same.
    """

    degree_from: float = TypedOption(
        "-f", "--from-degree",
        type=float,
        help="the start of the degree range to use for rotating the images"
    )

    degree_to: float = TypedOption(
        "-t", "--to-degree",
        type=float,
        help="the end of the degree range to use for rotating the images"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-rotated"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.degree_from is not None) and (self.degree_to is not None)

    def _create_pipeline(self, aug_seed):
        """
        Creates and returns the augmentation pipeline.

        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the pipeline
        :rtype: iaa.Sequential
        """
        if self.degree_from == self.degree_to:
            return iaa.Sequential([
                iaa.Affine(
                    rotate=self.degree_from,
                    seed=aug_seed,
                )
            ])
        else:
            return iaa.Sequential([
                iaa.Affine(
                    rotate=(self.degree_from, self.degree_to),
                    seed=aug_seed,
                )
            ])
