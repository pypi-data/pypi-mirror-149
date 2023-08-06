import json
import tensorflow as tf
import numpy as np

from pydantic import Field
from pydantic.typing import Literal
from typing import Optional, ClassVar, Type, Union
from brevettiai.data import FileLoader
from brevettiai.data.image import ImageKeys
from brevettiai.data.image.image_processor import ImageProcessor
from brevettiai.data.tf_types import TfRange, BBOX


class ScalingProcessor(ImageProcessor):
    type: Literal["ScalingProcessor"] = "ScalingProcessor"

    def process(self, image):
        """Process image according to processor"""
        max_ = tf.reduce_max(image)
        min_ = tf.reduce_min(image)
        image = (image - min_) / (max_ - min_)
        return image


class CropResizeProcessor(ImageProcessor):
    type: Literal["CropResizeProcessor"] = "CropResizeProcessor"
    output_height: int = Field(default=0, ge=0, description="Leave at 0 to infer")
    output_width: int = Field(default=0, ge=0, description="Leave at 0 to infer")

    roi_horizontal_offset: int = Field(
        default=0, ge=0, description="Horizontal coordinate of the top-left corner of the bounding box in image.")
    roi_vertical_offset: int = Field(
        default=0, ge=0, description="Vertical coordinate of the top-left corner of the bounding box in image.")
    roi_width: int = Field(default=0, ge=0, description="Width of the bounding box. Zero uses image boundary")
    roi_height: int = Field(default=0, ge=0, description="Height of the bounding box. Zero uses image boundary")

    interpolation: Literal["bilinear", "nearest"] = Field(
        default="bilinear", description="Interpolation mode of cropping and resizing")

    def output_size(self, input_height, input_width):
        """Calculated output size of output after postprocessing, given input image sizes"""
        height = self.roi_height or input_height
        width = self.roi_width or input_width
        return self.output_height or height, self.output_width or width

    def crop_size(self, input_height, input_width):
        height = input_height - self.roi_vertical_offset if self.roi_height == 0 else self.roi_height
        width = input_width - self.roi_horizontal_offset if self.roi_width == 0 else self.roi_width
        return height, width

    def bbox(self, input_height, input_width):
        """
        Calculate bounding box specified in pixel coordinates [y1, x1, y2, x2]
        The points both being included in the region of interest
        """
        height, width = self.crop_size(input_height, input_width)
        return self.roi_vertical_offset, self.roi_horizontal_offset, \
            self.roi_vertical_offset + height - 1, self.roi_horizontal_offset + width - 1

    def scale(self, input_height, input_width):
        """
        Calculate output image scale given input image size
        returns scale in height then width (sy, sx)
        """
        crop_height, crop_width = self.crop_size(input_height, input_width)
        output_height, output_width = self.output_size(input_width, input_height)
        return (crop_height-1) / (output_height-1), (crop_width-1) / (output_width-1),

    def affine_transform(self, input_height, input_width):
        sy, sx = self.scale(input_height, input_width)

        return np.array([
            [sx,  0, self.roi_horizontal_offset],
            [0, sy, self.roi_vertical_offset],
            [0, 0, 1]
        ])

    def process(self, image):
        shape = tf.shape(image)[:2]
        input_height, input_width = shape[0], shape[1]

        size = self.output_size(input_height, input_width)

        # Normalize bounding box to match crop_and_resize
        # https://www.tensorflow.org/api_docs/python/tf/image/crop_and_resize
        norm = tf.cast([input_height, input_width, input_height, input_width], tf.float32)-1
        bbox = tf.cast(self.bbox(input_height, input_width), tf.float32)
        boxes = [bbox / norm]

        # Crop and resize, attach batch dimension to match tf call
        return tf.image.crop_and_resize(
            image[None], boxes, box_indices=[0], crop_size=size, method=self.interpolation,
            extrapolation_value=0.0
        )[0]


