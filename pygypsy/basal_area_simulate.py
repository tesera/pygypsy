"""Basal Area Simulation"""
#pylint: disable=no-member
# these  functions can be improved because the increment is not
# autoregressive, so we can calculate it as a vector operation using
# the other arrays then the actual values are just the cumulative sums
# TODO: change initial age to data age
# TODO: change present density to density_at_data

import logging
import numpy as np

from pygypsy import basal_area_increment as incr


LOGGER = logging.getLogger(__name__)


# TODO: make this consistent with the other functions will need an option for
# making species proportion constant and not expentially increasing with the factor
def sim_basal_area_aw(initial_age, site_index, density_at_bh_age,
                      basal_area_at_bh_age, sdf_aw, correction_factor, densities,
                      use_correction_factor_future=False,
                      stop_at_initial_age=True,
                      fix_proportion_and_density_to_initial_age=False,
                      species_proportion_at_bh_age=None, present_density=None,
                      force_use_densities=False):
    '''Simlulate basal area forward in time for White Aspen

    It creates the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float initial_age: Clock that uses the oldest species as a reference
                              to become the stand age
    :param float site_index: site index of species Aw
    :param float basal_area_at_bh_age: basal area of Aw at breast height age
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float density_at_bh_age: initial density of species Aw at breast height age
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory
    :param bool use_correction_factor_future: switch that determine whether the correction
                                              factor will be used for the future years
    :param bool stop_at_initial_age: switch that determines whether simulation
                                     will stop at the date of the inventory or
                                     will continue for the length of the densities object
    :param bool fix_proportion_and_density_to_initial_age: if true, uses the
    proportion and density from the initial age for all years of the
    simulation. this is provided for consistency with a previous version which
    did this implicityly in for estiamting the basal area factors
    :param bool force_use_densities: ignore other parameters and just use them                                     densities object for calculating basal
                                     area increment

    '''
    max_age = initial_age if stop_at_initial_age else len(densities)

    basal_area_aw_arr = np.zeros(max_age)
    basal_area_temp = basal_area_at_bh_age

    for i, spec_comp_dict in enumerate(densities[0: max_age]):
        sc_factor = correction_factor \
                    if i < initial_age or use_correction_factor_future \
                       else 1
        if force_use_densities:
            years_from_bhage = spec_comp_dict['bhage_Aw']
            spec_proportion = spec_comp_dict['SC_Aw']
            present_density = spec_comp_dict['N_bh_AwT']
        else:
            years_from_bhage = spec_comp_dict['bhage_Aw']
            # TODO: revise to match the funcs of the other species
            spec_proportion = densities[initial_age]['SC_Aw'] \
                              if fix_proportion_and_density_to_initial_age \
                                 else spec_comp_dict['SC_Aw']
            present_density = densities[initial_age]['N_bh_AwT'] \
                              if fix_proportion_and_density_to_initial_age \
                                 else spec_comp_dict['N_bh_AwT']

        if density_at_bh_age > 0:
            if years_from_bhage > 0:
                spec_proportion = spec_proportion * sc_factor
                basal_area_increment = incr.increment_basal_area_aw(
                    spec_proportion, site_index, present_density,
                    density_at_bh_age, years_from_bhage, basal_area_temp
                )
                basal_area_temp = basal_area_temp + basal_area_increment
                new_basal_area = basal_area_temp

                if new_basal_area < 0:
                    new_basal_area = 0
            else:
                new_basal_area = 0
        else:
            basal_area_temp = 0
            new_basal_area = 0

        basal_area_aw_arr[i] = new_basal_area

    return basal_area_aw_arr


