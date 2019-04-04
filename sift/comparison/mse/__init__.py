"""Mean Squared Error
Computing the mean squared error of the images."""

from skimage import io
import numpy as np
from ..toolbox import cropping_images


def compare(original_fname, archived_fname):
    """Calculates the mean square error of the two given images

    Parameters
    ----------
    current_image_name : str
        The current website screenshot file path.
    archive_image_name : str
        The archive website screenshot file path.

    Returns
    -------
    mse_noise : float
        The mean squared error value.

    References
    ----------
    .. [1]  https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

    """

    current_image = io.imread(original_fname)
    archive_image = io.imread(archived_fname)
    (current_image_cropped, archive_image_cropped) = cropping_images(current_image, archive_image)

    mse_noise = np.sum((current_image_cropped.astype("float") - archive_image_cropped.astype("float")) ** 2)
    mse_noise /= float(current_image_cropped.shape[0] * current_image_cropped.shape[1])

    return (mse_noise, None)
