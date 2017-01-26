from __future__ import division

import logging
import numpy


LOGGER = logging.getLogger(__name__)


def ComputeGypsySiteIndex(species = 'Aw', totalHeight = 1.3, bhage = 0, totalAge = 0):
    '''
    Total age is unknown
    Breast height age is known
    Total height is known

    Equations and logic derived from:
    Huang, S., Meng, S.X., and Yang, Y. 2009. A growth and yield projection system (GYPSY) for natural and
    post-harvest stands in Alberta. Technical Report Pb. No.:T/216. Forest Management Branch, Alberta Sustainable
    Resource Development, Edmonton, AB, CAN.  Appendix I. Pp. 21,22.

    Error in white spruce equation discovered Dec 5 2014

    '''
    tage = totalAge
    si0 = 0
    iterCount = 0
    if totalHeight > 1.3:
        if bhage > 0 or totalAge > 0:
            if species == 'P' or \
               species == 'Pl' or \
               species == 'Pj' or \
               species == 'Pa' or \
               species == 'Pf':
                b1 = 12.84571
                b2 = -5.73936
                b3 = -0.91312
                b4 = 0.150668
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
                    k2 = si0**b3
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        #tage = totalAge
                        bhage = tage - y2bh
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/x20)
                    si0 = (si0+si1)/2
                SI_t=si1
                # estimating Site index BH
                k11=1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(SI_t)**1+b4*(50**0.5))
                k21= 1+numpy.exp(b1+b2*(numpy.log(50+y2bh+1)**0.5)+b3*numpy.log(SI_t)+b4*(50**0.5))
                SI_bh=SI_t*k11/k21


            if species == 'Sw' or \
               species == 'Se' or \
               species == 'Fd' or \
               species == 'Fb' or \
               species == 'Fa':
                b1 = 12.14943
                b2 = -3.77051
                b3 = -0.28534
                b4 = 0.165483
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50**2+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
                    k2 = si0**(b3*numpy.log(si0))
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = (numpy.exp((numpy.log(k3)/b2)**2)-1)**0.5
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        #tage = totalAge
                        bhage = tage - y2bh
                    #x10 = (1+numpy.exp(b1+b2*(numpy.log((tage**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    #x20 = (1+numpy.exp(b1+b2*(numpy.log((50**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x10 = (1+numpy.exp(b1+b2*((numpy.log((tage**2)+1))**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*((numpy.log((50**2)+1))**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/x20)
                    si0 = (si0+si1)/2
                    iterCount = iterCount + 1
                    if iterCount == 1000:
                        LOGGER.warning(('Site index Routine Terminated; iter > 1000 '
                                        'Sp = %s, treeHt = %s, treeSi = %s, treeAge = %s'),
                                       species, totalHeight, si0, totalAge)
                    SI_bh=0
                SI_t=si1
                # estimating Site index BH
                k11=1+numpy.exp(b1+b2*(((numpy.log(50**2+1)))**0.5)+b3*(numpy.log(SI_t))**2+b4*(50**0.5) )
                k21=1+numpy.exp(b1+b2*(numpy.log(1+(50+y2bh)**2)**0.5)+b3*((numpy.log(SI_t))**2)+b4*(50**0.5) )
                SI_bh=SI_t*k11/k21

            if species == 'Sb' or \
               species == 'Lt' or \
               species == 'La' or \
               species == 'Lw' or \
               species == 'L':
                b1 = 14.56236
                b2 = -6.04705
                b3 = -1.53715
                b4 = 0.240174
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
                    k2 = si0**b3
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        #tage = totalAge
                        bhage = tage - y2bh
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/x20)
                    si0 = (si0+si1)/2
                    SI_bh=0
                SI_t=si1
                # estimating Site index BH
                k11=1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(SI_t)+b4*(50**0.5))
                k21=1+numpy.exp(b1+b2*((numpy.log(50+y2bh+1))**0.5)+b3*numpy.log(SI_t)+b4*(50**0.5))
                SI_bh=SI_t*k11/k21

            if species == 'Aw' or \
               species == 'Bw' or \
               species == 'Pb' or \
               species == 'A' or \
               species == 'H':
                b1 = 9.908888
                b2 = -3.92451
                b3 = -0.32778
                b4 = 0.134376
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
                    k2 = si0**(b3*numpy.log(si0))
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        tage = totalAge
                        bhage = tage - y2bh
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/x20)
                    si0 = (si0+si1)/2
                    SI_bh=0
                SI_t=si1
                # estimating Site index BH
                SI_bh=SI_t*(1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(SI_t))**2+b4*(50**0.5)))/(1+numpy.exp(b1+b2*(numpy.log(50+y2bh+1)**0.5)+b3*((numpy.log(SI_t))**2)+b4*(50**0.5)))
        else:
            SI_t = 0
            SI_bh = 0
            y2bh = None
    else:
        if totalHeight<1.3:
            startHt = 0.01
            a = numpy.log(totalHeight/startHt)/totalAge
            y2bh=numpy.log(1.3/startHt)/a
        else:
            y2bh = totalAge


        guessSI = 10 # best SI_t guess
        tolerance = 0.00001
        within_tolerance = False
        iter_count = 0

        while within_tolerance == False:
            est_y2bh = computeGypsyY2BHGivenSpSI(species, guessSI)

            if abs(est_y2bh-y2bh) < tolerance:
                within_tolerance = True
                SI_t = guessSI
            else:
                guessSI = (((est_y2bh+y2bh)/2)/y2bh)*guessSI
                iter_count += 1
                if iter_count == 1000:
                    LOGGER.warning('Slow convergence')
                    break
        SI_bh = SI_t
        tage = totalAge
        bhage = tage - y2bh

    return bhage, tage, SI_t, y2bh, SI_bh

def ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(species = 'Aw', siteIndex = 1.3, totalAge = 0):
    '''
    Equations and logic derived from:
    Huang, S., Meng, S.X., and Yang, Y. 2009. A growth and yield projection system (GYPSY) for natural and
    post-harvest stands in Alberta. Technical Report Pb. No.:T/216. Forest Management Branch, Alberta Sustainable
    Resource Development, Edmonton, AB, CAN.  Appendix I. Pp. 21,22.

    Error in white spruce equation discovered Dec 5 2014

    '''
    tage = totalAge
    si0 = siteIndex
    treeHeight = 0
    if siteIndex > 1.3:
        if totalAge > 0:
            if species == 'P' or \
               species == 'Pl' or \
               species == 'Pj' or \
               species == 'Pa' or \
               species == 'Pf':
                b1 = 12.84571
                b2 = -5.73936
                b3 = -0.91312
                b4 = 0.150668
                x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/x20)
            if species == 'Sw' or \
               species == 'Se' or \
               species == 'Fd' or \
               species == 'Fb' or \
               species == 'Fa':
                b1 = 12.14943
                b2 = -3.77051
                b3 = -0.28534
                b4 = 0.165483
                #x10 = (1+numpy.exp(b1+b2*(numpy.log((50**2)+1)**0.5)+b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                #x20 = (1+numpy.exp(b1+b2*(numpy.log((totalAge**2)+1)**0.5)+b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                #treeHeight = siteIndex*(x10/x20)
                x10 = (1+numpy.exp(b1+b2*((numpy.log((50**2)+1))**0.5)+b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*((numpy.log((totalAge**2)+1))**0.5) +b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/x20)

            if species == 'Sb' or \
               species == 'Lt' or \
               species == 'La' or \
               species == 'Lw' or \
               species == 'L':
                b1 = 14.56236
                b2 = -6.04705
                b3 = -1.53715
                b4 = 0.240174
                x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/x20)
            if species == 'Aw' or \
               species == 'Bw' or \
               species == 'Pb' or \
               species == 'A' or \
               species == 'H':
                b1 = 9.908888
                b2 = -3.92451
                b3 = -0.32778
                b4 = 0.134376
                x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/x20)
        else:
            treeHeight = 0
    else:
            treeHeight = 0

    return treeHeight

