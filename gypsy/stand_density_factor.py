"""Stand desnity factor estimators"""
import numpy as np

def sdf_aw(sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Aw: species name
    :param float SI_bh_Aw: site index of species Aw
    :param float bhage_Aw: breast height age of speceis Aw
    :param float N_Aw: density of species Aw

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
            b3 = (1+c0) * SDF_Aw0**((c1 + np.log(SDF_Aw0))/SDF_Aw0)
            b2 = (c0/4) * (SDF_Aw0**0.5)**(1/(SDF_Aw0))
            b1 = -((1/((SDF_Aw0/1000)**(0.5))) + np.sqrt(1+np.sqrt(50/(np.sqrt(SDF_Aw0)*np.log(50+1))))) * np.log(50+1)
            k1 = 1+np.exp(b1 + (b2*SI_bh_Aw) + (b3*np.log(50+1)))
            k2 = 1+np.exp(b1 + (b2*SI_bh_Aw) + (b3*np.log(1+bhage_Aw)))
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


def sdf_sb(sp_Sb, SI_bh_Sb, tage_Sb, N_Sb, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Sb: species name
    :param float SI_bh_Sb: site index of species Sb
    :param float tage_Sb: total age of species Sb
    :param float N_Sb: density of species Sb

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
                    b1 = c1/ ((((SDF_Sb0/1000.0)**0.5)+np.log(50+1))**c2)
                    k1 = 1+np.exp(b1+(b2*np.log(SI_bh_Sb))+(b3*np.log(1+50)))
                    k2 = 1+np.exp(b1+(b2*np.log(SI_bh_Sb))+(b3*np.log(1+tage_Sb)))
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


def sdf_sw(sp_Sw, SI_bh_Sw, tage_Sw, SDF_Aw0, N_Sw, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Sw: species name
    :param float SI_bh_Sw: site index of species Sw
    :param float tage_Sw: total age of species Sw
    :param float SDF_Aw0: Stand Density Factor of species Aw, this parameter indicates that the density of Sw
    depends on the density of Aw
    :param float N_Sw: density of species Sw

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
                    b1 = (c1/((np.log(SDF_Sw0)+np.log(50+1))**c2))+(z1*((1+(SDF_Aw0/1000.0))**0.5))
                    k1 = 1+np.exp(b1+(b2*np.log(SI_bh_Sw))+(b3*np.log(50+1)))
                    k2 = 1+np.exp(b1+(b2*np.log(SI_bh_Sw))+(b3*np.log(1+tage_Sw)))
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


def sdf_pl(sp_Pl, SI_bh_Pl, tage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, N_Pl, printWarnings=True):
    '''Main purpose of this function is to estimate SDF for the species

    :param str sp_Pl: species name
    :param float SI_bh_Pl: site index of species Pl
    :param float tage_Pl: total age of species Pl
    :param float SDF_Aw0: Stand Density Factor of species Aw
    :param float SDF_Sw0: Stand Density Factor of species Sw
    :param float SDF_Pl0: Stand Density Factor of species Pl
    these parameters SDF above indicate that the density of Pl
    depends on the density of all otehr species
    :param float N_Pl: density of species Pl

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
                    k1 = 1+np.exp(b1+(b2*np.log(SI_bh_Pl))+(b3*np.log(50+1)))
                    k2 = 1+np.exp(b1+(b2*np.log(SI_bh_Pl))+(b3*np.log(1+tage_Pl)))
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
