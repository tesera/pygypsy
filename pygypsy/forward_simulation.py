"""Simulation"""
# TODO: change module/funct name - 'forward' is not necessary or strictly true
from __future__ import division
import logging
import datetime
from collections import defaultdict

import pandas as pd

from pygypsy.utils import _log_loop_progress, estimate_species_composition
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
from pygypsy.density import (
    estimate_density_aw,
    estimate_density_pl,
    estimate_density_sb,
    estimate_density_sw,
)
from pygypsy.asaCompileAgeGivenSpSiHt \
    import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge


LOGGER = logging.getLogger(__name__)
SPECIES = ('Aw', 'Sw', 'Sb', 'Pl')


def _get_initial_basal_area(current_basal_area):
    initial_basal_area = 0.001

    if initial_basal_area > current_basal_area * 0.5:
        initial_basal_area /= 2

    return initial_basal_area


# note: the complexity from basal area/factor finder simulation could be moved
# here. simulation supports using the values from the year of observation for
# all years before the year of observation. that could be enforced here, or
# with an intermediate function. it would be key to get that complexity out of
# the basal area simulation functions to vectorize them
# TODO: this could also be vectorized instead of in a loop
# DESIGN: could use callbacks here instead of calling each of the functions
# DESIGN: should the responsibility to return 0 be in the called functions or
#         in if clauses here?
def simulate_densities_speciescomp_topheight(n_years=250, start_at_data_year=False, **kwargs):
    '''Estimate, species composition, top height for all species along time

    Time is counted independently for each species.

    :param in duration:
    :param float startTage: It uses the oldest species as a reference to
                            become the stand age
    :param float startTageAw, startTageSw, startTageSb, and startTagePl: age
                                                                         for respective
                                                                         species
    :param float SDF_Pl0: Stand Density Factor of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param float SI_bh_Sw: site index of species Sw
    :param float SI_bh_Aw: site index of species Aw
    :param float SI_bh_Sb: site index of species Sb
    :param float SI_bh_Pl: site index of species Pl
    :param float y2bh_Aw: time elapseed in years from zero to breast height age of sp Aw
    :param float y2bh_Sw: time elapseed in years from zero to breast height age of sp Sw
    :param float y2bh_Sb: time elapseed in years from zero to breast height age of sp Sb
    :param float y2bh_Pl: time elapseed in years from zero to breast height age of sp Pl

    '''
    starttage = kwargs['startTage']
    starttageaw = kwargs['startTageAw']
    y2bh_aw = kwargs['y2bh_Aw']
    starttagesw = kwargs['startTageSw']
    y2bh_sw = kwargs['y2bh_Sw']
    starttagesb = kwargs['startTageSb']
    y2bh_sb = kwargs['y2bh_Sb']
    starttagepl = kwargs['startTagePl']
    y2bh_pl = kwargs['y2bh_Pl']
    sdf_aw0 = kwargs['SDF_Aw0']
    sdf_sw0 = kwargs['SDF_Sw0']
    sdf_pl0 = kwargs['SDF_Pl0']
    sdf_sb0 = kwargs['SDF_Sb0']
    si_bh_aw = kwargs['SI_bh_Aw']
    si_bh_sw = kwargs['SI_bh_Sw']
    si_bh_sb = kwargs['SI_bh_Sb']
    si_bh_pl = kwargs['SI_bh_Pl']
    densities_along_time = []

    end_year = n_years if not start_at_data_year else n_years + starttage

    year = 0 if not start_at_data_year else starttage
    tage_aw = starttageaw - starttage if not start_at_data_year else starttageaw
    tage_sw = starttagesw - starttage if not start_at_data_year else starttagesw
    tage_pl = starttagepl - starttage if not start_at_data_year else starttagepl
    tage_sb = starttagesb - starttage if not start_at_data_year else starttagesb

    while year < end_year:
        bhage_aw = tage_aw - y2bh_aw
        bhage_sw = tage_sw - y2bh_sw
        bhage_pl = tage_pl - y2bh_pl
        bhage_sb = tage_sb - y2bh_sb

        if bhage_aw < 0:
            n_bh_awt = 0
        else:
            # bhage instead of tage, as specified by the GYPSY model itself
            n_bh_awt = estimate_density_aw(sdf_aw0, bhage_aw, si_bh_aw)

        if tage_sb < 0:
            n_bh_sbt = 0
        else:
            n_bh_sbt = estimate_density_sb(sdf_sb0, tage_sb, si_bh_sb)

        if tage_sw < 0:
            n_bh_swt = 0
        else:
            n_bh_swt = estimate_density_sw(sdf_sw0, sdf_aw0, tage_sw, si_bh_sw)

        if tage_pl < 0:
            n_bh_plt = 0
        else:
            n_bh_plt = estimate_density_pl(sdf_aw0, sdf_sw0, sdf_sb0, sdf_pl0,
                                           tage_pl, si_bh_pl)

        if n_bh_awt <= 0:
            topheight_aw = 0
        else:
            topheight_aw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Aw', si_bh_aw, tage_aw
            )

        if n_bh_sbt <= 0:
            topheight_sb = 0
        else:
            topheight_sb = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Sb', si_bh_sb, tage_sb
            )

        if n_bh_swt <= 0:
            topheight_sw = 0
        else:
            topheight_sw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Sw', si_bh_sw, tage_sw
            )

        if n_bh_plt <= 0:
            topheight_pl = 0
        else:
            topheight_pl = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Pl', si_bh_pl, tage_pl
            )


        sc_aw, sc_sw, sc_sb, sc_pl = estimate_species_composition(
            n_bh_awt, n_bh_sbt,
            n_bh_swt, n_bh_plt
        )

        densities_along_time.append({
            'N_bh_AwT': n_bh_awt, 'N_bh_SwT': n_bh_swt,
            'N_bh_SbT': n_bh_sbt, 'N_bh_PlT': n_bh_plt,
            'SC_Aw': sc_aw, 'SC_Sw': sc_sw,
            'SC_Sb':sc_sb, 'SC_Pl': sc_pl,
            'tage_Aw': tage_aw, 'tage_Sw': tage_sw,
            'tage_Sb': tage_sb, 'tage_Pl': tage_pl,
            'bhage_Aw': bhage_aw, 'bhage_Sw': bhage_sw,
            'bhage_Sb': bhage_sb, 'bhage_Pl': bhage_pl,
            'topHeight_Aw': topheight_aw, 'topHeight_Sw': topheight_sw,
            'topHeight_Sb': topheight_sb, 'topHeight_Pl': topheight_pl
        })
        year += 1
        tage_aw += 1
        tage_sw += 1
        tage_pl += 1
        tage_sb += 1

    return densities_along_time


