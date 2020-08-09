"""Various functions used by objects in the project in order to either prepare
the coordinates of the drawing and no-drawing area and to control the experiment
based on location of mouse clicks.
"""

import time
import pickle
import typing
import numpy as np
from skimage.util import img_as_ubyte
import cv2
import params


def segment_areas(
        img_ar: np.ndarray,
        img_pos: tuple,
        img_size: tuple) -> typing.Tuple[np.ndarray, np.ndarray]:
    """Takes the image array, image position and size extracts the outlines
    and the shape of the body.

    Parameters
    ----------
    img_ar
        A Height*Width*RGBA of the reference image to parse. Assuming image
        read by scikit-image for compatibility.
    img_size
        The X and Y values of image size (in pixels).
    img_pos
        The X and Y values of image position (in pixels).

    Returns
    -------
    shape
        Array of pixel coordinates matching the 'inline' of the body,
        normalized to xy locations centered on 0, ranging from -1/2 to
        1/2 of monitor size.
    shape_outlines
        Identical to 'shape' returned argument, but coordinates indicate
        position of shape outlines.
    """

    # Convert image from skimage format to OpenCV
    img_ar = img_as_ubyte(img_ar)
    # Reverse on the inner most axes, RGBA>>ABGR
    img_ar = img_ar[:, :, ::-1]
    # We can lose the ALPHA channel now
    img_ar = cv2.cvtColor(img_ar, cv2.COLOR_RGBA2RGB)
    # Convert image to grayscale
    gray = cv2.cvtColor(img_ar, cv2.COLOR_RGB2GRAY)
    # Create a black and white image out of the grayscale
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    # Find contours based on the B&W image
    contours, _ = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Assign the contours back into the image, drawn as colored thin lines
    img_ar = cv2.drawContours(
        img_ar, contours, -1, params.CONTOUR_COLOR, 1)

    # Grab the pixels matching the contours colors, to be used as borders
    shape_outlines = np.array(
        np.where(np.all(img_ar[:, :, :] == params.CONTOUR_COLOR, 2))).T
    # Contours include a rectangular frame around the image itself,
    # so we need to clip it
    shape_outlines = shape_outlines[(
        (params.CLIPPING_SIZE < shape_outlines[:, 0]) & (
            shape_outlines[:, 0] < shape_outlines[:, 0].max()
            - params.CLIPPING_SIZE))]
    shape_outlines = shape_outlines[(
        (params.CLIPPING_SIZE < shape_outlines[:, 1]) & (
            shape_outlines[:, 1] < shape_outlines[:, 1].max()
            - params.CLIPPING_SIZE))]

    # Depending on the size to which we resize the images, the mean value of
    # non-contour pixels may be changed from almost white to greyer.
    # Therefore we need to take a lenient value - ~230 to ~240 (out of 255).
    shape = np.array(
        np.where(img_ar[:, :, :].mean(axis=2) > 235)).T

    # Flip the shapes sideways, as we previously pivoted it.
    shape_outlines = np.fliplr(shape_outlines)
    shape = np.fliplr(shape)

    for a in [shape, shape_outlines]:
        # Center on X-axis
        a[:, 0] = a[:, 0] + (img_pos[0] - img_size[0] // 2)
        # Center on Y-axis
        a[:, 1] = a[:, 1] + (img_pos[1] - img_size[1] // 2)

    return shape, shape_outlines


def get_in_radius_pixels(point: tuple, radius: int) -> np.ndarray:
    """Get an array of the xy locations of pixels that are within radial
    distance from a specific location.

    Parameters
    ----------
    point
        The xy coordinates of a pixel.
    radius
        The radius (in pixels) of the imaginary circe surrounding the point.

    Returns
    -------
        np.array of the pixels within radius distance from the point.
        Normalized to match the location of the point, rather than the
        center of the screen.
    -------

    """
    # Construct the array of pixels which may be effected
    x_val, y_val = np.mgrid[-radius: radius + 1: 1, -radius: radius + 1: 1]
    # The mask will be used to filter out the pixels further than
    # the radius around the center.
    mask = x_val * x_val + y_val * y_val <= radius * radius
    # Construct an array of DiameterXDiameter pixels
    in_radius_ar = np.vstack((x_val.flatten(), y_val.flatten())).T.reshape(
        (radius * 2 + 1, radius * 2 + 1, 2))
    # Return the pixels within radius distance, plus an offset so we test
    # the relevant location rather than center of the screen
    return in_radius_ar[mask] + np.array(point)


def test_if_point_in_area(point, a) -> bool:
    """Test whether both X and Y are inside the region of interest.

    Parameters
    ----------
    point
        xy coordinates of pixel.
    a
        np.ndarray of the shape (x, 2), containing the xy locations of pixels
        in the region of interest.
    Returns
    -------
    bool
        Returns the maximal match value as boolean. True means that at least
        one xy pair in a matches the point on both x an y. False means that
        no xy to xy match was found.
    """
    return (np.equal(point, a).sum(1) == 2).max().astype(bool)


def test_xy_proximity(point: np.ndarray, a: np.ndarray) -> bool:
    """Test whether both X and Y are inside the region of interest.

    Parameters
    ----------
    point
        xy coordinates of pixel.
    a
        np.ndarray of the shape (x, 2), containing the xy locations of pixels
        in the region of interest.
    Returns
    -------
    int
        Maximum 'match' (1) would mean that both x and y are inside
        the region of interest. If no match occurs, then output is 0.
    """
    cur_dists = np.abs(a - np.array(point))
    return (cur_dists < params.DOT_RADIUS).all(axis=1).any()
