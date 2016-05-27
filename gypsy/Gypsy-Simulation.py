# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:06:29 2016

@author: juliannosambatti
"""

import csv
import pandas as pd
import numpy 
import matplotlib.pyplot as plt

from asaCompileAgeGivenSpSiHt import computeTreeAge
from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge
from asaCompileAgeGivenSpSiHt import ComputeGypsySiteIndex

from GypsyDataPrep import dataPrepGypsy
from GYPSYNonSpatial import densityNonSpatialAw
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialAw

from GYPSYNonSpatial import densityNonSpatialSw
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialSw

from GYPSYNonSpatial import densityNonSpatialSb
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialSb

from GYPSYNonSpatial import densityNonSpatialPl
from GYPSYNonSpatial import BasalAreaIncrementNonSpatialPl

from GYPSYNonSpatial import (densityAw, densitySw, densitySb, densityPl)

from GYPSYNonSpatial import SCestimate

from GYPSYNonSpatial import GrossTotalVolume

from GYPSYNonSpatial import BAincIter_Aw
from GYPSYNonSpatial import BAincIter_Sw
from GYPSYNonSpatial import BAincIter_Sb
from GYPSYNonSpatial import BAincIter_Pl

from GYPSYNonSpatial import MerchantableVolumeAw
from GYPSYNonSpatial import MerchantableVolumeSw
from GYPSYNonSpatial import MerchantableVolumeSb
from GYPSYNonSpatial import MerchantableVolumePl

# input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion


data1 = pd.read_csv('/Users/juliannosambatti/Projects/Gipsy/Inputs/LCR_join10b_x_julianno_2row.csv')


fplotSim = dataPrepGypsy(data1)
#print fplotSim


inputDF = pd.DataFrame (fplotSim)



inputDF=inputDF.transpose()

#print inputDF





for plotID, row in inputDF.iterrows():
          
    
    SI_bh_Aw = inputDF.loc[plotID,'SI_Aw']
    SI_bh_Sw = inputDF.loc[plotID,'SI_Sw']
    SI_bh_Pl = inputDF.loc[plotID,'SI_Pl']
    SI_bh_Sb = inputDF.loc[plotID,'SI_Sb']
    
    N_bh_AwT  = inputDF.loc[plotID,'N_Aw']
    N_bh_SwT  = inputDF.loc[plotID,'N_Sw']
    N_bh_PlT  = inputDF.loc[plotID,'N_Pl']
    N_bh_SbT  = inputDF.loc[plotID,'N_Sb']
    
    #print N_bh_AwT, N_bh_SwT, N_bh_PlT, N_bh_SbT
    
    SCT = SCestimate (N_bh_AwT,  N_bh_SbT, N_bh_SwT, N_bh_PlT)

    SC_AwT = SCT[0]
    SC_SwT = SCT[1]
    SC_SbT = SCT[2]
    SC_PlT = SCT[3]
    
   
    
    
    y2bh_Aw = inputDF.loc[plotID,'y2bh_Aw']
    y2bh_Sw = inputDF.loc[plotID,'y2bh_Sw']
    y2bh_Sb = inputDF.loc[plotID,'y2bh_Sb']
    y2bh_Pl = inputDF.loc[plotID,'y2bh_Pl']
    
    tage_AwT  = inputDF.loc[plotID,'tage_Aw']
    tage_SwT  = inputDF.loc[plotID,'tage_Sw']
    tage_PlT  = inputDF.loc[plotID,'tage_Pl']
    tage_SbT  = inputDF.loc[plotID,'tage_Sb']
    
    bhage_AwT = tage_AwT  - y2bh_Aw
    bhage_SwT = tage_SwT  - y2bh_Sw
    bhage_PlT = tage_PlT  - y2bh_Pl
    bhage_SbT = tage_SbT  - y2bh_Sb
    
       
    BA_AwT  = inputDF.loc[plotID,'BA_Aw']
    BA_SwT  = inputDF.loc[plotID,'BA_Sw']
    BA_PlT  = inputDF.loc[plotID,'BA_Pl']
    BA_SbT  = inputDF.loc[plotID,'BA_Sb']
    
    BA_AwB = BA_AwT  
    BA_SwB = BA_SwT 
    BA_PlB = BA_PlT  
    BA_SbB = BA_SbT  
    
    
    BAinc_AwT  = inputDF.loc[plotID,'BAinc_Aw']
    BAinc_SwT  = inputDF.loc[plotID,'BAinc_Sw']
    BAinc_PlT  = inputDF.loc[plotID,'BAinc_Pl']
    BAinc_SbT  = inputDF.loc[plotID,'BAinc_Sb']
    
    BAinc_AwB = BAinc_AwT  
    BAinc_SwB = BAinc_SwT 
    BAinc_PlB = BAinc_PlT  
    BAinc_SbB = BAinc_SbT  
    
    SDF_Aw0  = inputDF.loc[plotID,'SDF_Aw']
    SDF_Sw0  = inputDF.loc[plotID,'SDF_Sw']
    SDF_Pl0  = inputDF.loc[plotID,'SDF_Pl']
    SDF_Sb0  = inputDF.loc[plotID,'SDF_Sb']
    
     
    N0_Aw  = inputDF.loc[plotID,'N0_Aw']
    N0_Sw  = inputDF.loc[plotID,'N0_Sw']
    N0_Pl  = inputDF.loc[plotID,'N0_Pl']
    N0_Sb  = inputDF.loc[plotID,'N0_Sb']
    
    StumpDOB_Aw = inputDF.loc[plotID,'StumpDOB_Aw']
    StumpHeight_Aw = inputDF.loc[plotID,'StumpHeight_Aw']
    TopDib_Aw = inputDF.loc[plotID,'TopDib_Aw']
    
    StumpDOB_Sb = inputDF.loc[plotID,'StumpDOB_Sb']
    StumpHeight_Sb = inputDF.loc[plotID,'StumpHeight_Sb']
    TopDib_Sb = inputDF.loc[plotID,'TopDib_Sb']
    
    StumpDOB_Sw = inputDF.loc[plotID,'StumpDOB_Sw']
    StumpHeight_Sw = inputDF.loc[plotID,'StumpHeight_Sw']
    TopDib_Sw = inputDF.loc[plotID,'TopDib_Sw']
    
    StumpDOB_Pl = inputDF.loc[plotID,'StumpDOB_Pl']
    StumpHeight_Pl  = inputDF.loc[plotID,'StumpHeight_Pl']
    TopDib_Pl = inputDF.loc[plotID,'TopDib_Pl']
    
    #print N0_Aw, N0_Sw, N0_Pl, N0_Sb
    
    tageData = [ tage_AwT, tage_SwT, tage_PlT, tage_SbT ]
    startTageAw = tageData[0]-1
    startTageSw = tageData[1]-1
    startTagePl = tageData[2]-1
    startTageSb = tageData[3]-1
    
    startTageAwF = tageData[0]
    startTageSwF = tageData[1]
    startTagePlF = tageData[2]
    startTageSbF = tageData[3]
    
    tageData = sorted (tageData, reverse=True)

    startTage = tageData[0]-1
    
    startTage_forward = tageData[0] + 1
    
    #print 'ages',  tageData[0], startTage, startTage_forward
  
 # input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion
    
    '''simulating growth backwards in time starting from the time at which data was taken minus 1 '''
    
    while startTage>0:
        
        '''Ages at time T-1''' 
        
        bhage_Aw = startTageAw  - y2bh_Aw
        bhage_Sw = startTageSw  - y2bh_Sw
        bhage_Pl = startTagePl  - y2bh_Pl
        bhage_Sb = startTageSb  - y2bh_Sb
        
        tage_Aw = startTageAw
        tage_Sw = startTageSw  
        tage_Pl = startTagePl  
        tage_Sb = startTageSb  

        #print tage_Pl  
        
        '''densities at time t-1 '''
        
        if bhage_Aw <0:
            N_bh_Aw = 0
        else:
            N_bh_Aw = densityAw (SDF_Aw0, bhage_Aw, SI_bh_Aw)
         
        if tage_Sb <0:
            N_bh_Sb = 0
        else:
            N_bh_Sb = densitySb (SDF_Sb0, tage_Sb, SI_bh_Sb)
            
        if tage_Sw < 0:
            N_bh_Sw = 0
        else:
            N_bh_Sw = densitySw (SDF_Sw0, SDF_Aw0, tage_Sw, SI_bh_Sw)
        
        if tage_Pl < 0:
            N_bh_Pl = 0
        else:
            N_bh_Pl = densityPl (SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_Pl , SI_bh_Pl)
 
        
        #print startTage, N_bh_Aw,  N_bh_Sb, N_bh_Sw, N_bh_Pl
        
        
        ''' species composition at time t-1 '''
            
        SC = SCestimate (N_bh_Aw,  N_bh_Sb, N_bh_Sw, N_bh_Pl)

        SC_Aw = SC[0]
        SC_Sw = SC[1]
        SC_Sb = SC[2]
        SC_Pl = SC[3]
        
        #print SC_Aw, SC_Sw, SC_Sb, SC_Pl
        

        #print BasalAreaIncrementNonSpatialAw (sp_Aw, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, BA_AwT )

        #print BAinc_AwT, BA_AwT, SC_Aw, SI_bh_Aw, N_bh_Aw, bhage_Aw

        '''
        I implicitly assume here that, if there are no plants of a given species in the stand at time t, then the Basal area is zero and it was zero in the previous years,
        it might be the case that the species got locally extinct, i.e., it existed before in the stand but died along the years. It is hard (but still possible) to 
        predict this part existence.
        
        '''
       
        if bhage_Aw >= 0 and N_bh_Aw >0:
            BA_Aw = BAincIter_Aw ('Aw', BAinc_AwB, BA_AwB, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, printWarnings = True)
            BA_AwB = BA_Aw[0]
            BAinc_AwB = BA_Aw[1]   
            topHeight_Aw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Aw',  SI_bh_Aw,  tage_Aw)
        else:
            BA_AwB = 0
            BAinc_AwB = 0
            topHeight_Aw=0
              
      
        if bhage_Sb >= 0 and N_bh_Sb>0:
            BA_Sb = BAincIter_Sb ('Sb', BAinc_SbB, BA_SbB, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, printWarnings = True)
            BA_SbB = BA_Sb [0]
            BAinc_SbB = BA_Sb[1]   
            topHeight_Sb=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sb',  SI_bh_Sb,  tage_Sb)
        else:
            BA_SbB = 0
            BAinc_SbB = 0
            topHeight_Sb = 0                           
       
       
        if bhage_Sw >= 0 and N_bh_Sw>0:
            BA_Sw = BAincIter_Sw ('Sw', BAinc_SwB, BA_SwB, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, printWarnings = True)
            BA_SwB = BA_Sw [0]
            BAinc_SwB = BA_Sw[1]  
            topHeight_Sw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sw',  SI_bh_Sw,  tage_Sw)
        else:
            BA_SwB = 0
            BAinc_SwB = 0
            topHeight_Sw = 0
        
        
        if bhage_Pl >= 0 and N_bh_Pl>0:
            BA_Pl = BAincIter_Pl ('Pl', BAinc_PlB, BA_PlB, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl, bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, printWarnings = True)
            BA_PlB = BA_Pl [0]  
            BAinc_PlB = BA_Pl[1]
            topHeight_Pl=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Pl',  SI_bh_Pl,  tage_Pl)
        else:
            BA_PlB = 0
            BAinc_PlB = 0
            topHeight_Pl = 0
            
        

        Tvol = GrossTotalVolume( BA_AwB, BA_SbB, BA_SwB, BA_PlB, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl)

        Tvol_Aw = Tvol[0]
        Tvol_Sb = Tvol[1]
        Tvol_Sw = Tvol[2]
        Tvol_Pl = Tvol[3]
        
        
        MVol_Aw = MerchantableVolumeAw(N_bh_Aw, BA_AwB, topHeight_Aw, StumpDOB_Aw, StumpHeight_Aw , TopDib_Aw, Tvol_Aw)   
        
        MVol_Sb = MerchantableVolumeSb(N_bh_Sb, BA_SbB, topHeight_Sb, StumpDOB_Sb, StumpHeight_Sb , TopDib_Sb, Tvol_Sb) 
        
        MVol_Sw = MerchantableVolumeSw(N_bh_Sw, BA_SwB, topHeight_Sw, StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, Tvol_Sw)
        
        MVol_Pl = MerchantableVolumePl(N_bh_Pl, BA_PlB, topHeight_Pl, StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, Tvol_Pl)
        
        #print startTage, BA_PlT, BAinc_PlT,  N_bh_Pl, SC_PlT
        
        
        #print startTage, N_bh_Pl, N_bh_Aw,  N_bh_Sw, N_bh_Sb 
        
        #print startTage, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl
        
        #print startTage, Tvol_Aw, Tvol_Sb, Tvol_Sw, Tvol_Pl
        
        print startTage, BA_PlT, BA_AwT, BA_SwT, BA_SbT
        
        #print startTage, SC_Pl, SC_Aw, SC_Sw, SC_Sb
        
        #print startTage, MVol_Aw, MVol_Sb, MVol_Sw, MVol_Pl
       
        startTage = startTage - 1
        startTageAw = startTageAw - 1
        startTageSw = startTageSw - 1 
        startTagePl = startTagePl - 1 
        startTageSb = startTageSb -1
        
        
        
        
    '''simulating growth forwards in time starting from the time at which data was taken '''
        
    while startTage_forward < 251:
        '''Ages at time T + 1''' 
        
        bhage_AwF = startTageAwF  - y2bh_Aw 
        bhage_SwF = startTageSwF  - y2bh_Sw 
        bhage_PlF = startTagePlF  - y2bh_Pl
        bhage_SbF = startTageSbF  - y2bh_Sb
        
        tage_AwF = startTageAwF 
        tage_SwF = startTageSwF  
        tage_PlF = startTagePlF  
        tage_SbF = startTageSbF  
        
        '''densities at time t+1 '''
        
        if N_bh_AwT == 0:
            N_bh_AwT = 0
            
        else:
            N_bh_AwT = densityAw (SDF_Aw0, bhage_AwF, SI_bh_Aw)
         
        if N_bh_SbT == 0:
            N_bh_SbT = 0
        else:
            N_bh_SbT = densitySb (SDF_Sb0, tage_SbF, SI_bh_Sb)
            
        if N_bh_SwT == 0:
            N_bh_SwT = 0
        else:
            N_bh_SwT = densitySw (SDF_Sw0, SDF_Aw0, tage_SwF, SI_bh_Sw)
        
        if N_bh_PlT == 0:
            N_bh_PlT = 0
        else:
            N_bh_PlT = densityPl (SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_PlF , SI_bh_Pl)
            
        #print startTage_forward, N_bh_AwT, N_bh_SbT, N_bh_SwT, N_bh_PlT
        
        
        SC_F = SCestimate (N_bh_AwT,  N_bh_SbT, N_bh_SwT, N_bh_PlT)

        SC_AwF = SC_F[0]
        SC_SwF = SC_F[1]
        SC_SbF = SC_F[2]
        SC_PlF = SC_F[3]
        
                
        if N_bh_AwT>0:
            BA_AwT = BA_AwT + BasalAreaIncrementNonSpatialAw('Aw', SC_AwF, SI_bh_Aw, N_bh_AwT, N0_Aw, bhage_AwF, BA_AwT)
            topHeight_Aw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Aw',  SI_bh_Aw,  tage_AwF)
        else:
            BA_AwT = 0
            topHeight_Aw = 0
        
        if N_bh_SbT>0:
            BA_SbT = BA_SbT + BasalAreaIncrementNonSpatialSb ('Sb', SC_SbF, SI_bh_Sb, N_bh_SbT, N0_Sb, bhage_SbF, BA_SbT)
            topHeight_Sb=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sb',  SI_bh_Sb,  tage_SbF)
        else:
            BA_SbT = 0
            topHeight_Sb = 0
            
        if N_bh_SwT>0:
            BA_SwT = BA_SwT + BasalAreaIncrementNonSpatialSw ('Sw', SC_SwF, SI_bh_Sw, N_bh_SwT, N0_Sw, bhage_SwF, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_SwT)
            topHeight_Sw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sw',  SI_bh_Sw,  tage_SwF)
        else:
            BA_SwT = 0
            topHeight_Sw = 0
            
        if N_bh_PlT>0:
            BA_PlT = BA_PlT + BasalAreaIncrementNonSpatialPl('Pl', SC_PlF, SI_bh_Pl, N_bh_PlT, N0_Pl, bhage_PlF, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_PlT)
            topHeight_Pl=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Pl',  SI_bh_Pl,  tage_PlF)
        else:
            BA_PlT = 0
            topHeight_Pl = 0
            
        Tvol = GrossTotalVolume( BA_AwT, BA_SbT, BA_SwT, BA_PlT, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl)

        Tvol_Aw = Tvol[0]
        Tvol_Sb = Tvol[1]
        Tvol_Sw = Tvol[2]
        Tvol_Pl = Tvol[3]
        
        
        MVol_Aw = MerchantableVolumeAw(N_bh_AwT, BA_AwT, topHeight_Aw, StumpDOB_Aw, StumpHeight_Aw , TopDib_Aw, Tvol_Aw)   
        
        MVol_Sb = MerchantableVolumeSb(N_bh_SbT, BA_SbT, topHeight_Sb, StumpDOB_Sb, StumpHeight_Sb , TopDib_Sb, Tvol_Sb) 
        
        MVol_Sw = MerchantableVolumeSw(N_bh_SwT, BA_SwT, topHeight_Sw, StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, Tvol_Sw)
        
        MVol_Pl = MerchantableVolumePl(N_bh_PlT, BA_PlT, topHeight_Pl, StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, Tvol_Pl)
        
        #print startTage_forward, N_bh_PlT, N_bh_AwT,  N_bh_SwT, N_bh_SbT 
        
        #print startTage_forward, SC_PlF, SC_AwF, SC_SwF, SC_SbF
            
        #print startTage_forward, Tvol_Aw, Tvol_Sb, Tvol_Sw, Tvol_Pl
        print startTage_forward, BA_PlT, BA_AwT, BA_SwT, BA_SbT  
        
        #print startTage_forward, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl
        
        #print startTage_forward, MVol_Aw, MVol_Sb, MVol_Sw, MVol_Pl
        
        
        startTage_forward += 1
        startTageAwF += 1
        startTageSwF += 1
        startTagePlF += 1
        startTageSbF += 1
        
 