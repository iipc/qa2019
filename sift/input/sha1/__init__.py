from hashlib import sha1
import os


def fetch(url, **kwargs):
    basename = sha1(url.encode()).hexdigest()
    local_path = kwargs.get('local_path', '')
    return_fname = ''
    if kwargs.get('archived', False):
        return_fname = basename + '-archived.jpeg'
    else:
        return_fname = basename + '.jpeg'

    return open(os.path.join(local_path, return_fname), 'r')
