"""Basal Area Simulation"""
import logging
import numpy as np

from gypsy import basal_area_increment as incr


LOGGER = logging.getLogger(__name__)


def sim_basal_area_aw(startTage, SI_bh_Aw, N0_Aw, BA_Aw0, SDF_Aw0, f_Aw,
                       densities, simulation_choice):
    '''This is a function that supports factor finder functions.

    It creates the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
    :param float SI_bh_Aw: site index of species Aw
    :param float BA_Aw0: basal area of Aw at breast height age, assumed to be very small
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float N0_Aw: initial density of species Aw at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop at the
    date of the inventory or will continue until year 250
    :param float f_Aw: correction factor that guarantees that trajectory passes through
    data obtained with inventory

    '''
    if simulation_choice == 'yes':
        max_age = startTage
    elif simulation_choice == 'no':
        max_age = 250

    basal_area_aw_arr = np.zeros(max_age)
    BA_tempAw = BA_Aw0

    for i, SC_Dict in enumerate(densities[0: max_age]):
        bhage_Aw = SC_Dict['bhage_Aw']
        SC_Aw = SC_Dict['SC_Aw']
        N_bh_AwT = SC_Dict['N_bh_AwT']

        if N0_Aw > 0:
            if bhage_Aw > 0:
                SC_Aw = (SC_Aw) * f_Aw
                BAinc_Aw = incr.increment_basal_area_aw('Aw', SC_Aw, SI_bh_Aw, N_bh_AwT,
                                                          N0_Aw, bhage_Aw, BA_tempAw)
                BA_tempAw = BA_tempAw + BAinc_Aw
                BA_AwB = BA_tempAw
                if BA_AwB < 0:
                    BA_AwB = 0
            else:
                BA_AwB = 0
        else:
            BA_tempAw = 0
            BA_AwB = 0

        basal_area_aw_arr[i] = BA_AwB

    return basal_area_aw_arr


def sim_basal_area_sb(startTage, startTageSb, y2bh_Sb, SC_Sb, SI_bh_Sb,
                       N_bh_SbT, N0_Sb, BA_Sb0, f_Sb, simulation_choice):
    '''This is a function that supports factor finder functions.

    It creates the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
    :param float startTageSb: species specific age counted independently
    :param float y2bh_Sb: time elapseed in years from zero to breast height age of sp Sb
    :param float SI_bh_Sb: site index of species Sb
    :param float BA_Sb0: basal area of Sb at breast height age, assumed to be very small
    :param float N_bh_SbT: density of species Sb at time T
    :param float N0_Sb: initial density of species Sb at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop at the
    date of the inventory or will continue until year 250
    :param float f_Sb: correction factor that guarantees that trajectory passes through
    data obtained with inventory

    '''
    if simulation_choice == 'yes':
        max_age = startTage
    elif simulation_choice == 'no':
        max_age = 250

    t = 0
    basal_area_arr = np.zeros(max_age)
    BA_tempSb = BA_Sb0

    while t < max_age:
        tage_Sb = startTageSb - startTage
        bhage_Sb = tage_Sb - y2bh_Sb

        if N0_Sb > 0:
            if bhage_Sb > 0:
                SC_Sb = (SC_Sb) * f_Sb
                BAinc_Sb = incr.increment_basal_area_sb('Sb', SC_Sb, SI_bh_Sb, N_bh_SbT,
                                                          N0_Sb, bhage_Sb, BA_tempSb)
                BA_tempSb = BA_tempSb + BAinc_Sb
                BA_SbB = BA_tempSb
                if BA_SbB < 0:
                    BA_SbB = 0
            else:
                BA_SbB = 0
        else:
            BA_tempSb = 0
            BA_SbB = 0

        basal_area_arr[t] = BA_SbB

        t += 1
        startTageSb += 1

    return basal_area_arr


def sim_basal_area_sw(startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw,
                       N_bh_SwT, N0_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0,
                       f_Sw, simulation_choice):
    '''This is a function that supports factor finder functions.

    It created the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
    :param float startTageSw: species specific age counted independently
    :param float y2bh_Sw: time elapseed in years from zero to breast height age of sp Sw
    :param float SI_bh_Sw: site index of species Sw
    :param float BA_Sw0: basal area of Sw at breast height age, assumed to be very small
    :param float N_bh_SwT: density of species Sw at time T
    :param float N0_Sw: initial density of species Sw at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop at the
    date of the inventory or will continue until year 250
    :param float f_Sw: correction factor that guarantees that trajectory passes through
    data obtained with inventory
    :param float SDF_Pl0: Stand Density Factor of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb

    '''
    if simulation_choice == 'yes':
        max_age = startTage
    elif simulation_choice == 'no':
        max_age = 250

    basal_area_arr = np.zeros(max_age)
    t = 0
    BA_tempSw = BA_Sw0

    while t < max_age:
        tage_Sw = startTageSw - startTage
        bhage_Sw = tage_Sw - y2bh_Sw

        if N0_Sw > 0:
            if bhage_Sw > 0:
                SC_Sw = (SC_Sw) * f_Sw
                BAinc_Sw = incr.increment_basal_area_sw('Sw', SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_tempSw)
                BA_tempSw = BA_tempSw + BAinc_Sw
                BA_SwB = BA_tempSw
                if BA_SwB < 0:
                    BA_SwB = 0
            else:
                BA_SwB = 0
        else:
            BA_tempSw = 0
            BA_SwB = 0

        basal_area_arr[t] = BA_SwB

        t += 1
        startTageSw += 1

    return basal_area_arr


def sim_basal_area_pl(startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl,
                       N_bh_PlT, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0,
                       f_Pl, simulation_choice):
    '''This is a function that supports factor finder functions.

    It created the trajectory of basal area from bhage up to the inventory year
    given a correction factor that is being optimized

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
    :param float startTagePl: species specific age counted independently
    :param float y2bh_Pl: time elapseed in years from zero to breast height age of sp Pl
    :param float SI_bh_Pl: site index of species Pl
    :param float BA_Pl0: basal area of Pl at breast height age, assumed to be very small
    :param float N_bh_PlT: density of species Pl at time T
    :param float N0_Pl: initial density of species Pl at breast height age
    :param str simulation_choice: switch that determines whether simulation will stop at the
    date of the inventory or will continue until year 250
    :param float f_Pl: correction factor that guarantees that trajectory passes through
    data obtained with inventory
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb

    '''
    if simulation_choice == 'yes':
        max_age = startTage
    elif simulation_choice == 'no':
        max_age = 250

    basal_area_arr = np.zeros(max_age)
    t = 0
    BA_tempPl = BA_Pl0

    while t < max_age:
        tage_Pl = startTagePl - startTage
        bhage_Pl = tage_Pl - y2bh_Pl
        if N0_Pl > 0:
            if bhage_Pl > 0:
                BAinc_Pl = f_Pl * incr.increment_basal_area_pl('Pl', SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl,
                                                                 bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_tempPl)
                BA_tempPl = BA_tempPl + BAinc_Pl
                BA_PlB = BA_tempPl
                if BA_PlB < 0:
                    BA_PlB = 0
            else:
                BA_PlB = 0
        else:
            BA_tempPl = 0
            BA_PlB = 0

        basal_area_arr[t] = BA_PlB

        t += 1
        startTagePl += 1

    return basal_area_arr
