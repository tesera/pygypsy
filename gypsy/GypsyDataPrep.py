# -*- coding: utf-8 -*-
""" Data Preparation
"""
from copy import deepcopy
from asaCompileAgeGivenSpSiHt import (computeTreeAge,
                                      ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge,
                                      ComputeGypsySiteIndex)

from GYPSYNonSpatial import (densityNonSpatialAw,
                             densityNonSpatialSb,
                             densityNonSpatialSw,
                             densityNonSpatialPl,
                             densityAw,
                             densitySw,
                             densitySb,
                             densityPl,
                             BasalAreaIncrementNonSpatialAw,
                             BasalAreaIncrementNonSpatialSw,
                             BasalAreaIncrementNonSpatialPl,
                             BasalAreaIncrementNonSpatialSb,
                             SCestimate)


# TODO: replace acronyms with something more verbose
# TODO: use pure functions or class instances to avoid mutating global state
# TODO: formal docstrings so we can generate nice documentation
# TODO: more subroutines and wrapper functions for easier readability


plot_dict = {}


def SIfromDomSp(domSp, SI):
    if SI > 0:
        if domSp == 'Aw':
            SI_Aw = SI
            SI_Pl = 0.85 * SI_Aw + 3.4
            SI_Sw = 1.31 * SI_Aw - 2.64
            SI_Fb = 0.92 * SI_Sw + 1.68
            SI_Fd = 0.94 * SI_Pl + 0.71
            SI_Sb = 0.64 * SI_Pl + 2.76
            SI_Pb = SI_Aw

        elif domSp == 'Sw':
            SI_Sw = SI
            SI_Pl = 0.86 * SI_Sw + 2.13
            SI_Aw = 0.76 * SI_Sw + 2.01
            SI_Fb = 0.92 * SI_Sw + 1.68
            SI_Fd = 0.74 * SI_Sw + 4.75
            SI_Sb = 0.64 * SI_Pl + 2.76
            SI_Pb = SI_Aw

        elif domSp == 'Fb':
            SI_Fb = SI
            SI_Sw = 1.09 * SI_Fb - 1.83
            SI_Pl = 0.86 * SI_Sw + 2.13
            SI_Aw = 0.76 * SI_Sw + 2.01
            SI_Fd = 0.74 * SI_Sw + 4.75
            SI_Sb = 0.64 * SI_Pl + 2.76
            SI_Pb = SI_Aw

        if domSp == 'Fd':
            SI_Fd = SI
            SI_Pl = 1.07 * SI_Fd - 0.76
            SI_Aw = 1.18 * SI_Pl  - 4.02
            SI_Sw = 1.36 * SI_Fd  - 6.45
            SI_Pb = SI_Aw
            SI_Fb = 0.92 * SI_Sw + 1.68
            SI_Sb = 0.64 * SI_Pl + 2.76

        if domSp == 'Pl':
            SI_Pl = SI
            SI_Aw = 1.18 * SI_Pl  - 4.02
            SI_Sw = 1.16 * SI_Pl  - 2.47
            SI_Fd = 0.94* SI_Pl + 0.71
            SI_Pb = SI_Aw
            SI_Fb = 0.92 * SI_Sw + 1.68
            SI_Sb = 0.64 * SI_Pl + 2.76

        if domSp == 'Pb':
            SI_Pb = SI
            SI_Aw = SI_Pb
            SI_Pl = 0.85 * SI_Aw + 3.4
            SI_Sw = 1.31 * SI_Aw -2.64
            SI_Fd = 0.92* SI_Pl + 1.68
            SI_Fb = 0.92 * SI_Sw + 1.68
            SI_Sb = 0.64 * SI_Pl + 2.76

    return SI_Aw, SI_Pl, SI_Sw, SI_Sb