def simulate_forwards_df(plot_df, utiliz_params=None, backwards=True,
                         n_years=250):
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
    :param int n_years: number of years to simulate
    :param bool backwards: whether the simulation from year zero to the
                           year of the data should be done

    :return: dictoriony with keys corresponding to plot id and values data
    frame of time  series of the simulated plot characteristics

    .. warning:: the backwards parameter must be set to True in order to
                 utilize the correction factors, which ensure the data passes
                 through 0 and the observation. without the backwards simulation,
                 this is already ensured. However, for Aspen, the factor found
                 is also used for the forward simulation

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

        densities = simulate_densities_speciescomp_topheight(
            n_years=n_years,
            start_at_data_year=False if backwards else True,
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

        species_factors = defaultdict(lambda: 1) if not backwards else \
                          get_basal_area_factors_for_all_species(
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
            use_correction_factor_future=True if backwards else False,
            stop_at_initial_age=False,
            force_use_densities=False if backwards else True
        )
        basal_area_sb_arr = sim_basal_area_sb(
            startTage, SI_bh_Sb, N0_Sb, BA_Sb0,
            species_factors['f_Sb'], densities,
            use_correction_factor_future=False, stop_at_initial_age=False,
            fix_proportion_and_density_to_initial_age=False,
            species_proportion_at_bh_age=SC_Sb, present_density=N_bh_SbT,
            force_use_densities=False if backwards else True
        )
        basal_area_sw_arr = sim_basal_area_sw(
            startTage, SI_bh_Sw, N0_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0,
            species_factors['f_Sw'], densities,
            use_correction_factor_future=False, stop_at_initial_age=False,
            fix_proportion_and_density_to_initial_age=False,
            species_proportion_at_bh_age=SC_Sw, present_density=N_bh_SwT,
            force_use_densities=False if backwards else True
        )
        basal_area_pl_arr = sim_basal_area_pl(
            startTage, SI_bh_Pl, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0,
            species_factors['f_Pl'], densities,
            use_correction_factor_future=False, stop_at_initial_age=False,
            fix_proportion_and_density_to_initial_age=False,
            species_proportion_at_bh_age=SC_Pl, present_density=N_bh_PlT,
            force_use_densities=False if backwards else True
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
