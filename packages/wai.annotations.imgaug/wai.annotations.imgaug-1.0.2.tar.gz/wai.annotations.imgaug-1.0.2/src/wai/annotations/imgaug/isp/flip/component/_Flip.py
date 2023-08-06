import imgaug.augmenters as iaa

from wai.common.cli.options import TypedOption
from wai.annotations.imgaug.isp.base.component import BaseImageAugmentation


LEFT_TO_RIGHT = "lr"
UP_TO_DOWN = "up"
LEFT_TO_RIGHT_AND_UP_TO_DOWN = "lrup"

DIRECTIONS = [
    LEFT_TO_RIGHT,
    UP_TO_DOWN,
    LEFT_TO_RIGHT_AND_UP_TO_DOWN
]


class Flip(BaseImageAugmentation):
    """
    Stream processor which flips images.
    """

    direction: str = TypedOption(
        "-d", "--direction",
        type=str,
        help="the direction to flip, available options: %s" % (", ".join(DIRECTIONS))
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-flipped"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        if self.direction is None:
            return False
        if self.direction not in DIRECTIONS:
            self.logger.warning("Invalid direction: %s" % self.direction)
            return False
        return True

    def _create_pipeline(self, aug_seed):
        """
        Creates and returns the augmentation pipeline.

        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the pipeline
        :rtype: iaa.Sequential
        """
        if self.direction == LEFT_TO_RIGHT:
            return iaa.Sequential([
                iaa.Fliplr(),
            ])
        elif self.direction == UP_TO_DOWN:
            return iaa.Sequential([
                iaa.Flipud(),
            ])
        elif self.direction == LEFT_TO_RIGHT_AND_UP_TO_DOWN:
            return iaa.Sequential([
                iaa.Fliplr(),
                iaa.Flipud(),
            ])
        else:
            raise Exception("Unsupported direction: %s" % self.direction)
