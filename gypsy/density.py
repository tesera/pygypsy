"""Density estimators"""
#pylint: disable=invalid-name,no-member
# The invalid name linting is disabled since this is a math heavy module
# it makes sense to use short names. Please still use sensible names for non
# mathematical variables
# no-member warning is also ignored - probably it is a c extension which
# pylint doesn't see
import numpy as np


def estimate_density_aw(SDF_Aw0, bhage_Aw, SI_bh_Aw, ret_detail=False):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Aw: site index of species Aw
    :param float bhage_Aw: breast height age of species Aw
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param bool ret_detail: whether additional values should be returned - used
    by other functions to iteratively solve this function for SDF
    '''
    if SDF_Aw0 > 0:
        c0 = 0.717966
        c1 = 6.67468
        b3 = (1+c0) \
             * SDF_Aw0 \
             **((c1+np.log(SDF_Aw0))/SDF_Aw0)
        b2 = (c0/4)*(SDF_Aw0**0.5)**(1/(SDF_Aw0))
        b1 = -((1/((SDF_Aw0/1000.0)**(0.5))) \
            + (np.sqrt(1+np.sqrt(50/(np.sqrt(SDF_Aw0)*np.log(50+1)))))) \
            * np.log(50+1)
        k1 = 1+np.exp(b1 + (b2*SI_bh_Aw) + (b3*np.log(50+1)))
        k2 = 1+np.exp(b1 + (b2*SI_bh_Aw) + (b3*np.log(1+bhage_Aw)))
        N_bh_Aw = SDF_Aw0*k1/k2
    else:
        N_bh_Aw = 0

    if ret_detail:
        return {
            'k1': k1,
            'k2': k2,
            'sdf': SDF_Aw0,
            'density': N_bh_Aw,
        }

    return N_bh_Aw

def estimate_density_sb(SDF_Sb0, tage_Sb, SI_bh_Sb, ret_detail=False):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Sb: site index of species Sb
    :param float tage_Sb: total age of species Sb
    :param float SDF_Sb0: Stand Density Factor of species Sb
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param bool ret_detail: whether additional values should be returned - used
    by other functions to iteratively solve this function for SDF

    '''
    if SDF_Sb0 > 0:
        c1 = -26.3836
        c2 = 0.166483
        c3 = 2.738569
        b2 = c3
        b3 = c3*(SDF_Sb0**(1/SDF_Sb0))
        b1 = c1/((((SDF_Sb0/1000.0)**0.5)+np.log(50+1))**c2)
        k1 = 1+np.exp(b1+(b2*np.log(SI_bh_Sb))+(b3*np.log(1+50)))
        k2 = 1+np.exp(b1+(b2*np.log(SI_bh_Sb))+(b3*np.log(1+tage_Sb)))
        N_bh_Sb = SDF_Sb0*k1/k2
    else:
        N_bh_Sb = 0

    if ret_detail:
        return {
            'k1': k1,
            'k2': k2,
            'sdf': SDF_Sb0,
            'density': N_bh_Sb,
        }

    return N_bh_Sb


def estimate_density_sw(SDF_Sw0, SDF_Aw0, tage_Sw, SI_bh_Sw, ret_detail=False):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Sw: site index of species Sw
    :param float tage_Sw: total age of species Sw
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param bool ret_detail: whether additional values should be returned - used
    by other functions to iteratively solve this function for SDF

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
        b1 = (c1/((np.log(SDF_Sw0)+np.log(50+1))**c2))+(z1*((1+(SDF_Aw0/1000.0))**0.5))
        k1 = 1+np.exp(b1+(b2*np.log(SI_bh_Sw))+(b3*np.log(50+1)))
        k2 = 1+np.exp(b1+(b2*np.log(SI_bh_Sw))+(b3*np.log(1+tage_Sw)))
        N_bh_Sw = SDF_Sw0*k1/k2
    else:
        N_bh_Sw = 0

    if ret_detail:
        return {
            'k1': k1,
            'k2': k2,
            'sdf': SDF_Sw0,
            'density': N_bh_Sw,
        }

    return N_bh_Sw


def estimate_density_pl(SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_Pl, SI_bh_Pl, ret_detail=False):
    '''Main purpose of this function is to project densities forward and backward
    in time for the species

    :param float SI_bh_Pl: site index of species Pl
    :param float tage_Pl: total age of species Pl
    :param float SDF_Pl0: Stand Density Factor of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sb0: Stand Density Factor of species Sb
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param bool ret_detail: whether additional values should be returned - used
    by other functions to iteratively solve this function for SDF

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
        b2 = c4/(np.sqrt(SDF_Pl0)**c5)
        b1 = \
             (c1 \
              + (z1*(SDF_Aw0/1000.0)/2.0) \
              + (z2*(SDF_Sw0/1000.0)/3.0) \
              + (z3*(SDF_Sb0/1000.0)/4.0)
             ) \
             + (c2/((SDF_Pl0**0.5)**c3))
        k1 = 1+np.exp(b1 + (b2*np.log(SI_bh_Pl)) + (b3*np.log(50+1)))
        k2 = 1+np.exp(b1 + (b2*np.log(SI_bh_Pl)) + (b3*np.log(1+tage_Pl)))
        N_bh_Pl = SDF_Pl0*k1/k2
    else:
        N_bh_Pl = 0

    if ret_detail:
        return {
            'k1': k1,
            'k2': k2,
            'sdf': SDF_Pl0,
            'density': N_bh_Pl,
        }

    return N_bh_Pl


