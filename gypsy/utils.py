""" Helper Functions
"""
from __future__ import division

import os
import errno
import logging

from log import CONSOLE_LOGGER_NAME


CONSOLE_LOGGER = logging.getLogger(CONSOLE_LOGGER_NAME)


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

def _log_loop_progress(i, length, n_reports=10):
    step = int(length/n_reports) if length > 10 else 1
    log_steps = range(0, length, step)

    if i in log_steps:
        progress = i/length*100
        CONSOLE_LOGGER.info('%.0f%% complete', progress)

