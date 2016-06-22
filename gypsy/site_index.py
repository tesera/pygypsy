# -*- coding: utf-8 -*-
"""Functions for calculating site indices

"""
from collections import defaultdict


# TODO: reduce repetition
# - decorator for returns_all_site_indices
# - utility functions/class for <species>_from_<otherspecies>
# - make species stuff case insensitive


def get_site_indices_from_dominant_species(dominant_species=None,
                                           dominant_species_site_index=None):
    """Calculate site indices for non-dominant species

    Keyword Arguments:
    dominant_species            -- (default None)
    dominant_species_site_index -- (default None)

    """

    functs = {
        'aw': _get_all_site_indices_from_dominant_aw,
        'sw': _get_all_site_indices_from_dominant_sw,
        'fb': _get_all_site_indices_from_dominant_fb,
        'fd': _get_all_site_indices_from_dominant_fd,
        'pl': _get_all_site_indices_from_dominant_pl,
        'pb': _get_all_site_indices_from_dominant_pb,
    }

    try:
        all_site_indices = functs[dominant_species](dominant_species_site_index)
    except KeyError:
        raise ValueError('No function is available to calculate site index from '
                         'species %s' %dominant_species)

    species_subset = ('aw', 'pl', 'sw', 'sb')
    site_indices_subset = {
        species: all_site_indices[species] for species in species_subset
    }

    # NOTE: using a dict here so that contents are explicit/non-ambiguous
    return site_indices_subset


def _get_all_site_indices_from_dominant_aw(site_index_aw):
    """Keyword Arguments:
    site_index_aw -- site index for aw

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_pl = 0.85 * site_index_aw + 3.4
    site_index_sw = 1.31 * site_index_aw - 2.64
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_fd = 0.94 * site_index_pl + 0.71
    site_index_sb = 0.64 * site_index_pl + 2.76
    site_index_pb = site_index_aw

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_all_site_indices_from_dominant_sw(site_index_sw):
    """Keyword Arguments:
    site_index_sw -- site index for sw

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_pl = 0.86 * site_index_sw + 2.13
    site_index_aw = 0.76 * site_index_sw + 2.01
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_fd = 0.74 * site_index_sw + 4.75
    site_index_sb = 0.64 * site_index_pl + 2.76
    site_index_pb = site_index_aw

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict

def _get_all_site_indices_from_dominant_fb(site_index_fb):
    """Keyword Arguments:
    site_index_fb -- site index for fb

    Returns: dict: species as keys and site indices as corresponding values

    """
    site_index_sw = 1.09 * site_index_fb - 1.83
    site_index_pl = 0.86 * site_index_sw + 2.13
    site_index_aw = 0.76 * site_index_sw + 2.01
    site_index_fd = 0.74 * site_index_sw + 4.75
    site_index_sb = 0.64 * site_index_pl + 2.76
    site_index_pb = site_index_aw

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_all_site_indices_from_dominant_fd(site_index_fd):
    """Keyword Arguments:
    site_index_fd -- site index for fd

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_pl = 1.07 * site_index_fd - 0.76
    site_index_aw = 1.18 * site_index_pl  - 4.02
    site_index_sw = 1.36 * site_index_fd  - 6.45
    site_index_pb = site_index_aw
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_sb = 0.64 * site_index_pl + 2.76

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_all_site_indices_from_dominant_pl(site_index_pl):
    """Keyword Arguments:
    site_index_pl -- site index for pl

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_aw = 1.18 * site_index_pl  - 4.02
    site_index_sw = 1.16 * site_index_pl  - 2.47
    site_index_fd = 0.94* site_index_pl + 0.71
    site_index_pb = site_index_aw
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_sb = 0.64 * site_index_pl + 2.76


    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict

def _get_all_site_indices_from_dominant_pb(site_index_pb):
    """Keyword Arguments:
    site_index_pb -- site index for pb

    Returns:
    dict: species as keys and site indices as corresponding values

    """
    site_index_aw = site_index_pb
    site_index_pl = 0.85 * site_index_aw + 3.4
    site_index_sw = 1.31 * site_index_aw - 2.64
    site_index_fd = 0.92 * site_index_pl + 1.68
    site_index_fb = 0.92 * site_index_sw + 1.68
    site_index_sb = 0.64 * site_index_pl + 2.76

    site_indices_dict = {'aw': site_index_aw,
                         'pl': site_index_pl,
                         'sw': site_index_sw,
                         'fb': site_index_fb,
                         'fd': site_index_fd,
                         'sb': site_index_sb,
                         'pb': site_index_pb}

    return site_indices_dict


