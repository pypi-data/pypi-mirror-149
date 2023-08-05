#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import io

from datarobot.enums import (
    DEFAULT_VISUAL_AI_IMAGE_FORMAT,
    DEFAULT_VISUAL_AI_IMAGE_QUALITY,
    DEFAULT_VISUAL_AI_IMAGE_RESAMPLE_METHOD,
    DEFAULT_VISUAL_AI_IMAGE_SIZE,
    DEFAULT_VISUAL_AI_IMAGE_SUBSAMPLING,
    DEFAULT_VISUAL_AI_SHOULD_RESIZE,
    SUPPORTED_IMAGE_FORMATS,
)

try:
    from PIL import Image
except ImportError:
    msg = (
        "Image transformation operations require installation of datarobot library, "
        "with optional `images` dependency. To install library with image support"
        "please use `pip install datarobot[images]`"
    )
    raise ImportError(msg)


class ImageOptions(object):
    """
    Image options class. Class holds image options related to image resizing and image reformatting.

    should_resize: bool
        Whether input image should be resized to new dimensions.
    image_size: Tuple[int, int]
        New image size (width, height). When both values (width, height) are specified and have
        positive values, than image resize operation will resize image to explicitly specified
        image format. This resize operation does not preserve image aspect ratio. If user would
        like to preserve image aspect ratio of original image than dimensions should be passed
        with only one dimension specified.
        For example:
          - value (200,) or (200,-1) will preserve aspect ratio and will resize to width=200
          - value (,200) or (-1,200) will preserve aspect ratio and will resize to height=200
    image_format: enums.ImageFormat | str
        What image format will be used to save result image after transformations. For example
        (ImageFormat.JPEG, ImageFormat.PNG). Values supported are in line with values supported
        by DataRobot. If no format is specified by passing `None` value original image format
        will be preserved.
    resample_method: enum.ImageResampleMethod
        What resampling method should be used when resizing image.
    """

    def __init__(
        self,
        should_resize=DEFAULT_VISUAL_AI_SHOULD_RESIZE,
        image_size=DEFAULT_VISUAL_AI_IMAGE_SIZE,
        image_format=DEFAULT_VISUAL_AI_IMAGE_FORMAT,
        image_quality=DEFAULT_VISUAL_AI_IMAGE_QUALITY,
        image_subsampling=DEFAULT_VISUAL_AI_IMAGE_SUBSAMPLING,
        resample_method=DEFAULT_VISUAL_AI_IMAGE_RESAMPLE_METHOD,
    ):
        self.should_resize = should_resize
        self.image_size = image_size
        self.resample_method = resample_method
        self.image_quality = image_quality
        self.image_format = image_format
        self.image_quality = image_quality
        self.image_subsampling = image_subsampling
        self._validate()

    def _validate(self):
        if self.should_resize is None:
            raise ValueError("Image transformation requires value `should_resize` parameter.")
        elif self.should_resize is True:
            if not self.image_size:
                raise ValueError("When resizing image `image_size` value is required.")
        if self.image_format and self.image_format not in SUPPORTED_IMAGE_FORMATS:
            raise ValueError(
                "Invalid image_format value. Please specify `None` "
                "to preserve current image format or one of supported "
                "image formats: {}".format(SUPPORTED_IMAGE_FORMATS)
            )


def get_bytes_from_image(
    image,
    image_format,
    image_quality=DEFAULT_VISUAL_AI_IMAGE_QUALITY,
    image_subsampling=DEFAULT_VISUAL_AI_IMAGE_SUBSAMPLING,
):
    """
    Save PIL image with in specified format and with specified options and return image image_bytes.

    Parameters
    ----------
    image: PIL.Image
        Image object instance
    image_quality: int
        Image quality when saving (supported by some image formats i.e. JPEG)
    image_subsampling: int
        Image subsampling when saving
    image_format: str
        PIL compatibile image format (i.e. PNG, JPEG) for full list of supported
        image types please refer to Pillow library documentation.

    Returns
    -------
    image_bytes representing Image
    """
    params = {}
    if image_quality is not None:
        params["quality"] = image_quality
    if image_subsampling is not None:
        params["subsampling"] = image_subsampling
    if image:
        bytes = io.BytesIO()
        image.save(fp=bytes, format=image_format, **params)
        return bytes.getvalue()
    return None


def get_image_from_bytes(image_bytes):
    """
    Create PIL Image instance using input bytes.

    Parameters
    ----------
    image_bytes: bytes | BytesIO
        Image in a form of bytes.

    Returns
    -------
    PIL.Image instance
    """
    if image_bytes:
        if isinstance(image_bytes, bytes):
            image_bytes = io.BytesIO(image_bytes)
        image = Image.open(image_bytes)
        return image
    return None


def get_resized_image_dimensions(org_size, image_size):
    """
    Calculate image dimensions using original_size and ImageOptions.

    Parameters
    ----------
    org_size: Tuple[int, int]
        Tuple representing image dimenstions (width, height)
    image_size: Tuple[int, int]
        New image size (width, height). When both values (width, height) are specified and have
        positive values, than image resize operation will resize image to explicitly specified
        image format. This resize operation does not preserve image aspect ratio. If user would
        like to preserve image aspect ratio of original image than dimensions should be passed
        with only one dimension specified.

        For example:
          - value (200,) or (200,-1) will preserve aspect ratio and will resize to width=200
          - value (None,200) or (-1,200) will preserve aspect ratio and will resize to height=200

    Returns
    -------
    Tuple[int, int] calculated dimensions representing (width, height)
    """
    new_width, new_height = image_size
    # keep only positive dimension values and treat zeros and negative numbers as missing values
    new_width = new_width if new_width and new_width > 0 else None
    new_height = new_height if new_height and new_height > 0 else None

    # if both dimensions are specified resize as user requested without aspect_ratio recalculation
    if new_width and new_height:
        return image_size
    # if both dimensions are missing we cannot recalculate target image dimensions
    if not new_width and not new_height:
        raise ValueError("At least one resize dimension is required")

    # if only one of dimensions is missing we `keep_aspect_ratio` of original and recalculate
    # missing dimension based on original image aspect ratio based on other dimension value
    org_width, org_height = org_size
    org_aspect_ratio = 1.0 * org_width / org_height
    if new_width:
        new_height = int(new_width / org_aspect_ratio)
    else:
        new_width = int(new_height * org_aspect_ratio)

    # return new image dimensions after recalculation using aspect_ratio
    return new_width, new_height


def format_image_bytes(image_bytes, image_options):
    """
    Format input image image_bytes and return reformatted image also in a form of image_bytes.

    Parameters
    ----------
    image_bytes: bytes
        Image in a form of image_bytes
    image_options : ImageOptions
        Class holding image formatting and image resize parameters

    Returns
    -------
    Image in a form of image_bytes
    """
    image = get_image_from_bytes(image_bytes)

    # if input image matches requested target parameters, do not recompute and return input
    if (
        image.width,
        image.height,
    ) == image_options.image_size and image.format == image_options.image_format:
        return image_bytes

    # Preserve image format if image_format is None
    if not image_options.image_format:
        image_options.image_format = image.format

    # if image should be resized calculate new image size and resize original image
    if image_options.should_resize:
        new_image_size = get_resized_image_dimensions(
            org_size=(image.width, image.height), image_size=image_options.image_size
        )
        image = image.resize(size=new_image_size, resample=image_options.resample_method)

    # convert to target image format and return as image_bytes
    return get_bytes_from_image(
        image=image,
        image_format=image_options.image_format,
        image_quality=image_options.image_quality,
        image_subsampling=image_options.image_subsampling,
    )
