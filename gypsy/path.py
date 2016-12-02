"""Path utility"""
import os


def _join(*args):
    """Join path elements locally or for s3

    For s3, we need a utility to join paths that will always use '/'. For local
    operations, need the platform specific path separator.

    :param args: path elements
    """
    if args[0].lower() == ('s3://'):
        path = '%s%s' % (
            args[0],
            '/'.join(args[1:]) # what if first element is
            )
    elif args[0].lower().startswith('s3://'):
        path = '/'.join(args)
    else:
        path = os.path.join(*args)

    return path
