"""Functions for calculating site indices

"""
from pygypsy.asaCompileAgeGivenSpSiHt import (
    ComputeGypsySiteIndex,
)


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
    dominant_species = dominant_species.lower()
    try:
        all_site_indices = functs[dominant_species](dominant_species_site_index)
    except KeyError:
        raise ValueError('No function is available to calculate site index from '
                         'species %s' %dominant_species)

    species_subset = ('Aw', 'Pl', 'Sw', 'Sb')
    site_indices_subset = {
        species: all_site_indices[species.lower()] for species in species_subset
    }

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


def _estimate_site_index(species, age, height):
    """Estimate site index of dominant species

    This is a wrapper around ComputeGypsySiteIndex for readability

    Keyword Arguments:
    species -- str, abbreviation of dominant species
    age     -- float, age of dominant species
    height  -- float, height of dominant species

    Return:
    float - site index

    """
    dominant_site_index_list = ComputeGypsySiteIndex(species,
                                                     height, 0, age)
    dominant_site_index = dominant_site_index_list[2]

    return dominant_site_index
