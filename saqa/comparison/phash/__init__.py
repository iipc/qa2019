"""Differences of Perceptual Hashes
Computing the differences between perceptual hashes of the images."""

from PIL import Image
import imagehash


def compare(original_fh, archived_fh):
    hash_size = 8
    original_phash = imagehash.phash(Image.open(original_fh.name), hash_size=hash_size)
    archived_phash = imagehash.phash(Image.open(archived_fh.name), hash_size=hash_size)

    return (1 - (original_phash - archived_phash ) / 2**hash_size, None)
