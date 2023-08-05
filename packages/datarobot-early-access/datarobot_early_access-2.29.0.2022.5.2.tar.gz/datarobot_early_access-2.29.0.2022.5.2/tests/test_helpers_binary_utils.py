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
import base64
from io import BytesIO
import time

from PIL import Image
import mock
import numpy as np
import pandas as pd
import pytest
import responses
import six

from datarobot.enums import ImageFormat
from datarobot.errors import ContentRetrievalTerminatedError
from datarobot.helpers.binary_data_utils import (
    get_bytes_for_path,
    get_bytes_for_url,
    get_encoded_file_contents_from_paths,
    get_encoded_file_contents_from_urls,
    get_encoded_image_contents_from_paths,
    get_encoded_image_contents_from_urls,
)
from datarobot.helpers.image_utils import format_image_bytes, ImageOptions

COLLECTION_TYPES_TEST_CASES = [
    pytest.param("image_urls", id="list"),
    pytest.param("images_urls_numpy_1d_arr", id="numpy_array"),
    pytest.param("images_urls_pandas_dataframe_column", id="dataframe_column"),
    pytest.param("images_urls_pandas_series", id="pandas_series"),
]

IMAGE_FORMAT_TEST_CASES = ImageFormat.ALL

FILE_CONTENT_METHODS = [
    get_encoded_file_contents_from_urls,
    get_encoded_file_contents_from_paths,
]

IMAGE_CONTENT_METHODS = [
    get_encoded_image_contents_from_urls,
    get_encoded_image_contents_from_paths,
]

GET_CONTENTS_ALL_METHODS = FILE_CONTENT_METHODS + IMAGE_CONTENT_METHODS


def get_image_bytes_helper(im_size, format="PNG", mode="RGB"):
    byte_arr = BytesIO()
    image = Image.new(mode=mode, size=im_size)
    image.format = format
    image.save(byte_arr, format=format)
    return byte_arr.getvalue()


@pytest.fixture(scope="session", params=COLLECTION_TYPES_TEST_CASES)
def all_collection_types(request):
    fixture = request.param
    return request.getfixturevalue(fixture)


@pytest.fixture(scope="session")
def image_urls():
    return [
        "http://datarobot.com/foo.jpg",
        "https://datarobot.com/bar.png",
        "http://datarobot.com/baz.jpeg",
    ]


@pytest.fixture(scope="session")
def image_sizes():
    return [(10, 10), (15, 30), (45, 15)]


@pytest.fixture(scope="session")
def image_data(image_sizes):
    return [get_image_bytes_helper(size) for size in image_sizes]


@pytest.fixture(scope="session")
def images_base64(image_data):
    return [base64.b64encode(image).decode("utf-8") for image in image_data]


@pytest.fixture(scope="session")
def images(image_data, image_urls):
    return {url: data for url, data in zip(image_urls, image_data)}


@pytest.fixture(scope="session")
def images_urls_numpy_1d_arr(image_urls):
    return np.array(image_urls, dtype=str)


@pytest.fixture(scope="session")
def images_urls_pandas_dataframe_column(image_urls):
    df = pd.DataFrame([[url, None] for url in image_urls], columns=["image_urls", "other_col"])
    return df["image_urls"]


@pytest.fixture(scope="session")
def mock_get_bytes_switcher(images):
    def get_data(location, *args, **kwargs):
        return images[location]

    with mock.patch("datarobot.helpers.binary_data_utils.get_bytes_switcher") as m:
        m.__getitem__.return_value = mock.MagicMock(wraps=get_data)
        yield m


@pytest.fixture(scope="session")
def mock_get_bytes_switched_out_of_order(images, image_urls):

    # return first after 0.5s, second after 0.1s, third instantly
    return_waits = [0.5, 0.1, 0]
    delayed_return_mock = DelayedBytesRetrieveMock(
        lookup=images, waits={key: wait for key, wait in zip(image_urls, return_waits)},
    )

    with mock.patch("datarobot.helpers.binary_data_utils.get_bytes_switcher") as m:
        m.__getitem__.return_value = mock.MagicMock(wraps=delayed_return_mock)
        yield m


@pytest.fixture(scope="session")
def images_urls_pandas_series(image_urls):
    return pd.Series(image_urls)


class DelayedBytesRetrieveMock:
    """Returns value after specified wait time for resource."""

    def __init__(self, lookup, waits=None):
        self.value_lookup = lookup
        self.wait_lookup = waits or {}

    def __call__(self, key, *args, **kwargs):
        value = self.value_lookup[key]
        wait = self.wait_lookup.get(key, 0)
        if wait:
            time.sleep(wait)
        return value


@pytest.fixture
def open_mock_path():
    return "{}.open".format("__builtin__" if six.PY2 else "builtins")


@pytest.mark.parametrize("method", FILE_CONTENT_METHODS)
def test__base64_conversion_for_file_methods__no_transformations(
    method, image_data, all_collection_types, mock_get_bytes_switcher, images_base64
):
    actual_results = method(all_collection_types)
    assert actual_results == images_base64


