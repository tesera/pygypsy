"""Stand desnity factor estimators"""
import numpy as np

def sdf_aw(sp, SI_bh, bhage, N, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
    :param float SI_bh: site index of species Aw
    :param float bhage: breast height age of speceis Aw
    :param float N: density of species Aw

    '''
    N_est = 0
    SDF0 = 0

    if N <= 0:
        return N_est, SDF0

    if bhage <= 0 or SI_bh <= 0:
        return N_est, SDF0

    if sp[0] in ('Aw', 'Bw', 'Pb', 'A', 'H'):
        c0 = 0.717966
        c1 = 6.67468
        SDF0 = N # best SDF guess
        acceptableDiff = 0.00001
        NDiffFlag = False
        iterCount = 0

        while NDiffFlag == False:
            b3 = (1+c0) * SDF0**((c1 + np.log(SDF0))/SDF0)
            b2 = (c0/4) * (SDF0**0.5)**(1/(SDF0))
            b1 = -((1/((SDF0/1000)**(0.5))) + np.sqrt(1+np.sqrt(50/(np.sqrt(SDF0)*np.log(50+1))))) * np.log(50+1)
            k1 = 1+np.exp(b1 + (b2*SI_bh) + (b3*np.log(50+1)))
            k2 = 1+np.exp(b1 + (b2*SI_bh) + (b3*np.log(1+bhage)))
            N_est = SDF0*k1/k2

            if abs(N-N_est) < acceptableDiff:
                NDiffFlag = True
            else:
                N_est = (N + N_est)/2
                SDF0 = N_est *k2/k1
            iterCount = iterCount + 1

            if iterCount == 1500:
                if printWarnings:
                    print '\n GYPSYNonSpatial.densityNonSpatialAw()'
                    print ' Slow convergence'
                return N_est, SDF0

    return N_est, SDF0


def sdf_sb(sp, SI_bh, tage, N, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
    :param float SI_bh: site index of species Sb
    :param float tage: total age of species Sb
    :param float N: density of species Sb

    '''
    N_est = 0
    SDF0 = 0

    if N > 0:
        if tage > 0 or SI_bh > 0:
            if sp[0] in ('Sb', 'Lt', 'La', 'Lw', 'L'):
                c1 = -26.3836
                c2 = 0.166483
                c3 = 2.738569
                SDF0 = N # best SDF guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(N-N_est) > acceptableDiff:
                    b2 = c3
                    b3 = c3*(SDF0**(1/SDF0))
                    b1 = c1/ ((((SDF0/1000.0)**0.5)+np.log(50+1))**c2)
                    k1 = 1+np.exp(b1+(b2*np.log(SI_bh))+(b3*np.log(1+50)))
                    k2 = 1+np.exp(b1+(b2*np.log(SI_bh))+(b3*np.log(1+tage)))
                    N_est = SDF0*k1/k2

                    if abs(N-N_est) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        N_est = (N + N_est)/2
                        SDF0 = N_est * k2/k1
                    iterCount = iterCount + 1

                    if iterCount == 150:
                        if printWarnings:
                            print '\n GYPSYNonSpatial.densityNonSpatialSb()'
                            print ' Slow convergence'
                        return N_est, SDF0

    return N_est, SDF0


def sdf_sw(sp, SI_bh, tage, SDF0, N, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
    :param float SI_bh: site index of species Sw
    :param float tage: total age of species Sw
    :param float SDF0: Stand Density Factor of species Aw, this parameter indicates that the density of Sw
    depends on the density of Aw
    :param float N: density of species Sw

    '''
    N_est = 0
    SDF0 = 0

    if N > 0:
        if tage > 0 or SI_bh > 0:
            if sp[0] in ('Sw', 'Se', 'Fd', 'Fb', 'Fa'):

                if SDF0 == 0:
                    z1 = 0
                elif SDF0 > 0:
                    z1 = 1

                c1 = -231.617
                c2 = 1.176995
                c3 = 1.733601
                SDF0 = N # best SDF guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(N-N_est) > acceptableDiff:
                    b3 = c3*(SDF0**(1/SDF0))
                    b2 = c3
                    b1 = (c1/((np.log(SDF0)+np.log(50+1))**c2))+(z1*((1+(SDF0/1000.0))**0.5))
                    k1 = 1+np.exp(b1+(b2*np.log(SI_bh))+(b3*np.log(50+1)))
                    k2 = 1+np.exp(b1+(b2*np.log(SI_bh))+(b3*np.log(1+tage)))
                    N_est = SDF0*k1/k2

                    if abs(N-N_est) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        N_est = (N + N_est)/2
                        SDF0 = N_est * k2/k1

                    iterCount = iterCount + 1

                    if iterCount == 150:
                        if printWarnings:
                            print '\n GYPSYNonSpatial.densityNonSpatialSw()'
                            print ' Slow convergence'
                        return N_est, SDF0

    return N_est, SDF0


def sdf_pl(sp, SI_bh, tage, SDF0, SDF0, SDF0, N, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp: species name
    :param float SI_bh: site index of species Pl
    :param float tage: total age of species Pl
    :param float SDF0: Stand Density Factor of species Aw
    :param float SDF0: Stand Density Factor of species Sw
    :param float SDF0: Stand Density Factor of species Pl
    these parameters SDF above indicate that the density of Pl
    depends on the density of all otehr species
    :param float N: density of species Pl

    '''
    N_est = 0
    SDF0 = 0

    if N > 0:
        if tage > 0 or SI_bh > 0:
            if sp[0] in ('P', 'Pl', 'Pj', 'Pa', 'Pf'):
                c1 = -5.25144
                c2 = -483.195
                c3 = 1.138167
                c4 = 1.017479
                c5 = -0.05471
                c6 = 4.11215

                if SDF0 == 0:
                    z1 = 0
                elif SDF0 > 0:
                    z1 = 1
                if SDF0 == 0:
                    z2 = 0
                elif SDF0 > 0:
                    z2 = 1
                if SDF0 == 0:
                    z3 = 0
                elif SDF0 > 0:
                    z3 = 1

                SDF0 = N # best SDF guess
                acceptableDiff = 0.00001
                NDiffFlag = False
                iterCount = 0

                while abs(N-N_est) > acceptableDiff:
                    k = (1+(c6*(SDF0**0.5)))/SDF0
                    b3 = c4*(SDF0**k)
                    b2 = c4/((SDF0**0.5)**c5)
                    b1 = (c1+(z1*(SDF0/1000.0)/2)+(z2*(SDF0/1000.0)/3)+(z3*(SDF0/1000.0)/4.0))+(c2/((SDF0**0.5)**c3))
                    k1 = 1+np.exp(b1+(b2*np.log(SI_bh))+(b3*np.log(50+1)))
                    k2 = 1+np.exp(b1+(b2*np.log(SI_bh))+(b3*np.log(1+tage)))
                    N_est = SDF0*k1/k2

                    if abs(N-N_est) < acceptableDiff:
                        NDiffFlag = True
                    else:
                        N_est = (N + N_est)/2
                        SDF0 = N_est * k2/k1

                    iterCount = iterCount + 1

                    if iterCount == 150:
                        if printWarnings:
                            print '\n GYPSYNonSpatial.densityNonSpatialSw()'
                            print ' Slow convergence'
                        return N_est, SDF0

    return N_est, SDF0
