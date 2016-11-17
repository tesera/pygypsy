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

from gypsy.density import (
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


