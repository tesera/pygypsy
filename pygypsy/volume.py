"""Volume calculations"""
#pylint: disable=invalid-name
# The invalid name linting is disabled since this is a math heavy module
# it makes sense to use short names. Please still use sensible names for non
# mathematical variables
# TODO: Merchantable volume should call the gross total volume functions
from __future__ import division
import numpy as np

DEFAULT_UTILIZATIONS = {
    "aw": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    },
    "sw": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    },
    "sb": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    },
    "pl": {
        "topDiamInsideBark": 7,
        "stumpDiamOutsideBark": 13,
        "stumpHeight": 0.3
    }
}


def _gross_totalvolume_aw(basal_area, top_height):
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
              * (basal_area ** a2) \
              * (top_height ** a3) \
              * np.exp(1 \
                       + (a4 / ((top_height ** 2) + 1)))

    return tot_vol


def _gross_totalvolume_sw(basal_area, top_height):
    '''White Spruce Gross Total Volume

    Note that inputs may be scalars, or numpy arrays.

    :param float basal_area: basal area
    :param float top_height: top height

    '''
    b1 = 0.41104
    b2 = 0.983108
    b3 = 0.971061
    tot_vol = b1 \
              * (basal_area ** b2) \
              * (top_height ** b3)

    return tot_vol


def _gross_totalvolume_sb(basal_area, top_height):
    '''Black Spruce Gross Total Volume

    Note that inputs may be scalars, or numpy arrays.

    :param float basal_area: basal area
    :param float top_height: top height

    '''
    b1 = 0.48628
    b2 = 0.982962
    b3 = 0.910603
    tot_vol = b1 \
              * (basal_area ** b2) \
              * (top_height ** b3)

    return tot_vol


def _gross_totalvolume_pl(basal_area, top_height):
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
              * (basal_area ** a2) \
              * (top_height ** a3) \
              * np.exp(
                  1 + (a4 / ((top_height ** 2) + 1)))

    return tot_vol

def gross_total_volume(species, *args):
    """Gross total volume

    :param str species: species abbreviation
    :param *args: additional arguments to species specific gross total
                  volume functions

    """
    return {
        'Aw': _gross_totalvolume_aw,
        'Sw': _gross_totalvolume_sw,
        'Sb': _gross_totalvolume_sb,
        'Pl': _gross_totalvolume_pl,
    }[species](*args)


def _merchantable_volume_aw(density, basal_area, top_height, total_volume,
                            stump_dob=13, top_dib=7, stump_height=0.3):
    '''Merchantable volume for white aspen

    Only new variables are the stump diameter outside bark, stump height and
    top diameter inside bark The if below was used (and in other functions) to
    avoid division by zero when density is zero, i.e., when the species is
    absent in the plot.

    :param float density: density
    :param float basal_area: basal area
    :param float top_height: top height
    :param float StumpHeight: stump height
    :param float TopDib: top diameter inside bark
    :param float total_volume: Gross total volume
    :param float StumpDOB:  stump diameter outside bark

    '''
    k = (basal_area * 10000.0 / density) ** 0.5
    b0 = 0.993673
    b1 = 923.5825
    b2 = -3.96171
    b3 = 3.366144
    b4 = 0.316236
    b5 = 0.968953
    b6 = -1.61247
    k1 = total_volume * (k ** b0)
    k2 = (
        b1 \
        * (top_height ** b2) \
        * (stump_dob ** b3) \
        * (stump_height ** b4) \
        * (top_dib ** b5) \
        * (k ** b6)
    ) + k
    merch_vol = k1 / k2

    return merch_vol


def _merchantable_volume_sb(density, basal_area, top_height, total_volume,
                            stump_dob=13, top_dib=7, stump_height=0.3):
    '''Merchantable volume black spruce

    The if below was used (and in other functions) to avoid division by zero
    when density is zero, i.e., when the species is absent in the plot.

    :param float density: density
    :param float top_height: top height
    :param float StumpDOB:  stump diameter outside bark
    :param float StumpHeight: stump height
    :param float TopDib: top diameter inside bark
    :param float total_volume: Gross total volume

    '''
    k = (basal_area * 10000.0 / density) ** 0.5
    b0 = 0.98152
    b1 = 0.678011
    b2 = -1.10256
    b3 = 4.148139
    b4 = 0.511391
    b5 = 1.484988
    b6 = -3.26425
    merch_vol = (total_volume * (k ** b0)) \
                / (
                    (b1 \
                      * (top_height ** b2) \
                      * (stump_dob ** b3) \
                      * (stump_height ** b4) \
                      * (top_dib ** b5) \
                      * (k ** b6)
                    ) + k
                )

    return merch_vol



def _merchantable_volume_sw(density, basal_area, top_height, total_volume,
                            stump_dob=13, top_dib=7, stump_height=0.3):
    '''Merchantable volume for white spruce

    The if below was used (and in other functions) to avoid
    division by zero when density is zero, i.e., when the
    species is absent in the plot.

    :param float density: density
    :param float top_height: top height
    :param float StumpDOB:  stump diameter outside bark
    :param float StumpHeight: stump height
    :param float TopDib: top diameter inside bark
    :param float total_volume: Gross total volume

    '''
    k = (basal_area * 10000.0 / density) ** 0.5
    b0 = 0.996262
    b1 = 7.021736
    b2 = -1.77615
    b3 = 1.91562
    b4 = 0.4111
    b5 = 1.024803
    b6 = -0.80121
    merch_vol = (total_volume * (k ** b0)) \
                / (
                    (b1 \
                     * (top_height ** b2) \
                     * (stump_dob ** b3) \
                     * (stump_height ** b4) \
                     * (top_dib ** b5) \
                     * (k ** b6)
                    ) + k
                )

    return merch_vol



def _merchantable_volume_pl(density, basal_area, top_height, total_volume,
                            stump_dob=13, top_dib=7, stump_height=0.3):
    '''Merchantable volume for lodgepole pine

    The if below was used (and in other functions) to avoid division by zero
    when density is zero, i.e., when the species is absent in the plot.

    :param float density: density
    :param float top_height: top height
    :param float StumpDOB:  stump diameter outside bark
    :param float StumpHeight: stump height
    :param float TopDib: top diameter inside bark
    :param float total_volume: Gross total volume

    '''
    k = (basal_area * 10000.0 / density) ** 0.5
    b0 = 0.989889
    b1 = 1.055091
    b2 = -0.19072
    b3 = 4.915593
    b4 = 0.42574
    b5 = 1.006379
    b6 = -4.87808
    merch_vol = (total_volume * (k ** b0)) \
                / (
                    (b1 \
                     * (top_height ** b2) \
                     * (stump_dob ** b3) \
                     * (stump_height ** b4) \
                     * (top_dib ** b5) \
                     * (k ** b6)
                    ) + k
                )

    return merch_vol


def merchantable_volume(species, *args, **kwargs):
    """Merchantable volume

    :param str species: species abbreviation
    :param *args: additional arguments to species specific gross total
                  volume functions

    """
    return {
        'Aw': _merchantable_volume_aw,
        'Sw': _merchantable_volume_sw,
        'Sb': _merchantable_volume_sb,
        'Pl': _merchantable_volume_pl,
    }[species](*args, **kwargs)
