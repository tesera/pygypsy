"""Stand density factor estimators"""
import logging

from pygypsy.density import (
    estimate_density_aw,
    estimate_density_sw,
    estimate_density_sb,
    estimate_density_pl,
)

LOGGER = logging.getLogger(__name__)


def estimate_sdf_aw(spc, site_index, bhage, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str spc: species_abbreviation
    :param float site_index: site index of species Aw
    :param float bhage: breast height age of speceis Aw
    :param float density: density of species Aw

    '''
    density_est = 0
    sdf = 0

    if density <= 0 or (bhage <= 0 and site_index <= 0):
        return density_est, sdf

    if spc not in ('Aw', 'Bw', 'Pb', 'A', 'H'):
        raise ValueError('%s is not a valid species', spc)

    sdf = density # best SDF guess
    tolerance = 0.00001
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        result = estimate_density_aw(sdf, bhage, site_index, ret_detail=True)
        k1 = result['k1'] #pylint: disable=invalid-name
        k2 = result['k2'] #pylint: disable=invalid-name
        density_est = result['density']

        if abs(density-density_est) < tolerance:
            within_tolerance = True
        else:
            density_est = (density + density_est) / 2
            sdf = density_est * k2 / k1

        iter_count += 1

        if iter_count == 1500:
            LOGGER.warning('Slow convergence')
            break

    return density_est, sdf


def estimate_sdf_sb(spc, site_index, tage, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str spc: species_abbreviation
    :param float site_index: site index of species Sb
    :param float tage: total age of species Sb
    :param float density: density of species Sb

    '''
    density_est = 0
    sdf = 0

    if density <= 0 or (tage <= 0 and site_index <= 0):
        return density_est, sdf

    if spc not in ('Sb', 'Lt', 'La', 'Lw', 'L'):
        raise ValueError('%s is not a valid species', spc)

    sdf = density # best SDF guess
    tolerance = 0.00001
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        result = estimate_density_sb(sdf, tage, site_index, ret_detail=True)
        k1 = result['k1'] #pylint: disable=invalid-name
        k2 = result['k2'] #pylint: disable=invalid-name
        density_est = result['density']

        if abs(density-density_est) < tolerance:
            within_tolerance = True
        else:
            density_est = (density + density_est)/2
            sdf = density_est * k2/k1

        iter_count += 1

        if iter_count == 150:
            LOGGER.warning('Slow convergence')
            break

    return density_est, sdf


def estimate_sdf_sw(spc, site_index, tage, sdfaw, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str spc: species_abbreviation
    :param float site_index: site index of species Sw
    :param float tage: total age of species Sw
    :param float sdfaw: Stand Density Factor of species Aw, this parameter indicates that
    the density of Sw depends on the density of Aw
    :param float density: density of species Sw

    '''
    density_est = 0
    sdf = 0

    if density <= 0 or (tage <= 0 and site_index <= 0):
        return density_est, sdf

    if spc not in ('Sw', 'Se', 'Fd', 'Fb', 'Fa'):
        raise ValueError('%s is not a valid species', spc)

    sdf = density # best SDF guess
    tolerance = 0.00001
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        result = estimate_density_sw(sdf, sdfaw, tage, site_index, ret_detail=True)
        k1 = result['k1'] #pylint: disable=invalid-name
        k2 = result['k2'] #pylint: disable=invalid-name
        density_est = result['density']

        if abs(density-density_est) < tolerance:
            within_tolerance = True
        else:
            density_est = (density + density_est)/2
            sdf = density_est * k2/k1

        iter_count += 1

        if iter_count == 150:
            LOGGER.warning('Slow convergence')
            break

    return density_est, sdf


def estimate_sdf_pl(spc, site_index, tage, sdfaw, sdfsw, sdfsb, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str spc: species_abbreviation
    :param float site_index: site index of species Pl
    :param float tage: total age of species Pl
    :param float sdfaw: Stand Density Factor of species Aw
    :param float sdfsw: Stand Density Factor of species Sw
    :param float sdfpl: Stand Density Factor of species Pl
    these parameters SDF above indicate that the density of Pl
    depends on the density of all otehr species
    :param float density: density of species Pl

    '''
    density_est = 0
    sdf = 0

    if density <= 0 or (tage <= 0 and site_index <= 0):
        return density_est, sdf

    if spc not in ('P', 'Pl', 'Pj', 'Pa', 'Pf'):
        raise ValueError('%s is not a valid species', spc)

    sdf = density # best SDF guess
    tolerance = 0.00001
    within_tolerance = False
    iter_count = 0

    while not within_tolerance:
        result = estimate_density_pl(sdfaw, sdfsw, sdfsb, sdf,
                                     tage, site_index, ret_detail=True)
        k1 = result['k1'] #pylint: disable=invalid-name
        k2 = result['k2'] #pylint: disable=invalid-name
        density_est = result['density']

        if abs(density-density_est) < tolerance:
            within_tolerance = True
        else:
            density_est = (density + density_est)/2
            sdf = density_est * k2/k1

        iter_count += 1

        if iter_count == 150:
            LOGGER.warning('Slow convergence')
            break

    return density_est, sdf
