"""Basal Area correction factor estimators"""
# TODO: validate that none of the variables taken from kwargs are missing
import logging
import numpy as np

from pygypsy.basal_area_simulate import (
    sim_basal_area_aw,
    sim_basal_area_sw,
    sim_basal_area_sb,
    sim_basal_area_pl,
)


LOGGER = logging.getLogger(__name__)


def get_basal_area_factors_for_all_species(**kwargs):
    f_sb = 0
    f_aw = 0
    f_sw = 0
    f_pl = 0

    if kwargs['N0_Aw'] > 0:
        f_aw = estimate_basal_area_factor_aw(**kwargs)
    if kwargs['N0_Sb'] > 0:
        f_sb = estimate_basal_area_factor_sb(**kwargs)
    if kwargs['N0_Sw'] > 0:
        f_sw = estimate_basal_area_factor_sw(**kwargs)
    if kwargs['N0_Pl'] > 0:
        f_pl = estimate_basal_area_factor_pl(**kwargs)

    return {
        'f_Aw':f_aw,
        'f_Sb':f_sb,
        'f_Sw':f_sw,
        'f_Pl':f_pl,
    }


def estimate_basal_area_factor_aw(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision one wants this estimate, which is
    given by the parameter - acceptableDiff -, and the time the convergence time

    :param float startTage: Clock that uses the oldest species as a reference to become
                            the stand age
    :param float SI_bh_Aw: site index of species Aw
    :param float N_bh_AwT: density of sp Aw at time T (it varies over time)
    :param float BA_Aw0: basal area of Aw at breast height age, assumed to be very small
    :param float BA_AwT: basal area of Aw at time T
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float N0_Aw: initial density of species Aw at breast height age
    :param list densities: array of 'densities' objects
    '''
    age_at_observation = kwargs['startTage']
    site_index = kwargs['SI_bh_Aw']
    present_density = kwargs['N_bh_AwT']
    basal_area_at_bh_age = kwargs['BA_Aw0']
    present_basal_area = kwargs['BA_AwT']
    sdf_aw = kwargs['SDF_Aw0']
    density_at_bh_age = kwargs['N0_Aw']
    densities = kwargs['densities']
    factor = 100
    factor1 = 100 * factor
    tolerance = 0.01 * present_basal_area
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        ba_est = sim_basal_area_aw(age_at_observation, site_index, density_at_bh_age,
                                   basal_area_at_bh_age, sdf_aw, factor,
                                   densities, use_correction_factor_future=False,
                                   stop_at_initial_age=True,
                                   fix_proportion_and_density_to_initial_age=False,
                                   species_proportion_at_bh_age=None,
                                   present_density=present_density)[-1]

        if abs(present_basal_area - ba_est) < tolerance:
            within_tolerance = True
        else:
            if (present_basal_area - ba_est) < 0:
                factor1 = factor
                factor_p = factor \
                           * (1 \
                              + (np.log10(present_basal_area) - np.log10(abs(ba_est))) \
                              / (100*np.log10(abs(ba_est))))
                factor = (factor_p+factor)/2
            elif (present_basal_area - ba_est) > 0:
                factor = (factor+factor1)/2

        iter_count += 1

        if iter_count == 10000:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            break
    return factor


def estimate_basal_area_factor_sb(**kwargs):
    '''Black spruce basal area factor estimator

    This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    :param float startTage: Clock that uses the oldest species as a reference to
                            become the stand age
    :param float SI_bh_Sb: site index of species Sb
    :param float N_bh_SbT: density of sp Sb at time T (it varies over time)
    :param float BA_Sb0: basal area of Sb at breast height age, assumed to be very small
    :param float BA_SbT: basal area of Sb at time T
    :param float N0_Sb: initial density of species Sb at breast height age
    :param float y2bh_Sb: time elapseed in years from zero to breast height age of sp Sb
    :param float startTageSb: species specific ages counted independently
    :param float SC_Sb: proportion of species Sb in the stand
    :param list densities: array of 'densities' objects

    '''
    age_at_observation = kwargs['startTage']
    site_index = kwargs['SI_bh_Sb']
    densities = kwargs['densities']
    density_at_bh_age = kwargs['N0_Sb']
    basal_area_at_bh_age = kwargs['BA_Sb0']
    present_basal_area = kwargs['BA_SbT']
    species_proportion_at_bh_age = kwargs['SC_Sb']
    present_density = kwargs['N_bh_SbT']
    factor = 1.2
    factor1 = 1.5 * factor
    tolerance = 0.1
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        ba_est = sim_basal_area_sb(age_at_observation, site_index,
                                   density_at_bh_age,
                                   basal_area_at_bh_age,
                                   factor, densities,
                                   fix_proportion_and_density_to_initial_age=True,
                                   species_proportion_at_bh_age=species_proportion_at_bh_age,
                                   present_density=present_density,
                                   stop_at_initial_age=True)[-1]

        if abs(present_basal_area - ba_est) < tolerance:
            within_tolerance = True
        else:
            if (present_basal_area - ba_est) < 0:
                factor1 = factor
                factor_p = factor \
                           * (
                               1 \
                               + (np.log10(present_basal_area) - np.log10(abs(ba_est))) \
                               / (10*np.log10(abs(ba_est))))
                factor = (factor_p+factor)/2
            elif (present_basal_area - ba_est) > 0:
                factor = (factor+factor1)/2

        iter_count += 1

        if iter_count == 1500:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            break

    return factor


def estimate_basal_area_factor_sw(**kwargs):
    '''White Spruce basal area factor estimator

    This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    :param float startTage: Clock that uses the oldest species as a reference
                            to become the stand age
    :param float SI_bh_Sw: site index of species Sw
    :param float N_bh_SwT: density of sp Sw at time T (it varies over time)
    :param float BA_Sw0: basal area of Sw at breast height age, assumed to be very small
    :param float BA_SwT: basal area of Sw at time T
    :param float N0_Sw: initial density of species Sw at breast height age
    :param float y2bh_Sw: time elapseed in years from zero to breast height age of sp Sw
    :param float startTageSw: species specific ages counted independently
    :param float SC_Sw: proportion of species Sw in the stand
    :param float SDF_Pl0: Stand Density Factor of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb
    :param list densities: array of 'densities' objects

    '''
    age_at_observation = kwargs['startTage']
    site_index = kwargs['SI_bh_Sw']
    densities = kwargs['densities']
    density_at_bh_age = kwargs['N0_Sw']
    species_proportion_at_bh_age = kwargs['SC_Sw']
    sdf_aw = kwargs['SDF_Aw0']
    sdf_pl = kwargs['SDF_Pl0']
    sdf_sb = kwargs['SDF_Sb0']
    basal_area_at_bh_age = kwargs['BA_Sw0']
    present_basal_area = kwargs['BA_SwT']
    present_density = kwargs['N_bh_SwT']
    factor = 2.5
    tolerance = 0.1
    within_tolerance = False
    iter_count = 0
    factor1 = 1.5 * factor

    while not within_tolerance:
        ba_est = sim_basal_area_sw(age_at_observation, site_index,
                                   density_at_bh_age, sdf_aw, sdf_pl, sdf_sb,
                                   basal_area_at_bh_age,
                                   factor, densities,
                                   fix_proportion_and_density_to_initial_age=True,
                                   species_proportion_at_bh_age=species_proportion_at_bh_age,
                                   present_density=present_density,
                                   stop_at_initial_age=True)[-1]
        if abs(present_basal_area - ba_est) < tolerance:
            within_tolerance = True
        else:
            if (present_basal_area - ba_est) < 0:
                factor1 = factor
                factor_p = factor \
                           * (1 \
                              + (np.log10(present_basal_area) - np.log10(abs(ba_est))) \
                              / (10*np.log10(abs(ba_est))))
                factor = (factor_p+factor)/2
            elif (present_basal_area - ba_est) > 0:
                factor = (factor + factor1)/2

        iter_count += 1

        if iter_count == 1500:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            break

    return factor


def estimate_basal_area_factor_pl(**kwargs):
    '''Lodgepole pine basal area factor estimator

    This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    :param float startTage: Clock that uses the oldest species as a reference
                            to become the stand age
    :param float SI_bh_Pl: site index of species Pl
    :param float N_bh_PlT: density of sp Pl at time T (it varies over time)
    :param float BA_Pl0: basal area of Pl at breast height age, assumed to be very small
    :param float BA_PlT: basal area of Pl at time T
    :param float N0_Pl: initial density of species Pl at breast height age
    :param float y2bh_Pl: time elapseed in years from zero to breast height age of sp Pl
    :param float startTagePl: species specific ages counted independently
    :param float SC_Pl: proportion of species Pl in the stand
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb
    :param list densities: array of 'densities' objects

    '''
    age_at_observation = kwargs['startTage']
    site_index = kwargs['SI_bh_Pl']
    density_at_bh_age = kwargs['N0_Pl']
    densities = kwargs['densities']
    sdf_aw = kwargs['SDF_Aw0']
    sdf_sw = kwargs['SDF_Sw0']
    sdf_sb = kwargs['SDF_Sb0']
    basal_area_at_bh_age = kwargs['BA_Pl0']
    present_basal_area = kwargs['BA_PlT']
    species_proportion_at_bh_age = kwargs['SC_Pl']
    present_density = kwargs['N_bh_PlT']
    factor = 100.0
    tolerance = 0.1
    within_tolerance = False
    iter_count = 0
    factor1 = 1.5 * factor

    while not within_tolerance:
        ba_est = sim_basal_area_pl(age_at_observation, site_index,
                                   density_at_bh_age, sdf_aw, sdf_sw, sdf_sb,
                                   basal_area_at_bh_age,
                                   factor, densities,
                                   fix_proportion_and_density_to_initial_age=True,
                                   species_proportion_at_bh_age=species_proportion_at_bh_age,
                                   present_density=present_density,
                                   stop_at_initial_age=True)[-1]

        if abs(present_basal_area - ba_est) < tolerance:
            within_tolerance = True
        else:
            if (present_basal_area - ba_est) < 0:
                factor1 = factor
                factor_p = factor * (present_basal_area / ba_est)
                factor = (factor_p+factor)/2
            elif (present_basal_area - ba_est) > 0:
                factor = (factor + factor1)/2

        iter_count += 1

        if iter_count == 150:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            break

    return factor
