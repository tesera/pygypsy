# -*- coding: utf-8 -*-
""" Data Preparation
"""
import pandas as pd
from copy import deepcopy
from asaCompileAgeGivenSpSiHt import (computeTreeAge,
                                      ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge,
                                      ComputeGypsySiteIndex)

from GYPSYNonSpatial import (densityNonSpatialAw,
                             densityNonSpatialSb,
                             densityNonSpatialSw,
                             densityNonSpatialPl,
                             densityAw,
                             densitySw,
                             densitySb,
                             densityPl,
                             BasalAreaIncrementNonSpatialAw,
                             BasalAreaIncrementNonSpatialSw,
                             BasalAreaIncrementNonSpatialPl,
                             BasalAreaIncrementNonSpatialSb,
                             SCestimate)


# TODO: replace acronyms with something more verbose
# TODO: use pure functions or class instances to avoid mutating global state
# TODO: formal docstrings so we can generate nice documentation
# TODO: more subroutines and wrapper functions for easier readability


PLOT_DICT = {}


def get_species_site_indices(dominant_species, site_index):
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

        if dominant_species == 'Fd':
            site_index_fb = site_index
            site_index_pl = 1.07 * site_index_fb - 0.76
            site_index_white_aspen = 1.18 * site_index_pl  - 4.02
            site_index_sw = 1.36 * site_index_fb  - 6.45
            site_index_pb = site_index_white_aspen
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_sb = 0.64 * site_index_pl + 2.76

        if dominant_species == 'Pl':
            site_index_pl = site_index
            site_index_white_aspen = 1.18 * site_index_pl  - 4.02
            site_index_sw = 1.16 * site_index_pl  - 2.47
            site_index_fb = 0.94* site_index_pl + 0.71
            site_index_pb = site_index_white_aspen
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_sb = 0.64 * site_index_pl + 2.76

        if dominant_species == 'Pb':
            site_index_pb = site_index
            site_index_white_aspen = site_index_pb
            site_index_pl = 0.85 * site_index_white_aspen + 3.4
            site_index_sw = 1.31 * site_index_white_aspen -2.64
            site_index_fb = 0.92* site_index_pl + 1.68
            site_index_fb = 0.92 * site_index_sw + 1.68
            site_index_sb = 0.64 * site_index_pl + 2.76

    return site_index_white_aspen, site_index_pl, site_index_sw, site_index_sb



