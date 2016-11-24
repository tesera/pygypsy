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


def estimate_species_composition(n_aw, n_sb, n_sw, n_pl):
    '''Calculates species composition based on their densities

    :param float N_Aw, N_Sb, N_Sw, and N_Pl: densities of the respective species

    '''
    n_total = n_aw + n_sb + n_sw + n_pl

    if n_total == 0:
        sc_aw = 0
        sc_sw = 0
        sc_sb = 0
        sc_pl = 0
    else:
        sc_aw = n_aw/n_total
        sc_sw = n_sw/n_total
        sc_sb = n_sb/n_total
        sc_pl = n_pl/n_total

    return sc_aw, sc_sw, sc_sb, sc_pl

def _filter_young_stands(prepped_plot_table, min_age=25):
    old_query_str = ('tage_Sw > {a} '
                     'or tage_Sb > {a} '
                     'or tage_Pl > {a} '
                     'or tage_Aw > {a}').format(a=min_age)
    old_ids = prepped_plot_table.query(old_query_str).index
    prepped_plot_table_old = prepped_plot_table[
        prepped_plot_table.index.isin(old_ids)
    ]
    prepped_plot_table_young = prepped_plot_table[
        ~prepped_plot_table.index.isin(old_ids)
    ]

    return prepped_plot_table_old, prepped_plot_table_young
