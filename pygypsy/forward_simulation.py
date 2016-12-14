# -*- coding: utf-8 -*-
"""Simulation"""
import logging
import datetime
import numpy as np
import pandas as pd

import basal_area_increment as incr
from GYPSYNonSpatial import densities_and_SCs_to_250
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


def BA_zeroAw(BA_Aw0, BA_AwT):
    while BA_Aw0 > BA_AwT * 0.5:
        BA_Aw0 = BA_Aw0 * 0.5
    return BA_Aw0

def BA_zeroSw(BA_Sw0, BA_SwT):
    while BA_Sw0 > BA_SwT * 0.5:
        BA_Sw0 = BA_Sw0 * 0.5
    return BA_Sw0

def BA_zeroSb(BA_Sb0, BA_SbT):
    while BA_Sb0 > BA_SbT * 0.5:
        BA_Sb0 = BA_Sb0 * 0.5
    return BA_Sb0

def BA_zeroPl(BA_Pl0, BA_PlT):
    while BA_Pl0 > BA_PlT * 0.5:
        BA_Pl0 = BA_Pl0 * 0.5
    return BA_Pl0

def BA0_lower_BAT_Aw(BA_AwT):
    BA_Aw0 = 0.001
    if BA_Aw0 > BA_AwT:
        BA_Aw0 = BA_zeroAw(BA_Aw0, BA_AwT)
    else:
        pass
    return BA_Aw0

def BA0_lower_BAT_Sw(BA_SwT):
    BA_Sw0 = 0.001
    if BA_Sw0 > BA_SwT:
        BA_Sw0 = BA_zeroSw(BA_Sw0, BA_SwT)
    else:
        pass
    return BA_Sw0

def BA0_lower_BAT_Sb(BA_SbT):
    BA_Sb0 = 0.001
    if BA_Sb0 > BA_SbT:
        BA_Sb0 = BA_zeroSb(BA_Sb0, BA_SbT)
    else:
        pass
    return BA_Sb0

def BA0_lower_BAT_Pl(BA_PlT):
    BA_Pl0 = 0.001
    if BA_Pl0 > BA_PlT:
        BA_Pl0 = BA_zeroPl(BA_Pl0, BA_PlT)
    else:
        pass
    return BA_Pl0

def get_factors_for_all_species(**kwargs):
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

