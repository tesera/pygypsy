# -*- coding: utf-8 -*-
"""Functions for calculating site indices

"""
from collections import defaultdict


# TODO: reduce repetition
# - decorator for returns_all_site_indices
# - utility functions/class for <species>_from_<otherspecies>
# - make species stuff case insensitive


def get_site_indices_from_dominant_species(dominant_species=None,
                                           dominant_species_site_index=None):
    """Calculate site indices for non-dominant species

    Keyword Arguments:
    dominant_species            -- (default None)
    dominant_species_site_index -- (default None)

    """

    functs = {
        'aw': _get_all_site_indices_from_dominant_aw,
        'sw': _get_all_site_indices_from_dominant_sw,
        'fb': _get_all_site_indices_from_dominant_fb,
        'fd': _get_all_site_indices_from_dominant_fd,
        'pl': _get_all_site_indices_from_dominant_pl,
        'pb': _get_all_site_indices_from_dominant_pb,
    }

    try:
        all_site_indices = functs[dominant_species](dominant_species_site_index)
    except KeyError:
        raise ValueError('No function is available to calculate site index from '
                         'species %s' %dominant_species)

    species_subset = ('aw', 'pl', 'sw', 'sb')
    site_indices_subset = {
        species: all_site_indices[species] for species in species_subset
    }

    # NOTE: using a dict here so that contents are explicit/non-ambiguous
    return site_indices_subset


def _get_all_site_indices_from_dominant_aw(site_index_aw):
    """Keyword Arguments:
    site_index_aw -- site index for aw

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_pl = 0.85 * site_index_aw + 3.4
    site_index_sw = 1.31 * site_index_aw - 2.64
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_fd = 0.94 * site_index_pl + 0.71
    site_index_sb = 0.64 * site_index_pl + 2.76
    site_index_pb = site_index_aw

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_all_site_indices_from_dominant_sw(site_index_sw):
    """Keyword Arguments:
    site_index_sw -- site index for sw

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_pl = 0.86 * site_index_sw + 2.13
    site_index_aw = 0.76 * site_index_sw + 2.01
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_fd = 0.74 * site_index_sw + 4.75
    site_index_sb = 0.64 * site_index_pl + 2.76
    site_index_pb = site_index_aw

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict

def _get_all_site_indices_from_dominant_fb(site_index_fb):
    """Keyword Arguments:
    site_index_fb -- site index for fb

    Returns: dict: species as keys and site indices as corresponding values

    """
    site_index_sw = 1.09 * site_index_fb - 1.83
    site_index_pl = 0.86 * site_index_sw + 2.13
    site_index_aw = 0.76 * site_index_sw + 2.01
    site_index_fd = 0.74 * site_index_sw + 4.75
    site_index_sb = 0.64 * site_index_pl + 2.76
    site_index_pb = site_index_aw

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_all_site_indices_from_dominant_fd(site_index_fd):
    """Keyword Arguments:
    site_index_fd -- site index for fd

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_pl = 1.07 * site_index_fd - 0.76
    site_index_aw = 1.18 * site_index_pl  - 4.02
    site_index_sw = 1.36 * site_index_fd  - 6.45
    site_index_pb = site_index_aw
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_sb = 0.64 * site_index_pl + 2.76

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_all_site_indices_from_dominant_pl(site_index_pl):
    """Keyword Arguments:
    site_index_pl -- site index for pl

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_aw = 1.18 * site_index_pl  - 4.02
    site_index_sw = 1.16 * site_index_pl  - 2.47
    site_index_fd = 0.94* site_index_pl + 0.71
    site_index_pb = site_index_aw
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_sb = 0.64 * site_index_pl + 2.76


    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict

def _get_all_site_indices_from_dominant_pb(site_index_pb):
    """Keyword Arguments:
    site_index_pb -- site index for pb

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_aw = site_index_pb
    site_index_pl = 0.85 * site_index_aw + 3.4
    site_index_sw = 1.31 * site_index_aw - 2.64
    site_index_fd = 0.92 * site_index_pl + 1.68
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_sb = 0.64 * site_index_pl + 2.76

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_temporary_dominant_species(actual_dominant_species):
    """Swap an actual dominant species for a temporary one
    Keyword Arguments:
    actual_dominant_species -- str

    Returns:
    str: a temporary dominant species

    """
    if actual_dominant_species == 'Pb':
        temp_dominant_species= 'Aw'
    elif actual_dominant_species == 'Fd' or actual_dominant_species == 'Fb':
        temp_dominant_species= 'Sw'
    else:
        raise ValueError('There is no temporary dominant species for species %s' \
                         % actual_dominant_species)

    return temp_dominant_species


def _estimate_dominant_species_site_index(dominant_species, age, height):
    """Estimate site index of dominant species

    This is a wrapper around ComputeGypsySiteIndex for readability

    It assumes site_index = site_index at time?

    Keyword Arguments:
    dominant_species -- str, abbreviation of dominant species
    age              -- float, age of dominant species
    height           -- float, height of dominant species

    Return:
    float - site index

    """
    dominant_site_index_list = ComputeGypsySiteIndex(dominant_species,
                                                     height, 0, age)
    # TODO: use dictionary for return from Computegypsysiteindex - that way someone
    # knows clearly what domSI[2] means
    dominant_site_index = dominant_site_index_list[2]

    return dominant_site_index




def _generate_fplot_dict(dominant_species, dominant_species_site_index,
                         all_species_site_indices):
    """Generate 'fplot'

    Given a known dominant species and its site index, and estimation of all
    site indices, generates the 'fplot' dictionary

    Keyword Arguments:
    dominant_species            -- str, dominant species abbrev
    dominant_species_site_index -- float, dominant species site index
    all_species_site_indices    -- dict, site index of all species

    Return:
    dict - ???

    """
    def gen_template_dict():
        return {
            'topHeight': 0, 'tage': 0, 'bhage': 0,
            'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13,
            'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0
        }

    fplot_dict = defaultdict(gen_template_dict)

    fplot_dict['Aw']['SI'] = all_species_site_indices['pl']
    fplot_dict['Pl']['SI'] = all_species_site_indices['pl']
    fplot_dict['Sw']['SI'] = all_species_site_indices['sw']
    fplot_dict['Sb']['SI'] = all_species_site_indices['sb']
    # override the given dominant species with the given value
    fplot_dict[dominant_species]['SI'] = dominant_species_site_index

    return fplot_dict
