# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:15:44 2016

@author: juliannosambatti
"""

import csv
import os
import pandas as pd
import numpy as np
from asaCompileAgeGivenSpSiHt import computeTreeAge
from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge
from asaCompileAgeGivenSpSiHt import ComputeGypsySiteIndex

from GYPSYNonSpatial import densityNonSpatialAw
from GYPSYNonSpatial import densityNonSpatialSb
from GYPSYNonSpatial import densityNonSpatialSw
from GYPSYNonSpatial import densityNonSpatialPl

from GYPSYNonSpatial import (densityAw, densitySw, densitySb, densityPl)

from GYPSYNonSpatial import BasalAreaIncrementNonSpatialAw
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialSw
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialPl
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialSb

from GYPSYNonSpatial import GrossTotalVolume

from GYPSYNonSpatial import MerchantableVolumeAw
from GYPSYNonSpatial import MerchantableVolumeSw
from GYPSYNonSpatial import MerchantableVolumePl
from GYPSYNonSpatial import MerchantableVolumeSb

from GYPSYNonSpatial import SCestimate



data = pd.read_csv('/Users/juliannosambatti/Projects/Gipsy/testData/stands2.csv')




#print data

#print data.shape  #gives number of rows and number of columns

fplot = {'Aw': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}, 
                 'Pl': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}, 
                 'Sw': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}, 
                 'Sb': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}
                 }

plotDict = {}
'''/// create data frame // '''

# input - species, top height, total age, BH age, N (or density), current Basal Area, Measured Percent Stocking, StumpDOB, StumpHeight, TopDib
def SIfromDomSp (domSp, SI):
    if SI>0:
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

'''function to define SI of all other species given the dominant species, which is the one from  data '''

def dataPrepGypsy (data):
    domSp='Aw'
    SI=1
    SIfromDomSp (domSp, SI)
        
          
    '''iterate over each row '''
    
    for i, row in data.iterrows():
    
        
        '''empty dictionary to be filled with below. Except those last three element that seem to be constants defined a priori '''
        
          # input - species, top height, total age, BH age, N (or density), current Basal Area, Measured Percent Stocking, StumpDOB, StumpHeight, TopDib, SI, Proportion of the sp
        
        fplot = {'Aw': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}, 
                 'Pl': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}, 
                 'Sw': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}, 
                 'Sb': {'topHeight': 0, 'tage': 0, 'bhage': 0, 'N': 0, 'BA': 0, 'PS': 16.9, 'StumpDOB':13, 'StumpHeight': 0.3, 'TopDib': 7, 'SI': 0, 'PCT': 0}
                 }
               
      
        PlotID = data.loc[i,'id_l1']
        
        tempDomSp = data.loc[i,'SP1']
        
        #print tempDomSp
    
        def initSI_estimation (tempDomSp) :    
            if tempDomSp == 'Pb':
                tempDomSp= 'Aw'
            elif tempDomSp == 'Fd' or tempDomSp == 'Fb':
                tempDomSp= 'Sw'
            return tempDomSp
        
        '''
        estimate SI Dom from inventory Age and HD !!!!
            Use this SI to estimate the other species SIs
            ex: FD is dom sp take HD and Age, assume FD is Sw generate SI for Sw
            
            get the SW SI
            calculate the SIs for other sp from the conversion formulas
        
        ''' 
        domTage = data.loc[i,'AGE']
        domHT = data.loc[i,'HD']
        
        
        def domSpSI_estim (tempDomSp, domTage, domHT):
            domSI = ComputeGypsySiteIndex(tempDomSp, domHT, 0, domTage)
            SI = domSI [2] 
            
            '''I am using SI = SI_t , site index based on total age from the ComputeGypsySiteIndex function '''
            
            return SI
        

        SI = domSpSI_estim(tempDomSp, domTage, domHT)
        
        #print 'kkk',tempDomSp,  SI
        '''WHY NOT USE THE DATA SIs ????? I prefer using the height and age to estimate SI usign Gypsy equations. After all, SI from inventory is already an estimate. 
        And we know that height and age have been directly measured. By using the SI from the inventory we may be propagating errors'''
        
        #SI = data.loc[i,'SI']
        
        
        DomSp = initSI_estimation (tempDomSp)
        
        SI_x = SIfromDomSp (DomSp, SI)

        #print SI_x
    
    
        '''fill the dictionary with estimated SIs - I filled all the SIs to avoid IFs and loops. Some of them will not be used. '''
        
        
        
        def otherSpSIs (SI, tempDomSp):
            if DomSp == 'Aw':
                fplot ['Aw']['SI'] = SI
                fplot ['Pl']['SI'] = SI_x[1]
                fplot ['Sw']['SI'] = SI_x[2]
                fplot ['Sb']['SI'] = SI_x[3]
            
            elif DomSp == 'Sw':
                fplot ['Aw']['SI'] = SI_x[0]
                fplot ['Pl']['SI'] = SI_x[1]
                fplot ['Sw']['SI'] = SI
                fplot ['Sb']['SI'] = SI_x[3]
                
            elif DomSp == 'Pl':
                fplot ['Aw']['SI'] = SI_x[0]
                fplot ['Pl']['SI'] = SI
                fplot ['Sw']['SI'] = SI_x[2]
                fplot ['Sb']['SI'] = SI_x[3]
                
            elif DomSp == 'Sb':
                fplot ['Aw']['SI'] = SI_x[0]
                fplot ['Pl']['SI'] = SI_x[1]
                fplot ['Sw']['SI'] = SI_x[2]
                fplot ['Sb']['SI'] = SI
            
            return fplot
        
        fplot = otherSpSIs (SI, DomSp)
        
        #print SI, DomSp , fplot ['Sw']['SI']
        #print '----\n'
       
                
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
                fplot [sp[0]]['tage'] = domTage
                fplot [sp[0]]['topHeight'] = domHT
                fplot [sp[0]] ['N'] = data.loc[i,'TPH'] * sp[1]/100
                fplot [sp[0]] ['BA'] = data.loc[i,'BPH'] * sp[1]/100
                x_Si = ComputeGypsySiteIndex(sp[0], fplot [sp[0]]['topHeight'], 0, fplot [sp[0]]['tage'])                           
                fplot [sp[0]] ['bhage'] = x_Si [0]
            #if, after re-arranging the proportions, dom species is another one, then we need to re-estimate everything  even for the new dom species
            
            #wrong below !!!! Which tree height to start with shall I use???    
            
            else:
                        
                siSp = fplot [sp[0]] ['SI']
                          
                fplot [sp[0]]['PCT']  = sp[1]
               
                '''estimate tree age iteratively calling computeTreeAge function  and inputing SI in the place ot treeSi and domHT as treeHT or topheight'''            
                
                fplot [sp[0]]['tage'] = computeTreeAge (sp[0] ,treeHt = domHT, treeSi=siSp, maxTreeAge = 450, rowIndex = 0, printWarnings = True)
                
                '''estimate topHeight from the same function above - redundant, but clearer for me - I think this is not necessary'''
                           
                #fplot [sp[0]]['topHeight'] = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge (sp[0], siSp, fplot [sp[0]]['tage'])
                
                '''density based on the proportion of the species'''
                                      
                fplot [sp[0]] ['N'] = data.loc[i,'TPH'] * sp[1]/100
                
                '''Basal area from the species proportion as well '''
                             
                fplot [sp[0]] ['BA'] = data.loc[i,'BPH'] * sp[1]/100
                
                '''calling the ComputeGypsySiteIndex function, estimate bhage '''
                
                x_Si = ComputeGypsySiteIndex(sp[0], domHT, 0, fplot [sp[0]]['tage'])
                                     
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
        
        plotDict [PlotID]= { 'PlotID': PlotID, 'SI_Aw': SI_Aw, 'SI_Sw': SI_Sw, 'SI_Pl': SI_Pl, 'SI_Sb': SI_Sb, 
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
        plotDF = pd.DataFrame(plotDict, index = [PlotID])
        plotDF.to_csv("/Users/juliannosambatti/Projects/Gipsy/testData/testOutput.csv", mode=mode, header = writeheader)
        
        '''
        # make sure that column names aren't written each time


# plotDF = pd.DataFrame(plotDict)
# plotDF.to_csv("/Users/juliannosambatti/Projects/Gipsy/testData/testOutput.csv")


    
       
      
    return plotDict, spList
    
    
print dataPrepGypsy (data)

    
