"""Increment functions

This module contains functions to increment plot characteristics at an annual
resolution.

It uses the non-spatial implementaion.

"""
# TODO: remove sp from function args & update uses of function

# NOTE: cython has a bug with ** and negative integer exponents, it coerces result to int
# pow(base, exponent) should be used if it is desired to use a negative integer with float
import numpy as np
cimport numpy as np

def increment_basal_area_aw(sp,
                            np.float64_t SC,
                            np.float64_t SI_bh,
                            np.float64_t N_bh,
                            np.float64_t N0,
                            np.float64_t bhage,
                            np.float64_t BA):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is also used to make basal area projections and as a function
    called by factor finder functions during estimation of correction factor
    for the species.

    :param str sp: species name
    :param float SI_bh: site index of species Aw
    :param float bhage: breast height age of speceis Aw
    :param float N_bh: density of species Aw
    :param float SC: proportion of species Aw in the stand
    :param float BA: Basal area of the species Aw
    :param float N0: initial density of species Aw at breast height age

    '''
    cdef np.float64_t BAinc, a1, a2, a3, a4, a5, X1, X2, X3, X4, X5, X6, d1, d2, \
        k, n, d
    if N_bh == 0:
        BAinc = 0

    if bhage < 0:
        bhage = 0

    if BA < 0:
        BAinc = 0
    elif N_bh > 0 and SI_bh > 0:
        a1 = 0.751313
        a2 = 0.018847
        a3 = 1.143762
        a4 = -0.03475
        a5 = 0.835189
        X1 = a1 * pow(10, -4)
        X2 = bhage ** 2
        X3 = np.exp(-a2 * bhage ** (0.5 + a1))
        X4 = SC ** a5
        X5 = (np.log(1 + N0 * (1 + bhage) ** 0.5)) ** 2
        X6 = SI_bh
        d1 = (1 + BA) ** a3
        d2 = 1 + np.exp(1 -np.log(1 + SC ** 2) / 2.0)
        k = a4 * np.log(0.01 + bhage / 10.0)
        n = X1 * X2 * X3 * X4 * X5 * X6
        d = d1 * d2
        BAinc = (n / d) + k

    return  BAinc


def increment_basal_area_sb(sp,
                            np.float64_t SC,
                            np.float64_t SI_bh,
                            np.float64_t N_bh,
                            np.float64_t N0,
                            np.float64_t bhage,
                            np.float64_t BA):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is used to make basal area projections and as a function
    called by factor finder functions during estimation of correction factor
    for the species.

    :param str sp: species name
    :param float SI_bh: site index of species Sb
    :param float bhage: breast height age of speceis Sb
    :param float N_bh: density of species Sb
    :param float SC: proportion of species Sb in the stand
    :param float BA: Basal area of the species Sb
    :param float N0: initial density of species Sb at total age

    '''
    cdef np.float64_t BAinc, a1, a2, a3, k, k1

    if N_bh == 0:
        BAinc = 0

    if bhage < 0:
        bhage = 0

    if BA < 0:
        BA = 0

    elif N_bh > 0 and SI_bh > 0:
        a1 = 0.966285
        a2 = 0.056315
        a3 = 0.17191

        k = ( 1 + ((N0 ** 0.5) * ((1 + bhage) ** 0.5))) \
            * ( np.exp(-(N0 / 4.0) / 10000.0)) \
            * (np.log(1 + SI_bh)) \
            / ((1 + BA) ** a2)

        k1 = (pow(10, -4)) \
             * a1 \
             * (np.exp(-a2 * bhage)) \
             * (SC ** a3) \
             * (bhage ** (a2 + np.sqrt(a1)))

        BAinc = k * k1

    return BAinc


