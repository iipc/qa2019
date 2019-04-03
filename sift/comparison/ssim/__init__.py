from skimage.measure import compare_ssim
import imutils
import cv2


def compare(original_fname, archived_fname):
    original = cv2.imread(original_fname)
    archived = cv2.imread(archived_fname)

    if original is not None and archived is not None:
        o_width, o_height = original.shape[:2]
        a_width, a_height = archived.shape[:2]
        f_width = min(o_width, a_width)
        f_height = min(o_height, a_height)
        original_cropped = original[0:f_width, 0:f_height]
        archived_cropped = archived[0:f_width, 0:f_height]
        original_gray = cv2.cvtColor(original_cropped, cv2.COLOR_BGR2GRAY)
        archived_gray = cv2.cvtColor(archived_cropped, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(original_gray, archived_gray, full=True)
    return score