@pytest.mark.parametrize("method", IMAGE_CONTENT_METHODS)
def test__base64_conversion_for_image_methods__no_transformations(
    method, image_data, all_collection_types, mock_get_bytes_switcher, images_base64
):
    # prepare image options that will make no transformations to original images
    # this way we should receive base64 values that should match these for org images
    image_options = ImageOptions(should_resize=False, image_format="PNG")
    actual_results = method(all_collection_types, image_options=image_options)
    assert actual_results == images_base64


@pytest.mark.parametrize("method", GET_CONTENTS_ALL_METHODS)
@pytest.mark.parametrize("threads", [1, 4])
def test__get_encoded_image__does_methods_keep_order(
    method, threads, image_urls, mock_get_bytes_switcher
):
    results_ordered = method(image_urls, n_threads=threads)
    results_reversed = method(list(reversed(image_urls)), n_threads=threads)
    assert results_ordered == list(reversed(results_reversed))


@pytest.mark.parametrize("method", FILE_CONTENT_METHODS)
def test_multithread__preserves_order_with_unordered_returns__file_methods(
    method, image_urls, mock_get_bytes_switched_out_of_order, images_base64
):
    """
    Given ordered list of file locations
    When processing using multiple threads and threads return out of order
    Then we should preserve original locations order on return
    """
    actual_result = method(image_urls, n_threads=3)
    assert images_base64 == actual_result


@pytest.mark.parametrize("method", IMAGE_CONTENT_METHODS)
def test_multithread__preserves_order_with_unordered_returns__image_methods(
    method, image_urls, mock_get_bytes_switched_out_of_order, images_base64
):
    """
    Given ordered list of image locations
    When processing using multiple threads and threads return out of order
    Then we should preserve original locations order on return
    """
    # prepare image options that will make no transformations to original images
    # this way we should receive base64 values that should match these for org images
    image_options = ImageOptions(should_resize=False, image_format="PNG")
    actual_result = method(image_urls, image_options=image_options, n_threads=3)
    assert actual_result == images_base64


@pytest.mark.parametrize(
    ["im_size_original", "im_size_requested"], [[(50, 50), (40, 40)], [(40, 60), (20, 30)]]
)
@pytest.mark.parametrize("should_resize", [True, False])
@pytest.mark.parametrize("image_format", IMAGE_FORMAT_TEST_CASES)
def test_format_image_bytes__triggered_by_should_resize(
    im_size_original, im_size_requested, should_resize, image_format
):
    original_image = get_image_bytes_helper(im_size_original)
    output_image_bytes = format_image_bytes(
        image_bytes=original_image,
        image_options=ImageOptions(
            should_resize=should_resize, image_size=im_size_requested, image_format=image_format
        ),
    )

    # inspect output image dimensions
    output_image = Image.open(BytesIO(output_image_bytes))
    actual_size = (output_image.width, output_image.height)

    if should_resize:
        # when resize takes place dimensions should match requested
        actual_size == im_size_requested
    else:
        # when no resize takes place dimensions should remain unchanged
        actual_size == im_size_original


@pytest.mark.parametrize(
    ["im_size_original", "im_size_requested", "im_size_expected"],
    [
        [(50, 50), (40, 40), (40, 40)],  # width = height
        [(30, 60), (35, 35), (35, 35)],  # width < height
        [(60, 30), (25, 25), (25, 25)],  # width > height
    ],
)
@pytest.mark.parametrize("image_format", IMAGE_FORMAT_TEST_CASES)
def test_format_image_bytes__no__keep_aspect_ratio(
    im_size_original, im_size_expected, im_size_requested, image_format
):
    original_image = get_image_bytes_helper(im_size_original, format=image_format)
    resized_image_bytes = format_image_bytes(
        image_bytes=original_image,
        image_options=ImageOptions(
            should_resize=True, image_size=im_size_requested, image_format=image_format
        ),
    )

    # inspect output image dimensions
    resized_image = Image.open(BytesIO(resized_image_bytes))
    actual_size = (resized_image.width, resized_image.height)
    assert im_size_requested == actual_size


@pytest.mark.parametrize(
    "image_format",
    [
        ImageFormat.JPEG,
        ImageFormat.TIFF,
        ImageFormat.GIF,
        ImageFormat.PPM,
        ImageFormat.BMP,
        ImageFormat.PNG,
    ],
)
def test_format_image_bytes__input_matches_output__when_no_transformation_needed(image_format):
    input_image_bytes = get_image_bytes_helper(im_size=(16, 16), format=image_format)
    output_image_bytes = format_image_bytes(
        image_bytes=input_image_bytes,
        image_options=ImageOptions(
            should_resize=True, image_size=(16, 16), image_format=image_format
        ),
    )
    assert bytearray(input_image_bytes) == bytearray(output_image_bytes)


