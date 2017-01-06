"""Simulation"""
# TODO: change module/funct name - 'forward' is not necessary or strictly true
from __future__ import division

import logging
import datetime
import pandas as pd

from GYPSYNonSpatial import densities_speciescomp_topheight_to_250
from utils import _log_loop_progress, estimate_species_composition
from pygypsy.basal_area_factor import get_basal_area_factors_for_all_species
from pygypsy.basal_area_simulate import (
    sim_basal_area_aw,
    sim_basal_area_sw,
    sim_basal_area_sb,
    sim_basal_area_pl,
)
from pygypsy.volume import(
    merchantable_volume,
    gross_total_volume,
    DEFAULT_UTILIZATIONS
)


LOGGER = logging.getLogger(__name__)
SPECIES = ('Aw', 'Sw', 'Sb', 'Pl')


def _get_initial_basal_area(current_basal_area):
    initial_basal_area = 0.001

    if initial_basal_area > current_basal_area * 0.5:
        initial_basal_area /= 2

    return initial_basal_area


def simulate_forwards_df(plot_df, utiliz_params=None):
    """Simulate the evolution of plot characteristics through time

    This begins with the simulation of densities, species, and top height.

    With the time series of those items in hand, the simulation from time zero
    (primary succession) to the time of observation can be skipped. If it is
    not skipped, an optimization routine is used to find factors for each
    species. The factors are multiplied with a parameter of the basal area
    increment to ensure that the simulation time timer zero to the time of
    observation passes through a basal area of 0 and the observed basal area.
    Between time zero and the time of observation, fixed values may optionally
    be used for density, species compositon. This optimization is expensive.

    Once the simulation reaches the year of observation, the simulated
    densities, species composition, and top heights are used in the increment
    functions, instead of using fixed values.

    :param plot_df: pandas.DataFrame with plot data
    :param utliz_params: dictionary of utilization parameters

    :return: dictoriony with keys corresponding to plot id and values data
    frame of time  series of the simulated plot characteristics

    """
    if utiliz_params is None:
        utiliz_params = DEFAULT_UTILIZATIONS

    output_dict = {}
    n_rows = plot_df.shape[0]

    for _, row in plot_df.iterrows():
        start = datetime.datetime.now()
        _log_loop_progress(_, n_rows)
        plot_id = str(int(row['id_l1']))

        LOGGER.debug('Starting simulation for plot: %s', plot_id)
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

        BA_Aw0 = _get_initial_basal_area(BA_AwT)
        BA_Sw0 = _get_initial_basal_area(BA_SwT)
        BA_Sb0 = _get_initial_basal_area(BA_SbT)
        BA_Pl0 = _get_initial_basal_area(BA_PlT)

        SC_Aw, SC_Sw, SC_Sb, SC_Pl = estimate_species_composition(
            N0_Aw, N0_Sb, N0_Sw, N0_Pl
        )

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

        species_factors = get_basal_area_factors_for_all_species(
            startTage=startTage,
            startTageAw=startTageAw, startTageSb=startTageSb,
            startTageSw=startTageSw, startTagePl=startTagePl,
            y2bh_Aw=y2bh_Aw, y2bh_Sb=y2bh_Sb, y2bh_Sw=y2bh_Sw, y2bh_Pl=y2bh_Pl,
            SC_Aw=SC_Aw, SC_Sb=SC_Sb, SC_Sw=SC_Sw, SC_Pl=SC_Pl,
            SI_bh_Aw=SI_bh_Aw, SI_bh_Sb=SI_bh_Sb, SI_bh_Sw=SI_bh_Sw, SI_bh_Pl=SI_bh_Pl,
            N_bh_AwT=N_bh_AwT, N_bh_SbT=N_bh_SbT, N_bh_SwT=N_bh_SwT, N_bh_PlT=N_bh_PlT,
            N0_Aw=N0_Aw, N0_Sb=N0_Sb, N0_Sw=N0_Sw, N0_Pl=N0_Pl,
            BA_Aw0=BA_Aw0, BA_Sb0=BA_Sb0, BA_Sw0=BA_Sw0, BA_Pl0=BA_Pl0,
            BA_AwT=BA_AwT, BA_SbT=BA_SbT, BA_SwT=BA_SwT, BA_PlT=BA_PlT,
            SDF_Pl0=SDF_Pl0, SDF_Sb0=SDF_Sb0, SDF_Aw0=SDF_Aw0, SDF_Sw0=SDF_Sw0,
            densities=densities
        )

        # use_correction_factor_future here is True because aspen was peculiar,
        # empirically demonstrated that using the factor for the whole
        # simulation yielded better results, probably because of variability in
        # density and basal area unique to aspen
        basal_area_aw_arr = sim_basal_area_aw(
            startTage, SI_bh_Aw, N0_Aw, BA_Aw0, SDF_Aw0,
            species_factors['f_Aw'], densities,
            use_correction_factor_future=True, stop_at_initial_age=False
        )
        basal_area_sb_arr = sim_basal_area_sb(
            startTage, SI_bh_Sb, N0_Sb, BA_Sb0,
            species_factors['f_Sb'], densities,
            use_correction_factor_future=False, stop_at_initial_age=False,
            fix_proportion_and_density_to_initial_age=False,
            species_proportion_at_bh_age=SC_Sb, present_density=N_bh_SbT
        )
        basal_area_sw_arr = sim_basal_area_sw(
            startTage, SI_bh_Sw, N0_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0,
            species_factors['f_Sw'], densities,
            use_correction_factor_future=False, stop_at_initial_age=False,
            fix_proportion_and_density_to_initial_age=False,
            species_proportion_at_bh_age=SC_Sw, present_density=N_bh_SwT
        )
        basal_area_pl_arr = sim_basal_area_pl(
            startTage, SI_bh_Pl, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0,
            species_factors['f_Pl'], densities,
            use_correction_factor_future=False, stop_at_initial_age=False,
            fix_proportion_and_density_to_initial_age=False,
            species_proportion_at_bh_age=SC_Pl, present_density=N_bh_PlT
        )

        output_df_aw = pd.DataFrame(basal_area_aw_arr, columns=['BA_Aw'])
        output_df_sw = pd.DataFrame(basal_area_sw_arr, columns=['BA_Sw'])
        output_df_sb = pd.DataFrame(basal_area_sb_arr, columns=['BA_Sb'])
        output_df_pl = pd.DataFrame(basal_area_pl_arr, columns=['BA_Pl'])

        densities_df = pd.DataFrame(densities)
        output_df = pd.concat(
            [densities_df, output_df_aw, output_df_sw, output_df_sb, output_df_pl],
            axis=1
        )

        for spec in SPECIES:
            output_df['Gross_Total_Volume_%s' % spec] = gross_total_volume(
                spec,
                output_df['BA_%s' % spec],
                output_df['topHeight_%s' % spec]
            )

            output_df['MerchantableVolume%s' % spec] = merchantable_volume(
                spec,
                output_df['N_bh_%sT' % spec],
                output_df['BA_%s' % spec],
                output_df['topHeight_%s' % spec],
                output_df['Gross_Total_Volume_%s' % spec],
                top_dib=utiliz_params[spec.lower()]['topDiamInsideBark'],
                stump_dob=utiliz_params[spec.lower()]['stumpDiamOutsideBark'],
                stump_height=utiliz_params[spec.lower()]['stumpHeight']
            )


        output_df['Gross_Total_Volume_Con'] = output_df['Gross_Total_Volume_Sw'] \
                                              + output_df['Gross_Total_Volume_Sb'] \
                                              + output_df['Gross_Total_Volume_Pl']
        output_df['Gross_Total_Volume_Dec'] = output_df['Gross_Total_Volume_Aw']
        output_df['Gross_Total_Volume_Tot'] = output_df['Gross_Total_Volume_Con'] \
                                              + output_df['Gross_Total_Volume_Dec']
        output_df['MerchantableVolume_Con'] = output_df['MerchantableVolumeSw'] \
                                              + output_df['MerchantableVolumeSb'] \
                                              + output_df['MerchantableVolumePl']
        output_df['MerchantableVolume_Dec'] = output_df['MerchantableVolumeAw']
        output_df['MerchantableVolume_Tot'] = output_df['MerchantableVolume_Con'] \
                                              + output_df['MerchantableVolume_Dec']

        output_dict[plot_id] = output_df

        end = datetime.datetime.now()
        duration = end - start
        LOGGER.debug('plot %s took %f seconds', plot_id, duration.total_seconds())

    return output_dict
