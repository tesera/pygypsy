""" Helper Functions
"""
from __future__ import division

import os
import errno
import shutil
import logging
from urlparse import urlparse
from copy import deepcopy

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


def _append_file(source, dest):
    with open(dest, 'wb') as dfd:
        with open(source, 'rb') as sfd:
            shutil.copyfileobj(sfd, dfd)


def _parse_s3_url(url):
    s3_bucket, s3_prefix = None, None

    if url.startswith('s3://'):
        outdir_url = urlparse(url)
        s3_bucket = outdir_url.netloc
        s3_prefix = outdir_url.path.strip('/')

    return {
        'bucket': s3_bucket,
        'prefix': s3_prefix,
    }


def _copy_file_to_s3(bucket_conn, source, dest):
    bucket_conn.upload_file(source, dest)


def _copy_file(source, dest, bucket_conn=None):
    if bucket_conn is None:
        shutil.copyfile(source, dest)
    else:
        _copy_file_to_s3(bucket_conn, source, dest)


def _generate_fplot_dict():
    """Generate 'fplot'

    Given a known dominant species and its site index, and estimation of all
    site indices, generates the 'fplot' dictionary

    Return:
    dict - ???

    ..note: topHeight - top height
    tage - total age
    bhage - breast height age
    N - density
    BA - current Basal Area
    PS - Measured Percent Stocking
    StumpDOB - stump diameter outside bark
    StumpHeight - stump height
    TopDib - top diameter inside bark
    site_index - site index
    PCT - species proportion in plot

    """
    default_species_params = {
        'topHeight': 0, 'tage': 0, 'bhage': 0,
        'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13,
        'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0
    }
    species = ('Aw', 'Pl', 'Sw', 'Sb')
    fplot_dict = {}

    for s in species:
        fplot_dict[s] = deepcopy(default_species_params)

    return fplot_dict


def _get_gypsy_valid_species(dominant_species):
    """Given the plot dominant species, get the gypsy species

    The dominant species in a plot may not be one of the species in the GYPSY
    model. Douglas Fir for example is not in the GYPSY model, and it is
    appropriate to substitute it with White Spruce.

    :param str dominant_species: abbreviation of plot dominant species
    """
    if dominant_species == 'Pb':
        dominant_species = 'Aw'
    elif dominant_species in ['Fd', 'Fb']:
        dominant_species = 'Sw'

    return dominant_species


def _reclassify_and_sort_species(species_abbrev_perc):
    '''Classify all species in valid gypsy species and sort by percent

    re-classification of species that are not considered in pygypsy as one of
    the species considered in pygypsy (Aw, Sw, Sb, or Pl) and sort the species
    to obtain the dominant species in the plot

    :param list species_abbrev_perc: list of tuples where each element is a
    species abbreviation followed by its percentage

    '''
    species_perc_dict = {'Aw':0, 'Pl':0, 'Sw':0, 'Sb':0}

    for tup in species_abbrev_perc:
        species_abbrev = tup[0]
        species_perc = tup[1]

        if species_abbrev in ['Aw', 'Pb']:
            species_perc_dict['Aw'] = species_perc_dict['Aw'] + species_perc

        elif species_abbrev in ['Sw', 'Fb', 'Fd']:
            species_perc_dict['Sw'] = species_perc_dict['Sw'] + species_perc

        elif species_abbrev == 'Pl':
            species_perc_dict['Pl'] = species_perc_dict['Pl'] + species_perc

        elif species_abbrev == 'Sb':
            species_perc_dict['Sb'] = species_perc_dict['Sb'] + species_perc

    sorted_species_perc_list = [(k, v) for v, k in sorted(
        [(v, k) for k, v in species_perc_dict.items()]
    )]
    sorted_species_perc_list.reverse()

    check_prop1 = sum(species_perc_dict.values())
    if check_prop1 != 100:
        raise ValueError(('Species proportions after grouping '
                          'into 4 species is not correct: %s') % check_prop1)

    return sorted_species_perc_list, species_perc_dict