@pytest.mark.parametrize(
    ["im_size_original", "im_size_requested", "im_size_expected"],
    [
        # width = height
        [(50, 50), (None, 40), (40, 40)],
        [(50, 50), (-1, 40), (40, 40)],
        [(50, 50), (40, None), (40, 40)],
        [(50, 50), (40, -1), (40, 40)],
        # width < height
        [(40, 60), (None, 30), (20, 30)],
        [(40, 60), (-1, 30), (20, 30)],
        [(40, 60), (30, None), (30, 45)],
        [(40, 60), (30, -1), (30, 45)],
        # width > height
        [(60, 40), (None, 30), (45, 30)],
        [(60, 40), (-1, 30), (45, 30)],
        [(60, 40), (30, None), (30, 20)],
        [(60, 40), (30, -1), (30, 20)],
    ],
)
@pytest.mark.parametrize("image_format", IMAGE_FORMAT_TEST_CASES)
def test_format_image_bytes__keep_aspect_ratio(
    im_size_original, im_size_expected, im_size_requested, image_format
):
    original_image = get_image_bytes_helper(im_size_original, format=image_format)
    resized_image_bytes = format_image_bytes(
        image_bytes=original_image,
        image_options=ImageOptions(
            should_resize=True, image_size=im_size_requested, image_format=image_format
        ),
    )

    # inspect output image dimensions
    resized_image = Image.open(BytesIO(resized_image_bytes))
    actual_size = (resized_image.width, resized_image.height)
    assert im_size_expected == actual_size


@responses.activate
def test_get_file_contents_from_path__expected_data_valid(image_urls, image_data):
    test_image_url = image_urls[0]
    test_image_data = image_data[0]

    responses.add(
        responses.GET,
        url=test_image_url,
        status=200,
        content_type="image/png",
        body=test_image_data,
    )
    result = get_bytes_for_url(location=test_image_url, headers={})

    # check if expected image contents is equal to BytesIO buffer value
    assert bytearray(test_image_data) == bytearray(result)


@responses.activate
def test_get_file_contents_from_path__data_and_expected_headers_valid(image_urls):
    test_image_url = image_urls[0]

    responses.add(responses.GET, url=test_image_url, status=200, content_type="image/png")

    test_header_user_agent = "TestUserAgent"
    test_header_accepts = "TestAccepts"
    test_headers = {"User-Agent": test_header_user_agent, "Accept": test_header_accepts}

    get_bytes_for_url(location=test_image_url, headers=test_headers)

    # check if headers passed to method were forwarded to http call
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_image_url
    assert responses.calls[0].request.headers["User-Agent"] == test_header_user_agent
    assert responses.calls[0].request.headers["Accept"] == test_header_accepts


@responses.activate
@pytest.mark.parametrize("status_code", [403, 404, 500])
def test_get_bytes_for_url__throws_ex__when_no_continue_on_error(status_code, image_urls):
    test_image_url = image_urls[0]
    responses.add(responses.GET, url=test_image_url, status=status_code, content_type="image/png")
    with pytest.raises(ContentRetrievalTerminatedError):
        get_bytes_for_url(location=test_image_url)


@responses.activate
@pytest.mark.parametrize("status_code", [403, 404, 500])
def test_get_bytes_for_url__dont_throw_ex__when_is_continue_on_error(status_code, image_urls):
    test_image_url = image_urls[0]
    responses.add(
        responses.GET, url=test_image_url, status=status_code, content_type="image/png",
    )
    content_bytes = get_bytes_for_url(location=test_image_url, continue_on_error=True)
    assert content_bytes is None


def test_get_file_contents_from_path(open_mock_path, image_data):
    test_image_data = image_data[0]
    test_image_path = "/some/path/foo.png"

    mock_open_func = mock.mock_open(read_data=test_image_data)
    with mock.patch(open_mock_path, mock_open_func):
        result = get_bytes_for_path(test_image_path)

    assert bytearray(test_image_data) == bytearray(result)


def test_get_file_contents_from_path__raises_ex__when_no_continue_on_error(
    open_mock_path, image_data
):
    test_image_data = image_data[0]
    test_image_path = "/some/path/foo.png"

    mock_open_func = mock.mock_open(read_data=test_image_data)
    mock_open_func.side_effect = OSError
    with mock.patch(open_mock_path, mock_open_func):
        with pytest.raises(ContentRetrievalTerminatedError):
            get_bytes_for_path(test_image_path)


def test_get_file_contents_from_url__dont_throw_ex__when_is_continue_on_error(
    open_mock_path, image_data
):
    test_image_data = image_data[0]
    test_image_path = "/some/path/foo.png"

    mock_open_func = mock.mock_open(read_data=test_image_data)
    mock_open_func.side_effect = OSError
    with mock.patch(open_mock_path, mock_open_func):
        content_bytes = get_bytes_for_path(test_image_path, continue_on_error=True)
        assert content_bytes is None
