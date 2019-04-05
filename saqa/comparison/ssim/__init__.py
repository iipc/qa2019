"""Structural Similarity (SSIM)
Computing the structural similarity of the images."""

from skimage.measure import compare_ssim
import imutils
import cv2
import os
from ..toolbox import cropping_images

def compare(original_fh, archived_fh):
    original = cv2.imread(original_fh.name)
    archived = cv2.imread(archived_fh.name)

    if original is not None and archived is not None:
        original_cropped, archived_cropped = cropping_images(original, archived)
        original_gray = cv2.cvtColor(original_cropped, cv2.COLOR_BGR2GRAY)
        archived_gray = cv2.cvtColor(archived_cropped, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(original_gray, archived_gray, full=True)
    return (score, {
        "screenshots_path": os.path.dirname(original_fh.name),
        "original_screenshot": os.path.basename(original_fh.name),
        "archived_screenshot": os.path.basename(archived_fh.name)
    })
