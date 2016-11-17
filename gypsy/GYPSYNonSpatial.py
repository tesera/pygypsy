"""Density

Acronyms:

b_hage = Breast Height Age
tage = Total age
si_Aw  =  estimated Site intex according to the paper in this case for Aspen (Aw)
y2bh = years until breast height age can be measured
SI_bh_Aw = Site index estimated with breast heigh age
N_bh_Aw = estimated N and should be equal N_Aw (for Aspen in this case Aw)

"""
# TODO: split these functions into appropriate other modules
# TODO: make all factor find functions use kwargs in the manner of AW
import logging
import numpy
import numpy as np
import pandas as pd

import basal_area_increment as incr
from gypsy.density import(
    estimate_density_aw,
    estimate_density_pl,
    estimate_density_sb,
    estimate_density_sw,
)
from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge


LOGGER = logging.getLogger(__name__)


# input - species, top height, total age, BHage (from the function),
#N (or density), current Basal Area,  Measured Percent Stocking,
#StumpDOB , StumpHeight, TopDib, SI, sp proportion
sp_Aw = ['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sb = ['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Pl = ['Pl', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sw = ['Sw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]


def SCestimate(N_Aw, N_Sb, N_Sw, N_Pl):
    '''This function calculates species composition based on their densities
    Constraint -> SC_Aw + SC_Sw + SC_Sb + SC_Pl ~1

    :param float N_Aw, N_Sb, N_Sw, and N_Pl: densities of the species Aw, Sb, Sw, and Pl

    '''
    N_total = N_Aw + N_Sb + N_Sw + N_Pl

    if N_total == 0:
        SC_Aw = 0
        SC_Sw = 0
        SC_Sb = 0
        SC_Pl = 0
    else:
        SC_Aw = N_Aw/N_total
        SC_Sw = N_Sw/N_total
        SC_Sb = N_Sb/N_total
        SC_Pl = N_Pl/N_total

    return SC_Aw, SC_Sw, SC_Sb, SC_Pl


def densities_and_SCs_to_250(**kwargs):
    '''The function returns density, species composition, top height estimates for
    all species along time, which is counted independently for each species.

    :param float startTage: It uses the oldest species as a reference to become the stand age
    :param float startTageAw, startTageSw, startTageSb, and startTagePl: species specific ages counted independently
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
    startTage = kwargs['startTage']
    startTageAw = kwargs['startTageAw']
    y2bh_Aw = kwargs['y2bh_Aw']
    startTageSw = kwargs['startTageSw']
    y2bh_Sw = kwargs['y2bh_Sw']
    startTageSb = kwargs['startTageSb']
    y2bh_Sb = kwargs['y2bh_Sb']
    startTagePl = kwargs['startTagePl']
    y2bh_Pl = kwargs['y2bh_Pl']
    SDF_Aw0 = kwargs['SDF_Aw0']
    SDF_Sw0 = kwargs['SDF_Sw0']
    SDF_Pl0 = kwargs['SDF_Pl0']
    SDF_Sb0 = kwargs['SDF_Sb0']
    SI_bh_Aw = kwargs['SI_bh_Aw']
    SI_bh_Sw = kwargs['SI_bh_Sw']
    SI_bh_Sb = kwargs['SI_bh_Sb']
    SI_bh_Pl = kwargs['SI_bh_Pl']
    densities_along_time = []
    startTageAwB = startTageAw
    startTageSwB = startTageSw
    startTagePlB = startTagePl
    startTageSbB = startTageSb
    t = 1

    while t < 250:
        tage_Aw = startTageAwB - startTage
        tage_Sw = startTageSwB - startTage
        tage_Pl = startTagePlB - startTage
        tage_Sb = startTageSbB - startTage
        bhage_Aw = tage_Aw - y2bh_Aw
        bhage_Sw = tage_Sw - y2bh_Sw
        bhage_Pl = tage_Pl - y2bh_Pl
        bhage_Sb = tage_Sb - y2bh_Sb

        if bhage_Aw < 0:
            N_bh_AwT = 0
        else:
            N_bh_AwT = estimate_density_aw(SDF_Aw0, bhage_Aw, SI_bh_Aw)

        if tage_Sb < 0:
            N_bh_SbT = 0
        else:
            N_bh_SbT = estimate_density_sb(SDF_Sb0, tage_Sb, SI_bh_Sb)

        if tage_Sw < 0:
            N_bh_SwT = 0
        else:
            N_bh_SwT = estimate_density_sw(SDF_Sw0, SDF_Aw0, tage_Sw, SI_bh_Sw)

        if tage_Pl < 0:
            N_bh_PlT = 0
        else:
            N_bh_PlT = estimate_density_pl(SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_Pl, SI_bh_Pl)



        if N_bh_AwT <= 0:
            topHeight_Aw = 0
        else:
            topHeight_Aw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Aw', SI_bh_Aw, tage_Aw)

        if N_bh_SbT <= 0:
            topHeight_Sb = 0
        else:
            topHeight_Sb = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sb', SI_bh_Sb, tage_Sb)

        if N_bh_SwT <= 0:
            topHeight_Sw = 0
        else:
            topHeight_Sw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sw', SI_bh_Sw, tage_Sw)

        if N_bh_PlT <= 0:
            topHeight_Pl = 0
        else:
            topHeight_Pl = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Pl', SI_bh_Pl, tage_Pl)


        SC_Aw, SC_Sw, SC_Sb, SC_Pl = SCestimate(N_bh_AwT, N_bh_SbT, N_bh_SwT, N_bh_PlT)

        densities_along_time.append({'N_bh_AwT': N_bh_AwT, 'N_bh_SwT': N_bh_SwT, 'N_bh_SbT': N_bh_SbT, 'N_bh_PlT': N_bh_PlT,
                                     'SC_Aw': SC_Aw, 'SC_Sw': SC_Sw, 'SC_Sb':SC_Sb, 'SC_Pl': SC_Pl,
                                     'tage_Aw': tage_Aw, 'tage_Sw': tage_Sw, 'tage_Sb': tage_Sb, 'tage_Pl': tage_Pl,
                                     'bhage_Aw': bhage_Aw, 'bhage_Sw': bhage_Sw, 'bhage_Sb': bhage_Sb, 'bhage_Pl': bhage_Pl,
                                     'topHeight_Aw': topHeight_Aw, 'topHeight_Sw': topHeight_Sw, 'topHeight_Sb': topHeight_Sb, 'topHeight_Pl': topHeight_Pl})
        t += 1
        startTageAwB += 1
        startTageSwB += 1
        startTagePlB += 1
        startTageSbB += 1

    return densities_along_time


def BAfactorFinder_Aw(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision one wants this estimate, which is
    given by the parameter - acceptableDiff -, and the time the convergence time

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
    :param float SI_bh_Aw: site index of species Aw
    :param float N_bh_AwT: density of sp Aw at time T (it varies over time)
    :param float BA_Aw0: basal area of Aw at breast height age, assumed to be very small
    :param float BA_AwT: basal area of Aw at time T
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float N0_Aw: initial density of species Aw at breast height age

    '''
    startTage = kwargs['startTage']
    SI_bh_Aw = kwargs['SI_bh_Aw']
    N_bh_AwT = kwargs['N_bh_AwT']
    BA_Aw0 = kwargs['BA_Aw0']
    BA_AwT = kwargs['BA_AwT']
    SDF_Aw0 = kwargs['SDF_Aw0']
    N0_Aw = kwargs['N0_Aw']
    densities = kwargs['densities']
    simulation_choice = 'yes'
    f_Aw = 100
    f_AwP1 = 100 * f_Aw
    acceptableDiff = 0.01 * BA_AwT
    BADiffFlag = False
    iterCount = 0

    while BADiffFlag == False:
        BA_AwB = BAfromZeroToDataAw(startTage, SI_bh_Aw, N0_Aw,
                                    BA_Aw0, SDF_Aw0, f_Aw, densities,
                                    simulation_choice)[-1]

        if abs(BA_AwT - BA_AwB) < acceptableDiff:
            BADiffFlag = True
        else:
            if (BA_AwT - BA_AwB) < 0:
                f_AwP1 = f_Aw
                f_AwP = f_Aw  *  (1+(numpy.log10(BA_AwT) - numpy.log10(abs(BA_AwB)))/ (100*numpy.log10(abs(BA_AwB))))
                f_Aw = (f_AwP+f_Aw)/2
            elif (BA_AwT - BA_AwB) > 0:
                f_AwN = f_Aw * (1+(numpy.log10(BA_AwT) + numpy.log10(abs(BA_AwB)))/ (100* numpy.log10(abs(BA_AwB))))
                f_Aw = (f_Aw+f_AwP1)/2

        iterCount = iterCount + 1

        if iterCount == 10000:
            LOGGER.warning(('GYPSYNonSpatial.BAfactorFinder_Aw()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_AwB, f_Aw)
            return f_Aw
    return f_Aw


def BAfromZeroToDataAw(startTage, SI_bh_Aw, N0_Aw, BA_Aw0, SDF_Aw0, f_Aw,
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
    LOGGER.debug('getting basal area from time zero to time of data for aspen')

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


def BAfactorFinder_Sb(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision with one wants this estimate, which is
    given by the parameter - acceptableDiff -, and the time the convergence time

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
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
    startTage = kwargs['startTage']
    startTageSb = kwargs['startTageSb']
    y2bh_Sb = kwargs['y2bh_Sb']
    SC_Sb = kwargs['SC_Sb']
    SI_bh_Sb = kwargs['SI_bh_Sb']
    N_bh_SbT = kwargs['N_bh_SbT']
    N0_Sb = kwargs['N0_Sb']
    BA_Sb0 = kwargs['BA_Sb0']
    BA_SbT = kwargs['BA_SbT']
    simulation_choice = 'yes'
    f_Sb = 1.2
    f_SbP1 = 1.5 * f_Sb
    acceptableDiff = 0.1
    BADiffFlag = False
    iterCount = 0

    while BADiffFlag == False:
        BA_SbB = BAfromZeroToDataSb(startTage, startTageSb, y2bh_Sb,
                                    SC_Sb, SI_bh_Sb, N_bh_SbT, N0_Sb,
                                    BA_Sb0, f_Sb, simulation_choice)[-1]

        if abs(BA_SbT - BA_SbB) < acceptableDiff:
            BADiffFlag = True
        else:
            if (BA_SbT - BA_SbB) < 0:
                f_SbP1 = f_Sb
                f_SbP = f_Sb  *  (1+(numpy.log10(BA_SbT) - numpy.log10(abs(BA_SbB)))/ (10*numpy.log10(abs(BA_SbB))))
                f_Sb = (f_SbP+f_Sb)/2
            elif (BA_SbT - BA_SbB) > 0:
                f_Sb = (f_Sb+f_SbP1)/2

        iterCount = iterCount + 1

        if iterCount == 1500:
            LOGGER.warning(('GYPSYNonSpatial.BAfactorFinder_Sb()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_SbB, f_Sb)
            return f_Sb

    return f_Sb


def BAfromZeroToDataSb(startTage, startTageSb, y2bh_Sb, SC_Sb, SI_bh_Sb,
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


def BAfactorFinder_Sw(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision with one wants this estimate, which is
    given by the parameter - acceptableDiff -, and the time the convergence time

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
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
    startTage = kwargs['startTage']
    startTageSw = kwargs['startTageSw']
    y2bh_Sw = kwargs['y2bh_Sw']
    SC_Sw = kwargs['SC_Sw']
    SI_bh_Sw = kwargs['SI_bh_Sw']
    N_bh_SwT = kwargs['N_bh_SwT']
    N0_Sw = kwargs['N0_Sw']
    SDF_Aw0 = kwargs['SDF_Aw0']
    SDF_Pl0 = kwargs['SDF_Pl0']
    SDF_Sb0 = kwargs['SDF_Sb0']
    BA_Sw0 = kwargs['BA_Sw0']
    BA_SwT = kwargs['BA_SwT']
    simulation_choice = 'yes'
    f_Sw = 2.5
    BA_SwB = BA_Sw0
    acceptableDiff = 0.1
    BADiffFlag = False
    iterCount = 0
    f_SwP1 = 1.5* f_Sw

    while BADiffFlag == False:
        BA_SwB = BAfromZeroToDataSw(startTage, startTageSw, y2bh_Sw,
                                    SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw,
                                    SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0,
                                    f_Sw, simulation_choice)[-1]
        if abs(BA_SwT - BA_SwB) < acceptableDiff:
            BADiffFlag = True
        else:
            if (BA_SwT - BA_SwB) < 0:
                f_SwP1 = f_Sw
                f_SwP = f_Sw  *  (1+(numpy.log10(BA_SwT) - numpy.log10(abs(BA_SwB)))/ (10*numpy.log10(abs(BA_SwB))))
                f_Sw = (f_SwP+f_Sw)/2
            elif (BA_SwT - BA_SwB) > 0:
                f_Sw = (f_Sw + f_SwP1)/2

        iterCount = iterCount + 1

        if iterCount == 1500:
            LOGGER.warning(('GYPSYNonSpatial.BAfactorFinder_Sw()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_SwB, f_Sw)
            return f_Sw

    return f_Sw


def BAfromZeroToDataSw(startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw,
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


def BAfactorFinder_Pl(**kwargs):
    '''This function guarantees that the trajectory of the species basal area
    passes through the basal area measured when the data was collected
    (inventory data)

    There is a trade-off between the precision with one wants this estimate, which is
    given by the parameter - acceptableDiff -, and the time the convergence time

    :param float startTage: Clock that uses the oldest species as a reference to become the stand age
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
    startTage = kwargs['startTage']
    startTagePl = kwargs['startTagePl']
    y2bh_Pl = kwargs['y2bh_Pl']
    SC_Pl = kwargs['SC_Pl']
    SI_bh_Pl = kwargs['SI_bh_Pl']
    N_bh_PlT = kwargs['N_bh_PlT']
    N0_Pl = kwargs['N0_Pl']
    SDF_Aw0 = kwargs['SDF_Aw0']
    SDF_Sw0 = kwargs['SDF_Sw0']
    SDF_Sb0 = kwargs['SDF_Sb0']
    BA_Pl0 = kwargs['BA_Pl0']
    BA_PlT = kwargs['BA_PlT']
    simulation_choice = 'yes'
    # the start guess is critical. If it is too large,
    # it may crash before the simulation. 100 worked
    # for a sample os stands. 1000 failed
    f_Pl = 100
    acceptableDiff = 0.1
    BADiffFlag = False
    iterCount = 0
    f_PlP1 = 1.5* f_Pl

    while BADiffFlag == False:
        BA_PlB = BAfromZeroToDataPl(startTage, startTagePl, y2bh_Pl,
                                    SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl,
                                    SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, f_Pl,
                                    simulation_choice)[-1]

        if abs(BA_PlT - BA_PlB) < acceptableDiff:
            BADiffFlag = True
        else:
            if (BA_PlT - BA_PlB) < 0:
                f_PlP1 = f_Pl
                f_PlP = f_Pl * (BA_PlT / BA_PlB)
                f_Pl = (f_PlP+f_Pl)/2
            elif (BA_PlT - BA_PlB) > 0:
                f_Pl = (f_Pl + f_PlP1)/2

        iterCount = iterCount + 1

        if iterCount == 150:
            LOGGER.warning(('GYPSYNonSpatial.BAfactorFinder_Pl()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_PlB, f_Pl)
            return f_Pl

    return f_Pl


def BAfromZeroToDataPl(startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl,
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
