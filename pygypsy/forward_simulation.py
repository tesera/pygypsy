# -*- coding: utf-8 -*-
"""Simulation"""
from __future__ import division

import logging
import datetime
import numpy as np
import pandas as pd

import basal_area_increment as incr
from GYPSYNonSpatial import densities_speciescomp_topheight_to_250
from utils import _log_loop_progress, estimate_species_composition
from pygypsy.basal_area_factor import (
    estimate_basal_area_factor_aw,
    estimate_basal_area_factor_sb,
    estimate_basal_area_factor_sw,
    estimate_basal_area_factor_pl,
)
from pygypsy.basal_area_simulate import (
    sim_basal_area_aw,
    sim_basal_area_sw,
    sim_basal_area_sb,
    sim_basal_area_pl,
)
from pygypsy.volume import(
    merchantable_volume,
    gross_total_volume,
)


logger = logging.getLogger(__name__)

SPECIES = ('Aw', 'Sw', 'Sb', 'Pl')

DEFAULT_UTILIZATIONS = {
    "aw": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    },
    "sw": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    },
    "sb": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    },
    "pl": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    }
}


def get_initial_basal_area(current_basal_area):
    initial_basal_area = 0.001

    if initial_basal_area > current_basal_area * 0.5:
        initial_basal_area /= 2

    return initial_basal_area


def get_basal_area_factors_for_all_species(**kwargs):
    logger.debug('Getting factors for all species')

    f_Sb = 0
    f_Aw = 0
    f_Sw = 0
    f_Pl = 0

    if kwargs['N0_Aw'] > 0:
        f_Aw = estimate_basal_area_factor_aw(**kwargs)

    if kwargs['N0_Sb'] > 0:
        f_Sb = estimate_basal_area_factor_sb(**kwargs)

    if kwargs['N0_Sw'] > 0:
        f_Sw = estimate_basal_area_factor_sw(**kwargs)

    if kwargs['N0_Pl'] > 0:
        f_Pl = estimate_basal_area_factor_pl(**kwargs)

    return {'f_Aw':f_Aw,
            'f_Sb':f_Sb,
            'f_Sw':f_Sw,
            'f_Pl':f_Pl,}

