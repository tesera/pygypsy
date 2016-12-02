"""Density"""
import logging

from pygypsy.density import (
    estimate_density_aw,
    estimate_density_pl,
    estimate_density_sb,
    estimate_density_sw,
)
from pygypsy.utils import estimate_species_composition
from pygypsy.asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge


LOGGER = logging.getLogger(__name__)


def densities_and_SCs_to_250(**kwargs):
    '''Estimate, species composition, top height for all species along time

    Time is counted independently for each species.

    :param float startTage: It uses the oldest species as a reference to
                            become the stand age
    :param float startTageAw, startTageSw, startTageSb, and startTagePl: age
                                                                         for respective
                                                                         species
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
    starttage = kwargs['startTage']
    starttageaw = kwargs['startTageAw']
    y2bh_aw = kwargs['y2bh_Aw']
    starttagesw = kwargs['startTageSw']
    y2bh_sw = kwargs['y2bh_Sw']
    starttagesb = kwargs['startTageSb']
    y2bh_sb = kwargs['y2bh_Sb']
    starttagepl = kwargs['startTagePl']
    y2bh_pl = kwargs['y2bh_Pl']
    sdf_aw0 = kwargs['SDF_Aw0']
    sdf_sw0 = kwargs['SDF_Sw0']
    sdf_pl0 = kwargs['SDF_Pl0']
    sdf_sb0 = kwargs['SDF_Sb0']
    si_bh_aw = kwargs['SI_bh_Aw']
    si_bh_sw = kwargs['SI_bh_Sw']
    si_bh_sb = kwargs['SI_bh_Sb']
    si_bh_pl = kwargs['SI_bh_Pl']
    densities_along_time = []
    starttageawb = starttageaw
    starttageswb = starttagesw
    starttageplb = starttagepl
    starttagesbb = starttagesb
    year = 1

    while year < 250:
        tage_aw = starttageawb - starttage
        tage_sw = starttageswb - starttage
        tage_pl = starttageplb - starttage
        tage_sb = starttagesbb - starttage
        bhage_aw = tage_aw - y2bh_aw
        bhage_sw = tage_sw - y2bh_sw
        bhage_pl = tage_pl - y2bh_pl
        bhage_sb = tage_sb - y2bh_sb

        if bhage_aw < 0:
            n_bh_awt = 0
        else:
            n_bh_awt = estimate_density_aw(sdf_aw0, bhage_aw, si_bh_aw)

        if tage_sb < 0:
            n_bh_sbt = 0
        else:
            n_bh_sbt = estimate_density_sb(sdf_sb0, tage_sb, si_bh_sb)

        if tage_sw < 0:
            n_bh_swt = 0
        else:
            n_bh_swt = estimate_density_sw(sdf_sw0, sdf_aw0, tage_sw, si_bh_sw)

        if tage_pl < 0:
            n_bh_plt = 0
        else:
            n_bh_plt = estimate_density_pl(sdf_aw0, sdf_sw0, sdf_sb0, sdf_pl0,
                                           tage_pl, si_bh_pl)



        if n_bh_awt <= 0:
            topheight_aw = 0
        else:
            topheight_aw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Aw', si_bh_aw, tage_aw
            )

        if n_bh_sbt <= 0:
            topheight_sb = 0
        else:
            topheight_sb = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Sb', si_bh_sb, tage_sb
            )

        if n_bh_swt <= 0:
            topheight_sw = 0
        else:
            topheight_sw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Sw', si_bh_sw, tage_sw
            )

        if n_bh_plt <= 0:
            topheight_pl = 0
        else:
            topheight_pl = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
                'Pl', si_bh_pl, tage_pl
            )


        sc_aw, sc_sw, sc_sb, sc_pl = estimate_species_composition(n_bh_awt, n_bh_sbt,
                                                                  n_bh_swt, n_bh_plt)

        densities_along_time.append({
            'N_bh_AwT': n_bh_awt, 'N_bh_SwT': n_bh_swt,
            'N_bh_SbT': n_bh_sbt, 'N_bh_PlT': n_bh_plt,
            'SC_Aw': sc_aw, 'SC_Sw': sc_sw,
            'SC_Sb':sc_sb, 'SC_Pl': sc_pl,
            'tage_Aw': tage_aw, 'tage_Sw': tage_sw,
            'tage_Sb': tage_sb, 'tage_Pl': tage_pl,
            'bhage_Aw': bhage_aw, 'bhage_Sw': bhage_sw,
            'bhage_Sb': bhage_sb, 'bhage_Pl': bhage_pl,
            'topHeight_Aw': topheight_aw, 'topHeight_Sw': topheight_sw,
            'topHeight_Sb': topheight_sb, 'topHeight_Pl': topheight_pl
        })
        year += 1
        starttageawb += 1
        starttageswb += 1
        starttageplb += 1
        starttagesbb += 1

    return densities_along_time


