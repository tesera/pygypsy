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
PLOT_DICT = {}


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


def prep_standtable(data):
    '''
    define site_index of all other species given the dominant species

    :param data:
    '''
    n_rows = data.shape[0]
    for i, row in data.iterrows():
        _log_loop_progress(i, n_rows)
        # top height, total age, BH age, N (or density), current Basal Area,
        # Measured Percent Stocking, StumpDOB, StumpHeight, TopDib, site_index,
        # Proportion of the species
        _default_species_fplot_dict = {
            'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0,
            'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7,
            'site_index': 0, 'PCT': 0
        }
        # plot properties for each species, starting with default values
        # defined above
        fplot = {
            'Aw': deepcopy(_default_species_fplot_dict),
            'Pl': deepcopy(_default_species_fplot_dict),
            'Sw': deepcopy(_default_species_fplot_dict),
            'Sb': deepcopy(_default_species_fplot_dict),
        }

        plot_id = row['id_l1']

        temporary_dominant_species = row['SP1']

        # TODO: pull these functions out of the outer function
        def initsite_index_estimation(temporary_dominant_species):
            if temporary_dominant_species == 'Pb':
                temporary_dominant_species = 'Aw'
            elif temporary_dominant_species in ['Fd', 'Fb']:
                temporary_dominant_species = 'Sw'
            return temporary_dominant_species

        # estimate site_index Dom from inventory Age and HD !!!!
        # Use this site_index to estimate the other species SIs
        # ex: FD is dom species take HD and Age, assume FD is Sw generate site_index for Sw
        # get the SW site_index
        # calculate the SIs for other species from the conversion formulas

        dominant_species_current_age = row['AGE']
        dominant_species_current_height = row['HD']


        def dominant_species_site_index_estim(
                temporary_dominant_species,
                dominant_species_current_age,
                dominant_species_current_height
            ):
            dom_si = ComputeGypsySiteIndex(
                temporary_dominant_species,
                dominant_species_current_height,
                0,
                dominant_species_current_age
            )
            site_index = dom_si[2]
            return site_index


        site_index = dominant_species_site_index_estim(
            temporary_dominant_species,
            dominant_species_current_age,
            dominant_species_current_height
        )
        dominant_species = initsite_index_estimation(temporary_dominant_species)
        site_index_x = get_species_site_indices(dominant_species, site_index)

        # TODO: this function uses variables from the enclosing scope
        # need to pass the variable into the function instead
        def get_other_species_site_index(site_index):
            """
            fill the dictionary with estimated SIs

            fill all the SIs to avoid IFs and loops. Some of them will not be used.

            :param site_index:
            """
            if dominant_species == 'Aw':
                fplot['Aw']['SI'] = site_index
                fplot['Pl']['SI'] = site_index_x[1]
                fplot['Sw']['SI'] = site_index_x[2]
                fplot['Sb']['SI'] = site_index_x[3]

            elif dominant_species == 'Sw':
                fplot['Aw']['SI'] = site_index_x[0]
                fplot['Pl']['SI'] = site_index_x[1]
                fplot['Sw']['SI'] = site_index
                fplot['Sb']['SI'] = site_index_x[3]

            elif dominant_species == 'Pl':
                fplot['Aw']['SI'] = site_index_x[0]
                fplot['Pl']['SI'] = site_index
                fplot['Sw']['SI'] = site_index_x[2]
                fplot['Sb']['SI'] = site_index_x[3]

            elif dominant_species == 'Sb':
                fplot['Aw']['SI'] = site_index_x[0]
                fplot['Pl']['SI'] = site_index_x[1]
                fplot['Sw']['SI'] = site_index_x[2]
                fplot['Sb']['SI'] = site_index

            return fplot

        fplot = get_other_species_site_index(site_index)

        sp1 = row['SP1']
        sp2 = row['SP2']
        sp3 = row['SP3']
        sp4 = row['SP4']
        sp5 = row['SP5']

        pct1 = row['PCT1']
        pct2 = row['PCT2']
        pct3 = row['PCT3']
        pct4 = row['PCT4']
        pct5 = row['PCT5']



        species_abbrev_percent_list = [
            (sp1, pct1), (sp2, pct2), (sp3, pct3), (sp4, pct4), (sp5, pct5)
        ]

        check_prop = sum(zip(*species_abbrev_percent_list)[1])
        if check_prop != 100:
            raise ValueError('Species proportions not correct: %s' % check_prop)

        # TODO: does species perc dict need to be an argument? if so
        # it should be immutable
        def sort_species(species_perc_list, species_perc_dict={'Aw':0, 'Pl':0, 'Sw':0, 'Sb':0}):
            '''
            re-classification of species that are not considered in pygypsy as
            one of the species considered in pygypsy (Aw, Sw, Sb, or Pl)
            and sort the species to obtain the dominant species in the plot
            '''
            for species in species_perc_list:
                if species[0] in ['Aw', 'Pb']:
                    species_perc_dict['Aw'] = species_perc_dict['Aw'] + species[1]

                elif species[0] in ['Sw', 'Fb', 'Fd']:
                    species_perc_dict['Sw'] = species_perc_dict['Sw'] + species[1]

                elif species[0] == 'Pl':
                    species_perc_dict['Pl'] = species_perc_dict['Pl'] + species[1]

                elif species[0] == 'Sb':
                    species_perc_dict['Sb'] = species_perc_dict['Sb'] + species[1]

            sorted_species_perc_list = [(k, v) for v, k in sorted(
                [(v, k) for k, v in species_perc_dict.items()]
            )]

            sorted_species_perc_list.reverse()

            check_prop1 = sum(species_perc_dict.values())
            if check_prop1 != 100:
                raise ValueError(
                    ('Species proportions after grouping '
                     'into 4 species is not correct: %s') % check_prop1
                )

            return sorted_species_perc_list, species_perc_dict

        outer_sorted_species_perc_list, outer_species_perc_dict = \
            sort_species(species_abbrev_percent_list)

        fplot['Aw']['PCT'] = outer_species_perc_dict['Aw']
        fplot['Pl']['PCT'] = outer_species_perc_dict['Pl']
        fplot['Sw']['PCT'] = outer_species_perc_dict['Sw']
        fplot['Sb']['PCT'] = outer_species_perc_dict['Sb']

        dominant_species = outer_sorted_species_perc_list[0]



        # iterate over each ranked species - populate the dictionary with
        # values estimated from the dominant species' site_index
        for species in outer_sorted_species_perc_list:

            if species[1] == 0:
                break
            elif species[0] == dominant_species[0]:
                fplot[species[0]]['tage'] = dominant_species_current_age
                fplot[species[0]]['topHeight'] = dominant_species_current_height
                fplot[species[0]]['N'] = row['TPH'] * species[1] / 100
                fplot[species[0]]['BA'] = row['BPH'] * species[1] / 100
                x_si = ComputeGypsySiteIndex(
                    species[0],
                    fplot[species[0]]['topHeight'],
                    0,
                    fplot[species[0]]['tage']
                )
                fplot[species[0]]['bhage'] = x_si[0]
                # if, after re-arranging the proportions, dom species is another
                # one then we need to re-estimate everything  even for the new
                # dominant species

            else:
                si_sp = fplot[species[0]]['SI']
                fplot[species[0]]['PCT'] = species[1]

                fplot[species[0]]['tage'] = computeTreeAge(
                    species[0],
                    treeHt=dominant_species_current_height,
                    treeSi=si_sp,
                    maxTreeAge=450,
                    rowIndex=0,
                    printWarnings=True
                )

                # density based on the proportion of the species
                fplot[species[0]]['N'] = row['TPH'] * species[1]/100

                # Basal area from the species proportion as well
                fplot[species[0]]['BA'] = row['BPH'] * species[1]/100

                # calling the ComputeGypsySiteIndex function, estimate bhage
                x_si = ComputeGypsySiteIndex(
                    species[0], dominant_species_current_height, 0,
                    fplot[species[0]]['tage']
                )
                fplot[species[0]]['bhage'] = x_si[0]


        # now we have different lists containing:
        # species, top height, total age, BHage (from the function),
        # N (or density), current Basal Area,  Measured Percent Stocking,
        # StumpDOB , StumpHeight, TopDib, site_index, species proportion
        site_index_white_aspen = fplot['Aw']['SI']
        site_index_sw = fplot['Sw']['SI']
        site_index_pl = fplot['Pl']['SI']
        site_index_sb = fplot['Sb']['SI']

        density_aw = fplot['Aw']['N']
        density_sw = fplot['Sw']['N']
        density_pl = fplot['Pl']['N']
        density_sb = fplot['Sb']['N']

        # TODO: sometimes these values are zero because TPH is zero
        # ...WHY TPH IS ZERO????
        y2bh_aw = fplot['Aw']['tage'] - fplot['Aw']['bhage']
        y2bh_sw = fplot['Sw']['tage'] - fplot['Sw']['bhage']
        y2bh_pl = fplot['Pl']['tage'] - fplot['Pl']['bhage']
        y2bh_sb = fplot['Sb']['tage'] - fplot['Sb']['bhage']

        # y2bh CANNOT BE NEGATIVE

        tage_aw = fplot['Aw']['tage']
        tage_sw = fplot['Sw']['tage']
        tage_pl = fplot['Pl']['tage']
        tage_sb = fplot['Sb']['tage']

        #print tage_sw



        sp_aw = [
            'Aw',
            fplot['Aw']['topHeight'],
            fplot['Aw']['tage'],
            fplot['Aw']['bhage'],
            fplot['Aw']['N'],
            fplot['Aw']['BA'],
            fplot['Aw']['PS'],
            fplot['Aw']['StumpDOB'],
            fplot['Aw']['StumpHeight'],
            fplot['Aw']['TopDib'],
            fplot['Aw']['SI'],
            fplot['Aw']['PCT']
        ]
        sp_pl = [
            'Pl',
            fplot['Pl']['topHeight'],
            fplot['Pl']['tage'],
            fplot['Pl']['bhage'],
            fplot['Pl']['N'],
            fplot['Pl']['BA'],
            fplot['Pl']['PS'],
            fplot['Pl']['StumpDOB'],
            fplot['Pl']['StumpHeight'],
            fplot['Pl']['TopDib'],
            fplot['Pl']['SI'],
            fplot['Pl']['PCT']
        ]
        sp_sw = [
            'Sw',
            fplot['Sw']['topHeight'],
            fplot['Sw']['tage'],
            fplot['Sw']['bhage'],
            fplot['Sw']['N'],
            fplot['Sw']['BA'],
            fplot['Sw']['PS'],
            fplot['Sw']['StumpDOB'],
            fplot['Sw']['StumpHeight'],
            fplot['Sw']['TopDib'],
            fplot['Sw']['SI'],
            fplot['Sw']['PCT']
        ]
        sp_sb = [
            'Sb',
            fplot['Sb']['topHeight'],
            fplot['Sb']['tage'],
            fplot['Sb']['bhage'],
            fplot['Sb']['N'],
            fplot['Sb']['BA'],
            fplot['Sb']['PS'],
            fplot['Sb']['StumpDOB'],
            fplot['Sb']['StumpHeight'],
            fplot['Sb']['TopDib'],
            fplot['Sb']['SI'],
            fplot['Sb']['PCT']
        ]

        bhage_aw = sp_aw[3]
        tage_aw = sp_aw[2]
        site_index_white_aspen = sp_aw[10]
        y2bh_aw = tage_aw - bhage_aw
        site_index_bh_aw = sp_aw[10]
        # treeHeight is the Top Height or Htop in the paper
        top_height_aw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_aw[0], site_index_white_aspen, tage_aw
        )

        bhage_sb = sp_sb[3]
        tage_sb = sp_sb[2]
        si_sb = sp_sb[10]
        site_index_bh_sb = sp_sb[10]
        top_height_sb = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_sb[0], si_sb, tage_sb
        )

        bhage_pl = sp_pl[3]
        tage_pl = sp_pl[2]
        si_pl = sp_pl[10]
        y2bh_pl = tage_pl - bhage_pl
        site_index_bh_pl = sp_pl[10]
        top_height_pl = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_pl[0], si_pl, tage_pl
        )

        bhage_sw = sp_sw[3]
        tage_sw = sp_sw[2]
        si_sw = sp_sw[10]
        y2bh_sw = tage_sw - bhage_sw
        site_index_bh_sw = sp_sw[10]
        top_height_sw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_sw[0], si_sw, tage_sw
        )

        # si, bhage, and tage are passed on from the above.
        # sdfs estimated iteratively
        # using N from the original input sp_aw etc as the input (density_aw) etc
        # I think it is suposed to be the density of the species at the bhage = 0, although
        # the paper says current or inital density
        density_aw = sp_aw[4]
        density_sb = sp_sb[4]
        density_sw = sp_sw[4]
        density_pl = sp_pl[4]

        y_aw = estimate_sdf_aw(sp_aw, site_index_bh_aw, bhage_aw, density_aw)
        sdf_aw0 = y_aw[1]
        density_bh_aw = y_aw[0]

        y_sb = estimate_sdf_sb(sp_sb, site_index_bh_sb, tage_sb, density_sb)
        sdf_sb0 = y_sb[1]
        density_bh_sb = y_sb[0]

        y_sw = estimate_sdf_sw(sp_sw, site_index_bh_sw, tage_sw, sdf_aw0, density_sw)
        sdf_sw0 = y_sw[1]
        density_bh_sw = y_sw[0]

        y_pl = estimate_sdf_pl(
            sp_pl, site_index_bh_pl, tage_pl,
            sdf_aw0, sdf_sw0, sdf_sb0, density_pl
        )
        sdf_pl0 = y_pl[1]
        density_bh_pl = y_pl[0]

        # estimating species densities at time zero
        initial_density_aw = estimate_density_aw(sdf_aw0, 0, site_index_bh_aw)
        initial_density_sb = estimate_density_sb(sdf_sb0, 0, site_index_bh_sb)
        initial_density_sw = estimate_density_sw(sdf_sw0, sdf_aw0, 0, site_index_bh_sw)
        initial_density_pl = estimate_density_pl(
            sdf_aw0, sdf_sw0, sdf_sb0, sdf_pl0, 0, site_index_bh_pl
        )

        # estimating species-specific Basal area increment from Densities
        species_composition = estimate_species_composition(density_bh_aw, density_bh_sb, density_bh_sw, density_bh_pl)

        species_composition_aw = species_composition[0]
        species_composition_sw = species_composition[1]
        species_composition_sb = species_composition[2]
        species_composition_pl = species_composition[3]

        basal_area_aw = sp_aw[5]
        basal_area_sb = sp_sb[5]
        basal_area_sw = sp_sw[5]
        basal_area_pl = sp_pl[5]

        basal_area_increment_aw = incr.increment_basal_area_aw(
            sp_aw, species_composition_aw, site_index_bh_aw, density_bh_aw,
            initial_density_aw, bhage_aw, basal_area_aw
        )
        basal_area_increment_sb = incr.increment_basal_area_sb(
            sp_sb, species_composition_sb, site_index_bh_sb, density_bh_sb,
            initial_density_sb, bhage_sb, basal_area_sb
        )
        basal_area_increment_sw = incr.increment_basal_area_sw(
            sp_sw, species_composition_sw, site_index_bh_sw, density_bh_sw,
            initial_density_sw, bhage_sw, sdf_aw0, sdf_pl0, sdf_sb0, basal_area_sw
        )
        basal_area_increment_pl = incr.increment_basal_area_pl(
            sp_pl, species_composition_pl, site_index_bh_pl, density_bh_pl,
            initial_density_pl, bhage_pl, sdf_aw0, sdf_sw0, sdf_sb0, basal_area_pl
        )

        stump_dob_aw = sp_aw[7]
        stump_height_aw = sp_aw[8]
        top_dib_aw = sp_aw[9]

        stump_dob_sb = sp_sb[7]
        stump_height_sb = sp_sb[8]
        top_dib_sb = sp_sb[9]

        stump_dob_sw = sp_sw[7]
        stump_height_sw = sp_sw[8]
        top_dib_sw = sp_sw[9]

        stump_dob_pl = sp_pl[7]
        stump_height_pl = sp_pl[8]
        top_dib_pl = sp_pl[9]

        PLOT_DICT[plot_id] = {
            'id_l1': plot_id,
            'SI_Aw': site_index_white_aspen,
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
            'StumpDOB_Aw': stump_dob_aw,
            'StumpDOB_Sb': stump_dob_sb,
            'StumpDOB_Sw': stump_dob_sw,
            'StumpDOB_Pl': stump_dob_pl,
            'StumpHeight_Aw': stump_height_aw,
            'StumpHeight_Sb': stump_height_sb,
            'Stumpheight_Sw': stump_height_sw,
            'StumpHeight_Pl': stump_height_pl,
            'TopDib_Aw': top_dib_aw,
            'TopDib_Sb': top_dib_sb,
            'TopDib_Sw': top_dib_sw,
            'TopDib_Pl': top_dib_pl,
            'topHeight_Aw': top_height_aw,
            'topHeight_Sw': top_height_sw,
            'topHeight_Sb': top_height_sb,
            'topHeight_Pl': top_height_pl
        }

        plot_df = pd.DataFrame(PLOT_DICT)
        plot_df = plot_df.transpose()

    return plot_df
