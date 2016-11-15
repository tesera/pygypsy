"""Increment functions

This module contains functions to increment plot characteristics at an annual
resolution.

It uses the non-spatial implementaion.

"""
import numpy as np


def increment_basal_area_aw(sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw):
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
        X3 = np.exp(-a2*bhage_Aw**(0.5+a1))
        X4 = SC_Aw**a5
        X5 = (np.log(1+N0_Aw*(1+bhage_Aw)**0.5))**2
        X6 = SI_bh_Aw
        d1 = (1+BA_Aw)**a3
        d2 = 1+np.exp(1 -np.log(1+SC_Aw**2)/2.0)
        k = a4*np.log(0.01+bhage_Aw/10.0)
        n = X1*X2*X3*X4*X5*X6
        d = d1*d2
        BAinc_Aw = (n/d) + k

    return  BAinc_Aw


def increment_basal_area_sb(sp_Sb, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, BA_Sb):
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
        k = (1+((N0_Sb**0.5)*((1+bhage_Sb)**0.5)))*(np.exp(-(N0_Sb/4.0)/10000.0))*(np.log(1+SI_bh_Sb))/((1+BA_Sb)**a2)

        k1 = (10**-4)*a1*(np.exp(-a2*bhage_Sb))*(SC_Sb**a3)*(bhage_Sb**(a2+np.sqrt(a1)))
        BAinc_Sb = k*k1

    return BAinc_Sb


def increment_basal_area_sw(sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw,
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

        k = (a4*z1*np.log(1+(SDF_Aw0/10000.0))) + (a5*z2*np.log(1+(SDF_Pl0/10000.0))) + (z3*np.log(1+(SDF_Sb0/10000.0)))
        k1 = (10**-4)*a1*((a2+bhage_Sw)**2)*((1+bhage_Sw)**((a1**0.5)+a2-a3))*np.exp(-a2*bhage_Sw)*(SC_Sw**a6)
        k2 = 1 + np.exp(1 + k + ((np.log(1+((N0_Sw**0.5)/10000.0)))/2.0)  + (a3 * np.log(1+BA_Sw)))
        m = (np.log(1+(N0_Sw*((1+bhage_Sw)**0.5)))**2)* ((SI_bh_Sw)**0.5)* np.exp(-(N0_Sw/10.0)/10000.0)
        BAinc_Sw = k1*m/k2

    return BAinc_Sw


def increment_basal_area_pl(sp_Pl, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl,
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

        k = (z1*np.log(1+(SDF_Aw0/1000.0))) + (z2*(np.log(1+(SDF_Sw0/1000.0)))/2.0)+ (z3*(np.log(1+(SDF_Sb0/1000.0)))/2.0)
        k1 = (10**-4)*a1*bhage_Pl * np.exp(-a2* bhage_Pl) * (1 + ((np.log(1+ bhage_Pl))/2.0))
        k2 = 1+np.exp((k/2.0)+ np.log(1+((N0_Pl/3.0)/10000.0)) - (a3 * (SC_Pl**0.5)) + (a4*np.log(1+BA_Pl)))
        m1 = (1+a3+(SI_bh_Pl**a6)) * (N0_Pl**0.5) * np.exp(-(N0_Pl/3.0)/10000.0)
        m2 = a5 * np.log(0.01+(bhage_Pl/10.0))
        BAinc_Pl = (k1*m1/k2)+m2

    return BAinc_Pl
