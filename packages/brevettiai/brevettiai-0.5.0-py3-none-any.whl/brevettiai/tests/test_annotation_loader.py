import unittest
import json
import tensorflow as tf

from brevettiai.tests import get_resource
from brevettiai.data.image import ImageLoader, AnnotationLoader
from brevettiai.data.tf_types import BBOX
from brevettiai.io import io_tools


class TestImageLoaderBbox(unittest.TestCase):
    test_image_path = get_resource("0_1543413266626.bmp")
    test_annotation_path = get_resource("1651574629796.json")
    bbox = BBOX(x1=10, x2=210, y1=30, y2=130)

    def test_loader_bbox_selection(self):
        classes = set([anno["label"] for anno in
                       json.loads(io_tools.read_file(self.test_annotation_path))["annotations"]])
        annotation_bbox, _ = AnnotationLoader(classes=classes).load(path=self.test_annotation_path, bbox=self.bbox)
        image_bbox, _ = ImageLoader(interpolation_method="nearest").load(self.test_image_path, bbox=self.bbox)
        image_raw, _ = ImageLoader(interpolation_method="nearest").load(self.test_image_path)
        annotation_raw, _ = AnnotationLoader(classes=classes).load(path=self.test_annotation_path,
                                                 metadata={"_image_file_shape": image_raw.shape})

        # Test that annotation is not empty
        tf.debugging.assert_greater(tf.reduce_mean(tf.abs(annotation_bbox)), 1e-4)

        # Test that image_bbox is correct region
        tf.debugging.assert_less_equal(tf.reduce_mean(tf.abs(
            image_bbox -
            image_raw[self.bbox.y1:self.bbox.y2 + 1, self.bbox.x1:self.bbox.x2 + 1])), 1e-4)

        # Test that area outputs shape of output image
        tf.debugging.assert_less_equal(tf.cast(tf.abs(
            self.bbox.area - annotation_bbox.shape[0] * annotation_bbox.shape[1]), dtype=tf.int64),
            tf.constant(0, dtype=tf.int64))

        # Test that annotation_bbox is correct region
        tf.debugging.assert_less_equal(tf.reduce_sum(tf.abs(
            annotation_bbox -
            annotation_raw[self.bbox.y1:self.bbox.y2 + 1, self.bbox.x1:self.bbox.x2 + 1])), 25.0)

        tf.debugging.assert_less_equal(tf.reduce_sum(
            tf.abs(tf.convert_to_tensor(annotation_bbox.shape)[:2] - tf.convert_to_tensor(image_bbox.shape)[:2])), 0)


if __name__ == '__main__':
    unittest.main()
