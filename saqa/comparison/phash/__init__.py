"""Differences of Perceptual Hashes
Computing the differences between perceptual hashes of the images."""

from PIL import Image
import imagehash
import os


def compare(original_fh, archived_fh):
    hash_size = 8
    original_phash = imagehash.phash(Image.open(original_fh.name), hash_size=hash_size)
    archived_phash = imagehash.phash(Image.open(archived_fh.name), hash_size=hash_size)

    return (1 - (original_phash - archived_phash ) / 2**hash_size, {
        "screenshots_path": os.path.dirname(original_fh.name),
        "original_screenshot": os.path.basename(original_fh.name),
        "archived_screenshot": os.path.basename(archived_fh.name)
    })