def increment_basal_area_sw(sp,
                            np.float64_t SC,
                            np.float64_t SI_bh,
                            np.float64_t N_bh,
                            np.float64_t N0,
                            np.float64_t bhage,
                            np.float64_t SDF_Aw0,
                            np.float64_t SDF_Pl0,
                            np.float64_t SDF_Sb0,
                            np.float64_t BA):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is used to make basal area projections and as a function
    called by factor finder functions during estimation of correction factor
    for the species.

    :param str sp: species name
    :param float SI_bh: site index of species Sw
    :param float bhage: breast height age of speceis Sw
    :param float N_bh: density of species Sw
    :param float SC: proportion of species Sw in the stand
    :param float BA: Basal area of the species Sw
    :param float N0: initial density of species Sw at total age
    :param float SDF_Pl0: Stand Density Factor of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb

    '''
    cdef np.float64_t BAinc, \
        a1, a2, a3, a4, a5, a6, \
        z1, z2, z3, k, k1, k2, m

    if N_bh == 0:
        BAinc = 0

    if bhage < 0:
        bhage = 0

    if BA < 0:
        BA = 0

    if N_bh > 0 and SI_bh > 0:
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

        k = (a4 * z1 * np.log(1 + (SDF_Aw0 / 10000.0 ))) \
            + (a5 * z2 * np.log(1 + (SDF_Pl0 / 10000.0))) \
            + (z3 * np.log(1 + (SDF_Sb0 / 10000.0)))

        k1 = (pow(10, -4)) \
             * a1 \
             * ((a2 + bhage) ** 2) \
             * ((1 + bhage) ** ((a1 ** 0.5) + a2 - a3)) \
             * np.exp(-a2 * bhage)\
             * (SC ** a6)

        k2 = 1 \
             + np.exp(
                 1 \
                 + k \
                 + ((np.log(1 + ((N0 ** 0.5) / 10000.0))) / 2.0) \
                 + (a3 * np.log(1 + BA))
             )

        m = (np.log(1 + (N0 * ((1 + bhage) ** 0.5))) ** 2) \
            * (SI_bh ** 0.5) \
            * np.exp(-(N0 / 10.0) / 10000.0)

        BAinc = k1 * m / k2

    return BAinc


def increment_basal_area_pl(sp,
                            np.float64_t SC,
                            np.float64_t SI_bh,
                            np.float64_t N_bh,
                            np.float64_t N0,
                            np.float64_t bhage,
                            np.float64_t SDF_Aw0,
                            np.float64_t SDF_Sw0,
                            np.float64_t SDF_Sb0,
                            np.float64_t BA):
    '''Predicts the increment in basal area for the subsequent year for the
    species.

    This function is used to make basal area projections and as a
    function called by factor finder functions during estimation of correction
    factor for the species.

    :param str sp: species name
    :param float SC: proportion of species Pl in the stand
    :param float SI_bh: site index of species Pl
    :param float bhage: breast height age of species Pl
    :param float N_bh: density of species Pl
    :param float BA: Basal area of the species Pl
    :param float N0: initial density of species Pl at total age
    :param float SDFSw0: Stand Density Factor of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb

    '''
    cdef np.float64_t BAinc, a1, a2, a3, a4, a5, a6, \
        z1, z2, z3, k, k1, k2, m1, m2

    if N_bh == 0:
        BAinc = 0

    if bhage < 0:
        bhage = 0

    if BA <= 0 or SC == 0:
        BA = 0
        BAinc = 0

    if N_bh > 0 and SI_bh > 0:
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

        k = (z1 * np.log(1 + (SDF_Aw0 / 1000.0))) \
            + (z2 * (np.log(1 + (SDF_Sw0 / 1000.0))) / 2.0)\
            + (z3 * (np.log(1 + (SDF_Sb0 / 1000.0))) / 2.0)

        k1 = pow(10, -4) \
             * a1 \
             * bhage \
             * np.exp(-a2* bhage) \
             * (1 + ((np.log(1 + bhage)) / 2.0))

        k2 = 1 \
             + np.exp(
                 ( k / 2.0) \
                 + np.log(1 + ((N0 / 3.0) / 10000.0)) \
                 - (a3 * (SC ** 0.5)) \
                 + (a4 * np.log(1 + BA))
             )

        m1 = (1 + a3 + (SI_bh ** a6)) \
             * (N0 ** 0.5) \
             * np.exp(-(N0 / 3.0) / 10000.0)

        m2 = a5 * np.log(0.01 + (bhage / 10.0))

        BAinc = (k1 * m1 / k2) + m2

    return BAinc
