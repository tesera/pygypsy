"""Data Preparation

Calculates and joins parameters required for pygypsy to a plot table

"""
#pylint: disable=no-member
import logging
import pandas as pd
from copy import deepcopy

import basal_area_increment as incr
from pygypsy.stand_density_factor import (
    estimate_sdf_aw,
    estimate_sdf_sb,
    estimate_sdf_sw,
    estimate_sdf_pl,
)
from pygypsy.density import (
    estimate_density_aw,
    estimate_density_sw,
    estimate_density_sb,
    estimate_density_pl,
)
from utils import _log_loop_progress
from pygypsy.utils import estimate_species_composition
from pygypsy.asaCompileAgeGivenSpSiHt import (
    computeTreeAge,
    ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge,
    ComputeGypsySiteIndex,
)

# TODO: use pure functions or class instances to avoid mutating global state
# TODO: don't nest functions


LOGGER = logging.getLogger(__name__)

# TODO: use funct from site_index module
def get_species_site_indices(dominant_species, site_index):
    '''
    This function gets the site indices for all other species in a plot
    given the site indices of the dominant species of that plot
    '''
    if site_index > 0:
        if dominant_species == 'Aw':
            site_index_white_aspen = site_index
            site_index_pl = 0.85 * site_index_white_aspen + 3.4
            site_index_sw = 1.31 * site_index_white_aspen - 2.64
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_fb = 0.94 * site_index_pl + 0.71
            site_index_sb = 0.64 * site_index_pl + 2.76
            site_index_pb = site_index_white_aspen

        elif dominant_species == 'Sw':
            site_index_sw = site_index
            site_index_pl = 0.86 * site_index_sw + 2.13
            site_index_white_aspen = 0.76 * site_index_sw + 2.01
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_fb = 0.74 * site_index_sw + 4.75
            site_index_sb = 0.64 * site_index_pl + 2.76
            site_index_pb = site_index_white_aspen

        elif dominant_species == 'Fb':
            site_index_fb = site_index
            site_index_sw = 1.09 * site_index_fb - 1.83
            site_index_pl = 0.86 * site_index_sw + 2.13
            site_index_white_aspen = 0.76 * site_index_sw + 2.01
            site_index_fb = 0.74 * site_index_sw + 4.75
            site_index_sb = 0.64 * site_index_pl + 2.76
            site_index_pb = site_index_white_aspen

        elif dominant_species == 'Fd':
            site_index_fb = site_index
            site_index_pl = 1.07 * site_index_fb - 0.76
            site_index_white_aspen = 1.18 * site_index_pl  - 4.02
            site_index_sw = 1.36 * site_index_fb - 6.45
            site_index_pb = site_index_white_aspen
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_sb = 0.64 * site_index_pl + 2.76

        elif dominant_species == 'Pl':
            site_index_pl = site_index
            site_index_white_aspen = 1.18 * site_index_pl  - 4.02
            site_index_sw = 1.16 * site_index_pl - 2.47
            site_index_fb = 0.94* site_index_pl + 0.71
            site_index_pb = site_index_white_aspen
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_sb = 0.64 * site_index_pl + 2.76

        elif dominant_species == 'Pb':
            site_index_pb = site_index
            site_index_white_aspen = site_index_pb
            site_index_pl = 0.85 * site_index_white_aspen + 3.4
            site_index_sw = 1.31 * site_index_white_aspen -2.64
            site_index_fb = 0.92* site_index_pl + 1.68
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_sb = 0.64 * site_index_pl + 2.76

        elif dominant_species == 'Sb':
            site_index_sb = site_index
            site_index_pl = 1.57 * site_index_sb - 4.33
            site_index_sb = 0.64 * site_index_pl + 2.76
            site_index_fb = 0.92* site_index_pl + 1.68
            site_index_sw = 1.16 * site_index_pl - 2.47
            site_index_white_aspen = 1.18 * site_index_pl - 4.02
            site_index_pb = site_index_white_aspen


    return site_index_white_aspen, site_index_pl, site_index_sw, site_index_sb

