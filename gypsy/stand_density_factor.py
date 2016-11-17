"""Stand density factor estimators"""
import logging

from gypsy.GYPSYNonSpatial import (
    densityAw,
    densitySw,
    densitySb,
    densityPl,
)

LOGGER = logging.getLogger(__name__)


def sdf_aw(sp, site_index, bhage, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species list
    :param float site_index: site index of species Aw
    :param float bhage: breast height age of speceis Aw
    :param float density: density of species Aw

    '''
    density_est = 0
    SDF0 = 0

    if density <= 0 or bhage <= 0 or site_index <= 0:
        return density_est, SDF0

    if sp[0] in ('Aw', 'Bw', 'Pb', 'A', 'H'):
        SDF0 = density # best SDF guess
        tolerance = 0.00001
        within_tolerance = False
        iter_count = 0

        while not within_tolerance:
            result = densityAw(SDF0, bhage, site_index, ret_detail=True)
            k1 = result['k1']
            k2 = result['k2']
            density_est = result['density']

            if abs(density-density_est) < tolerance:
                within_tolerance = True
            else:
                density_est = (density + density_est) / 2
                SDF0 = density_est * k2 / k1

            iter_count += 1

            if iter_count == 1500:
                LOGGER.warning('Slow convergence')
                break

    return density_est, SDF0


def sdf_sb(sp, site_index, tage, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species list
    :param float site_index: site index of species Sb
    :param float tage: total age of species Sb
    :param float density: density of species Sb

    '''
    density_est = 0
    SDF0 = 0

    if density > 0 and (tage > 0 or site_index > 0):
        if sp[0] in ('Sb', 'Lt', 'La', 'Lw', 'L'):
            SDF0 = density # best SDF guess
            tolerance = 0.00001
            within_tolerance = False
            iter_count = 0

            while not within_tolerance:
                result = densitySb(SDF0, tage, site_index, ret_detail=True)
                k1 = result['k1']
                k2 = result['k2']
                density_est = result['density']

                if abs(density-density_est) < tolerance:
                    within_tolerance = True
                else:
                    density_est = (density + density_est)/2
                    SDF0 = density_est * k2/k1
                    iter_count += 1

                if iter_count == 150:
                    LOGGER.warning('Slow convergence')
                    break

    return density_est, SDF0


def sdf_sw(sp, site_index, tage, SDF0_aw, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species list
    :param float site_index: site index of species Sw
    :param float tage: total age of species Sw
    :param float SDF0_aw: Stand Density Factor of species Aw, this parameter indicates that
    the density of Sw depends on the density of Aw
    :param float density: density of species Sw

    '''
    density_est = 0
    SDF0 = 0

    if density > 0 and (tage > 0 or site_index > 0):
        if sp[0] in ('Sw', 'Se', 'Fd', 'Fb', 'Fa'):
            SDF0 = density # best SDF guess
            tolerance = 0.00001
            within_tolerance = False
            iter_count = 0

            while not within_tolerance:
                result = densitySw(SDF0, SDF0_aw, tage, site_index, ret_detail=True)
                k1 = result['k1']
                k2 = result['k2']
                density_est = result['density']

                if abs(density-density_est) < tolerance:
                    within_tolerance = True
                else:
                    density_est = (density + density_est)/2
                    SDF0 = density_est * k2/k1

                iter_count += 1

                if iter_count == 150:
                    LOGGER.warning('Slow convergence')
                    break

    return density_est, SDF0


def sdf_pl(sp, site_index, tage, SDF0_aw, SDF0_sw, SDF0_sb, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species list
    :param float site_index: site index of species Pl
    :param float tage: total age of species Pl
    :param float SDF0_aw: Stand Density Factor of species Aw
    :param float SDF0_sw: Stand Density Factor of species Sw
    :param float SDF0_pl: Stand Density Factor of species Pl
    these parameters SDF above indicate that the density of Pl
    depends on the density of all otehr species
    :param float density: density of species Pl

    '''
    density_est = 0
    SDF0 = 0

    if density > 0 and (tage > 0 or site_index > 0):
        if sp[0] in ('P', 'Pl', 'Pj', 'Pa', 'Pf'):
            SDF0 = density # best SDF guess
            tolerance = 0.00001
            within_tolerance = False
            iter_count = 0

            while not within_tolerance:
                result = densityPl(SDF0_aw, SDF0_sw, SDF0_sb, SDF0, tage, site_index, ret_detail=True)
                k1 = result['k1']
                k2 = result['k2']
                density_est = result['density']

                if abs(density-density_est) < tolerance:
                    within_tolerance = True
                else:
                    density_est = (density + density_est)/2
                    SDF0 = density_est * k2/k1

                iter_count += 1

                if iter_count == 150:
                    LOGGER.warning('Slow convergence')
                    break

    return density_est, SDF0