def dataPrepGypsy(data):
    ''' define SI of all other species given the dominant species

    :param data: # TODO:
    '''
    domSp = 'Aw'
    SI = 1
    SIfromDomSp(domSp, SI)

    for _, row in data.iterrows():

        # top height, total age, BH age, N (or density), current Basal Area,
        # Measured Percent Stocking, StumpDOB, StumpHeight, TopDib, SI,
        # Proportion of the species
        _default_species_fplot_dict = {
            'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0,
            'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7,
            'SI': 0, 'PCT': 0
        }
        # plot properties for each species, starting with default values
        # defined above
        fplot = {
            'Aw': deepcopy(_default_species_fplot_dict),
            'Pl': deepcopy(_default_species_fplot_dict),
            'Sw': deepcopy(_default_species_fplot_dict),
            'Sb': deepcopy(_default_species_fplot_dict),
        }

        PlotID = row['id_l1']

        tempDomSp = row['SP1']

        #print tempDomSp
        # TODO: pull these functions out of the outer function
        def initSI_estimation(tempDomSp):
            if tempDomSp == 'Pb':
                tempDomSp = 'Aw'
            elif tempDomSp == 'Fd' or tempDomSp == 'Fb':
                tempDomSp = 'Sw'
            return tempDomSp

        # estimate SI Dom from inventory Age and HD !!!!
        # Use this SI to estimate the other species SIs
        # ex: FD is dom sp take HD and Age, assume FD is Sw generate SI for Sw
        # get the SW SI
        # calculate the SIs for other sp from the conversion formulas

        domTage = row['AGE']
        domHT = row['HD']


        def domSpSI_estim(tempDomSp, domTage, domHT):
            domSI = ComputeGypsySiteIndex(tempDomSp, domHT, 0, domTage)
            SI = domSI[2]
            # using SI = SI_t , site index based on total age
            # from the ComputeGypsySiteIndex function
            return SI


        SI = domSpSI_estim(tempDomSp, domTage, domHT)
        DomSp = initSI_estimation(tempDomSp)
        SI_x = SIfromDomSp(DomSp, SI)

        # TODO: this function uses variables from the enclosing scope
        # need to pass the variable into the function instead
        def otherSpSIs(SI):
            """fill the dictionary with estimated SIs

            fill all the SIs to avoid IFs and loops. Some of them will not be used.

            :param SI: # TODO
            """
            if DomSp == 'Aw':
                fplot['Aw']['SI'] = SI
                fplot['Pl']['SI'] = SI_x[1]
                fplot['Sw']['SI'] = SI_x[2]
                fplot['Sb']['SI'] = SI_x[3]

            elif DomSp == 'Sw':
                fplot['Aw']['SI'] = SI_x[0]
                fplot['Pl']['SI'] = SI_x[1]
                fplot['Sw']['SI'] = SI
                fplot['Sb']['SI'] = SI_x[3]

            elif DomSp == 'Pl':
                fplot['Aw']['SI'] = SI_x[0]
                fplot['Pl']['SI'] = SI
                fplot['Sw']['SI'] = SI_x[2]
                fplot['Sb']['SI'] = SI_x[3]

            elif DomSp == 'Sb':
                fplot['Aw']['SI'] = SI_x[0]
                fplot['Pl']['SI'] = SI_x[1]
                fplot['Sw']['SI'] = SI_x[2]
                fplot['Sb']['SI'] = SI

            return fplot

        fplot = otherSpSIs(SI)

        #print SI, DomSp , fplot['Sw']['SI']
        #print '----\n'


        sp1 = row['SP1']
        sp2 = row['SP2']
        sp3 = row['SP3']
        sp4 = row['SP4']
        sp5 = row['SP5']

        pct1 = row['PCT1']
        pct2 = row['PCT2']
        pct3 = row['PCT3']
        pct4 = row['PCT4']
        pct5 = row['PCT5']



        spList = [
            (sp1, pct1), (sp2, pct2), (sp3, pct3), (sp4, pct4), (sp5, pct5)
        ]

        check_prop = sum(zip(*spList)[1])
        if check_prop != 100:
            raise ValueError('Species proportions not correct: %s' % check_prop)


        def sortedSp(spList, spList1={'Aw':0, 'Pl':0, 'Sw':0, 'Sb':0}):

            for sp in spList:
                if sp[0] == 'Aw' or sp[0] == 'Pb':
                    spList1['Aw'] = spList1['Aw'] + sp[1]

                elif sp[0] == 'Sw' or sp[0] == 'Fb' or sp[0] == 'Fd':
                    spList1['Sw'] = spList1['Sw'] + sp[1]

                elif sp[0] == 'Pl':
                    spList1['Pl'] = spList1['Pl'] + sp[1]

                elif sp[0] == 'Sb':
                    spList1['Sb'] = spList1['Sb'] + sp[1]

            sorted_spList1 = [(k, v) for v, k in sorted(
                [(v, k) for k, v in spList1.items()]
            )]

            sorted_spList1.reverse()

            check_prop1 = sum(spList1.values())
            if check_prop1 != 100:
                raise ValueError(
                    ('Species proportions after grouping '
                     'into 4 species is not correct: %s') % check_prop1
                )

            return sorted_spList1, spList1

        sorted_spList1, spList1 = sortedSp(spList)

        fplot['Aw']['PCT'] = spList1['Aw']
        fplot['Pl']['PCT'] = spList1['Pl']
        fplot['Sw']['PCT'] = spList1['Sw']
        fplot['Sb']['PCT'] = spList1['Sb']

        domSp = sorted_spList1[0]



        # iterate over each ranked species - populate the dictionary with
        # values estimated from the dominant species' SI
        for sp in sorted_spList1:

            if sp[1] == 0:
                break
            elif sp[0] == domSp[0]:
                fplot[sp[0]]['tage'] = domTage
                fplot[sp[0]]['topHeight'] = domHT
                fplot[sp[0]]['N'] = row['TPH'] * sp[1] / 100
                fplot[sp[0]]['BA'] = row['BPH'] * sp[1] / 100
                x_Si = ComputeGypsySiteIndex(
                    sp[0],
                    fplot[sp[0]]['topHeight'],
                    0,
                    fplot[sp[0]]['tage']
                )
                fplot[sp[0]]['bhage'] = x_Si[0]
                # if, after re-arranging the proportions, dom species is another
                # one then we need to re-estimate everything  even for the new
                # dominant species

            else:
                siSp = fplot[sp[0]]['SI']
                fplot[sp[0]]['PCT'] = sp[1]
                # estimate tree age iteratively calling computeTreeAge function
                # and inputing SI in the place ot treeSi and domHT as
                # treeHT or topheight'''

                fplot[sp[0]]['tage'] = computeTreeAge(
                    sp[0],
                    treeHt=domHT,
                    treeSi=siSp,
                    maxTreeAge=450,
                    rowIndex=0,
                    printWarnings=True
                )

                # density based on the proportion of the species
                fplot[sp[0]]['N'] = row['TPH'] * sp[1]/100

                # Basal area from the species proportion as well
                fplot[sp[0]]['BA'] = row['BPH'] * sp[1]/100

                # calling the ComputeGypsySiteIndex function, estimate bhage
                x_Si = ComputeGypsySiteIndex(
                    sp[0], domHT, 0,
                    fplot[sp[0]]['tage']
                )
                fplot[sp[0]]['bhage'] = x_Si[0]


        # now we have different lists containing:
        # species, top height, total age, BHage (from the function),
        # N (or density), current Basal Area,  Measured Percent Stocking,
        # StumpDOB , StumpHeight, TopDib, SI, sp proportion
        SI_Aw = fplot['Aw']['SI']
        SI_Sw = fplot['Sw']['SI']
        SI_Pl = fplot['Pl']['SI']
        SI_Sb = fplot['Sb']['SI']

        N_Aw = fplot['Aw']['N']
        N_Sw = fplot['Sw']['N']
        N_Pl = fplot['Pl']['N']
        N_Sb = fplot['Sb']['N']

        # TODO: sometimes these values are zero because TPH is zero
        # ...WHY TPH IS ZERO????
        y2bh_Aw = fplot['Aw']['tage'] - fplot['Aw']['bhage']
        y2bh_Sw = fplot['Sw']['tage'] - fplot['Sw']['bhage']
        y2bh_Pl = fplot['Pl']['tage'] - fplot['Pl']['bhage']
        y2bh_Sb = fplot['Sb']['tage'] - fplot['Sb']['bhage']

        # y2bh CANNOT BE NEGATIVE

        tage_Aw = fplot['Aw']['tage']
        tage_Sw = fplot['Sw']['tage']
        tage_Pl = fplot['Pl']['tage']
        tage_Sb = fplot['Sb']['tage']

        #print tage_Sw



        sp_Aw = ['Aw', fplot['Aw']['topHeight'], fplot['Aw']['tage'], fplot['Aw']['bhage'], fplot['Aw']['N'], fplot['Aw']['BA'], fplot['Aw']['PS'], fplot['Aw']['StumpDOB'], fplot['Aw']['StumpHeight'], fplot['Aw']['TopDib'], fplot['Aw']['SI'], fplot['Aw']['PCT']]
        sp_Pl = ['Pl', fplot['Pl']['topHeight'], fplot['Pl']['tage'], fplot['Pl']['bhage'], fplot['Pl']['N'], fplot['Pl']['BA'], fplot['Pl']['PS'], fplot['Pl']['StumpDOB'], fplot['Pl']['StumpHeight'], fplot['Pl']['TopDib'], fplot['Pl']['SI'], fplot['Pl']['PCT']]
        sp_Sw = ['Sw', fplot['Sw']['topHeight'], fplot['Sw']['tage'], fplot['Sw']['bhage'], fplot['Sw']['N'], fplot['Sw']['BA'], fplot['Sw']['PS'], fplot['Sw']['StumpDOB'], fplot['Sw']['StumpHeight'], fplot['Sw']['TopDib'], fplot['Sw']['SI'], fplot['Sw']['PCT']]
        sp_Sb = ['Sb', fplot['Sb']['topHeight'], fplot['Sb']['tage'], fplot['Sb']['bhage'], fplot['Sb']['N'], fplot['Sb']['BA'], fplot['Sb']['PS'], fplot['Sb']['StumpDOB'], fplot['Sb']['StumpHeight'], fplot['Sb']['TopDib'], fplot['Sb']['SI'], fplot['Sb']['PCT']]

        bhage_Aw = sp_Aw[3]
        tage_Aw = sp_Aw[2]
        si_Aw = sp_Aw[10]
        y2bh_Aw = tage_Aw - bhage_Aw
        SI_bh_Aw = sp_Aw[10]
        # treeHeight is the Top Height or Htop in the paper
        topHeight_Aw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_Aw[0], si_Aw, tage_Aw
        )

        bhage_Sb = sp_Sb[3]
        tage_Sb = sp_Sb[2]
        si_Sb = sp_Sb[10]
        SI_bh_Sb = sp_Sb[10]
        topHeight_Sb = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_Sb[0], si_Sb, tage_Sb
        )

        bhage_Pl = sp_Pl[3]
        tage_Pl = sp_Pl[2]
        si_Pl = sp_Pl[10]
        y2bh_Pl = tage_Pl - bhage_Pl
        SI_bh_Pl = sp_Pl[10]
        topHeight_Pl = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_Pl[0], si_Pl, tage_Pl
        )

        bhage_Sw = sp_Sw[3]
        tage_Sw = sp_Sw[2]
        si_Sw = sp_Sw[10]
        y2bh_Sw = tage_Sw - bhage_Sw
        SI_bh_Sw = sp_Sw[10]
        topHeight_Sw = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(
            sp_Sw[0], si_Sw, tage_Sw
        )

        # si, bhage, and tage are passed on from the above.
        # SDFs estimated iteratively
        # using N from the original input sp_Aw etc as the input (N_Aw) etc
        # I think it is suposed to be the density of the species at the bhage = 0, although
        # the paper says current or inital density
        N_Aw = sp_Aw[4]
        N_Sb = sp_Sb[4]
        N_Sw = sp_Sw[4]
        N_Pl = sp_Pl[4]

        y_Aw = densityNonSpatialAw(sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw)
        SDF_Aw0 = y_Aw[1]
        N_bh_Aw = y_Aw[0]

        y_Sb = densityNonSpatialSb(sp_Sb, SI_bh_Sb, tage_Sb, N_Sb)
        SDF_Sb0 = y_Sb[1]
        N_bh_Sb = y_Sb[0]

        y_Sw = densityNonSpatialSw(sp_Sw, SI_bh_Sw, tage_Sw, SDF_Aw0, N_Sw)
        SDF_Sw0 = y_Sw[1]
        N_bh_Sw = y_Sw[0]

        y_Pl = densityNonSpatialPl(sp_Pl, SI_bh_Pl, tage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, N_Pl)
        SDF_Pl0 = y_Pl[1]
        N_bh_Pl = y_Pl[0]

        # estimating species densities at time zero
        N0_Aw = densityAw(SDF_Aw0, 0, SI_bh_Aw)
        N0_Sb = densitySb(SDF_Sb0, 0, SI_bh_Sb)
        N0_Sw = densitySw(SDF_Sw0, SDF_Aw0, 0, SI_bh_Sw)
        N0_Pl = densityPl(SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, 0, SI_bh_Pl)

        # estimating sp-specific Basal area increment from Densities
        SC = SCestimate(N_bh_Aw, N_bh_Sb, N_bh_Sw, N_bh_Pl)

        SC_Aw = SC[0]
        SC_Sw = SC[1]
        SC_Sb = SC[2]
        SC_Pl = SC[3]

        BA_Aw = sp_Aw[5]
        BA_Sb = sp_Sb[5]
        BA_Sw = sp_Sw[5]
        BA_Pl = sp_Pl[5]

        BAinc_Aw = BasalAreaIncrementNonSpatialAw(sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw)
        BAinc_Sb = BasalAreaIncrementNonSpatialSb(sp_Sb, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, BA_Sb)
        BAinc_Sw = BasalAreaIncrementNonSpatialSw(sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw)
        BAinc_Pl = BasalAreaIncrementNonSpatialPl(sp_Pl, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl, bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl)

        StumpDOB_Aw = sp_Aw[7]
        StumpHeight_Aw = sp_Aw[8]
        TopDib_Aw = sp_Aw[9]

        StumpDOB_Sb = sp_Sb[7]
        StumpHeight_Sb = sp_Sb[8]
        TopDib_Sb = sp_Sb[9]

        StumpDOB_Sw = sp_Sw[7]
        StumpHeight_Sw = sp_Sw[8]
        TopDib_Sw = sp_Sw[9]

        StumpDOB_Pl = sp_Pl[7]
        StumpHeight_Pl = sp_Pl[8]
        TopDib_Pl = sp_Pl[9]

        plot_dict[PlotID] = {
            'PlotID': PlotID, 'SI_Aw': SI_Aw, 'SI_Sw': SI_Sw, 'SI_Pl': SI_Pl, 'SI_Sb': SI_Sb,
            'N_Aw': N_Aw, 'N_Sw': N_Sw, 'N_Pl': N_Pl, 'N_Sb': N_Sb,
            'y2bh_Aw': y2bh_Aw, 'y2bh_Sw': y2bh_Sw, 'y2bh_Pl': y2bh_Pl, 'y2bh_Sb': y2bh_Sb,
            'tage_Aw': tage_Aw, 'tage_Sw': tage_Sw, 'tage_Pl': tage_Pl, 'tage_Sb': tage_Sb,
            'BA_Aw': BA_Aw, 'BA_Sw': BA_Sw, 'BA_Pl': BA_Pl, 'BA_Sb': BA_Sb,
            'BAinc_Aw': BAinc_Aw, 'BAinc_Sw': BAinc_Sw, 'BAinc_Pl': BAinc_Pl, 'BAinc_Sb': BAinc_Sb,
            'SDF_Aw': SDF_Aw0, 'SDF_Sw': SDF_Sw0, 'SDF_Pl': SDF_Pl0, 'SDF_Sb': SDF_Sb0,
            'N0_Aw': N0_Aw, 'N0_Sb': N0_Sb, 'N0_Sw': N0_Sw, 'N0_Pl': N0_Pl,
            'StumpDOB_Aw': StumpDOB_Aw, 'StumpDOB_Sb': StumpDOB_Sb, 'StumpDOB_Sw': StumpDOB_Sw, 'StumpDOB_Pl': StumpDOB_Pl,
            'StumpHeight_Aw': StumpHeight_Aw, 'StumpHeight_Sb': StumpHeight_Sb, 'StumpHeight_Sw': StumpHeight_Sw, 'StumpHeight_Pl': StumpHeight_Pl,
            'TopDib_Aw': TopDib_Aw, 'TopDib_Sb': TopDib_Sb, 'TopDib_Sw': TopDib_Sw, 'TopDib_Pl': TopDib_Pl,
            'topHeight_Aw': topHeight_Aw, 'topHeight_Sw': topHeight_Sw, 'topHeight_Sb': topHeight_Sb, 'topHeight_Pl': topHeight_Pl
        }

    return plot_dict, spList