def _get_temporary_dominant_species(actual_dominant_species):
    """Swap an actual dominant species for a temporary one
    Keyword Arguments:
    actual_dominant_species -- str

    Returns:
    str: a temporary dominant species

    """
    if actual_dominant_species == 'Pb':
        temp_dominant_species= 'Aw'
    elif actual_dominant_species == 'Fd' or actual_dominant_species == 'Fb':
        temp_dominant_species= 'Sw'
    else:
        raise ValueError('There is no temporary dominant species for species %s' \
                         % actual_dominant_species)

    return temp_dominant_species


def _estimate_dominant_species_site_index(dominant_species, age, height):
    """Estimate site index of dominant species

    This is a wrapper around ComputeGypsySiteIndex for readability

    It assumes site_index = site_index at time?

    Keyword Arguments:
    dominant_species -- str, abbreviation of dominant species
    age              -- float, age of dominant species
    height           -- float, height of dominant species

    Return:
    float - site index

    """
    dominant_site_index_list = ComputeGypsySiteIndex(temp_dominant_species,
                                                     domHT, 0, domTage)
    # TODO: use dictionary for return from Computegypsysiteindex - that way someone
    # knows clearly what domSI[2] means
    dominant_site_index = dominant_site_index_list[2]

    return dominant_site_index




def _generate_fplot_dict(dominant_species, dominant_species_site_index,
                         all_species_site_indices):
    """Generate 'fplot'

    Given a known dominant species and its site index, and estimation of all
    site indices, generates the 'fplot' dictionary

    Keyword Arguments:
    dominant_species            -- str, dominant species abbrev
    dominant_species_site_index -- float, dominant species site index
    all_species_site_indices    -- dict, site index of all species

    Return:
    dict - ???

    """
    def gen_template_dict():
        return {
            'topHeight': 0, 'tage': 0, 'bhage': 0,
            'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13,
            'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0
        }

    fplot_dict = defaultdict(gen_template_dict)

    fplot_dict['Aw']['SI'] = all_species_site_indices['pl']
    fplot_dict['Pl']['SI'] = all_species_site_indices['pl']
    fplot_dict['Sw']['SI'] = all_species_site_indices['sw']
    fplot_dict['Sb']['SI'] = all_species_site_indices['sb']
    # override the given dominant species with the given value
    fplot_dict[dominant_species]['SI'] = dominant_species_site_index

    return fplot_dict