def computeTreeAge(siSp='',treeHt = 20, treeSi=15, maxTreeAge = 450,
                   rowIndex = 0):
    if treeHt >1.3:
        maxTreeAgeAw = 200
        maxTreeAgePl = 250
        maxTreeAgeSw = 450
        maxTreeAgeSb = 450
        maxTreeAge = {'Aw': maxTreeAgeAw, 'Pl': maxTreeAgePl, 'Sw': maxTreeAgeSw, 'Sb': maxTreeAgeSb}
        treeAge = (treeHt/treeSi)*25
        htDiffFlag = False
        iterCount = 0
        acceptableDiff = 0.0001
        while htDiffFlag == False:
            newHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, treeSi, treeAge)
            if abs(treeHt-newHt) < acceptableDiff:
                htDiffFlag = True
            else:
                #treeAge = ((treeHt-newHt)/treeHt)*(treeAge/2) + treeAge
                treeAge = ((treeHt-newHt)/treeHt)*(treeAge) + treeAge
            iterCount = iterCount + 1

            if iterCount == 150:
                LOGGER.info(('Slow convergence'
                             'Sp = %s, treeHt = %s, treeSi = %s, treeAge = %s'),
                            siSp, treeHt, treeSi, treeAge)
            if treeAge > 1000:
                htDiffFlag = True
                LOGGER.warning(('Tree Age Search Routine Terminated; treeAge > 1000 '
                                'Sp = %s, treeHt = %s, treeSi = %s, treeAge = %s'),
                               siSp, treeHt, treeSi, treeAge)
                treeAge = maxTreeAge[siSp]
            if treeAge < 0:
                htDiffFlag = True
                LOGGER.warning('Slow convergence with negative treeAge: %s', treeAge)
                treeAge = 0
    else:
        y2bh = computeGypsyY2BHGivenSpSI(siSp, treeSi)
        ht = 1.3
        startHt = 0.01 # start tree height assumed tom be 1 cm

        a = numpy.log(ht/startHt)/y2bh
        treeAge = numpy.log(treeHt/startHt)/a

    return treeAge



def computeGypsyY2BHGivenSpSI(species = 'Aw', si0 = 5):
    '''
    Compute years to breast height given species and site index

    Huang, S., Meng, S.X., and Yang, Y. 2009. A growth and yield projection system (GYPSY) for natural and
    post-harvest stands in Alberta. Technical Report Pb. No.:T/216. Forest Management Branch, Alberta Sustainable
    Resource Development, Edmonton, AB, CAN.  Appendix I. Pp. 21,22.
    '''
    if species == 'P' or \
               species == 'Pl' or \
               species == 'Pj' or \
               species == 'Pa' or \
               species == 'Pf':
        b1 = 12.84571
        b2 = -5.73936
        b3 = -0.91312
        b4 = 0.150668
        k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
        k2 = si0**b3
        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
        y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
    if species == 'Sw' or \
               species == 'Se' or \
               species == 'S'  or \
               species == 'Fd' or \
               species == 'Fb' or \
               species == 'Fa':
        b1 = 12.14943
        b2 = -3.77051
        b3 = -0.28534
        b4 = 0.165483
        k1 = numpy.exp(b1+b2*(numpy.log(50**2+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
        k2 = si0**(b3*numpy.log(si0))
        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
        y2bh = (numpy.exp((numpy.log(k3)/b2)**2)-1)**0.5
    if species == 'Sb' or \
               species == 'Lt' or \
               species == 'La' or \
               species == 'Lw' or \
               species == 'L':
        b1 = 14.56236
        b2 = -6.04705
        b3 = -1.53715
        b4 = 0.240174
        k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
        k2 = si0**b3
        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
        y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
    if species == 'Aw' or \
               species == 'Bw' or \
               species == 'Pb' or \
               species == 'A' or \
               species == 'H':
        b1 = 9.908888
        b2 = -3.92451
        b3 = -0.32778
        b4 = 0.134376
        k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
        k2 = si0**(b3*numpy.log(si0))
        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
        y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
    return  y2bh
