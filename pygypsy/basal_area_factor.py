"""Basal Area correction factor estimators"""
import logging
import numpy as np

from pygypsy.basal_area_simulate import (
    sim_basal_area_aw,
    sim_basal_area_sw,
    sim_basal_area_sb,
    sim_basal_area_pl,
)


LOGGER = logging.getLogger(__name__)


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

    '''
    initial_age = kwargs['startTage']
    site_index = kwargs['SI_bh_Aw']
    # present_density = kwargs['N_bh_AwT']
    basal_area_at_bh_age = kwargs['BA_Aw0']
    present_basal_area = kwargs['BA_AwT']
    sdf_aw = kwargs['SDF_Aw0']
    density_at_bh_age = kwargs['N0_Aw']
    densities = kwargs['densities']
    simulation_choice = 'yes'
    factor = 100
    factor1 = 100 * factor
    tolerance = 0.01 * present_basal_area
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        ba_est = sim_basal_area_aw(initial_age, site_index, density_at_bh_age,
                                   basal_area_at_bh_age, sdf_aw, factor, densities,
                                   simulation_choice)[-1]

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

        iter_count = iter_count + 1

        if iter_count == 10000:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            return factor
    return factor


def estimate_basal_area_factor_sb(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision with one wants this estimate, which is
    given by the parameter - tolerance -, and the time the convergence time

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

    '''
    LOGGER.debug('Getting basal area factor for black spruce')
    initial_age = kwargs['startTage']
    initial_age_sb = kwargs['startTageSb']
    years_to_bh_sb = kwargs['y2bh_Sb']
    species_comp_sb = kwargs['SC_Sb']
    site_index = kwargs['SI_bh_Sb']
    present_density = kwargs['N_bh_SbT']
    density_at_bh_age = kwargs['N0_Sb']
    basal_area_at_bh_age = kwargs['BA_Sb0']
    present_basal_area = kwargs['BA_SbT']
    simulation_choice = 'yes'
    factor = 1.2
    factor1 = 1.5 * factor
    tolerance = 0.1
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        ba_est = sim_basal_area_sb(initial_age, initial_age_sb, years_to_bh_sb,
                                   species_comp_sb, site_index, present_density,
                                   density_at_bh_age, basal_area_at_bh_age, factor,
                                   simulation_choice)[-1]

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

        iter_count = iter_count + 1

        if iter_count == 1500:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            return factor

    return factor


def estimate_basal_area_factor_sw(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision with one wants this estimate, which is
    given by the parameter - tolerance -, and the time the convergence time

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

    '''
    LOGGER.debug('Getting basal area factor for white spruce')
    initial_age = kwargs['startTage']
    initial_age_sw = kwargs['startTageSw']
    years_to_bh_sw = kwargs['y2bh_Sw']
    species_comp_sw = kwargs['SC_Sw']
    site_index = kwargs['SI_bh_Sw']
    present_density = kwargs['N_bh_SwT']
    density_at_bh_age = kwargs['N0_Sw']
    sdf_aw = kwargs['SDF_Aw0']
    sdf_pl = kwargs['SDF_Pl0']
    sdf_sb = kwargs['SDF_Sb0']
    basal_area_at_bh_age = kwargs['BA_Sw0']
    present_basal_area = kwargs['BA_SwT']
    simulation_choice = 'yes'
    factor = 2.5
    tolerance = 0.1
    within_tolerance = False
    iter_count = 0
    factor1 = 1.5* factor

    while not within_tolerance:
        ba_est = sim_basal_area_sw(initial_age, initial_age_sw, years_to_bh_sw,
                                   species_comp_sw, site_index, present_density,
                                   density_at_bh_age, sdf_aw, sdf_pl, sdf_sb,
                                   basal_area_at_bh_age, factor, simulation_choice)[-1]
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

        iter_count = iter_count + 1

        if iter_count == 1500:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            return factor

    return factor


def estimate_basal_area_factor_pl(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision with one wants this estimate, which is
    given by the parameter - tolerance -, and the time the convergence time

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

    '''
    initial_age = kwargs['startTage']
    initial_age_pl = kwargs['startTagePl']
    years_to_bh_pl = kwargs['y2bh_Pl']
    species_comp_pl = kwargs['SC_Pl']
    site_index = kwargs['SI_bh_Pl']
    present_density = kwargs['N_bh_PlT']
    density_at_bh_age = kwargs['N0_Pl']
    sdf_aw = kwargs['SDF_Aw0']
    sdf_sw = kwargs['SDF_Sw0']
    sdf_sb = kwargs['SDF_Sb0']
    basal_area_at_bh_age = kwargs['BA_Pl0']
    present_basal_area = kwargs['BA_PlT']
    simulation_choice = 'yes'
    # the start guess is critical. If it is too large,
    # it may crash before the simulation. 100 worked
    # for a sample os stands. 1000 failed
    factor = 100.0
    tolerance = 0.1
    within_tolerance = False
    iter_count = 0
    factor1 = 1.5* factor

    while not within_tolerance:
        ba_est = sim_basal_area_pl(initial_age, initial_age_pl, years_to_bh_pl,
                                   species_comp_pl, site_index, present_density,
                                   density_at_bh_age, sdf_aw, sdf_sw, sdf_sb,
                                   basal_area_at_bh_age, factor, simulation_choice)[-1]

        if abs(present_basal_area - ba_est) < tolerance:
            within_tolerance = True
        else:
            if (present_basal_area - ba_est) < 0:
                factor1 = factor
                factor_p = factor * (present_basal_area / ba_est)
                factor = (factor_p+factor)/2
            elif (present_basal_area - ba_est) > 0:
                factor = (factor + factor1)/2

        iter_count = iter_count + 1

        if iter_count == 150:
            LOGGER.warning(('Slow convergence with Basal Area: %s'
                            ' and factor:%s '), ba_est, factor)
            return factor

    return factor
