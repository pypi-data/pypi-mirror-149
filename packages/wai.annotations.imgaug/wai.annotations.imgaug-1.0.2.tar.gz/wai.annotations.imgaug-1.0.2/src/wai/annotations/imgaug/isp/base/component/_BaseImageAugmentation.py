import io
import imageio
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug.augmentables.polys import Polygon, PolygonsOnImage
import numpy as np
import PIL

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.geometry import Polygon as WaiPolygon
from wai.common.geometry import Point as WaiPoint
from wai.annotations.domain.image import ImageInstance, Image
from wai.annotations.imgaug.isp.base.component import BaseISP


class BaseImageAugmentation(BaseISP):
    """
    Base class for stream processors that augment images.
    """

    def _create_pipeline(self, aug_seed):
        """
        Creates and returns the augmentation pipeline.

        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the pipeline
        :rtype: iaa.Sequential
        """
        raise NotImplementedError()

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
        seq = self._create_pipeline(aug_seed)

        img_in = element.data
        image = imageio.imread(element.data.data)

        # convert annotations
        bboxesoi = None
        polysoi = None
        if element.annotations_type() == LocatedObjects:
            has_polys = False
            for obj in element.annotations:
                if obj.has_polygon():
                    has_polys = True
                    break
            if has_polys:
                polys = []
                for obj in element.annotations:
                    x = obj.get_polygon_x()
                    y = obj.get_polygon_y()
                    points = []
                    for i in range(len(x)):
                        points.append((x[i], y[i]))
                    poly = Polygon(points)
                    polys.append(poly)
                    polysoi = PolygonsOnImage(polys, shape=image.shape)
            else:
                bboxes = []
                for obj in element.annotations:
                    bbox = BoundingBox(x1=obj.x, y1=obj.y, x2=obj.x + obj.width - 1, y2=obj.y + obj.height - 1)
                    bboxes.append(bbox)
                bboxesoi = BoundingBoxesOnImage(bboxes, shape=image.shape)

        # augment
        bbs_aug = None
        polys_aug = None
        if bboxesoi is not None:
            image_aug, bbs_aug = seq(image=image, bounding_boxes=bboxesoi)
        elif polysoi is not None:
            image_aug, polys_aug = seq(image=image, polygons=polysoi)
        else:
            image_aug = seq(image=image)

        # update annotations
        annotations_new = element.annotations
        if bbs_aug is not None:
            objs_aug = []
            for i, bbox in enumerate(bbs_aug):
                # skip ones outside image
                if bbox.is_out_of_image(image_aug):
                    continue
                # clip bboxes to fit into image
                bbox = bbox.clip_out_of_image(image_aug)
                # update located object
                obj_aug = element.annotations[i].get_clone()
                obj_aug.x = bbox.x1
                obj_aug.y = bbox.y1
                obj_aug.width = bbox.x2 - bbox.x1 + 1
                obj_aug.height = bbox.y2 - bbox.y1 + 1
                objs_aug.append(obj_aug)
                annotations_new = LocatedObjects(objs_aug)
        elif polys_aug is not None:
            objs_aug = []
            for i, poly in enumerate(polys_aug):
                # skip ones outside image
                if poly.is_out_of_image(image_aug):
                    continue
                # clip bboxes to fit into image
                polys = poly.clip_out_of_image(image_aug)
                if len(polys) == 0:
                    continue
                for p in polys:
                    # update located object
                    obj_aug = element.annotations[i].get_clone()
                    bbox = p.to_bounding_box()
                    obj_aug.x = bbox.x1
                    obj_aug.y = bbox.y1
                    obj_aug.width = bbox.x2 - bbox.x1 + 1
                    obj_aug.height = bbox.y2 - bbox.y1 + 1
                    points = []
                    for row in p.coords:
                        points.append(WaiPoint((int(row[0])), int(row[1])))
                    obj_aug.set_polygon(WaiPolygon(*points))
                    objs_aug.append(obj_aug)
            annotations_new = LocatedObjects(objs_aug)

        img_pil = PIL.Image.fromarray(np.uint8(image_aug))
        pil_img_bytes = io.BytesIO()
        img_pil.save(pil_img_bytes, format=img_in.format.pil_format_string)
        img_out = Image(img_in.filename, pil_img_bytes.getvalue(), img_in.format, img_pil.size)

        # new element
        result = element.__class__(img_out, annotations_new)
        return result