class ImageLoader(FileLoader):
    type: Literal["ImageLoader"] = "ImageLoader"
    output_key: str = Field(default="img", exclude=True)
    postprocessor: Optional[Union[CropResizeProcessor, ImageProcessor]] = Field(default_factory=CropResizeProcessor)
    interpolation_method: Optional[Literal["bilinear", "nearest"]] = Field(default="bilinear")
    channels: Literal[0, 1, 3, 4] = Field(default=0, description="Number of channels in images, 0 to autodetect")
    metadata_spec = {
        ImageKeys.BOUNDING_BOX: BBOX.build
    }

    def output_shape(self, image_height=None, image_width=None):
        output_channels = self.channels if self.channels else None
        if self.postprocessor is None:
            return image_height, image_width, output_channels
        else:
            return (*self.postprocessor.output_size(image_height, image_width),
                    self.postprocessor.output_channels(output_channels))

    def load(self, path, metadata=None, postprocess=True, bbox: BBOX = BBOX()):
        metadata = metadata or dict()
        data, meta = super().load(path, metadata)
        bbox = metadata.get(ImageKeys.BOUNDING_BOX, bbox)

        if tf.strings.length(data) > 0:
            image = tf.io.decode_image(data, expand_animations=False, channels=self.channels)
            ifs = tf.convert_to_tensor(tf.shape(image))
            if bbox.area <= 1:
                bbox = BBOX(x1=bbox.x1, y1=bbox.y1, x2=bbox.x1 + ifs[1], y2=bbox.y1 + ifs[0])

            image = tf.image.crop_and_resize(image[None],
                                             [[bbox.y1 / ifs[0], bbox.x1 / ifs[1],
                                               bbox.y1 / ifs[0] + 1, bbox.x1  / ifs[1] +  1]] ,
                                             box_indices=[0],
                                             crop_size=ifs[:2],
                                             method=self.interpolation_method,
                                             extrapolation_value=0.0)[0, :bbox.shape[0], :bbox.shape[1]]
            _image_file_shape = tf.convert_to_tensor(tf.shape(image))
            if postprocess and self.postprocessor is not None:
                image = self.postprocessor.process(image)
        else:
            if postprocess and self.postprocessor is not None:
                image = tf.constant(0, dtype=tf.float32, shape=(1, 1, 1))
            else:
                image = tf.constant(0, dtype=tf.uint8, shape=(1, 1, 1))
            _image_file_shape = tf.convert_to_tensor(tf.shape(image))

        meta["_image_file_shape"] = _image_file_shape

        return image, meta


class ImageStabiliser(FileLoader):
    type: Literal["ImageStabilisationLoader"] = "ImageStabilisationLoader"

    interpolation: Literal["NEAREST", "BILINEAR"] = Field(default="NEAREST")
    image_key: str = Field(default="img")
    label_key: str = Field(default="segmentation")

    enabled: bool = Field(default=False)

    def load_matrix(self, path):
        bcfile = json.loads(self._io.read_file(path))
        matrices = bcfile.get("transforms", np.eye(2, 3))
        matrices = np.array(matrices).astype(np.float32)
        return np.pad(matrices.reshape((-1, 6)), [[0, 0], [0, 2]])

    def __call__(self, x, *args, **kwargs):
        matrices = tf.numpy_function(self.load_matrix, [x["path"]], [tf.float32], name="load_matrix")
        image_shape = tf.shape(x[self.image_key][0])
        print(image_shape)
        x[self.image_key] = tf.raw_ops.ImageProjectiveTransformV3(images=x[self.image_key],
                                                       transforms=matrices[0],
                                                       output_shape=image_shape[:2],
                                                       fill_value=0,
                                                       interpolation=self.interpolation)
        if self.label_key in x:
            x[self.label_key] = tf.raw_ops.ImageProjectiveTransformV3(images=x[self.label_key],
                                                                        transforms=matrices[0],
                                                                        output_shape=image_shape[:2],
                                                                        fill_value=0,
                                                                        interpolation=self.interpolation)

        return x

class BcimgSequenceLoader(ImageLoader):
    type: Literal["BcimgSequenceLoader"] = "BcimgSequenceLoader"
    range_meta: ClassVar[Type] = TfRange
    metadata_spec = {ImageKeys.SEQUENCE_RANGE: range_meta.build}

    def output_shape(self, image_height=None, image_width=None):
        output_channels = self.channels if self.channels else None
        return (*self.postprocessor.output_size(image_height, image_width), output_channels)

    def load_sequence(self, path, postprocess=True):
        try:
            path = path.item()
        except AttributeError:
            pass
        header = json.loads(self._io.read_file(path))["Image"]

        if header["DType"] == "eGrayScale8":
            channels = 1
        else:
            raise NotImplementedError(f"dtype of bcimg.json '{header['DType']}' not implemented")
        shape = np.array((
            int(header["Frames"]),
            int(header["OriginalSize"]["Height"]),
            int(header["OriginalSize"]["Width"]),
            channels
        ), np.int32)
        sequence_fmt = self._io.path.join(path[:-10].decode(), "image_files", f"{{:06d}}.{header['Format']}").format
        sequence_files = np.array([sequence_fmt(i) for i in range(shape[0])])
        return sequence_files, shape

    def load(self, path, metadata=None, postprocess=True, bbox:BBOX = BBOX()):
        files, shape = tf.numpy_function(self.load_sequence, [path], [tf.string, tf.int32], name="load_header")

        if metadata is not None:
            # Select frames
            if ImageKeys.SEQUENCE_RANGE in metadata:
                files = metadata[ImageKeys.SEQUENCE_RANGE].slice(files)

        images, meta = tf.map_fn(
            fn=lambda x: super(BcimgSequenceLoader, self).load(x, metadata, postprocess=postprocess, bbox=bbox),
            elems=files,
            fn_output_signature=(tf.float32, {'_image_file_shape': tf.int32}),
            parallel_iterations=16
        )
        _image_file_shape = meta["_image_file_shape"][0]
        return images, {"_image_file_shape": _image_file_shape, "_sequence_files": files}