def dataPrepGypsy(data):
    ''' define site_index of all other species given the dominant species

    :param data:
    '''
    dominant_species = 'Aw'
    site_index = 1
    get_species_site_indices(dominant_species, site_index)

    for _, row in data.iterrows():

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


        def dominant_species_site_index_estim(temporary_dominant_species, dominant_species_current_age, dominant_species_current_height):
            dom_si = ComputeGypsySiteIndex(temporary_dominant_species, dominant_species_current_height, 0, dominant_species_current_age)
            site_index = dom_si[2]
            # using site_index = site_index_t , site index based on total age
            # from the ComputeGypsySiteIndex function
            return site_index


        site_index = dominant_species_site_index_estim(temporary_dominant_species, dominant_species_current_age, dominant_species_current_height)
        dominant_species = initsite_index_estimation(temporary_dominant_species)
        site_index_x = get_species_site_indices(dominant_species, site_index)

        # TODO: this function uses variables from the enclosing scope
        # need to pass the variable into the function instead
        def get_other_species_site_index(site_index):
            """fill the dictionary with estimated SIs

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

        outer_sorted_species_perc_list, outer_species_perc_dict = sort_species(species_abbrev_percent_list)

        fplot['Aw']['PCT'] = outer_species_perc_dict['Aw']
        fplot['Pl']['PCT'] = outer_species_perc_dict['Pl']
        fplot['Sw']['PCT'] = outer_species_perc_dict['Sw']
        fplot['Sb']['PCT'] = outer_species_perc_dict['Sb']

        dominant_species =outer_sorted_species_perc_list[0]



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
                x_Si = ComputeGypsySiteIndex(
                    species[0],
                    fplot[species[0]]['topHeight'],
                    0,
                    fplot[species[0]]['tage']
                )
                fplot[species[0]]['bhage'] = x_Si[0]
                # if, after re-arranging the proportions, dom species is another
                # one then we need to re-estimate everything  even for the new
                # dominant species

            else:
                siSp = fplot[species[0]]['SI']
                fplot[species[0]]['PCT'] = species[1]
                # estimate tree age iteratively calling computeTreeAge function
                # and inputing site_index in the place ot treeSi and dominant_species_current_height as
                # treeHT or topheight'''

                fplot[species[0]]['tage'] = computeTreeAge(
                    species[0],
                    treeHt=dominant_species_current_height,
                    treeSi=siSp,
                    maxTreeAge=450,
                    rowIndex=0,
                    printWarnings=True
                )

                # density based on the proportion of the species
                fplot[species[0]]['N'] = row['TPH'] * species[1]/100

                # Basal area from the species proportion as well
                fplot[species[0]]['BA'] = row['BPH'] * species[1]/100

                # calling the ComputeGypsySiteIndex function, estimate bhage
                x_Si = ComputeGypsySiteIndex(
                    species[0], dominant_species_current_height, 0,
                    fplot[species[0]]['tage']
                )
                fplot[species[0]]['bhage'] = x_Si[0]


        # now we have different lists containing:
        # species, top height, total age, BHage (from the function),
        # N (or density), current Basal Area,  Measured Percent Stocking,
        # StumpDOB , StumpHeight, TopDib, site_index, species proportion
        site_index_white_aspen = fplot['Aw']['SI']
        site_index_sw = fplot['Sw']['SI']
        site_index_pl = fplot['Pl']['SI']
        site_index_sb = fplot['Sb']['SI']

        N_Aw = fplot['Aw']['N']
        N_sw = fplot['Sw']['N']
        N_pl = fplot['Pl']['N']
        N_sb = fplot['Sb']['N']

        # TODO: sometimes these values are zero because TPH is zero
        # ...WHY TPH IS ZERO????
        y2bh_Aw = fplot['Aw']['tage'] - fplot['Aw']['bhage']
        y2bh_sw = fplot['Sw']['tage'] - fplot['Sw']['bhage']
        y2bh_pl = fplot['Pl']['tage'] - fplot['Pl']['bhage']
        y2bh_sb = fplot['Sb']['tage'] - fplot['Sb']['bhage']

        # y2bh CANNOT BE NEGATIVE

        tage_Aw = fplot['Aw']['tage']
        tage_sw = fplot['Sw']['tage']
        tage_pl = fplot['Pl']['tage']
        tage_sb = fplot['Sb']['tage']

        #print tage_sw



        sp_Aw = ['Aw', fplot['Aw']['topHeight'], fplot['Aw']['tage'], fplot['Aw']['bhage'], fplot['Aw']['N'], fplot['Aw']['BA'], fplot['Aw']['PS'], fplot['Aw']['StumpDOB'], fplot['Aw']['StumpHeight'], fplot['Aw']['TopDib'], fplot['Aw']['SI'], fplot['Aw']['PCT']]
        sp_pl = ['Pl', fplot['Pl']['topHeight'], fplot['Pl']['tage'], fplot['Pl']['bhage'], fplot['Pl']['N'], fplot['Pl']['BA'], fplot['Pl']['PS'], fplot['Pl']['StumpDOB'], fplot['Pl']['StumpHeight'], fplot['Pl']['TopDib'], fplot['Pl']['SI'], fplot['Pl']['PCT']]
        sp_sw = ['Sw', fplot['Sw']['topHeight'], fplot['Sw']['tage'], fplot['Sw']['bhage'], fplot['Sw']['N'], fplot['Sw']['BA'], fplot['Sw']['PS'], fplot['Sw']['StumpDOB'], fplot['Sw']['StumpHeight'], fplot['Sw']['TopDib'], fplot['Sw']['SI'], fplot['Sw']['PCT']]
        sp_sb = ['Sb', fplot['Sb']['topHeight'], fplot['Sb']['tage'], fplot['Sb']['bhage'], fplot['Sb']['N'], fplot['Sb']['BA'], fplot['Sb']['PS'], fplot['Sb']['StumpDOB'], fplot['Sb']['StumpHeight'], fplot['Sb']['TopDib'], fplot['Sb']['SI'], fplot['Sb']['PCT']]

        bhage_Aw = sp_Aw[3]
        tage_Aw = sp_Aw[2]
        site_index_white_aspen = sp_Aw[10]
        y2bh_Aw = tage_Aw - bhage_Aw
        site_index_bh_Aw = sp_Aw[10]
        # treeHeight is the Top Height or Htop in the paper
        topHeight_Aw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_Aw[0], site_index_white_aspen, tage_Aw
        )

        bhage_sb = sp_sb[3]
        tage_sb = sp_sb[2]
        si_sb = sp_sb[10]
        site_index_bh_sb = sp_sb[10]
        topHeight_sb = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_sb[0], si_sb, tage_sb
        )

        bhage_pl = sp_pl[3]
        tage_pl = sp_pl[2]
        si_pl = sp_pl[10]
        y2bh_pl = tage_pl - bhage_pl
        site_index_bh_pl = sp_pl[10]
        topHeight_pl = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_pl[0], si_pl, tage_pl
        )

        bhage_sw = sp_sw[3]
        tage_sw = sp_sw[2]
        si_sw = sp_sw[10]
        y2bh_sw = tage_sw - bhage_sw
        site_index_bh_sw = sp_sw[10]
        topHeight_sw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_sw[0], si_sw, tage_sw
        )

        # si, bhage, and tage are passed on from the above.
        # SDFs estimated iteratively
        # using N from the original input sp_Aw etc as the input (N_Aw) etc
        # I think it is suposed to be the density of the species at the bhage = 0, although
        # the paper says current or inital density
        N_Aw = sp_Aw[4]
        N_sb = sp_sb[4]
        N_sw = sp_sw[4]
        N_pl = sp_pl[4]

        y_Aw = densityNonSpatialAw(sp_Aw, site_index_bh_Aw, bhage_Aw, N_Aw)
        SDF_Aw0 = y_Aw[1]
        N_bh_Aw = y_Aw[0]

        y_sb = densityNonSpatialSb(sp_sb, site_index_bh_sb, tage_sb, N_sb)
        SDF_sb0 = y_sb[1]
        N_bh_sb = y_sb[0]

        y_sw = densityNonSpatialSw(sp_sw, site_index_bh_sw, tage_sw, SDF_Aw0, N_sw)
        SDF_sw0 = y_sw[1]
        N_bh_sw = y_sw[0]

        y_pl = densityNonSpatialPl(sp_pl, site_index_bh_pl, tage_pl, SDF_Aw0, SDF_sw0, SDF_sb0, N_pl)
        SDF_pl0 = y_pl[1]
        N_bh_pl = y_pl[0]

        # estimating species densities at time zero
        N0_Aw = densityAw(SDF_Aw0, 0, site_index_bh_Aw)
        N0_sb = densitySb(SDF_sb0, 0, site_index_bh_sb)
        N0_sw = densitySw(SDF_sw0, SDF_Aw0, 0, site_index_bh_sw)
        N0_pl = densityPl(SDF_Aw0, SDF_sw0, SDF_sb0, SDF_pl0, 0, site_index_bh_pl)

        # estimating species-specific Basal area increment from Densities
        SC = SCestimate(N_bh_Aw, N_bh_sb, N_bh_sw, N_bh_pl)

        SC_Aw = SC[0]
        SC_sw = SC[1]
        SC_sb = SC[2]
        SC_pl = SC[3]

        BA_Aw = sp_Aw[5]
        BA_sb = sp_sb[5]
        BA_sw = sp_sw[5]
        BA_pl = sp_pl[5]

        BAinc_Aw = BasalAreaIncrementNonSpatialAw(sp_Aw, SC_Aw, site_index_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw)
        BAinc_sb = BasalAreaIncrementNonSpatialSb(sp_sb, SC_sb, site_index_bh_sb, N_bh_sb, N0_sb, bhage_sb, BA_sb)
        BAinc_sw = BasalAreaIncrementNonSpatialSw(sp_sw, SC_sw, site_index_bh_sw, N_bh_sw, N0_sw, bhage_sw, SDF_Aw0, SDF_pl0, SDF_sb0, BA_sw)
        BAinc_pl = BasalAreaIncrementNonSpatialPl(sp_pl, SC_pl, site_index_bh_pl, N_bh_pl, N0_pl, bhage_pl, SDF_Aw0, SDF_sw0, SDF_sb0, BA_pl)

        StumpDOB_Aw = sp_Aw[7]
        StumpHeight_Aw = sp_Aw[8]
        TopDib_Aw = sp_Aw[9]

        StumpDOB_sb = sp_sb[7]
        StumpHeight_sb = sp_sb[8]
        TopDib_sb = sp_sb[9]

        StumpDOB_sw = sp_sw[7]
        StumpHeight_sw = sp_sw[8]
        TopDib_sw = sp_sw[9]

        StumpDOB_pl = sp_pl[7]
        StumpHeight_pl = sp_pl[8]
        TopDib_pl = sp_pl[9]

        PLOT_DICT[plot_id] = {
            'PlotID': plot_id, 'SI_Aw': site_index_white_aspen, 'SI_sw': site_index_sw, 'SI_pl': site_index_pl, 'SI_sb': site_index_sb,
            'N_Aw': N_Aw, 'N_sw': N_sw, 'N_pl': N_pl, 'N_sb': N_sb,
            'y2bh_Aw': y2bh_Aw, 'y2bh_sw': y2bh_sw, 'y2bh_pl': y2bh_pl, 'y2bh_sb': y2bh_sb,
            'tage_Aw': tage_Aw, 'tage_sw': tage_sw, 'tage_pl': tage_pl, 'tage_sb': tage_sb,
            'BA_Aw': BA_Aw, 'BA_sw': BA_sw, 'BA_pl': BA_pl, 'BA_sb': BA_sb,
            'BAinc_Aw': BAinc_Aw, 'BAinc_sw': BAinc_sw, 'BAinc_pl': BAinc_pl, 'BAinc_sb': BAinc_sb,
            'SDF_Aw': SDF_Aw0, 'SDF_sw': SDF_sw0, 'SDF_pl': SDF_pl0, 'SDF_sb': SDF_sb0,
            'N0_Aw': N0_Aw, 'N0_sb': N0_sb, 'N0_sw': N0_sw, 'N0_pl': N0_pl,
            'StumpDOB_Aw': StumpDOB_Aw, 'StumpDOB_sb': StumpDOB_sb, 'StumpDOB_sw': StumpDOB_sw, 'StumpDOB_pl': StumpDOB_pl,
            'StumpHeight_Aw': StumpHeight_Aw, 'StumpHeight_sb': StumpHeight_sb, 'StumpHeight_sw': StumpHeight_sw, 'StumpHeight_pl': StumpHeight_pl,
            'TopDib_Aw': TopDib_Aw, 'TopDib_sb': TopDib_sb, 'TopDib_sw': TopDib_sw, 'TopDib_pl': TopDib_pl,
            'topHeight_Aw': topHeight_Aw, 'topHeight_sw': topHeight_sw, 'topHeight_sb': topHeight_sb, 'topHeight_pl': topHeight_pl
        }

        plot_df = pd.DataFrame(PLOT_DICT)
        plot_df = plot_df.transpose()

    return plot_df
