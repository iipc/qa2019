"""Sum of Absolute Difference
Computing the sum of absolute difference of the images."""

from skimage import io
import cv2
from ..toolbox import cropping_images
from PIL import Image


def compare(original_fh, archived_fh):
    # source: https://rosettacode.org/wiki/Percentage_difference_between_images#Python
    """Calculates the vector difference score of the two given images

    Parameters
    ----------
    current_image_name : str
        The current website screenshot file path.
    archive_image_name : str
        The archive website screenshot file path.

    Returns
    -------
    vec_score : float
        The vector difference score.

    References
    ----------
    .. [1] https://rosettacode.org/wiki/Percentage_difference_between_images#Python

    """
    current_image = io.imread(original_fh.name)
    archive_image = io.imread(archived_fh.name)
    (current_image_cropped, archive_image_cropped) = cropping_images(current_image, archive_image)
    current_image = cv2.cvtColor(current_image_cropped, cv2.COLOR_BGR2RGB)
    current_image = Image.fromarray(current_image)
    archive_image = cv2.cvtColor(archive_image_cropped, cv2.COLOR_BGR2RGB)
    archive_image = Image.fromarray(archive_image)
    assert current_image.mode == archive_image.mode, "Different kinds of images."
    assert current_image.size == archive_image.size, "Different sizes."

    pairs = zip(current_image.getdata(), archive_image.getdata())
    if len(current_image.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = current_image.size[0] * current_image.size[1] * 3

    vec_score = 100 - ((dif / 255.0 * 100) / ncomponents)  # convert to percentage match

    return (vec_score, None)