def simulate_forwards_df(plot_df, simulation_choice='yes',
                         utiliz_params=None):
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

        BA_Aw0 = BA0_lower_BAT_Aw(BA_AwT)
        BA_Sw0 = BA0_lower_BAT_Sw(BA_SwT)
        BA_Sb0 = BA0_lower_BAT_Sb(BA_SbT)
        BA_Pl0 = BA0_lower_BAT_Pl(BA_PlT)
        SC_Aw, SC_Sw, SC_Sb, SC_Pl = estimate_species_composition(N0_Aw, N0_Sb, N0_Sw, N0_Pl)

        tageData = [tage_AwT, tage_SwT, tage_PlT, tage_SbT]
        startTageAw = tageData[0]
        startTageSw = tageData[1]
        startTagePl = tageData[2]
        startTageSb = tageData[3]
        startTageAwF = tageData[0]+1
        startTageSwF = tageData[1]+1
        startTagePlF = tageData[2]+1
        startTageSbF = tageData[3]+1

        tageData = sorted(tageData, reverse=True)
        startTage = int(tageData[0])

        densities = densities_and_SCs_to_250(
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
        species_factors = get_factors_for_all_species(
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
        # simulation choice here is no because aspen was peculiar, empirically demonstrated that using the factor
        # for the whole simulation yielded better results, probably because of variability in density and basal area
        # unique to aspen
        # we can't do simulation choice = no here for sb, sw, pl because the factor should not be applied for them
        # sw, sb, pl use the factor until the time of data. the subsequent years use the regular basal area increment formula
        # julianno sambatti, november 10, 2016
        BA_0_to_data_Aw_arr = sim_basal_area_aw(startTage, SI_bh_Aw, N0_Aw, BA_Aw0, SDF_Aw0, f_Aw, densities, simulation_choice='no')
        BA_0_to_data_Sb_arr = sim_basal_area_sb(startTage, startTageSb, y2bh_Sb, SC_Sb, SI_bh_Sb, N_bh_SbT, N0_Sb, BA_Sb0, f_Sb, simulation_choice)
        BA_0_to_data_Sw_arr = sim_basal_area_sw(startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0, f_Sw, simulation_choice)
        BA_0_to_data_Pl_arr = sim_basal_area_pl(startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, f_Pl, simulation_choice)

        output_DF_Aw = pd.DataFrame(BA_0_to_data_Aw_arr, columns=['BA_Aw'])
        output_DF_Sw = pd.DataFrame(BA_0_to_data_Sw_arr, columns=['BA_Sw'])
        output_DF_Sb = pd.DataFrame(BA_0_to_data_Sb_arr, columns=['BA_Sb'])
        output_DF_Pl = pd.DataFrame(BA_0_to_data_Pl_arr, columns=['BA_Pl'])

        if simulation_choice == 'no':
            continue

        # allocate extra space for the simulation results
        # this is not ideal, would rather follow what is done for aspen, but at least
        # this only appends once instead of for every year in the iteration
        n_extra_rows = len(densities) - startTage+1
        output_DF_Sb = pd.concat([
            output_DF_Sb,
            pd.DataFrame({'BA_Sb': [np.NaN]*n_extra_rows})
        ], axis=0, ignore_index=True)
        output_DF_Sw = pd.concat([
            output_DF_Sw,
            pd.DataFrame({'BA_Sw': [np.NaN]*n_extra_rows})
        ], axis=0, ignore_index=True)
        output_DF_Pl = pd.concat([
            output_DF_Pl,
            pd.DataFrame({'BA_Pl': [np.NaN]*n_extra_rows})
        ], axis=0, ignore_index=True)

        logger.debug('Starting main simulation')
        t = startTage
        for SC_Dict in densities[t-1:]:
            bhage_SwF = SC_Dict['bhage_Sw']
            SC_SwF = SC_Dict['SC_Sw']
            N_bh_SwT = SC_Dict['N_bh_SwT']

            bhage_SbF = SC_Dict['bhage_Sb']
            SC_SbF = SC_Dict['SC_Sb']
            N_bh_SbT = SC_Dict['N_bh_SbT']

            bhage_PlF = SC_Dict['bhage_Pl']
            SC_PlF = SC_Dict['SC_Pl']
            N_bh_PlT = SC_Dict['N_bh_PlT']
            logger.debug('Simulating year %d', t)


            # TODO: Aw uses bafromzerotodataaw as described and called above,
            # but htese are here to avoid using the factors, which should only
            # apply until time t, then a implicit factor of 1 is used we can
            # refactor the frmozerotodata functions to switch the factor off
            # after a certain year, then the whole for loop containing this
            # comment could be removed
            if N_bh_SbT > 0:
                BA_SbT = BA_SbT + incr.increment_basal_area_sb('Sb', SC_SbF, SI_bh_Sb, N_bh_SbT, N0_Sb, bhage_SbF, BA_SbT)
                if BA_SbT < 0:
                    BA_SbT = 0
            else:
                BA_SbT = 0

            if N_bh_SwT > 0:
                BA_SwT = BA_SwT + incr.increment_basal_area_sw('Sw', SC_SwF, SI_bh_Sw, N_bh_SwT, N0_Sw, bhage_SwF, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_SwT)
                if BA_SwT < 0:
                    BA_SwT = 0
            else:
                BA_SwT = 0

            if N_bh_PlT > 0:
                BA_PlT = BA_PlT + incr.increment_basal_area_pl('Pl', SC_PlF, SI_bh_Pl, N_bh_PlT, N0_Pl, bhage_PlF, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_PlT)
                if BA_PlT < 0:
                    BA_PlT = 0
            else:
                BA_PlT = 0

            output_DF_Sw.at[t, 'BA_Sw'] = BA_SwT
            output_DF_Sb.at[t, 'BA_Sb'] = BA_SbT
            output_DF_Pl.at[t, 'BA_Pl'] = BA_PlT

            t += 1
            startTageAwF += 1
            startTageSwF += 1
            startTagePlF += 1
            startTageSbF += 1

        densities_DF = pd.DataFrame(densities)
        output_DF = pd.concat(
            [densities_DF, output_DF_Aw, output_DF_Sw, output_DF_Sb, output_DF_Pl],
            axis=1
        )
        #http://stackoverflow.com/questions/25314547/cell-var-from-loop-warning-from-pylint

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