# TODO: use func from site index modeule - move to utlls
def get_gypsy_valid_species(dominant_species):
    """Given the plot dominant species, get the gypsy species

    Pb is reassigned to Aw
    Fd or Fb are reassigned to Sw

    :param dominant_species:
    """
    if dominant_species == 'Pb':
        dominant_species = 'Aw'
    elif dominant_species in ['Fd', 'Fb']:
        dominant_species = 'Sw'

    return dominant_species

# TODO: use func from site index module
def dominant_species_site_index_estim(dominant_species,
                                      dominant_species_current_age,
                                      dominant_species_current_height):
    dom_si = ComputeGypsySiteIndex(
        dominant_species,
        dominant_species_current_height,
        0,
        dominant_species_current_age
    )
    site_index = dom_si[2]

    return site_index

# TODO: combine with funct from site_index module - move to utils
def generate_species_dict():
    """Create empty spcies dict

    Species dict has keys which are species.

    value are dicts with keys corresponding to parameter names and values
    corresponding to parameter values

    topHeight - top height
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
        'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0,
        'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7,
        'site_index': 0, 'PCT': 0
    }
    # plot properties for each species, starting with default values
    # defined above
    species_dict = {
        'Aw': deepcopy(default_species_params),
        'Pl': deepcopy(default_species_params),
        'Sw': deepcopy(default_species_params),
        'Sb': deepcopy(default_species_params),
    }

    return species_dict

def populate_species_dict_with_indices(species_dict, dominant_species,
                                       dominant_species_site_index,
                                       estimated_site_indices):
    """Fill the dictionary with estimated SIs

    Fill all the SIs to avoid IFs and loops. Some of them will not be
    used.

    :param species_dict: dictionary used to store params for all species
    :param dominant_species_site_index: site index for dominant species
    :param dominant_species: abbreviation, dominant species for
                             the plot
    :param estimated_site_indices: array of estimated site indices from
                                   get_species_site_indices function

    """
    local_species_dict = deepcopy(species_dict)

    if dominant_species == 'Aw':
        local_species_dict['Aw']['SI'] = dominant_species_site_index
        local_species_dict['Pl']['SI'] = estimated_site_indices[1]
        local_species_dict['Sw']['SI'] = estimated_site_indices[2]
        local_species_dict['Sb']['SI'] = estimated_site_indices[3]

    elif dominant_species == 'Sw':
        local_species_dict['Aw']['SI'] = estimated_site_indices[0]
        local_species_dict['Pl']['SI'] = estimated_site_indices[1]
        local_species_dict['Sw']['SI'] = dominant_species_site_index
        local_species_dict['Sb']['SI'] = estimated_site_indices[3]

    elif dominant_species == 'Pl':
        local_species_dict['Aw']['SI'] = estimated_site_indices[0]
        local_species_dict['Pl']['SI'] = dominant_species_site_index
        local_species_dict['Sw']['SI'] = estimated_site_indices[2]
        local_species_dict['Sb']['SI'] = estimated_site_indices[3]

    elif dominant_species == 'Sb':
        local_species_dict['Aw']['SI'] = estimated_site_indices[0]
        local_species_dict['Pl']['SI'] = estimated_site_indices[1]
        local_species_dict['Sw']['SI'] = estimated_site_indices[2]
        local_species_dict['Sb']['SI'] = dominant_species_site_index

    return local_species_dict


# TODO: split into 2 functions
def reclassify_and_sort_species(species_abbrev_perc_tuples_list):
    '''Classify all species in valid gypsy species and sort by percent

    re-classification of species that are not considered in pygypsy as one of
    the species considered in pygypsy (Aw, Sw, Sb, or Pl) and sort the species
    to obtain the dominant species in the plot

    '''
    species_perc_dict = {'Aw':0, 'Pl':0, 'Sw':0, 'Sb':0}
    for species_abbrev_perc_tup in species_abbrev_perc_tuples_list:
        species_abbrev = species_abbrev_perc_tup[0]
        species_perc = species_abbrev_perc_tup[1]

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


def populate_species_dict(partial_species_list,
                          sorted_species_abbrev_perc_tuples_list,
                          dominant_species=None, row=None,
                          dominant_species_current_age=None,
                          dominant_species_current_height=None):
    """Fill partial fplot

    Given fplot with proportion filled out, add age, top height, basal area,
    density

    :param partial_species_list:
    :param sorted_species_abbrev_perc_tuples_list:
    :param dominant_species:
    :param dominant_species_current_age:
    :param dominant_species_current_height:

    """
    species_dict = deepcopy(partial_species_list)
    outer_sorted_species_perc_list = sorted_species_abbrev_perc_tuples_list
    for species in outer_sorted_species_perc_list:
        # TODO: continue or raise, not break? if this is true, there's no species at all, I think
        if species[1] == 0:
            break
        # TODO: this is always true on first pass of the loop
        elif species[0] == dominant_species[0]:
            species_dict[species[0]]['tage'] = dominant_species_current_age
            species_dict[species[0]]['topHeight'] = dominant_species_current_height
            species_dict[species[0]]['N'] = row['TPH'] * species[1] / 100
            species_dict[species[0]]['BA'] = row['BPH'] * species[1] / 100
            x_si = ComputeGypsySiteIndex(
                species[0],
                species_dict[species[0]]['topHeight'],
                0,
                species_dict[species[0]]['tage']
            )
            species_dict[species[0]]['bhage'] = x_si[0]
            # if, after re-arranging the proportions, dom species is another
            # one then we need to re-estimate everything  even for the new
            # dominant species
        else:
            si_sp = species_dict[species[0]]['SI']
            species_dict[species[0]]['PCT'] = species[1]
            species_dict[species[0]]['tage'] = computeTreeAge(
                species[0],
                treeHt=dominant_species_current_height,
                treeSi=si_sp,
                maxTreeAge=450,
                rowIndex=0,
                printWarnings=True
            )
            # density based on the proportion of the species
            species_dict[species[0]]['N'] = row['TPH'] * species[1]/100
            # Basal area from the species proportion as well
            species_dict[species[0]]['BA'] = row['BPH'] * species[1]/100
            # calling the ComputeGypsySiteIndex function, estimate bhage
            x_si = ComputeGypsySiteIndex(
                species[0], dominant_species_current_height, 0,
                species_dict[species[0]]['tage']
            )
            species_dict[species[0]]['bhage'] = x_si[0]
    return species_dict


def prep_standtable(data):
    '''Define site_index of all other species given the dominant species

    The site index is only defined for the dominant species in a plot. This
    function uses the dominant species and its site index to estimate the site
    indices for other species. It estimates other values and returns a data
    frame of all of the values for all plots input.

    estimates site_index Dom from inventory Age and HD
    this site_index is used to estimate the site index of the other species
    for example:
    - FD is dom species take HD and Age
    - assume FD is Sw generate site_index for Sw
    - get the SW site_index
    - calculate the SIs for other species from the conversion formulas

    :param data: input data frame

    '''
    plot_dict = {}
    n_rows = data.shape[0]
    for i, row in data.iterrows():
        _log_loop_progress(i, n_rows)

        # from the row, compile a list of species abbreviation and percents
        species_abbrev_percent_list = [
            (row['SP1'], row['PCT1']),
            (row['SP2'], row['PCT2']),
            (row['SP3'], row['PCT3']),
            (row['SP4'], row['PCT4']),
            (row['SP5'], row['PCT5'])
        ]

        # validate species percents add to 100
        check_prop = sum(zip(*species_abbrev_percent_list)[1])
        if check_prop != 100:
            raise ValueError('Species proportions not correct: %s' % check_prop)

        # pull some key vaiables off the row
        plot_id = row['id_l1']
        plot_dominant_species = row['SP1']
        dominant_species_current_age = row['AGE']
        dominant_species_current_height = row['HD']

        site_index = dominant_species_site_index_estim(
            plot_dominant_species,
            dominant_species_current_age,
            dominant_species_current_height
        )

        temp_dominant_species = get_gypsy_valid_species(plot_dominant_species)

        # TODO: should this use plot dominant species instead of temp?
        gypsy_site_indices = get_species_site_indices(temp_dominant_species,
                                                      site_index)

        empty_species_dict = generate_species_dict()
        species_dict = populate_species_dict_with_indices(
            empty_species_dict,
            temp_dominant_species,
            site_index, gypsy_site_indices)

        outer_sorted_species_perc_list, outer_species_perc_dict = \
            reclassify_and_sort_species(species_abbrev_percent_list)

        species_dict['Aw']['PCT'] = outer_species_perc_dict['Aw']
        species_dict['Pl']['PCT'] = outer_species_perc_dict['Pl']
        species_dict['Sw']['PCT'] = outer_species_perc_dict['Sw']
        species_dict['Sb']['PCT'] = outer_species_perc_dict['Sb']

        dominant_species = outer_sorted_species_perc_list[0]

        species_dict = populate_species_dict(
            species_dict, outer_sorted_species_perc_list,
            dominant_species=dominant_species,
            row=row,
            dominant_species_current_age=dominant_species_current_age,
            dominant_species_current_height=dominant_species_current_height
        )

        density_aw = species_dict['Aw']['N']
        density_sw = species_dict['Sw']['N']
        density_pl = species_dict['Pl']['N']
        density_sb = species_dict['Sb']['N']

        tage_aw = species_dict['Aw']['tage']
        tage_sw = species_dict['Sw']['tage']
        tage_pl = species_dict['Pl']['tage']
        tage_sb = species_dict['Sb']['tage']

        bhage_aw = species_dict['Aw']['bhage']
        bhage_sw = species_dict['Sw']['bhage']
        bhage_pl = species_dict['Pl']['bhage']
        bhage_sb = species_dict['Sb']['bhage']

        y2bh_aw = tage_aw - bhage_aw
        y2bh_sw = tage_sw - bhage_sw
        y2bh_pl = tage_pl - bhage_pl
        y2bh_sb = tage_sb - bhage_sb

        site_index_aw = species_dict['Aw']['SI']
        site_index_sw = species_dict['Sw']['SI']
        site_index_pl = species_dict['Pl']['SI']
        site_index_sb = species_dict['Sb']['SI']

        basal_area_aw = species_dict['Aw']['BA']
        basal_area_sb = species_dict['Sb']['BA']
        basal_area_sw = species_dict['Sw']['BA']
        basal_area_pl = species_dict['Pl']['BA']

        # Top height for all species
        top_height_aw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            'Aw', site_index_aw, tage_aw
        )
        top_height_sb = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            'Sb', site_index_sb, tage_sb
        )
        top_height_pl = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            'Pl', site_index_pl, tage_pl
        )
        top_height_sw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            'Sw', site_index_sw, tage_sw
        )

        # stand desnity factor for all species
        y_aw = estimate_sdf_aw('Aw', site_index_aw, bhage_aw, density_aw)
        sdf_aw0 = y_aw[1]
        density_bh_aw = y_aw[0]

        y_sb = estimate_sdf_sb('Sb', site_index_sb, tage_sb, density_sb)
        sdf_sb0 = y_sb[1]
        density_bh_sb = y_sb[0]

        y_sw = estimate_sdf_sw('Sw', site_index_sw, tage_sw, sdf_aw0, density_sw)
        sdf_sw0 = y_sw[1]
        density_bh_sw = y_sw[0]

        y_pl = estimate_sdf_pl(
            'Pl', site_index_pl, tage_pl,
            sdf_aw0, sdf_sw0, sdf_sb0, density_pl
        )
        sdf_pl0 = y_pl[1]
        density_bh_pl = y_pl[0]

        # estimating species densities at time zero
        initial_density_aw = estimate_density_aw(sdf_aw0, 0, site_index_aw)
        initial_density_sb = estimate_density_sb(sdf_sb0, 0, site_index_sb)
        initial_density_sw = estimate_density_sw(
            sdf_sw0, sdf_aw0, 0, site_index_sw
        )
        initial_density_pl = estimate_density_pl(
            sdf_aw0, sdf_sw0, sdf_sb0, sdf_pl0, 0, site_index_pl
        )

        # estimating species-specific Basal area increment from Densities
        species_composition = estimate_species_composition(
            density_bh_aw, density_bh_sb, density_bh_sw, density_bh_pl
        )
        species_composition_aw = species_composition[0]
        species_composition_sw = species_composition[1]
        species_composition_sb = species_composition[2]
        species_composition_pl = species_composition[3]

        # TODO: are these increments used in simulation? can we remove
        basal_area_increment_aw = incr.increment_basal_area_aw(
            species_composition_aw, site_index_aw, density_bh_aw,
            initial_density_aw, bhage_aw, basal_area_aw
        )
        basal_area_increment_sb = incr.increment_basal_area_sb(
             species_composition_sb, site_index_sb, density_bh_sb,
            initial_density_sb, bhage_sb, basal_area_sb
        )
        basal_area_increment_sw = incr.increment_basal_area_sw(
            species_composition_sw, site_index_sw, density_bh_sw,
            initial_density_sw, bhage_sw, sdf_aw0, sdf_pl0,
            sdf_sb0, basal_area_sw
        )
        basal_area_increment_pl = incr.increment_basal_area_pl(
            species_composition_pl, site_index_pl, density_bh_pl,
            initial_density_pl, bhage_pl, sdf_aw0, sdf_sw0,
            sdf_sb0, basal_area_pl
        )

        plot_dict[plot_id] = {
            'SI_Aw': site_index_aw,
            'SI_Sw': site_index_sw,
            'SI_Pl': site_index_pl,
            'SI_Sb': site_index_sb,
            'N_Aw': density_aw,
            'N_Sw': density_sw,
            'N_Pl': density_pl,
            'N_Sb': density_sb,
            'y2bh_Aw': y2bh_aw,
            'y2bh_Sw': y2bh_sw,
            'y2bh_Pl': y2bh_pl,
            'y2bh_Sb': y2bh_sb,
            'tage_Aw': tage_aw,
            'tage_Sw': tage_sw,
            'tage_Pl': tage_pl,
            'tage_Sb': tage_sb,
            'BA_Aw': basal_area_aw,
            'BA_Sw': basal_area_sw,
            'BA_Pl': basal_area_pl,
            'BA_Sb': basal_area_sb,
            'BAinc_Aw': basal_area_increment_aw,
            'BAinc_Sw': basal_area_increment_sw,
            'BAinc_Pl': basal_area_increment_pl,
            'BAinc_Sb': basal_area_increment_sb,
            'SDF_Aw': sdf_aw0,
            'SDF_Sw': sdf_sw0,
            'SDF_Pl': sdf_pl0,
            'SDF_Sb': sdf_sb0,
            'N0_Aw': initial_density_aw,
            'N0_Sb': initial_density_sb,
            'N0_Sw': initial_density_sw,
            'N0_Pl': initial_density_pl,
            'StumpDOB_Aw': species_dict['Aw']['StumpDOB'],
            'StumpDOB_Sb': species_dict['Sb']['StumpDOB'],
            'StumpDOB_Sw': species_dict['Sw']['StumpDOB'],
            'StumpDOB_Pl': species_dict['Pl']['StumpDOB'],
            'StumpHeight_Aw': species_dict['Aw']['StumpHeight'],
            'StumpHeight_Sb': species_dict['Sb']['StumpHeight'],
            'Stumpheight_Sw': species_dict['Sw']['StumpHeight'],
            'StumpHeight_Pl': species_dict['Pl']['StumpHeight'],
            'TopDib_Aw': species_dict['Aw']['TopDib'],
            'TopDib_Sb': species_dict['Sb']['TopDib'],
            'TopDib_Sw': species_dict['Sw']['TopDib'],
            'TopDib_Pl': species_dict['Pl']['TopDib'],
            'topHeight_Aw': top_height_aw,
            'topHeight_Sw': top_height_sw,
            'topHeight_Sb': top_height_sb,
            'topHeight_Pl': top_height_pl
        }

        plot_df = pd.DataFrame(plot_dict)
        plot_df = plot_df.transpose()

    return plot_df
