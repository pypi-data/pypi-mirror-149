import numpy as np
import pytest

from ovary_analysis.utils.image import pad_label_im, pad_im_to_min_size


def test_pad_label_im():
    raw_im = np.random.random((10, 20, 20))
    label_im = np.random.random((8, 20, 20)).astype(int)

    label_im_2 = pad_label_im(raw_im, label_im)
    assert label_im_2.shape == raw_im.shape


def test_pad_label_im_no_pad():
    raw_im_shape = (10, 20, 20)
    raw_im = np.random.random(raw_im_shape)
    label_im = np.random.random(raw_im_shape).astype(int)

    label_im_2 = pad_label_im(raw_im, label_im)
    assert label_im_2.shape == raw_im.shape
    assert label_im_2 is label_im


def test_pad_label_im_bad_shape():
    raw_im = np.random.random((10, 20, 20))
    label_im = np.random.random((20, 20, 20)).astype(int)

    with pytest.raises(AssertionError):
        _ = pad_label_im(raw_im, label_im)


def test_pad_image_min_size_no_pad():
    test_im = np.random.random((100, 80, 90))
    min_size = [80, 80, 80]

    padded_im = pad_im_to_min_size(test_im, min_size)

    assert padded_im is test_im
    np.testing.assert_array_equal(padded_im.shape, test_im.shape)


def test_pad_image():
    test_im = np.random.random((100, 60, 90))
    min_size = [80, 80, 80]

    padded_im = pad_im_to_min_size(test_im, min_size)

    np.testing.assert_array_equal(padded_im.shape, [100, 80, 90])