def simulate_forwards_df(plot_df, utiliz_params=None):
    """Run forwards simulation

    Keyword Arguments:
    plot_df -- pandas.DataFrame with plot data

    Return:
    !TODO!
    """
    if utiliz_params is None:
        utiliz_params = DEFAULT_UTILIZATIONS

    output_dict = {}
    logger.debug('Starting forwards simulation')
    n_rows = plot_df.shape[0]

    for _, row in plot_df.iterrows():
        start = datetime.datetime.now()
        _log_loop_progress(_, n_rows)
        plot_id = str(int(row['id_l1']))

        logger.info('Starting simulation for plot: %s', plot_id)
        SI_bh_Aw = row.at['SI_Aw']
        SI_bh_Sw = row.at['SI_Sw']
        SI_bh_Pl = row.at['SI_Pl']
        SI_bh_Sb = row.at['SI_Sb']
        N_bh_AwT = row.at['N_Aw']
        N_bh_SwT = row.at['N_Sw']
        N_bh_PlT = row.at['N_Pl']
        N_bh_SbT = row.at['N_Sb']
        y2bh_Aw = row.at['y2bh_Aw']
        y2bh_Sw = row.at['y2bh_Sw']
        y2bh_Sb = row.at['y2bh_Sb']
        y2bh_Pl = row.at['y2bh_Pl']
        tage_AwT = row.at['tage_Aw']
        tage_SwT = row.at['tage_Sw']
        tage_PlT = row.at['tage_Pl']
        tage_SbT = row.at['tage_Sb']
        BA_AwT = row.at['BA_Aw']
        BA_SwT = row.at['BA_Sw']
        BA_PlT = row.at['BA_Pl']
        BA_SbT = row.at['BA_Sb']
        SDF_Aw0 = row.at['SDF_Aw']
        SDF_Sw0 = row.at['SDF_Sw']
        SDF_Pl0 = row.at['SDF_Pl']
        SDF_Sb0 = row.at['SDF_Sb']
        N0_Aw = row.at['N0_Aw']
        N0_Sw = row.at['N0_Sw']
        N0_Pl = row.at['N0_Pl']
        N0_Sb = row.at['N0_Sb']

        # TODO: don't we already have this in the data frame from data prep?
        BA_Aw0 = get_initial_basal_area(BA_AwT)
        BA_Sw0 = get_initial_basal_area(BA_SwT)
        BA_Sb0 = get_initial_basal_area(BA_SbT)
        BA_Pl0 = get_initial_basal_area(BA_PlT)

        # TODO: don't we already have this in the data frame from data prep?
        SC_Aw, SC_Sw, SC_Sb, SC_Pl = estimate_species_composition(N0_Aw, N0_Sb, N0_Sw, N0_Pl)

        tageData = [tage_AwT, tage_SwT, tage_PlT, tage_SbT]
        startTageAw = tageData[0]
        startTageSw = tageData[1]
        startTagePl = tageData[2]
        startTageSb = tageData[3]

        tageData = sorted(tageData, reverse=True)
        startTage = int(tageData[0])

        densities = densities_speciescomp_topheight_to_250(
            startTage=startTage,
            startTageAw=startTageAw,
            y2bh_Aw=y2bh_Aw,
            startTageSw=startTageSw,
            y2bh_Sw=y2bh_Sw,
            startTageSb=startTageSb,
            y2bh_Sb=y2bh_Sb,
            startTagePl=startTagePl,
            y2bh_Pl=y2bh_Pl,
            SDF_Aw0=SDF_Aw0,
            SDF_Sw0=SDF_Sw0,
            SDF_Pl0=SDF_Pl0,
            SDF_Sb0=SDF_Sb0,
            SI_bh_Aw=SI_bh_Aw,
            SI_bh_Sw=SI_bh_Sw,
            SI_bh_Sb=SI_bh_Sb,
            SI_bh_Pl=SI_bh_Pl
        )

        # estimating correction factor to fit BA at t0 and BA at t and
        # choosing whether simulating with multiplication factor
        # or starting at t recalculating the densities and SC
        species_factors = get_basal_area_factors_for_all_species(
            startTage=startTage,
            startTageAw=startTageAw,
            y2bh_Aw=y2bh_Aw,
            SC_Aw=SC_Aw,
            SI_bh_Aw=SI_bh_Aw,
            N_bh_AwT=N_bh_AwT,
            N0_Aw=N0_Aw,
            BA_Aw0=BA_Aw0,
            BA_AwT=BA_AwT,
            startTageSb=startTageSb,
            y2bh_Sb=y2bh_Sb,
            SC_Sb=SC_Sb,
            SI_bh_Sb=SI_bh_Sb,
            N_bh_SbT=N_bh_SbT,
            N0_Sb=N0_Sb,
            BA_Sb0=BA_Sb0,
            BA_SbT=BA_SbT,
            startTageSw=startTageSw,
            y2bh_Sw=y2bh_Sw,
            SC_Sw=SC_Sw,
            SI_bh_Sw=SI_bh_Sw,
            N_bh_SwT=N_bh_SwT,
            N0_Sw=N0_Sw,
            SDF_Pl0=SDF_Pl0,
            SDF_Sb0=SDF_Sb0,
            BA_Sw0=BA_Sw0,
            BA_SwT=BA_SwT,
            startTagePl=startTagePl,
            y2bh_Pl=y2bh_Pl,
            SC_Pl=SC_Pl,
            SI_bh_Pl=SI_bh_Pl,
            N_bh_PlT=N_bh_PlT,
            N0_Pl=N0_Pl,
            SDF_Aw0=SDF_Aw0,
            SDF_Sw0=SDF_Sw0,
            BA_Pl0=BA_Pl0,
            BA_PlT=BA_PlT,
            densities=densities,
            printWarnings=True
        )

        f_Aw = species_factors['f_Aw']
        f_Sw = species_factors['f_Sw']
        f_Sb = species_factors['f_Sb']
        f_Pl = species_factors['f_Pl']

        logger.debug('Getting basal area from time 0 to time of data')
        # use_correction_factor_future here is True because aspen was peculiar,
        # empirically demonstrated that using the factor for the whole
        # simulation yielded better results, probably because of variability in
        # density and basal area unique to aspen we can't do simulation choice
        # = no here for sb, sw, pl because the factor should not be applied for
        # them sw, sb, pl use the factor until the time of data. the subsequent
        # years use the regular basal area increment formula julianno sambatti,
        # november 10, 2016

        # TODO: something is amiss with this new approach; everything is OK until startTage,
        #       then the new approahc and the old approach begin to diverge, with the new approach
        #       having higher values than old
        #       the old approach used density, species comp, bhage from SC_Dict
        #       which was a dict of the params which came frmo an array of the params
        #       generated frmo the smiulate_species_comp_tree_height_etc_to_250 function
        #
        #       but here, below, i guess all those values are fixed and from the time of the data
        #       i think that would account for it
        #       in other words, need to pass that densities dict through and use the values?
        #       that's pretty confusing though. yeesh
        #
        #       basically, make sb, sq, pl sim_basal_area_functions work like
        #       aw function using densities/dict array
        #
        #       further inspection of those functions indicates they can be improved
        #       because the increment only dependds on other values, so we can
        #       calculate it as a vector operation using the other arrays then
        #       the actual values are just the cumulative sums of the
        #       increments that's something for another day; because it is
        #       complicated by the whole factor business
        BA_0_to_data_Aw_arr = sim_basal_area_aw(
            startTage, SI_bh_Aw, N0_Aw, BA_Aw0, SDF_Aw0, f_Aw, densities,
            use_correction_factor_future=True, stop_at_initial_age=False
        )
        BA_0_to_data_Sb_arr = sim_basal_area_sb(
            startTage, SI_bh_Sb, N0_Sb,
            BA_Sb0, f_Sb, densities, stop_at_initial_age=False
        )
        BA_0_to_data_Sw_arr = sim_basal_area_sw(
            startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw,
            SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0, f_Sw, stop_at_initial_age=False
        )
        BA_0_to_data_Pl_arr = sim_basal_area_pl(
            startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl,
            SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, f_Pl, stop_at_initial_age=False
        )

        output_DF_Aw = pd.DataFrame(BA_0_to_data_Aw_arr, columns=['BA_Aw'])
        output_DF_Sw = pd.DataFrame(BA_0_to_data_Sw_arr, columns=['BA_Sw'])
        output_DF_Sb = pd.DataFrame(BA_0_to_data_Sb_arr, columns=['BA_Sb'])
        output_DF_Pl = pd.DataFrame(BA_0_to_data_Pl_arr, columns=['BA_Pl'])

        densities_DF = pd.DataFrame(densities)
        output_DF = pd.concat(
            [densities_DF, output_DF_Aw, output_DF_Sw, output_DF_Sb, output_DF_Pl],
            axis=1
        )

        #import ipdb; ipdb.set_trace()
        for spec in SPECIES:
            output_DF['Gross_Total_Volume_%s' % spec] = gross_total_volume(
                spec,
                output_DF['BA_%s' % spec],
                output_DF['topHeight_%s' % spec]
            )

        output_DF['Gross_Total_Volume_Con'] = output_DF['Gross_Total_Volume_Sw'] \
                                              + output_DF['Gross_Total_Volume_Sb'] \
                                              + output_DF['Gross_Total_Volume_Pl']
        output_DF['Gross_Total_Volume_Dec'] = output_DF['Gross_Total_Volume_Aw']
        output_DF['Gross_Total_Volume_Tot'] = output_DF['Gross_Total_Volume_Con'] \
                                              + output_DF['Gross_Total_Volume_Dec']

        # this could go in the loop above, but is left here for now since
        # the tests are sensitive to column order
        for spec in SPECIES:
            output_DF['MerchantableVolume%s' % spec] = merchantable_volume(
                spec,
                output_DF['N_bh_%sT' % spec],
                output_DF['BA_%s' % spec],
                output_DF['topHeight_%s' % spec],
                output_DF['Gross_Total_Volume_%s' % spec],
                top_dib=utiliz_params[spec.lower()]['topDiamInsideBark'],
                stump_dob=utiliz_params[spec.lower()]['stumpDiamOutsideBark'],
                stump_height=utiliz_params[spec.lower()]['stumpHeight']
            )

        output_DF['MerchantableVolume_Con'] = output_DF['MerchantableVolumeSw'] \
                                              + output_DF['MerchantableVolumeSb'] \
                                              + output_DF['MerchantableVolumePl']
        output_DF['MerchantableVolume_Dec'] = output_DF['MerchantableVolumeAw']
        output_DF['MerchantableVolume_Tot'] = output_DF['MerchantableVolume_Con'] \
                                              + output_DF['MerchantableVolume_Dec']

        output_dict[plot_id] = output_DF

        end = datetime.datetime.now()
        duration = end - start
        logger.info('plot %s took %f seconds', plot_id, duration.total_seconds())

    return output_dict