def sim_basal_area_sb(initial_age, site_index, density_at_bh_age,
                      basal_area_at_bh_age, correction_factor, densities,
                      use_correction_factor_future=False,
                      stop_at_initial_age=True,
                      fix_proportion_and_density_to_initial_age=False,
                      species_proportion_at_bh_age=None, present_density=None,
                      force_use_densities=False):
    '''Simlulate basal area forward in time for Black Spruce

    It creates the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float initial_age: Clock that uses the oldest species as a reference to become
                              the stand age
    :param float initial_age_sb: species specific age counted independently
    :param float site_index: site index of species Sb
    :param float basal_area_at_bh_age: basal area of Sb at breast height age
    :param float density_at_bh_age: initial density of species Sb at breast height age
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory
    :param bool use_correction_factor_future: switch that determine whether the correction
                                              factor will be used for the future years
    :param bool stop_at_initial_age: switch that determines whether simulation
                                     will stop at the date of the inventory or
                                     will continue for the length of the densities object

    :param bool fix_proportion_and_density_to_initial_age: if true, uses the
    proportion and density from the initial age for all years of the
    simulation. this is provided for consistency with a previous version which
    did this implicityly in for estiamting the basal area factors
    :param bool force_use_densities: ignore other parameters and just use them                                     densities object for calculating basal
                                     area increment

    '''
    max_age = initial_age if stop_at_initial_age else len(densities)
    basal_area_arr = np.zeros(max_age)
    basal_area_temp = basal_area_at_bh_age

    for i, spec_comp_dict in enumerate(densities[0: max_age]):
        sc_factor = correction_factor \
                    if i < initial_age or use_correction_factor_future \
                       else 1
        if force_use_densities:
            years_from_bhage = spec_comp_dict['bhage_Aw']
            spec_proportion = spec_comp_dict['SC_Aw']
            present_density = spec_comp_dict['N_bh_AwT']
        else:
            years_from_bhage = spec_comp_dict['bhage_Sb']
            if i==0:
                spec_proportion = species_proportion_at_bh_age
            elif i < initial_age:
                pass
            else:
                spec_proportion = spec_comp_dict['SC_Sw']
            present_density = present_density \
                              if i < initial_age or fix_proportion_and_density_to_initial_age \
                              else spec_comp_dict['N_bh_SbT']

        if density_at_bh_age > 0:
            if years_from_bhage > 0:
                spec_proportion = spec_proportion * sc_factor
                basal_area_increment = incr.increment_basal_area_sb(
                    spec_proportion, site_index, present_density,
                    density_at_bh_age, years_from_bhage, basal_area_temp
                )
                basal_area_temp = basal_area_temp + basal_area_increment
                new_basal_area = basal_area_temp

                if new_basal_area < 0:
                    new_basal_area = 0
            else:
                new_basal_area = 0
        else:
            basal_area_temp = 0
            new_basal_area = 0

        basal_area_arr[i] = new_basal_area

    return basal_area_arr


def sim_basal_area_sw(initial_age, site_index, density_at_bh_age, sdf_aw,
                      sdf_pl, sdf_sb, basal_area_at_bh_age, correction_factor,
                      densities, use_correction_factor_future=False,
                      stop_at_initial_age=True,
                      fix_proportion_and_density_to_initial_age=False,
                      species_proportion_at_bh_age=None, present_density=None,
                      force_use_densities=False):
    '''Simlulate basal area forward in time for White Spruce
    It created the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float initial_age: Clock that uses the oldest species as a reference to
                              become the stand age
    :param float site_index: site index of species Sw
    :param float basal_area_at_bh_age: basal area of Sw at breast height age
    :param float density_at_bh_age: initial density of species Sw at breast height age
    :param float sdf_pl: Stand Density Factor of species Pl
    :param float sdf_aw: Stand Density Factor of species Aw
    :param float sdf_sb: Stand Density Factor of species Sb
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory
    :param bool use_correction_factor_future: switch that determine whether the correction
                                              factor will be used for the future years
    :param bool stop_at_initial_age: switch that determines whether simulation
                                     will stop at the date of the inventory or
                                     will continue for the length of the densities object
    :param bool fix_proportion_and_density_to_initial_age: if true, uses the
    proportion and density from the initial age for all years of the
    simulation. this is provided for consistency with a previous version which
    did this implicityly in for estiamting the basal area factors
    :param bool force_use_densities: ignore other parameters and just use them                                     densities object for calculating basal
                                     area increment

    '''
    max_age = initial_age if stop_at_initial_age else len(densities)
    basal_area_arr = np.zeros(max_age)
    basal_area_temp = basal_area_at_bh_age

    # some of the conditional assignments in this loop could be simplified by
    # initializing them outside the loop and assigning them when the simulation
    # passes the initial age. this is not done because we are striving to reach
    # a place where these are more configurable and thus easier to test
    for i, spec_comp_dict in enumerate(densities[0: max_age]):
        sc_factor = correction_factor \
                    if i < initial_age or use_correction_factor_future\
                       else 1
        if force_use_densities:
            years_from_bhage = spec_comp_dict['bhage_Aw']
            spec_proportion = spec_comp_dict['SC_Aw']
            present_density = spec_comp_dict['N_bh_AwT']
        else:
            years_from_bhage = spec_comp_dict['bhage_Sw']
            # the first time in this for loop, spec proportion must be assigned
            if i==0:
                spec_proportion = species_proportion_at_bh_age
            # until the year of the data is reached we then do not reassign it, and the
            # value of spec_proportion * sc_factor increases exponentially
            elif i < initial_age:
                pass
            # future values use the estimated species proportion and it is constant
            else:
                spec_proportion = spec_comp_dict['SC_Sw']
            present_density = present_density \
                              if i < initial_age or fix_proportion_and_density_to_initial_age \
                              else spec_comp_dict['N_bh_SwT']

        if density_at_bh_age > 0:
            if years_from_bhage > 0:
                spec_proportion = spec_proportion * sc_factor
                basal_area_increment = incr.increment_basal_area_sw(
                    spec_proportion, site_index, present_density,
                    density_at_bh_age, years_from_bhage, sdf_aw, sdf_pl,
                    sdf_sb, basal_area_temp
                )
                basal_area_temp = basal_area_temp + basal_area_increment
                new_basal_area = basal_area_temp

                if new_basal_area < 0:
                    new_basal_area = 0
            else:
                new_basal_area = 0
        else:
            basal_area_temp = 0
            new_basal_area = 0

        basal_area_arr[i] = new_basal_area

    return basal_area_arr


