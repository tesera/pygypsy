# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:06:29 2016

@author: juliannosambatti
"""

import csv
import pandas as pd
import numpy 
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

from GYPSYNonSpatial import BAincIter_Aw
from GYPSYNonSpatial import BAincIter_Sw
from GYPSYNonSpatial import BAincIter_Sb
#from GYPSYNonSpatial import BAincIter_Pl

# input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion
sp_Aw=['Aw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sb=['Sb', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Pl=['Pl', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]
sp_Sw=['Sw', 0, 0, 0, 0, 0, 0, 13, 0.3, 7, 0, 0]

data1 = pd.read_csv('/Users/juliannosambatti/Projects/Gipsy/Inputs/LCR_join10b_x_julianno_1row.csv')


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
    
    #print 'kkkk', BA_PlT
    
    BAinc_AwT  = inputDF.loc[plotID,'BAinc_Aw']
    BAinc_SwT  = inputDF.loc[plotID,'BAinc_Sw']
    BAinc_PlT  = inputDF.loc[plotID,'BAinc_Pl']
    BAinc_SbT  = inputDF.loc[plotID,'BAinc_Sb']
    
    SDF_Aw0  = inputDF.loc[plotID,'SDF_Aw']
    SDF_Sw0  = inputDF.loc[plotID,'SDF_Sw']
    SDF_Pl0  = inputDF.loc[plotID,'SDF_Pl']
    SDF_Sb0  = inputDF.loc[plotID,'SDF_Sb']
    
     
    N0_Aw  = inputDF.loc[plotID,'N0_Aw']
    N0_Sw  = inputDF.loc[plotID,'N0_Sw']
    N0_Pl  = inputDF.loc[plotID,'N0_Pl']
    N0_Sb  = inputDF.loc[plotID,'N0_Sb']
    
    #print N0_Aw, N0_Sw, N0_Pl, N0_Sb
    
    tageData = [ tage_AwT, tage_SwT, tage_PlT, tage_SbT ]
    startTageAw = tageData[0]-1
    startTageSw = tageData[1]-1
    startTagePl = tageData[2]-1
    startTageSb = tageData[3]-1
    
    tageData = sorted (tageData, reverse=True)

    startTage = tageData[0]-1
    
    startTage_forward = tageData[0] + 1
  
 # input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion
    
    
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
            BA_Aw = BAincIter_Aw (sp_Aw, BAinc_AwT, BA_AwT, SC_Aw, SI_bh_Aw, N_bh_Aw, N0_Aw, bhage_Aw, printWarnings = True)
            BA_AwT = BA_Aw[0]
            BAinc_AwT = BA_Aw[1]            
        else:
            BA_AwT = 0
            BAinc_AwT = 0
        
               
        
        
      
        if bhage_Sb >= 0 and N_bh_Sb>0:
            BA_Sb = BAincIter_Sb (sp_Sb, BAinc_SbT, BA_SbT, SC_Sb, SI_bh_Sb, N_bh_Sb, N0_Sb, bhage_Sb, printWarnings = True)
            BA_SbT = BA_Sb [0]
            BAinc_SbT = BA_Sb[1]           
        else:
            BA_SbT = 0
            BAinc_SbT = 0
        
        
               
       
       
        if bhage_Sw >= 0 and N_bh_Sw>0:
            BA_Sw = BAincIter_Sw (sp_Sw, BAinc_SwT, BA_SwT, SC_Sw, SI_bh_Sw, N_bh_Sw, N0_Sw, bhage_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, printWarnings = True)
            BA_SwT = BA_Sw [0]
            BAinc_SwT = BA_Sw[1]           
        else:
            BA_SwT = 0
            BAinc_SwT = 0
        
        
        
        
        
        
        if bhage_Pl >= 0 and N_bh_Pl>0:
            BA_Pl = BAincIter_Pl (sp_Pl, BAinc_PlT, BA_PlT, SC_Pl, SI_bh_Pl, N_bh_Pl, N0_Pl, bhage_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, printWarnings = True)
            BA_PlT = BA_Pl [0]         
        else:
            BA_PlT = 0
            BAinc_PlT = 0
        

        
        
        
        #print startTage, BA_PlT, BAinc_PlT,  N_bh_Pl, SC_PlT
        
        
        print startTage, N_bh_Aw,  N_bh_Sb, N_bh_Sw, N_bh_Pl
        
        #print startTage, BA_PlT, BA_AwT, BA_SwT, BA_SbT
        
        #print startTage, SC_Pl, SC_Aw, SC_Sw, SC_Sb
       
        startTage = startTage - 1
        startTageAw = startTageAw - 1
        startTageSw = startTageSw - 1 
        startTagePl = startTagePl - 1 
        startTageSb = startTageSb -1
        
        
    while startTage_forward <250:
        
 