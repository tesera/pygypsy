"""Density and Increment Functions

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
import os
import logging
import numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge
from utils import _mkdir_p

logger = logging.getLogger(__name__)

# input - species, top height, total age, BHage (from the function),
#N (or density), current Basal Area,  Measured Percent Stocking,
#StumpDOB , StumpHeight, TopDib, SI, sp proportion

sp_Aw = ['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sb = ['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Pl = ['Pl', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sw = ['Sw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]


def densityNonSpatialAw(sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Aw: species name
    :param float SI_bh_Aw: site index of species Aw
    :param float bhage_Aw: breast height age of speceis Aw
    :param float N_Aw: densit of species Aw

    '''
    N_est_Aw = 0
    SDF_Aw0 = 0

    if N_Aw <= 0:
        return N_est_Aw, SDF_Aw0

    if bhage_Aw <= 0 or SI_bh_Aw <= 0:
        return N_est_Aw, SDF_Aw0

    if sp_Aw[0] in ('Aw', 'Bw', 'Pb', 'A', 'H'):
        c0 = 0.717966
        c1 = 6.67468
        SDF_Aw0 = N_Aw # best SDF_Aw guess
        acceptableDiff = 0.00001
        NDiffFlag = False
        iterCount = 0

        while NDiffFlag == False:
            b3 = (1+c0) * SDF_Aw0**((c1 + numpy.log(SDF_Aw0))/SDF_Aw0)
            b2 = (c0/4) * (SDF_Aw0**0.5)**(1/(SDF_Aw0))
            b1 = -((1/((SDF_Aw0/1000)**(0.5))) + numpy.sqrt(1+numpy.sqrt(50/(numpy.sqrt(SDF_Aw0)*numpy.log(50+1))))) * numpy.log(50+1)
            k1 = 1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50+1)))
            k2 = 1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(1+bhage_Aw)))
            N_est_Aw = SDF_Aw0*k1/k2

            if abs(N_Aw-N_est_Aw) < acceptableDiff:
                NDiffFlag = True
            else:
                N_est_Aw = (N_Aw + N_est_Aw)/2
                SDF_Aw0 = N_est_Aw *k2/k1
            iterCount = iterCount + 1

            if iterCount == 1500:
                if printWarnings:
                    print '\n GYPSYNonSpatial.densityNonSpatialAw()'
                    print ' Slow convergence'
                return N_est_Aw, SDF_Aw0

    return N_est_Aw, SDF_Aw0


def densityNonSpatialSb(sp_Sb, SI_bh_Sb, tage_Sb, N_Sb, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Sb: species name
    :param float SI_bh_Sb: site index of species Sb
    :param float tage_Sb: total age of species Sb
    :param float N_Sb: densit of species Sb

    '''
    N_est_Sb = 0
    SDF_Sb0 = 0

    if N_Sb > 0:
        if tage_Sb > 0 or SI_bh_Sb > 0:
            if sp_Sb[0] in ('Sb', 'Lt', 'La', 'Lw', 'L'):
                c1 = -26.3836
                c2 = 0.166483
                c3 = 2.738569
                SDF_Sb0 = N_Sb # best SDF_Sb guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(N_Sb-N_est_Sb) > acceptableDiff:
                    b2 = c3
                    b3 = c3*(SDF_Sb0**(1/SDF_Sb0))
                    b1 = c1/ ((((SDF_Sb0/1000.0)**0.5)+numpy.log(50+1))**c2)
                    k1 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+50)))
                    k2 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+tage_Sb)))
                    N_est_Sb = SDF_Sb0*k1/k2

                    if abs(N_Sb-N_est_Sb) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        N_est_Sb = (N_Sb + N_est_Sb)/2
                        SDF_Sb0 = N_est_Sb * k2/k1
                    iterCount = iterCount + 1

                    if iterCount == 150:
                        if printWarnings:
                            print '\n GYPSYNonSpatial.densityNonSpatialSb()'
                            print ' Slow convergence'
                        return N_est_Sb, SDF_Sb0

    return N_est_Sb, SDF_Sb0


def minimum_sdf_aw(bhage_aw, si_bh_aw):
    """estimate N given that SDF have been estimated

    """
    x0 = [200.0]
    optimize = fmin(densityAw, x0, args=(bhage_aw, si_bh_aw))

    return optimize


def densityNonSpatialSw(sp_Sw, SI_bh_Sw, tage_Sw, SDF_Aw0, N_Sw, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Sw: species name
    :param float SI_bh_Sw: site index of species Sw
    :param float tage_Sw: total age of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw, this parameter indicates that the density of Sw
    depends on the density of Aw
    :param float N_Sw: densit of species Sw

    '''
    N_est_Sw = 0
    SDF_Sw0 = 0

    if N_Sw > 0:
        if tage_Sw > 0 or SI_bh_Sw > 0:
            if sp_Sw[0] in ('Sw', 'Se', 'Fd', 'Fb', 'Fa'):

                if SDF_Aw0 == 0:
                    z1 = 0
                elif SDF_Aw0 > 0:
                    z1 = 1

                c1 = -231.617
                c2 = 1.176995
                c3 = 1.733601
                SDF_Sw0 = N_Sw # best SDF_Sb guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(N_Sw-N_est_Sw) > acceptableDiff:
                    b3 = c3*(SDF_Sw0**(1/SDF_Sw0))
                    b2 = c3
                    b1 = (c1/((numpy.log(SDF_Sw0)+numpy.log(50+1))**c2))+(z1*((1+(SDF_Aw0/1000.0))**0.5))
                    k1 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(50+1)))
                    k2 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(1+tage_Sw)))
                    N_est_Sw = SDF_Sw0*k1/k2

                    if abs(N_Sw-N_est_Sw) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        N_est_Sw = (N_Sw + N_est_Sw)/2
                        SDF_Sw0 = N_est_Sw * k2/k1

                    iterCount = iterCount + 1

                    if iterCount == 150:
                        if printWarnings:
                            print '\n GYPSYNonSpatial.densityNonSpatialSw()'
                            print ' Slow convergence'
                        return N_est_Sw, SDF_Sw0

    return N_est_Sw, SDF_Sw0


def densityNonSpatialPl(sp_Pl, SI_bh_Pl, tage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, N_Pl, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Pl: species name
    :param float SI_bh_Pl: site index of species Pl
    :param float tage_Pl: total age of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param float SDF_Pl0: Stand Density Factor of species Pl
    these parameters SDF above indicate that the density of Pl
    depends on the density of all otehr species
    :param float N_Pl: densit of species Pl

    '''
    N_est_Pl = 0
    SDF_Pl0 = 0

    if N_Pl > 0:
        if tage_Pl > 0 or SI_bh_Pl > 0:
            if sp_Pl[0] in ('P', 'Pl', 'Pj', 'Pa', 'Pf'):
                c1 = -5.25144
                c2 = -483.195
                c3 = 1.138167
                c4 = 1.017479
                c5 = -0.05471
                c6 = 4.11215

                if SDF_Aw0 == 0:
                    z1 = 0
                elif SDF_Aw0 > 0:
                    z1 = 1
                if SDF_Sw0 == 0:
                    z2 = 0
                elif SDF_Sw0 > 0:
                    z2 = 1
                if SDF_Sb0 == 0:
                    z3 = 0
                elif SDF_Sb0 > 0:
                    z3 = 1

                SDF_Pl0 = N_Pl # best SDF_Sb guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(N_Pl-N_est_Pl) > acceptableDiff:
                    k = (1+(c6*(SDF_Pl0**0.5)))/SDF_Pl0
                    b3 = c4*(SDF_Pl0**k)
                    b2 = c4/((SDF_Pl0**0.5)**c5)
                    b1 = (c1+(z1*(SDF_Aw0/1000.0)/2)+(z2*(SDF_Sw0/1000.0)/3)+(z3*(SDF_Sb0/1000.0)/4.0))+(c2/((SDF_Pl0**0.5)**c3))
                    k1 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Pl))+(b3*numpy.log(50+1)))
                    k2 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Pl))+(b3*numpy.log(1+tage_Pl)))
                    N_est_Pl = SDF_Pl0*k1/k2

                    if abs(N_Pl-N_est_Pl) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        N_est_Pl = (N_Pl + N_est_Pl)/2
                        SDF_Pl0 = N_est_Pl * k2/k1

                    iterCount = iterCount + 1

                    if iterCount == 150:
                        if printWarnings:
                            print '\n GYPSYNonSpatial.densityNonSpatialSw()'
                            print ' Slow convergence'
                        return N_est_Pl, SDF_Pl0

    return N_est_Pl, SDF_Pl0


def densityAw(SDF_Aw0, bhage_Aw, SI_bh_Aw):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Aw: site index of species Aw
    :param float bhage_Aw: breast height age of species Aw
    :param floar SDF_Aw0: Stand Density Factor of species Aw

    '''

    if SDF_Aw0 > 0:
        c0 = 0.717966
        c1 = 6.67468
        b3 = (1+c0) * SDF_Aw0**((c1+numpy.log(SDF_Aw0))/SDF_Aw0)
        b2 = (c0/4)*(SDF_Aw0**0.5)**(1/(SDF_Aw0))
        b1 = -((1/((SDF_Aw0/1000.0)**(0.5))) + (numpy.sqrt(1+numpy.sqrt(50/(numpy.sqrt(SDF_Aw0)*numpy.log(50+1)))))) * numpy.log(50+1)
        k1 = 1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(50+1)))
        k2 = 1+numpy.exp(b1 + (b2*SI_bh_Aw) + (b3*numpy.log(1+bhage_Aw)))
        N_bh_Aw = SDF_Aw0*k1/k2
    else:
        N_bh_Aw = 0

    return N_bh_Aw

def densitySb(SDF_Sb0, tage_Sb, SI_bh_Sb):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Sb: site index of species Sb
    :param float tage_Sb: total age of species Sb
    :param float SDF_Sb0: Stand Density Factor of species Sb
    :param float SDF_Aw0: Stand Density Factor of species Aw

    '''

    if SDF_Sb0 > 0:
        c1 = -26.3836
        c2 = 0.166483
        c3 = 2.738569
        b2 = c3
        b3 = c3*(SDF_Sb0**(1/SDF_Sb0))
        b1 = c1/((((SDF_Sb0/1000.0)**0.5)+numpy.log(50+1))**c2)
        k1 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+50)))
        k2 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sb))+(b3*numpy.log(1+tage_Sb)))
        N_bh_Sb = SDF_Sb0*k1/k2

    else:
        N_bh_Sb = 0

    return N_bh_Sb


def densitySw(SDF_Sw0, SDF_Aw0, tage_Sw, SI_bh_Sw):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Sw: site index of species Sw
    :param float tage_Sw: total age of species Sw
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw

    '''

    if SDF_Sw0 > 0:

        if SDF_Aw0 == 0:
            z1 = 0
        elif SDF_Aw0 > 0:
            z1 = 1

        c1 = -231.617
        c2 = 1.176995
        c3 = 1.733601
        b3 = c3*(SDF_Sw0**(1/SDF_Sw0))
        b2 = c3
        b1 = (c1/((numpy.log(SDF_Sw0)+numpy.log(50+1))**c2))+(z1*((1+(SDF_Aw0/1000.0))**0.5))
        k1 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(50+1)))
        k2 = 1+numpy.exp(b1+(b2*numpy.log(SI_bh_Sw))+(b3*numpy.log(1+tage_Sw)))

        N_bh_Sw = SDF_Sw0*k1/k2

    else:
        N_bh_Sw = 0

    return N_bh_Sw


def densityPl(SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_Pl, SI_bh_Pl):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Pl: site index of species Pl
    :param float tage_Pl: total age of species Pl
    :param float SDF_Pl0: Stand Density Factor of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb
    :param float SDF_Sw0: Stand Density Factor of species Sw

    '''

    if SDF_Pl0 > 0:
        c1 = -5.25144
        c2 = -483.195
        c3 = 1.138167
        c4 = 1.017479
        c5 = -0.05471
        c6 = 4.11215

        if SDF_Aw0 == 0:
            z1 = 0
        elif SDF_Aw0 > 0:
            z1 = 1
        if SDF_Sw0 == 0:
            z2 = 0
        elif SDF_Sw0 > 0:
            z2 = 1
        if SDF_Sb0 == 0:
            z3 = 0
        elif SDF_Sb0 > 0:
            z3 = 1

        k = (1+(c6*(SDF_Pl0**0.5)))/SDF_Pl0
        b3 = c4*(SDF_Pl0**k)
        b2 = c4/(numpy.sqrt(SDF_Pl0)**c5)
        b1 = (c1+(z1*(SDF_Aw0/1000.0)/2.0) + (z2*(SDF_Sw0/1000.0)/3.0) + (z3*(SDF_Sb0/1000.0)/4.0)) + (c2/((SDF_Pl0**0.5)**c3))
        k1 = 1+numpy.exp(b1 + (b2*numpy.log(SI_bh_Pl)) + (b3*numpy.log(50+1)))
        k2 = 1+numpy.exp(b1 + (b2*numpy.log(SI_bh_Pl)) + (b3*numpy.log(1+tage_Pl)))
        N_bh_Pl = SDF_Pl0*k1/k2
    else:
        N_bh_Pl = 0

    return N_bh_Pl


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


def BasalAreaIncrementNonSpatialAw(sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is also used to make basal area projections and as a function
    called by factor finder functions during estimation of correction factor
    for the species.

    :param str sp_Aw: species name
    :param float SI_bh_Aw: site index of species Aw
    :param float bhage_Aw: breast height age of speceis Aw
    :param float N_bh_Aw: density of species Aw
    :param float SC_Aw: proportion of species Aw in the stand
    :param float BA_Aw: Basal area of the species Aw
    :param float N0_Aw: initial density of species Aw at breast height age

    '''

    if N_bh_Aw == 0:
        BAinc_Aw = 0

    if bhage_Aw < 0:
        bhage_Aw = 0

    if BA_Aw < 0:
        BAinc_Aw = 0
    elif N_bh_Aw > 0 and SI_bh_Aw > 0:
        a1 = 0.751313
        a2 = 0.018847
        a3 = 1.143762
        a4 = -0.03475
        a5 = 0.835189
        X1 = a1* 10**(-4)
        X2 = (bhage_Aw)**2
        X3 = numpy.exp(-a2*bhage_Aw**(0.5+a1))
        X4 = SC_Aw**a5
        X5 = (numpy.log(1+N0_Aw*(1+bhage_Aw)**0.5))**2
        X6 = SI_bh_Aw
        d1 = (1+BA_Aw)**a3
        d2 = 1+numpy.exp(1 -numpy.log(1+SC_Aw**2)/2.0)
        k = a4*numpy.log(0.01+bhage_Aw/10.0)
        n = X1*X2*X3*X4*X5*X6
        d = d1*d2
        BAinc_Aw = (n/d) + k

    return  BAinc_Aw


def BAincIter_Aw(sp_Aw, BAinc_AwT, BA_AwT, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw,
                 bhage_Aw, printWarnings=True):
    '''This is a function used to estimate basal area decrease moving backwards in
    time.

    It is not used in the code, but was left here in case this approach is
    attempted again in the future

    '''
    acceptableDiff = 0.00001
    BADiffFlag = False
    iterCount = 0
    BA_Aw = BA_AwT - BAinc_AwT
    # BA_Aw = best estimate of BA  and BAinc_AwT
    # best estimate of decrement to previous year , ie, at time T-1

    while BADiffFlag == False:
        BAinc_AwtoT = BasalAreaIncrementNonSpatialAw(sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw)
        BA_AwT_est = BA_Aw + BAinc_AwtoT

        if abs(BA_AwT_est - BA_AwT) < acceptableDiff:
            BADiffFlag = True
        else:
            BA_Aw = (1+ ((BA_AwT - BA_AwT_est)/ BA_AwT)) * BA_Aw

        iterCount = iterCount + 1

        if iterCount == 150:
            if printWarnings:
                print '\n GYPSYNonSpatial.BAincIter_Aw()'
                print ' Slow convergence'
            return BA_Aw, BAinc_AwT

    return BA_Aw, BAinc_AwtoT


def BasalAreaIncrementNonSpatialSb(sp_Sb, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, BA_Sb):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is used to make basal area projections and as a function
    called by factor finder functions during estimation of correction factor
    for the species.

    :param str sp_Sb: species name
    :param float SI_bh_Sb: site index of species Sb
    :param float bhage_Sb: breast height age of speceis Sb
    :param float N_bh_Sb: density of species Sb
    :param float SC_Sb: proportion of species Sb in the stand
    :param float BA_Sb: Basal area of the species Sb
    :param float N0_Sb: initial density of species Sb at total age

    '''
    if N_bh_Sb == 0:
        BAinc_Sb = 0

    if bhage_Sb < 0:
        bhage_Sb = 0

    if BA_Sb < 0:
        BA_Sb = 0

    elif N_bh_Sb > 0 and SI_bh_Sb > 0:
        a1 = 0.966285
        a2 = 0.056315
        a3 = 0.17191
        k = (1+((N0_Sb**0.5)*((1+bhage_Sb)**0.5)))*(numpy.exp(-(N0_Sb/4.0)/10000.0))*(numpy.log(1+SI_bh_Sb))/((1+BA_Sb)**a2)

        k1 = (10**-4)*a1*(numpy.exp(-a2*bhage_Sb))*(SC_Sb**a3)*(bhage_Sb**(a2+numpy.sqrt(a1)))
        BAinc_Sb = k*k1

    return BAinc_Sb


def BAincIter_Sb(sp_Sb, BAinc_SbT, BA_SbT, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb,
                 bhage_Sb, printWarnings=True):
    '''This is a function used to estimate basal area decrease moving backwards in
    time. It is not used in the code, but was left here in case this approach
    is attempted again in the future

    '''
    acceptableDiff = 0.00001
    BADiffFlag = False
    iterCount = 0
    BA_Sb = BA_SbT - BAinc_SbT
    # BA_Sb = best estimate of BA  and BAinc_AwT
    # best estimate of decrement to previous year , ie, at time T-1

    while BADiffFlag == False:
        BAinc_SbtoT = BasalAreaIncrementNonSpatialSb(sp_Sb, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, BA_Sb)
        # based on best estimate of BA at time T-1
        BA_SbT_est = BA_Sb + BAinc_SbtoT

        if abs(BA_SbT_est - BA_SbT) < acceptableDiff:           #BA_SbT is known
            BADiffFlag = True
        else:
            BA_Sb = (1+ ((BA_SbT - BA_SbT_est)/ BA_SbT)) * BA_Sb

        iterCount = iterCount + 1

        if iterCount == 150:
            if printWarnings:
                print '\n GYPSYNonSpatial.BAincIter_Aw()'
                print ' Slow convergence'
            return BA_Sb, BAinc_SbT

    return BA_Sb, BAinc_SbtoT


def BasalAreaIncrementNonSpatialSw(sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw,
                                   bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is used to make basal area projections and as a function
    called by factor finder functions during estimation of correction factor
    for the species.

    :param str sp_Sw: species name
    :param float SI_bh_Sw: site index of species Sw
    :param float bhage_Sw: breast height age of speceis Sw
    :param float N_bh_Sw: density of species Sw
    :param float SC_Sw: proportion of species Sw in the stand
    :param float BA_Sw: Basal area of the species Sw
    :param float N0_Sw: initial density of species Sw at total age
    :param float SDF_Pl0: Stand Density Factor of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb

    '''
    if N_bh_Sw == 0:
        BAinc_Sw = 0

    if bhage_Sw < 0:
        bhage_Sw = 0

    if BA_Sw < 0:
        BA_Sw = 0

    if N_bh_Sw > 0 and SI_bh_Sw > 0:
        a1 = 0.089153
        a2 = 0.072171
        a3 = -0.11483
        a4 = 5.839408
        a5 = 1.753002
        a6 = 0.239521

        if SDF_Aw0 == 0:
            z1 = 0
        elif SDF_Aw0 > 0:
            z1 = 1
        if SDF_Pl0 == 0:
            z2 = 0
        elif SDF_Pl0 > 0:
            z2 = 1
        if SDF_Sb0 == 0:
            z3 = 0
        elif SDF_Sb0 > 0:
            z3 = 1

        k = (a4*z1*numpy.log(1+(SDF_Aw0/10000.0))) + (a5*z2*numpy.log(1+(SDF_Pl0/10000.0))) + (z3*numpy.log(1+(SDF_Sb0/10000.0)))
        k1 = (10**-4)*a1*((a2+bhage_Sw)**2)*((1+bhage_Sw)**((a1**0.5)+a2-a3))*numpy.exp(-a2*bhage_Sw)*(SC_Sw**a6)
        k2 = 1 + numpy.exp(1 + k + ((numpy.log(1+((N0_Sw**0.5)/10000.0)))/2.0)  + (a3 * numpy.log(1+BA_Sw)))
        m = (numpy.log(1+(N0_Sw*((1+bhage_Sw)**0.5)))**2)* ((SI_bh_Sw)**0.5)* numpy.exp(-(N0_Sw/10.0)/10000.0)
        BAinc_Sw = k1*m/k2

    return BAinc_Sw


def BAincIter_Sw(sp_Sw, BAinc_SwT, BA_SwT, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw,
                 bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, printWarnings=True):
    '''This is a function used to estimate basal area decrease moving backwards in
    time.

    It is not used in the application, but was left here in case this approach is
    attempted again in the future

    '''
    acceptableDiff = 0.00001
    BADiffFlag = False
    iterCount = 0
    BA_Sw = BA_SwT - BAinc_SwT
    # BA_Sw = best estimate of BA  and BAinc_AwT best
    # estimate of decrement to previous year , ie, at time T-1

    while BADiffFlag == False:
        BAinc_SwtoT = BasalAreaIncrementNonSpatialSw(sp_Sw, SC_Sw, SI_bh_Sw,
                                                     N_bh_Sw, N0_Sw, bhage_Sw,
                                                     SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw)
        BA_SwT_est = BA_Sw + BAinc_SwtoT

        if abs(BA_SwT_est - BA_SwT) < acceptableDiff:
            BADiffFlag = True
        else:
            BA_Sw = (1+ ((BA_SwT - BA_SwT_est)/ BA_SwT)) * BA_Sw

        iterCount = iterCount + 1

        if iterCount == 150:
            if printWarnings:
                print '\n GYPSYNonSpatial.BAincIter_Aw()'
                print ' Slow convergence'
            return BA_Sw, BAinc_SwT

    return BA_Sw, BAinc_SwtoT


def BasalAreaIncrementNonSpatialPl(sp_Pl, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl,
                                   bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is used to make basal area projections and as a
    function called by factor finder functions during estimation of correction
    factor for the species.

    :param str sp_Pl: species name
    :param float SI_bh_Pl: site index of species Pl
    :param float bhage_Pl: breast height age of species Pl
    :param float N_bh_Pl: density of species Pl
    :param float SC_Pl: proportion of species Pl in the stand
    :param float BA_Pl: Basal area of the species Pl
    :param float N0_Pl: initial density of species Pl at total age
    :param float SDFSw0: Stand Density Factor of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb

    '''

    if N_bh_Pl == 0:
        BAinc_Pl = 0

    if bhage_Pl < 0:
        bhage_Pl = 0

    if BA_Pl <= 0 or SC_Pl == 0:
        BA_Pl = 0
        BAinc_Pl = 0

    if N_bh_Pl > 0 and SI_bh_Pl > 0:
        a1 = 3.923984
        a2 = 0.05752
        a3 = 0.560402
        a4 = 0.672506
        a5 = -0.00358
        a6 = 0.775765

        if SDF_Aw0 == 0:
            z1 = 0
        elif SDF_Aw0 > 0:
            z1 = 1
        if SDF_Sw0 == 0:
            z2 = 0
        elif SDF_Sw0 > 0:
            z2 = 1
        if SDF_Sb0 == 0:
            z3 = 0
        elif SDF_Sb0 > 0:
            z3 = 1

        k = (z1*numpy.log(1+(SDF_Aw0/1000.0))) + (z2*(numpy.log(1+(SDF_Sw0/1000.0)))/2.0)+ (z3*(numpy.log(1+(SDF_Sb0/1000.0)))/2.0)
        k1 = (10**-4)*a1*bhage_Pl * numpy.exp(-a2* bhage_Pl) * (1 + ((numpy.log(1+ bhage_Pl))/2.0))
        k2 = 1+numpy.exp((k/2.0)+ numpy.log(1+((N0_Pl/3.0)/10000.0)) - (a3 * (SC_Pl**0.5)) + (a4*numpy.log(1+BA_Pl)))
        m1 = (1+a3+(SI_bh_Pl**a6)) * (N0_Pl**0.5) * numpy.exp(-(N0_Pl/3.0)/10000.0)
        m2 = a5 * numpy.log(0.01+(bhage_Pl/10.0))
        BAinc_Pl = (k1*m1/k2)+m2

    return BAinc_Pl


def BAincIter_Pl(sp_Pl, BAinc_PlT, BA_PlT, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl,
                 bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, printWarnings=True):
    '''This is a function used to estimate basal area decrease moving backwards in
    time.

    It is not used in the code, but was left here in case this approach is
    attempted again in the future

    '''
    acceptableDiff = 0.00001
    BADiffFlag = False
    iterCount = 0
    BA_Pl = BA_PlT - BAinc_PlT
    # BA_Pl = best estimate of BA  and BAinc_AwT
    #best estimate of decrement to previous year , ie, at time T-1

    while BADiffFlag == False:
        BAinc_PltoT = BasalAreaIncrementNonSpatialPl(sp_Pl, SC_Pl, SI_bh_Pl,
                                                     N_bh_Pl, N0_Pl, bhage_Pl,
                                                     SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl)
        # based on best estimate of BA at time T-1
        BA_PlT_est = BA_Pl + BAinc_PltoT

        if abs(BA_PlT_est - BA_PlT) < acceptableDiff:           #BA_SbT is known
            BADiffFlag = True
        else:
            BA_Pl = (1+ ((BA_PlT - BA_PlT_est)/ BA_PlT)) * BA_Pl

        iterCount = iterCount + 1

        if iterCount == 150:
            if printWarnings:
                print '\n GYPSYNonSpatial.BAincIter_Aw()'
                print ' Slow convergence'
            return BA_Pl, BAinc_PlT

    return BA_Pl, BAinc_PltoT


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
            N_bh_AwT = densityAw(SDF_Aw0, bhage_Aw, SI_bh_Aw)

        if tage_Sb < 0:
            N_bh_SbT = 0
        else:
            N_bh_SbT = densitySb(SDF_Sb0, tage_Sb, SI_bh_Sb)

        if tage_Sw < 0:
            N_bh_SwT = 0
        else:
            N_bh_SwT = densitySw(SDF_Sw0, SDF_Aw0, tage_Sw, SI_bh_Sw)

        if tage_Pl < 0:
            N_bh_PlT = 0
        else:
            N_bh_PlT = densityPl(SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_Pl, SI_bh_Pl)



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
            logger.warning(('GYPSYNonSpatial.BAfactorFinder_Aw()'
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
    logger.debug('getting basal area from time zero to time of data for aspen')

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
                BAinc_Aw = BasalAreaIncrementNonSpatialAw('Aw', SC_Aw, SI_bh_Aw, N_bh_AwT,
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
    logger.debug('Getting basal area factor for black spruce')
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
            logger.warning(('GYPSYNonSpatial.BAfactorFinder_Sb()'
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
                BAinc_Sb = BasalAreaIncrementNonSpatialSb('Sb', SC_Sb, SI_bh_Sb, N_bh_SbT,
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
    logger.debug('Getting basal area factor for white spruce')
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
            logger.warning(('GYPSYNonSpatial.BAfactorFinder_Sw()'
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
                BAinc_Sw = BasalAreaIncrementNonSpatialSw('Sw', SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_tempSw)
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
            logger.warning(('GYPSYNonSpatial.BAfactorFinder_Pl()'
                 ' Slow convergence with Basal Area: %s'
                 ' and factor:%s '), BA_Pl0, BA_PlB, f_Pl)
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
                BAinc_Pl = f_Pl * BasalAreaIncrementNonSpatialPl('Pl', SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl,
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


def GrossTotalVolume_Aw(basal_area, top_height):
    ''' White Aspen Gross Total Volume

    Note that inputs may be scalars, or numpy arrays.

    :param float basal_area: basal area
    :param float top_height: top height

    '''
    a1 = 0.248718
    a2 = 0.98568
    a3 = 0.857278
    a4 = -24.9961
    tot_vol = a1 \
              * (basal_area**a2) \
              * (top_height**a3) \
              * numpy.exp( 1 \
                           + ( a4 / (( top_height**2 ) + 1 ))
              )

    return tot_vol


def GrossTotalVolume_Sw(basal_area, top_height):
    '''White Spruce Gross Total Volume

    Note that inputs may be scalars, or numpy arrays.

    :param float basal_area: basal area
    :param float top_height: top height

    '''
    b1 = 0.41104
    b2 = 0.983108
    b3 = 0.971061
    tot_vol = b1 \
              * (basal_area**b2) \
              * (top_height**b3)

    return tot_vol


def GrossTotalVolume_Sb(basal_area, top_height):
    '''Black Spruce Gross Total Volume

    Note that inputs may be scalars, or numpy arrays.

    :param float basal_area: basal area
    :param float top_height: top height

    '''
    b1 = 0.48628
    b2 = 0.982962
    b3 = 0.910603
    tot_vol = b1 \
              * (basal_area**b2) \
              * (top_height**b3)

    return tot_vol


def GrossTotalVolume_Pl(basal_area, top_height):
    '''Lodgepole Pine Gross Total Volume

    Note that inputs may be scalars, or numpy arrays.

    :param float basal_area: basal area
    :param float top_height: top height

    '''
    a1 = 0.194086
    a2 = 0.988276
    a3 = 0.949346
    a4 = -3.39036
    tot_vol = a1 \
              * (basal_area**a2) \
              * (top_height**a3) \
              * numpy.exp(
                  1 + ( a4 / (( top_height**2 ) + 1 ))
              )

    return tot_vol

def gross_total_volume(species, *args):
    return {
        'Aw': GrossTotalVolume_Aw,
        'Sw': GrossTotalVolume_Sw,
        'Sb': GrossTotalVolume_Sb,
        'Pl': GrossTotalVolume_Pl,
    }[species](*args)



def MerchantableVolumeAw(N_bh, BA, topHeight, StumpDOB,
                         StumpHeight, TopDib, Tvol):
    '''Merchantable volume for white aspen

    Only new variables are the stump diameter outside bark, stump height and
    top diameter inside bark The if below was used (and in other functions) to
    avoid division by zero when density is zero, i.e., when the species is
    absent in the plot.

    :param float N_bh: density of sp Aw
    :param float topHeight: top height of Aw
    :param float StumpDOB:  stump diameter outside bark of Aw
    :param float StumpHeight: stump height of Aw
    :param float TopDib: top diameter inside bark
    :param float Tvol: Gross total volume of Aw

    '''
    if N_bh > 0:
        k = (BA * 10000.0 / N_bh)**0.5
    else:
        k = 0

    if k > 0 and topHeight > 0:
        b0 = 0.993673
        b1 = 923.5825
        b2 = -3.96171
        b3 = 3.366144
        b4 = 0.316236
        b5 = 0.968953
        b6 = -1.61247
        k1 = Tvol * (k**b0)
        k2 = (b1* (topHeight**b2) * (StumpDOB**b3) * (StumpHeight**b4) * (TopDib**b5)  * (k**b6)) + k
        MVol = k1/k2
    else:
        MVol = 0

    return MVol


def MerchantableVolumeSb(N_bh, BA, topHeight, StumpDOB,
                         StumpHeight, TopDib, Tvol):
    '''Merchantable volume black spruce

    The if below was used (and in other functions) to avoid division by zero
    when density is zero, i.e., when the species is absent in the plot.

    :param float N_bh: density of sp Sb
    :param float topHeight: top height of Sb
    :param float StumpDOB:  stump diameter outside bark of Sb
    :param float StumpHeight: stump height of Sb
    :param float TopDib: top diameter inside bark of Sb
    :param float Tvol: Gross total volume of Sb

    '''
    if N_bh > 0:
        k = (BA * 10000.0 / N_bh)**0.5
    else:
        k = 0

    if k > 0 and  topHeight > 0:
        if sp[0] in('Sb', 'Lt', 'La', 'Lw', 'L'):
            b0 = 0.98152
            b1 = 0.678011
            b2 = -1.10256
            b3 = 4.148139
            b4 = 0.511391
            b5 = 1.484988
            b6 = -3.26425
            StumpDOB = sp[7]
            StumpHeight = sp[8]
            TopDib = sp[9]
            MVol = (Tvol * (k**b0))/ ((b1* (topHeight**b2) * (StumpDOB**b3) * (StumpHeight**b4) * (TopDib**b5) * (k**b6)) +k)
    else:
        MVol = 0

    return MVol



def MerchantableVolumeSw(N_bh, BA, topHeight, StumpDOB,
                         StumpHeight, TopDib, Tvol):
    '''
    Merchantable volume only new variables are the stump diameter outside bark, stump height and top diameter inside bark

    The if below was used (and in other functions) to avoid
    division by zero when density is zero, i.e., when the
    species is absent in the plot.

    :param float N_bh: density of sp Sw
    :param float topHeight: top height of Sw
    :param float StumpDOB:  stump diameter outside bark of Sw
    :param float StumpHeight: stump height of Sw
    :param float TopDib: top diameter inside bark of Sw
    :param float Tvol: Gross total volume of Sw
    '''
    if N_bh > 0:
        k = (BA * 10000.0 / N_bh)**0.5
    else:
        k = 0
    if k > 0 and  topHeight > 0:
        if sp[0] in ('Sw', 'Se', 'Fd', 'Fb', 'Fa'):
            b0 = 0.996262
            b1 = 7.021736
            b2 = -1.77615
            b3 = 1.91562
            b4 = 0.4111
            b5 = 1.024803
            b6 = -0.80121
            MVol = (Tvol * (k**b0)) /   ((b1* (topHeight**b2) * (sp[7]**b3) * (sp[8]**b4) * (sp[9]**b5) * (k**b6)) +k)
    else:
        MVol = 0

    return MVol



def MerchantableVolumePl(N_bh, BA, topHeight, StumpDOB,
                         StumpHeight, TopDib, Tvol):
    '''Merchantable volume lodgepole pine

    The if below was used (and in other functions) to avoid division by zero
    when density is zero, i.e., when the species is absent in the plot.

    :param float N_bh: density of sp Pl
    :param float topHeight: top height of Pl
    :param float StumpDOB:  stump diameter outside bark of Pl
    :param float StumpHeight: stump height of Pl
    :param float TopDib: top diameter inside bark of Pl
    :param float Tvol: Gross total volume of Pl

    '''
    if N_bh > 0:
        k = (BA * 10000.0 / N_bh)**0.5
    else:
        k = 0

    if k > 0 and topHeight > 0:
        if sp[0] in ('P', 'Pl', 'Pj', 'Pa', 'Pf'):
            b0 = 0.989889
            b1 = 1.055091
            b2 = -0.19072
            b3 = 4.915593
            b4 = 0.42574
            b5 = 1.006379
            b6 = -4.87808
            MVol = (Tvol * (k**b0)) / ((b1* (topHeight**b2) * (sp[7]**b3) * (sp[8]**b4) * (sp[9]**b5) * (k**b6)) +k)
    else:
        MVol = 0

    return MVol


def merchantable_volume(species, *args):
    return {
        'Aw': MerchantableVolumeAw,
        'Sw': MerchantableVolumeSw,
        'Sb': MerchantableVolumeSb,
        'Pl': MerchantableVolumePl,
    }[species](*args)


def _plot_simulation_variables(simulation_df, ax=None, plot_vars=None, y_lab=''):
    """
    Keyword Arguments:
    simulation_df -- output of gypsy simulation
    axes          -- axes object ????
    plot_vars     -- list of strings identifying variable (column names) to plot
    """

    if plot_vars is None:
        raise ValueError('Variable to plot must be specified')

    simulation_vars = simulation_df.loc[:, plot_vars]
    simulation_vars.plot(ax=ax)
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel(y_lab, fontsize=10)
    ax.legend(loc=2, prop={'size':6})
    ax.tick_params(axis='both', which='major', labelsize=8)



def plot_BA(output_DF, ax=None):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['BA_Aw', 'BA_Sw', 'BA_Sb', 'BA_Pl'],
                               y_lab='BA (m2)')

def plot_merchantableVol(output_DF, ax):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['MerchantableVolumeAw', 'MerchantableVolumeSw',
                                          'MerchantableVolumeSb', 'MerchantableVolumePl'],
                               y_lab='Merc. Vo. (m3)')

def plot_merchantableVol_Con_Dec(output_DF, ax):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['MerchantableVolume_Con',
                                          'MerchantableVolume_Dec',
                                          'MerchantableVolume_Tot'],
                               y_lab='Merc. Vo. (m3)')

def plot_topHeight(output_DF, ax=None):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['topHeight_Aw', 'topHeight_Sw',
                                          'topHeight_Sb', 'topHeight_Pl'],
                               y_lab='Top Height (m)')


def plot_GrTotVol(output_DF, ax):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['Gross_Total_Volume_Aw', 'Gross_Total_Volume_Sw',
                                          'Gross_Total_Volume_Sb', 'Gross_Total_Volume_Pl'],
                               y_lab='Gr. Tot. Vol. (m3)')

def plot_GrTotVol_Con_Dec(output_DF, ax):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['Gross_Total_Volume_Con',
                                          'Gross_Total_Volume_Dec',
                                          'Gross_Total_Volume_Tot'],
                               y_lab='Gr. Tot. Vol. (m3)')


def plot_SC(output_DF, ax):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['SC_Aw', 'SC_Sw', 'SC_Sb', 'SC_Pl'],
                               y_lab='Sp. Comp.')

def plot_N(output_DF, ax):
    _plot_simulation_variables(output_DF, ax=ax,
                               plot_vars=['N_bh_AwT', 'N_bh_SwT', 'N_bh_SbT', 'N_bh_PlT'],
                               y_lab='Density')

def save_plot(output_DF, path):
    '''Save plots of gypsy simulation output

    Creates a panel and includes all plots generated as gypsy outputs
    (output_DF) and saves the panel on a folder determined byt path

    '''
    _mkdir_p(os.path.dirname(path))
    fig = plt.figure(1)
    sub1 = fig.add_subplot(321)
    sub2 = fig.add_subplot(322)
    sub3 = fig.add_subplot(323)
    sub4 = fig.add_subplot(324)
    sub5 = fig.add_subplot(325)
    sub6 = fig.add_subplot(326)

    plot_BA(output_DF, ax=sub1)
    plot_merchantableVol_Con_Dec(output_DF, ax=sub2)
    plot_topHeight(output_DF, ax=sub3)
    plot_GrTotVol_Con_Dec(output_DF, ax=sub4)
    plot_SC(output_DF, ax=sub5)

    plot_N(output_DF, ax=sub6)
    plt.tight_layout()
    plt.savefig(path) #TODO: specify page size here to reduce legend size
    plt.close()

    return True
