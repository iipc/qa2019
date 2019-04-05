"""Handling input generated by using SHA1 of URL in the filename of screenshots."""

from hashlib import sha1
import os


def fetch(url, **kwargs):
    basename = sha1(url.encode()).hexdigest()
    local_path = kwargs.get('local_path', '')
    result_fname = ''
    if kwargs.get('archived', False):
        result_fname = basename + '-archived.jpeg'
    else:
        result_fname = basename + '.jpeg'

    return open(os.path.join(local_path, result_fname), 'r')