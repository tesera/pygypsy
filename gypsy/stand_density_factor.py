"""Stand desnity factor estimators"""
import logging
import numpy as np


LOGGER = logging.getLogger(__name__)


def sdf_aw(sp, site_index, bhage, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
    :param float site_index: site index of species Aw
    :param float bhage: breast height age of speceis Aw
    :param float density: density of species Aw

    '''
    density_est = 0
    SDF0 = 0

    if density <= 0:
        return density_est, SDF0

    if bhage <= 0 or site_index <= 0:
        return density_est, SDF0

    if sp[0] in ('Aw', 'Bw', 'Pb', 'A', 'H'):
        c0 = 0.717966
        c1 = 6.67468
        SDF0 = density # best SDF guess
        acceptableDiff = 0.00001
        NDiffFlag = False
        iterCount = 0

        while NDiffFlag == False:
            b3 = (1+c0) * SDF0**((c1 + np.log(SDF0))/SDF0)
            b2 = (c0/4) * (SDF0**0.5)**(1/(SDF0))
            b1 = -((1/((SDF0/1000)**(0.5))) + np.sqrt(1+np.sqrt(50/(np.sqrt(SDF0)*np.log(50+1))))) * np.log(50+1)
            k1 = 1+np.exp(b1 + (b2*site_index) + (b3*np.log(50+1)))
            k2 = 1+np.exp(b1 + (b2*site_index) + (b3*np.log(1+bhage)))
            density_est = SDF0*k1/k2

            if abs(density-density_est) < acceptableDiff:
                NDiffFlag = True
            else:
                density_est = (density + density_est)/2
                SDF0 = density_est *k2/k1
            iterCount = iterCount + 1

            if iterCount == 1500:
                LOGGER.warning('Slow convergence')
                break

    return density_est, SDF0


def sdf_sb(sp, site_index, tage, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
    :param float site_index: site index of species Sb
    :param float tage: total age of species Sb
    :param float density: density of species Sb

    '''
    density_est = 0
    SDF0 = 0

    if density > 0:
        if tage > 0 or site_index > 0:
            if sp[0] in ('Sb', 'Lt', 'La', 'Lw', 'L'):
                c1 = -26.3836
                c2 = 0.166483
                c3 = 2.738569
                SDF0 = density # best SDF guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(density-density_est) > acceptableDiff:
                    b2 = c3
                    b3 = c3*(SDF0**(1/SDF0))
                    b1 = c1/ ((((SDF0/1000.0)**0.5)+np.log(50+1))**c2)
                    k1 = 1+np.exp(b1+(b2*np.log(site_index))+(b3*np.log(1+50)))
                    k2 = 1+np.exp(b1+(b2*np.log(site_index))+(b3*np.log(1+tage)))
                    density_est = SDF0*k1/k2

                    if abs(density-density_est) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        density_est = (density + density_est)/2
                        SDF0 = density_est * k2/k1
                    iterCount = iterCount + 1

                    if iterCount == 150:
                        LOGGER.warning('Slow convergence')
                        break

    return density_est, SDF0


def sdf_sw(sp, site_index, tage, SDF0, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
    :param float site_index: site index of species Sw
    :param float tage: total age of species Sw
    :param float SDF0: Stand Density Factor of species Aw, this parameter indicates that the density of Sw
    depends on the density of Aw
    :param float density: density of species Sw

    '''
    density_est = 0
    SDF0 = 0

    if density > 0:
        if tage > 0 or site_index > 0:
            if sp[0] in ('Sw', 'Se', 'Fd', 'Fb', 'Fa'):

                if SDF0 == 0:
                    z1 = 0
                elif SDF0 > 0:
                    z1 = 1

                c1 = -231.617
                c2 = 1.176995
                c3 = 1.733601
                SDF0 = density # best SDF guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(density-density_est) > acceptableDiff:
                    b3 = c3*(SDF0**(1/SDF0))
                    b2 = c3
                    b1 = (c1/((np.log(SDF0)+np.log(50+1))**c2))+(z1*((1+(SDF0/1000.0))**0.5))
                    k1 = 1+np.exp(b1+(b2*np.log(site_index))+(b3*np.log(50+1)))
                    k2 = 1+np.exp(b1+(b2*np.log(site_index))+(b3*np.log(1+tage)))
                    density_est = SDF0*k1/k2

                    if abs(density-density_est) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        density_est = (density + density_est)/2
                        SDF0 = density_est * k2/k1

                    iterCount = iterCount + 1

                    if iterCount == 150:
                        LOGGER.warning('Slow convergence')
                        break

    return density_est, SDF0


def sdf_pl(sp, site_index, tage, SDF0_aw, SDF0_sw, SDF0_sb, density):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
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

    if density > 0:
        if tage > 0 or site_index > 0:
            if sp[0] in ('P', 'Pl', 'Pj', 'Pa', 'Pf'):
                c1 = -5.25144
                c2 = -483.195
                c3 = 1.138167
                c4 = 1.017479
                c5 = -0.05471
                c6 = 4.11215

                if SDF0_aw == 0:
                    z1 = 0
                elif SDF0_aw > 0:
                    z1 = 1
                if SDF0_sw == 0:
                    z2 = 0
                elif SDF0_sw > 0:
                    z2 = 1
                if SDF0_sb == 0:
                    z3 = 0
                elif SDF0_sb > 0:
                    z3 = 1

                SDF0 = density # best SDF guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(density-density_est) > acceptableDiff:
                    k = (1+(c6*(SDF0**0.5)))/SDF0
                    b3 = c4*(SDF0**k)
                    b2 = c4/((SDF0**0.5)**c5)
                    b1 = (c1+(z1*(SDF0_aw/1000.0)/2)+(z2*(SDF0_sw/1000.0)/3)+(z3*(SDF0_sb/1000.0)/4.0))+(c2/((SDF0**0.5)**c3))
                    k1 = 1+np.exp(b1+(b2*np.log(site_index))+(b3*np.log(50+1)))
                    k2 = 1+np.exp(b1+(b2*np.log(site_index))+(b3*np.log(1+tage)))
                    density_est = SDF0*k1/k2

                    if abs(density-density_est) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        density_est = (density + density_est)/2
                        SDF0 = density_est * k2/k1

                    iterCount = iterCount + 1

                    if iterCount == 150:
                        LOGGER.warning('Slow convergence')
                        break

    return density_est, SDF0
