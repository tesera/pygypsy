"""Data Preparation

Calculates and joins parameters required for pygypsy to a plot table

"""
#pylint: disable=no-member
import logging
import pandas as pd
from copy import deepcopy

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
from pygypsy.site_index import (
    get_site_indices_from_dominant_species,
    _estimate_site_index
)
from pygypsy.utils import (
    _get_gypsy_valid_species,
    _log_loop_progress,
    _generate_fplot_dict,
    _reclassify_and_sort_species,
)
from pygypsy.asaCompileAgeGivenSpSiHt import (
    computeTreeAge,
    ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge,
    ComputeGypsySiteIndex,
)


LOGGER = logging.getLogger(__name__)


def _populate_species_dict_with_indices(species_dict, estimated_site_indices):
    """Fill the dictionary with estimated SIs

    Fill all the SIs to avoid IFs and loops. Some of them will not be
    used.

    :param species_dict: dictionary used to store params for all species
    :param estimated_site_indices: array of estimated site indices from
                                   get_species_site_indices function

    ..note: the dominant species in the estiamted_site_indices uses its
    observed site index

    """
    local_species_dict = deepcopy(species_dict)

    for species, site_index in estimated_site_indices.items():
        local_species_dict[species]['SI'] = site_index

    return local_species_dict


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
        # TODO: raise NoDominantSpeciesError and catch it where called instead of break
        # confirmed with julianno
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

        site_index = _estimate_site_index(
            plot_dominant_species,
            dominant_species_current_age,
            dominant_species_current_height
        )

        temp_dominant_species = _get_gypsy_valid_species(plot_dominant_species)
        gypsy_site_indices = get_site_indices_from_dominant_species(
            temp_dominant_species,
            site_index
        )
        empty_species_dict = _generate_fplot_dict()
        species_dict = _populate_species_dict_with_indices(empty_species_dict,
                                                           gypsy_site_indices)

        outer_sorted_species_perc_list, outer_species_perc_dict = \
            _reclassify_and_sort_species(species_abbrev_percent_list)

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
