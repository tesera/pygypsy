""" Helper Functions
"""
import errno
import os


def _mkdir_p(path):
    """ Make directory recursively
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
