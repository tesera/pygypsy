"""Basal Area correction factor estimators"""
#pylint: disable=no-member
import logging
import numpy as np

from gypsy.basal_area_simulate import (
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
        BA_AwB = sim_basal_area_aw(startTage, SI_bh_Aw, N0_Aw,
                                    BA_Aw0, SDF_Aw0, f_Aw, densities,
                                    simulation_choice)[-1]

        if abs(BA_AwT - BA_AwB) < acceptableDiff:
            BADiffFlag = True
        else:
            if (BA_AwT - BA_AwB) < 0:
                f_AwP1 = f_Aw
                f_AwP = f_Aw  *  (1+(np.log10(BA_AwT) - np.log10(abs(BA_AwB)))/ (100*np.log10(abs(BA_AwB))))
                f_Aw = (f_AwP+f_Aw)/2
            elif (BA_AwT - BA_AwB) > 0:
                f_AwN = f_Aw * (1+(np.log10(BA_AwT) + np.log10(abs(BA_AwB)))/ (100* np.log10(abs(BA_AwB))))
                f_Aw = (f_Aw+f_AwP1)/2

        iterCount = iterCount + 1

        if iterCount == 10000:
            LOGGER.warning(('GYPSYNonSpatial.estimate_basal_area_factor_aw()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_AwB, f_Aw)
            return f_Aw
    return f_Aw


def estimate_basal_area_factor_sb(**kwargs):
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
        BA_SbB = sim_basal_area_sb(startTage, startTageSb, y2bh_Sb,
                                    SC_Sb, SI_bh_Sb, N_bh_SbT, N0_Sb,
                                    BA_Sb0, f_Sb, simulation_choice)[-1]

        if abs(BA_SbT - BA_SbB) < acceptableDiff:
            BADiffFlag = True
        else:
            if (BA_SbT - BA_SbB) < 0:
                f_SbP1 = f_Sb
                f_SbP = f_Sb  *  (1+(np.log10(BA_SbT) - np.log10(abs(BA_SbB)))/ (10*np.log10(abs(BA_SbB))))
                f_Sb = (f_SbP+f_Sb)/2
            elif (BA_SbT - BA_SbB) > 0:
                f_Sb = (f_Sb+f_SbP1)/2

        iterCount = iterCount + 1

        if iterCount == 1500:
            LOGGER.warning(('GYPSYNonSpatial.estimate_basal_area_factor_sb()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_SbB, f_Sb)
            return f_Sb

    return f_Sb




def estimate_basal_area_factor_sw(**kwargs):
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
        BA_SwB = sim_basal_area_sw(startTage, startTageSw, y2bh_Sw,
                                    SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw,
                                    SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0,
                                    f_Sw, simulation_choice)[-1]
        if abs(BA_SwT - BA_SwB) < acceptableDiff:
            BADiffFlag = True
        else:
            if (BA_SwT - BA_SwB) < 0:
                f_SwP1 = f_Sw
                f_SwP = f_Sw  *  (1+(np.log10(BA_SwT) - np.log10(abs(BA_SwB)))/ (10*np.log10(abs(BA_SwB))))
                f_Sw = (f_SwP+f_Sw)/2
            elif (BA_SwT - BA_SwB) > 0:
                f_Sw = (f_Sw + f_SwP1)/2

        iterCount = iterCount + 1

        if iterCount == 1500:
            LOGGER.warning(('GYPSYNonSpatial.estimate_basal_area_factor_sw()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_SwB, f_Sw)
            return f_Sw

    return f_Sw


def estimate_basal_area_factor_pl(**kwargs):
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
        BA_PlB = sim_basal_area_pl(startTage, startTagePl, y2bh_Pl,
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
            LOGGER.warning(('GYPSYNonSpatial.estimate_basal_area_factor_pl()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_PlB, f_Pl)
            return f_Pl

    return f_Pl