def sim_basal_area_pl(initial_age, site_index, density_at_bh_age, sdf_aw,
                      sdf_sw, sdf_sb, basal_area_at_bh_age, correction_factor,
                      densities, use_correction_factor_future=False,
                      stop_at_initial_age=True,
                      fix_proportion_and_density_to_initial_age=False,
                      species_proportion_at_bh_age=None, present_density=None,
                      force_use_densities=False):
    '''Simlulate basal area forward in time for Lodgepole Pine

    :param float initial_age: Clock that uses the oldest species as a reference to
                              become the stand age
    :param float site_index: site index of species Pl
    :param float basal_area_at_bh_age: basal area of Pl at breast height age
    :param float density_at_bh_age: initial density of species Pl at breast height age
    :param float sdf_sw: Stand Density Factor of species Sw
    :param float sdf_aw: Stand Density Factor of species Aw
    :param float sdf_sb: Stand Density Factor of species Sb
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory
    :param bool use_correction_factor_future: switch that determine whether the correction
                                              factor will be used for the future years
    :param bool stop_at_initial_age: switch that determines whether simulation
                                     will stop at the date of the inventory or
                                     will continue for the length of the densities object
    :param bool fix_proportion_and_density_to_initial_age: if true, uses the
    proportion and density from the initial age for all years of the
    simulation. this is provided for consistency with a previous version which
    did this implicityly in for estiamting the basal area factors
    :param bool force_use_densities: ignore other parameters and just use them                                     densities object for calculating basal
                                     area increment

    '''
    max_age = initial_age if stop_at_initial_age else len(densities)
    basal_area_arr = np.zeros(max_age)
    basal_area_temp = basal_area_at_bh_age

    for i, spec_comp_dict in enumerate(densities[0: max_age]):
        sc_factor = correction_factor \
                    if i < initial_age or use_correction_factor_future \
                       else 1
        if force_use_densities:
            years_from_bhage = spec_comp_dict['bhage_Aw']
            spec_proportion = spec_comp_dict['SC_Aw']
            present_density = spec_comp_dict['N_bh_AwT']
        else:
            years_from_bhage = spec_comp_dict['bhage_Pl']
            # the first time in this for loop, spec proportion must be assigned
            if i==0:
                spec_proportion = species_proportion_at_bh_age
            # until the year of the data is reached we then do not reassign it, and the
            # value of spec_proportion * sc_factor increases exponentially
            elif i < initial_age:
                pass
            # future values use the estimated species proportion and it is constant
            else:
                spec_proportion = spec_comp_dict['SC_Pl']
            present_density = present_density \
                              if i < initial_age or fix_proportion_and_density_to_initial_age \
                              else spec_comp_dict['N_bh_PlT']

        if density_at_bh_age > 0:
            if years_from_bhage > 0:
                # factor empirically determined to work better when multiplied
                # with whole increment
                basal_area_increment = sc_factor \
                                       * incr.increment_basal_area_pl(
                                           spec_proportion, site_index,
                                           present_density, density_at_bh_age,
                                           years_from_bhage, sdf_aw, sdf_sw,
                                           sdf_sb, basal_area_temp
                                       )
                basal_area_temp = basal_area_temp + basal_area_increment
                new_basal_area = basal_area_temp

                if new_basal_area < 0:
                    new_basal_area = 0
            else:
                new_basal_area = 0
        else:
            basal_area_temp = 0
            new_basal_area = 0

        basal_area_arr[i] = new_basal_area

    return basal_area_arr