def dataPrepGypsy(microstand_df):
    data = microstand_df

    # TODO: are these used?
    dominant_species='Aw'
    site_index=1
    # TODO: not assigned?!!
    get_site_index_from_dominant_species(dominant_species, site_index)

    for i, row in data.iterrows():

        # input - species, top height, total age, BH age, N (or density),
        # current Basal Area, Measured Percent Stocking, StumpDOB,
        # StumpHeight, TopDib, SI, Proportion of the sp

        # TODO: defaultdict?

        plot_id = data.loc[i,'id_l1']
        temp_dominant_species = data.loc[i,'SP1']
        dominant_species_age = data.loc[i,'AGE']
        dominant_species_height = data.loc[i,'HD']

        # Use this SI to estimate the other species SIs
        # ex: FD is dom sp take HD and Age, assume FD is Sw generate SI for Sw
        # get the SW SI calculate the SIs for other sp from the conversion formulas
        # ...
        # get site index for dominant species in microstand
        SI = _estimate_dominant_species_site_index(temp_dominant_species,
                                                   dominant_species_age,
                                                   dominant_species_height)
        dominant_species_site_index = SI

        # WHY NOT USE THE DATA SIs?
        # I prefer using the height and age to estimate SI usign Gypsy equations.
        # After all, SI from inventory is already an estimate.
        # And we know that height and age have been directly measured.
        # By using the SI from the inventory we may be propagating errors
        # e.g. SI = data.loc[i,'SI']
        # ...
        # get a dominant species compatible with all_species_site_index
        dominant_species = _get_temporary_dominant_species(temp_dominant_species)
        all_species_site_indices = get_site_indices_from_dominant_species(
            dominant_species,
            dominant_species_site_index
        )


        # TODO: need a more descriptive name than fplot - what does it mean?
        fplot = _generate_fplot_dict(dominant_species, dominant_species_site_index,
                                     all_species_site_indices)


        sp1 = data.loc[i,'SP1']
        sp2 = data.loc[i,'SP2']
        sp3 = data.loc[i,'SP3']
        sp4 = data.loc[i,'SP4']
        sp5 = data.loc[i,'SP5']

        pct1 = data.loc[i,'PCT1']
        pct2 = data.loc[i,'PCT2']
        pct3 = data.loc[i,'PCT3']
        pct4 = data.loc[i,'PCT4']
        pct5 = data.loc[i,'PCT5']



        spList = [(sp1, pct1), (sp2, pct2) , (sp3, pct3) , (sp4, pct4), (sp5, pct5)] 

        check_prop = sum(zip(*spList)[1])
        if check_prop !=100:
            raise ValueError ('Species proportions not correct: %s' %check_prop)


        def sortedSp (spList, spList1 =  { 'Aw':0, 'Pl':0, 'Sw':0, 'Sb':0}):

            for sp in spList:
                if sp[0]=='Aw' or sp[0]=='Pb' :
                    spList1 ['Aw'] = spList1 ['Aw'] + sp[1]

                elif sp[0]=='Sw' or sp[0]=='Fb' or sp[0]=='Fd':
                    spList1 ['Sw'] = spList1 ['Sw'] + sp[1]

                elif sp[0]=='Pl':
                    spList1 ['Pl'] = spList1 ['Pl'] + sp[1]

                elif sp[0]=='Sb':
                    spList1 ['Sb'] = spList1 ['Sb'] + sp[1]

            sorted_spList1 = [(k,v) for v,k in sorted( [(v,k) for k,v in spList1.items()] ) ]

            sorted_spList1.reverse() 

            check_prop1 = sum(spList1.values())
            if check_prop1 !=100:
                raise ValueError ('Species proportions after grouping into 4 species is not correct: %s' %check_prop1)

            return sorted_spList1, spList1

        sorted_spList1, spList1 = sortedSp (spList)

        print sorted_spList1

        fplot ['Aw']['PCT'] = spList1['Aw']
        fplot ['Pl']['PCT'] = spList1['Pl']
        fplot ['Sw']['PCT'] = spList1['Sw']
        fplot ['Sb']['PCT'] = spList1['Sb']


        #print spList1['Sw']

        domSp = sorted_spList1[0]

        #print domSp

        #print sorted_spList1


        '''iterate over each ranked species - populate the dictionary with values estimated from the dominant species' SI '''

        for sp in sorted_spList1:

            if sp[1]==0:
                break
            elif sp[0] == domSp[0]:
                fplot [sp[0]]['tage'] = dominant_species_age
                fplot [sp[0]]['topHeight'] = dominant_species_height
                fplot [sp[0]] ['N'] = data.loc[i,'TPH'] * sp[1]/100
                fplot [sp[0]] ['BA'] = data.loc[i,'BPH'] * sp[1]/100
                x_Si = ComputeGypsySiteIndex(sp[0], fplot [sp[0]]['topHeight'], 0, fplot [sp[0]]['tage'])
                fplot [sp[0]] ['bhage'] = x_Si [0]
            #if, after re-arranging the proportions, dom species is another one, then we need to re-estimate everything  even for the new dom species

            #wrong below !!!! Which tree height to start with shall I use???

            else:

                siSp = fplot [sp[0]] ['SI']

                fplot [sp[0]]['PCT']  = sp[1]

                '''estimate tree age iteratively calling computeTreeAge function  and inputing SI in the place ot treeSi and dominant_species_height as treeHT or topheight'''

                fplot [sp[0]]['tage'] = computeTreeAge (sp[0] ,treeHt = dominant_species_height, treeSi=siSp, maxTreeAge = 450, rowIndex = 0, printWarnings = True)

                '''estimate topHeight from the same function above - redundant, but clearer for me - I think this is not necessary'''

                #fplot [sp[0]]['topHeight'] = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge (sp[0], siSp, fplot [sp[0]]['tage'])

                '''density based on the proportion of the species'''

                fplot [sp[0]] ['N'] = data.loc[i,'TPH'] * sp[1]/100

                '''Basal area from the species proportion as well '''

                fplot [sp[0]] ['BA'] = data.loc[i,'BPH'] * sp[1]/100

                '''calling the ComputeGypsySiteIndex function, estimate bhage '''

                x_Si = ComputeGypsySiteIndex(sp[0], dominant_species_height, 0, fplot [sp[0]]['tage'])

                fplot [sp[0]] ['bhage'] = x_Si [0]

        #print fplot


       # print '-------------------------------'
        #print 'Plot ID    ', Plot_Id
        #print '-------------------------------'
        '''
    now we have different lists containing:
    species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion

        '''
        SI_Aw = fplot ['Aw']['SI'] 
        SI_Sw = fplot ['Sw']['SI'] 
        SI_Pl = fplot ['Pl']['SI'] 
        SI_Sb = fplot ['Sb']['SI'] 

        N_Aw = fplot ['Aw']['N'] 
        N_Sw = fplot ['Sw']['N'] 
        N_Pl = fplot ['Pl']['N'] 
        N_Sb = fplot ['Sb']['N'] 

        #print 'NNN', N_Aw, N_Sw, N_Sb, N_Pl
        '''sometimes these values are zero because TPH is zero...WHY TPH IS ZERO????'''

        y2bh_Aw = fplot ['Aw']['tage'] - fplot ['Aw']['bhage'] 
        y2bh_Sw = fplot ['Sw']['tage'] - fplot ['Sw']['bhage']
        y2bh_Pl = fplot ['Pl']['tage'] - fplot ['Pl']['bhage']
        y2bh_Sb = fplot ['Sb']['tage'] - fplot ['Sb']['bhage']

        tage_Aw = fplot ['Aw']['tage'] 
        tage_Sw = fplot ['Sw']['tage']
        tage_Pl = fplot ['Pl']['tage']
        tage_Sb = fplot ['Sb']['tage'] 

        #print tage_Sw


        sp_Aw=['Aw', fplot ['Aw'] ['topHeight'], fplot ['Aw'] ['tage'], fplot ['Aw'] ['bhage'], fplot ['Aw'] ['N'], fplot ['Aw'] ['BA'], fplot ['Aw'] ['PS'], fplot ['Aw'] ['StumpDOB'], fplot ['Aw'] ['StumpHeight'], fplot ['Aw'] ['TopDib'], fplot ['Aw'] ['SI'], fplot ['Aw'] ['PCT']]
        sp_Pl=['Pl', fplot ['Pl'] ['topHeight'], fplot ['Pl'] ['tage'], fplot ['Pl'] ['bhage'], fplot ['Pl'] ['N'], fplot ['Pl'] ['BA'], fplot ['Pl'] ['PS'], fplot ['Pl'] ['StumpDOB'], fplot ['Pl'] ['StumpHeight'], fplot ['Pl'] ['TopDib'], fplot ['Pl'] ['SI'], fplot ['Pl'] ['PCT']]
        sp_Sw=['Sw', fplot ['Sw'] ['topHeight'], fplot ['Sw'] ['tage'], fplot ['Sw'] ['bhage'], fplot ['Sw'] ['N'], fplot ['Sw'] ['BA'], fplot ['Sw'] ['PS'], fplot ['Sw'] ['StumpDOB'], fplot ['Sw'] ['StumpHeight'], fplot ['Sw'] ['TopDib'], fplot ['Sw'] ['SI'], fplot ['Sw'] ['PCT']]
        sp_Sb=['Sb', fplot ['Sb'] ['topHeight'], fplot ['Sb'] ['tage'], fplot ['Sb'] ['bhage'], fplot ['Sb'] ['N'], fplot ['Sb'] ['BA'], fplot ['Sb'] ['PS'], fplot ['Sb'] ['StumpDOB'], fplot ['Sb'] ['StumpHeight'], fplot ['Sb'] ['TopDib'], fplot ['Sb'] ['SI'], fplot ['Sb'] ['PCT']]
        bhage_Aw=sp_Aw[3]
        tage_Aw=sp_Aw[2]
        si_Aw=sp_Aw[10]
        y2bh_Aw= tage_Aw - bhage_Aw
        SI_bh_Aw=sp_Aw[10]

        '''treeHeight is the Top Height or Htop in the paper'''
        topHeight_Aw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Aw[0],  si_Aw,  tage_Aw)

        '''

        print ' estimated Site Index for species Aw is:  ', si_Aw
        print ' estimated Total age for species Aw is:  ', tage_Aw
        print ' estimated BH age for species Aw is:  ', bhage_Aw
        print ' estimated Site Index BH for species Aw is:  ',SI_bh_Aw
        print ' estimated number of years until measuring BH becomes possible:  ',  y2bh_Aw
        print '----------------------'

        '''

        #x_Sb=ComputeGypsySiteIndex(sp_Sb[0],  sp_Sb[1],  sp_Sb[2], sp_Sb[3])

        bhage_Sb=sp_Sb[3]
        tage_Sb=sp_Sb[2]
        si_Sb =sp_Sb[10]
        SI_bh_Sb=sp_Sb[10]

        '''treeHeight is the Top Height or Htop in the paper'''
        topHeight_Sb=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Sb[0],  si_Sb,  tage_Sb)

        '''
        print ' estimated Site Index for species Sb is:  ', si_Sb
        print ' estimated Total age for species Sb is:  ', tage_Sb
        print ' estimated BH age for species Sb is:  ', bhage_Sb
        print ' estimated Site Index BH for species Sb is:  ',SI_bh_Sb
        print ' estimated number of years until measuring BH becomes possible:  ', y2bh_Sb
        print '----------------------'
        '''
        #x_Pl=ComputeGypsySiteIndex(sp_Pl[0],  sp_Pl[1],  sp_Pl[2], sp_Pl[3])

        bhage_Pl=sp_Pl[3]
        tage_Pl=sp_Pl[2]
        si_Pl =sp_Pl[10]
        y2bh_Pl = tage_Pl - bhage_Pl
        SI_bh_Pl=sp_Pl[10]

        '''treeHeight is the Top Height or Htop in the paper'''
        topHeight_Pl=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Pl[0],  si_Pl,  tage_Pl)
        '''
        print ' estimated Site Index for species Pl is:  ', si_Pl
        print ' estimated Top Height for species Pl is:  ', topHeight_Pl
        print ' estimated Total age for species Pl is:  ', tage_Pl
        print ' estimated BH age for species Pl is:  ', bhage_Pl
        print ' estimated Site Index BH for species Pl is:  ', SI_bh_Pl
        print ' estimated number of years until measuring BH becomes possible:  ', y2bh_Pl
        print '----------------------'
        '''
        #x_Sw=ComputeGypsySiteIndex(sp_Sw[0],  sp_Sw[1],  sp_Sw[2], sp_Sw[3])

        bhage_Sw=sp_Sw[3]
        tage_Sw=sp_Sw[2]
        si_Sw =sp_Sw[10]
        y2bh_Sw = tage_Sw - bhage_Sw
        SI_bh_Sw=sp_Sw[10]



        '''treeHeight is the Top Height or Htop in the paper'''
        topHeight_Sw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(sp_Sw[0],  si_Sw,  tage_Sw)


        '''
        print ' estimated Site Index for species Sw is:  ', si_Sw
        print ' estimated Top Height for species Sw is:  ', topHeight_Sw
        print ' estimated Total age for species Sw is:  ', tage_Sw
        print ' estimated BH age for species Sw is:  ', bhage_Sw
        print ' estimated Site Index BH for species Sw is:  ', SI_bh_Sw
        print ' estimated number of years until measuring BH becomes possible:  ', y2bh_Sw
        print '----------------------'
        '''
        '''
        si, bhage, and tage are passed on from the above. SDFs estimated iteratively
        '''

        '''I am using N from the original input sp_Aw etc as the input (N_Aw) etc
        I think it is suposed to be the density of the species at the bhage = 0, although
        the paper says current or inital density

        '''
        #print 'kkkk', tage_Aw, tage_Sw, tage_Sb, tage_Pl
        #print 'bhage', bhage_Aw, bhage_Sw, bhage_Sb, bhage_Pl

        '''estimating species densities from, SI and data '''

        N_Aw = sp_Aw[4]
        N_Sb = sp_Sb[4]
        N_Sw = sp_Sw[4]
        N_Pl = sp_Pl[4]



        y_Aw=densityNonSpatialAw (sp_Aw, SI_bh_Aw, bhage_Aw, N_Aw, printWarnings = True)
        SDF_Aw0 = y_Aw[1]
        N_bh_Aw=y_Aw[0]


        y_Sb=densityNonSpatialSb(sp_Sb, SI_bh_Sb, tage_Sb, N_Sb)
        SDF_Sb0 = y_Sb[1]
        N_bh_Sb=y_Sb[0]

        y_Sw= densityNonSpatialSw (sp_Sw, SI_bh_Sw, tage_Sw, SDF_Aw0, N_Sw)
        SDF_Sw0 = y_Sw[1]
        N_bh_Sw=y_Sw[0]

        y_Pl =densityNonSpatialPl (sp_Pl, SI_bh_Pl, tage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, N_Pl)
        SDF_Pl0 = y_Pl[1]
        N_bh_Pl = y_Pl[0]

        #print 'N_Sw' , N_Sw, bhage_Sw, SI_bh_Sw, N_bh_Sw, SDF_Sw0

        '''estimating species densities at time zero '''

        N0_Aw = densityAw (SDF_Aw0, 0, SI_bh_Aw)
        N0_Sb = densitySb (SDF_Sb0, 0, SI_bh_Sb)
        N0_Sw = densitySw (SDF_Sw0, SDF_Aw0, 0, SI_bh_Sw)
        N0_Pl = densityPl (SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, 0, SI_bh_Pl)



        '''estimating sp-specific Basal area increment from Densities '''

        SC = SCestimate (N_bh_Aw,  N_bh_Sb, N_bh_Sw, N_bh_Pl)

        #print N_bh_Aw,  N_bh_Sb, N_bh_Sw, N_bh_Pl


        SC_Aw = SC[0]
        SC_Sw = SC[1]
        SC_Sb = SC[2]
        SC_Pl = SC[3]


        BA_Aw=sp_Aw[5]
        BA_Sb=sp_Sb[5]
        BA_Sw=sp_Sw[5]
        BA_Pl=sp_Pl[5]


        BAinc_Aw = BasalAreaIncrementNonSpatialAw (sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_Aw)

        BAinc_Sb = BasalAreaIncrementNonSpatialSb (sp_Sb, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, BA_Sb)

        BAinc_Sw = BasalAreaIncrementNonSpatialSw (sp_Sw, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw)

        BAinc_Pl = BasalAreaIncrementNonSpatialPl (sp_Pl, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl, bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl) 



        #print 'kkkk', BA_Aw,  BAinc_Aw, SC_Aw, N0_Aw, N_bh_Aw

        StumpDOB_Aw=sp_Aw[7]
        StumpHeight_Aw =sp_Aw[8]
        TopDib_Aw = sp_Aw[9]

        StumpDOB_Sb=sp_Sb[7]
        StumpHeight_Sb =sp_Sb[8]
        TopDib_Sb = sp_Sb[9]

        StumpDOB_Sw=sp_Sw[7]
        StumpHeight_Sw =sp_Sw[8]
        TopDib_Sw = sp_Sw[9]

        StumpDOB_Pl=sp_Pl[7]
        StumpHeight_Pl =sp_Pl[8]
        TopDib_Pl = sp_Pl[9]



        '''estimating sp-specific gross total volume 

        Tvol = GrossTotalVolume( BA_Aw, BA_Sb, BA_Sw, BA_Pl, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl)

        Tvol_Aw = Tvol[0]
        Tvol_Sb = Tvol[1]
        Tvol_Sw = Tvol[2]
        Tvol_Pl = Tvol[3]



        estimating merchantable volume

        MVol_Aw = MerchantableVolumeAw(N_bh_Aw, BA_Aw, topHeight_Aw, StumpDOB_Aw, StumpHeight_Aw , TopDib_Aw, Tvol_Aw)

        MVol_Sb = MerchantableVolumeSb(N_bh_Sb, BA_Sb, topHeight_Sb, StumpDOB_Sb, StumpHeight_Sb , TopDib_Sb, Tvol_Sb)

        MVol_Sw = MerchantableVolumeSw(N_bh_Sw, BA_Sw, topHeight_Sw, StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, Tvol_Sw)

        MVol_Pl = MerchantableVolumePl(N_bh_Pl, BA_Pl, topHeight_Pl, StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, Tvol_Pl)



        '''

        plotDict [plot_id]= { 'plot_id': plot_id, 'SI_Aw': SI_Aw, 'SI_Sw': SI_Sw, 'SI_Pl': SI_Pl, 'SI_Sb': SI_Sb, 
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
        print plotDict

        # with open ("/Users/juliannosambatti/Projects/Gipsy/testData/testOutput.csv", 'a') as f:
        #     f_csv = csv.DictWriter(f, csv_columns)
        #     f_csv.writeheader()
        #     f_csv.writerows(plotDict)
        '''
        writeheader = True if i==0 else False
        mode = 'a' if i > 0 else 'w'
        plotDF = pd.DataFrame(plotDict, index = [plot_id])
        plotDF.to_csv("/Users/juliannosambatti/Projects/Gipsy/testData/testOutput.csv", mode=mode, header = writeheader)

        '''
        # make sure that column names aren't written each time


# plotDF = pd.DataFrame(plotDict)
# plotDF.to_csv("/Users/juliannosambatti/Projects/Gipsy/testData/testOutput.csv")



    return plotDict, spList
