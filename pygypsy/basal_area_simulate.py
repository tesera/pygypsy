"""Basal Area Simulation"""
#pylint: disable=no-member
import logging
import numpy as np

from pygypsy import basal_area_increment as incr


LOGGER = logging.getLogger(__name__)


def sim_basal_area_aw(initial_age, site_index, density_at_bh_age,
                      basal_area_at_bh_age, sdf_aw, correction_factor,
                      densities, simulation_choice):
    '''Simlulate basal area forward in time for White Aspen

    It creates the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float initial_age: Clock that uses the oldest species as a reference
                              to become the stand age
    :param float site_index: site index of species Aw
    :param float basal_area_at_bh_age: basal area of Aw at breast height age
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float density_at_bh_age: initial density of species Aw at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop
                                  at the date of the inventory or will continue until
                                  year 250
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory

    '''
    if simulation_choice == 'yes':
        max_age = initial_age
    elif simulation_choice == 'no':
        max_age = 250

    basal_area_aw_arr = np.zeros(max_age)
    basal_area_temp = basal_area_at_bh_age

    for i, spec_comp_dict in enumerate(densities[0: max_age]):
        bh_age_aw = spec_comp_dict['bhage_Aw']
        spec_comp = spec_comp_dict['SC_Aw']
        present_density = spec_comp_dict['N_bh_AwT']

        if density_at_bh_age > 0:
            if bh_age_aw > 0:
                spec_comp = spec_comp * correction_factor
                basal_area_increment = incr.increment_basal_area_aw(
                    'Aw', spec_comp, site_index, present_density,
                    density_at_bh_age, bh_age_aw, basal_area_temp
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


def sim_basal_area_sb(initial_age, initial_age_sb, years_to_bh_sb, spec_comp, site_index,
                      present_density, density_at_bh_age, basal_area_at_bh_age,
                      correction_factor, simulation_choice):
    '''Simlulate basal area forward in time for Black Spruce

    It creates the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float initial_age: Clock that uses the oldest species as a reference to become
                              the stand age
    :param float initial_age_sb: species specific age counted independently
    :param float years_to_bh_sb: time elapseed in years from zero to breast height age
                                 of Sb
    :param float spec_comp: proportion of basal area for Sb
    :param float site_index: site index of species Sb
    :param float basal_area_at_bh_age: basal area of Sb at breast height age
    :param float present_density: density of species Sb at time T
    :param float density_at_bh_age: initial density of species Sb at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop at
                                  the date of the inventory or continue until year 250
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory

    '''
    if simulation_choice == 'yes':
        max_age = initial_age
    elif simulation_choice == 'no':
        max_age = 250

    year = 0
    basal_area_arr = np.zeros(max_age)
    basal_area_temp = basal_area_at_bh_age

    while year < max_age:
        tage_sb = initial_age_sb - initial_age
        bh_age_sb = tage_sb - years_to_bh_sb

        if density_at_bh_age > 0:
            if bh_age_sb > 0:
                spec_comp = spec_comp * correction_factor
                basal_area_increment = incr.increment_basal_area_sb(
                    'Sb', spec_comp, site_index, present_density,
                    density_at_bh_age, bh_age_sb, basal_area_temp
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

        basal_area_arr[year] = new_basal_area

        year += 1
        initial_age_sb += 1

    return basal_area_arr


def sim_basal_area_sw(initial_age, intial_age_sw, years_to_bh, spec_comp, site_index,
                      present_density, density_at_bh_age, sdf_aw, sdf_pl, sdf_sb,
                      basal_area_at_bh_age, correction_factor, simulation_choice):
    '''Simlulate basal area forward in time for White Spruce
    It created the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float initial_age: Clock that uses the oldest species as a reference to
                              become the stand age
    :param float intial_age: species specific age counted independently
    :param float years_to_bh: time elapseed in years from zero to breast height
                              age of sp Sw
    :param float spec_comp: proportion of basal area for Sw
    :param float site_index: site index of species Sw
    :param float basal_area_at_bh_age: basal area of Sw at breast height age
    :param float present_density: density of species Sw at time T
    :param float density_at_bh_age: initial density of species Sw at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop
                                  at the date of the inventory or will continue until
                                  year 250
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory
    :param float sdf_pl: Stand Density Factor of species Pl
    :param float sdf_aw: Stand Density Factor of species Aw
    :param float sdf_sb: Stand Density Factor of species Sb

    '''
    if simulation_choice == 'yes':
        max_age = initial_age
    elif simulation_choice == 'no':
        max_age = 250

    basal_area_arr = np.zeros(max_age)
    year = 0
    basal_area_temp = basal_area_at_bh_age

    while year < max_age:
        tage = intial_age_sw - initial_age
        bh_age_sw = tage - years_to_bh

        if density_at_bh_age > 0:
            if bh_age_sw > 0:
                spec_comp = spec_comp * correction_factor
                basal_area_increment = incr.increment_basal_area_sw(
                    'Sw', spec_comp, site_index, present_density, density_at_bh_age,
                    bh_age_sw, sdf_aw, sdf_pl, sdf_sb, basal_area_temp
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

        basal_area_arr[year] = new_basal_area

        year += 1
        intial_age_sw += 1

    return basal_area_arr


def sim_basal_area_pl(initial_age, initial_age_pl, years_to_bh, spec_comp, site_index,
                      present_density, density_at_bh_age, sdf_aw, sdf_sw, sdf_sb,
                      basal_area_at_bh_age, correction_factor, simulation_choice):
    '''Simlulate basal area forward in time for Lodgepole Pine

    :param float initial_age: Clock that uses the oldest species as a reference to
                              become the stand age
    :param float initial_age: species specific age counted independently
    :param float years_to_bh: time elapseed in years from zero to breast height age for
                              species Pl
    :param float spec_comp: proportion of basal area for Pl
    :param float site_index: site index of species Pl
    :param float basal_area_at_bh_age: basal area of Pl at breast height age
    :param float present_density: density of species Pl at time T
    :param float density_at_bh_age: initial density of species Pl at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop at
                                  the date of the inventory or continue until year 250
    :param float correction_factor: correction factor that guarantees that trajectory
                                    passes through data obtained with inventory
    :param float sdf_sw: Stand Density Factor of species Sw
    :param float sdf_aw: Stand Density Factor of species Aw
    :param float sdf_sb: Stand Density Factor of species Sb

    '''
    if simulation_choice == 'yes':
        max_age = initial_age
    elif simulation_choice == 'no':
        max_age = 250

    basal_area_arr = np.zeros(max_age)
    year = 0
    basal_area_temp = basal_area_at_bh_age

    while year < max_age:
        tage = initial_age_pl - initial_age
        bh_age_pl = tage - years_to_bh
        if density_at_bh_age > 0:
            if bh_age_pl > 0:
                basal_area_increment = correction_factor \
                                       * incr.increment_basal_area_pl(
                                           'Pl', spec_comp, site_index, present_density,
                                           density_at_bh_age, bh_age_pl, sdf_aw, sdf_sw,
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

        basal_area_arr[year] = new_basal_area

        year += 1
        initial_age_pl += 1

    return basal_area_arr
