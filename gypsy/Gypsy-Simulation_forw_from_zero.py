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

from GYPSYNonSpatial import BAfactorFinder_Aw
from GYPSYNonSpatial import BAfromZeroToDataAw
from GYPSYNonSpatial import BAfactorFinder_Sb
from GYPSYNonSpatial import BAfromZeroToDataSb
from GYPSYNonSpatial import BAfactorFinder_Sw
from GYPSYNonSpatial import BAfromZeroToDataSw
from GYPSYNonSpatial import BAfactorFinder_Pl
from GYPSYNonSpatial import BAfromZeroToDataPl

from GYPSYNonSpatial import MerchantableVolumeAw
from GYPSYNonSpatial import MerchantableVolumeSw
from GYPSYNonSpatial import MerchantableVolumeSb
from GYPSYNonSpatial import MerchantableVolumePl

# input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion


data1 = pd.read_csv('/Users/juliannosambatti/Projects/Gipsy/testData/stands8.csv')


fplotSim = dataPrepGypsy(data1)[0]

spList = dataPrepGypsy(data1)[1]

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
    
    SCT = SCestimate (N_bh_AwT,  N_bh_SbT, N_bh_SwT, N_bh_PlT)

    SC_AwT = SCT[0]
    SC_SwT = SCT[1]
    SC_SbT = SCT[2]
    SC_PlT = SCT[3]
   
    
    BA_Aw0 = N0_Aw * 3.14* (0.1/2.0)**2 
    BA_Sw0 = N0_Sw * 3.14* (0.1/2.0)**2 
    BA_Sb0 = N0_Pl * 3.14* (0.1/2.0)**2 
    BA_Pl0 = N0_Sb * 3.14* (0.1/2.0)**2 
    #print BA_Aw0
    
    
    SC_0 = SCestimate (N0_Aw, N0_Sb, N0_Sw, N0_Pl )
    SC_Aw0 = SC_0[0]
    SC_Sw0 = SC_0[1]
    SC_Sb0 = SC_0[2]
    SC_Pl0 = SC_0[3]
    
    SC_Aw = SC_Aw0
    SC_Sw = SC_Sw0
    SC_Sb = SC_Sb0
    SC_Pl = SC_Pl0
    
    #print SC_Sw
        
    
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
    startTageAw = tageData[0]
    startTageSw = tageData[1]
    startTagePl = tageData[2]
    startTageSb = tageData[3]
    
    startTageAwF = tageData[0]+1
    startTageSwF = tageData[1]+1
    startTagePlF = tageData[2]+1
    startTageSbF = tageData[3]+1

    max_Age = 250    
    
    tageData = sorted (tageData, reverse=True)

    startTage = tageData[0]
    
    startTage_forward = tageData[0] + 1
    

    #print startTage, startTageAw, y2bh_Aw, SC_Aw, SI_bh_Aw, N_bh_AwT, N0_Aw, BA_Aw0
  
  
 # input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion
    
    '''estimating correction factor to fit BA at t0 and BA at t and choosing whether simulating with multiplication factor
       or starting at t recalculating the densities and SC'''
    
    if N0_Aw > 0:
        f_Aw = BAfactorFinder_Aw (startTage, startTageAw, y2bh_Aw, SC_Aw, SI_bh_Aw, N_bh_AwT, N0_Aw, BA_Aw0, BA_AwT,  printWarnings = True)
    else:
        f_Aw = 0
    #print 'f_Aw =  ', f_Aw
    
    if N0_Sb > 0:
        f_Sb = BAfactorFinder_Sb (startTage, startTageSb, y2bh_Sb, SC_Sb, SI_bh_Sb, N_bh_SbT, N0_Sb, BA_Sb0, BA_SbT, printWarnings = True)
    else:
        f_Sb = 0
    #print 'f_Sb =  ', f_Sb
    
    if N0_Sw > 0:
        f_Sw = BAfactorFinder_Sw (startTage, startTageSw, y2bh_Sw,  SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw,  SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0, BA_SwT, printWarnings = True)
    else:
        f_Sw = 0
    #print 'f_Sw =  ', f_Sw
        
    if N0_Sw > 0:
        f_Pl = BAfactorFinder_Pl (startTage, startTagePl, y2bh_Pl,  SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl,  SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, BA_PlT, printWarnings = True)
    else:
        f_Pl = 0
    #print 'f_Pl =  ', f_Pl
    
    #print startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, BA_Sw0, f_Sw
    
    '''choosing no implies in simulating forward after time t using the same factor estimated and used to simulate until time t
       choosing yes, implies in simulating forward ignoring the factor estimated and used until time t and estimate, at every cycle, densities,
       SCs etc
    ''' 
    
    simulation_choice = 'yes'
    
    BA_0_to_data_Aw = BAfromZeroToDataAw (startTage, startTageAw, y2bh_Aw, SC_Aw, SI_bh_Aw, N_bh_AwT, N0_Aw, BA_Aw0, f_Aw, simulation_choice)
    BA_0_to_data_Sb = BAfromZeroToDataSb (startTage, startTageSb, y2bh_Sb, SC_Sb, SI_bh_Sb, N_bh_SbT, N0_Sb, BA_Sb0, f_Sb, simulation_choice)
    BA_0_to_data_Sw = BAfromZeroToDataSw (startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0, f_Sw, simulation_choice)
    BA_0_to_data_Pl = BAfromZeroToDataPl (startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, f_Pl, simulation_choice)
    
    
    if simulation_choice == 'no':  
        
        BA_0_to_data_Aw = BAfromZeroToDataAw (startTage, startTageAw, y2bh_Aw, SC_Aw, SI_bh_Aw, N_bh_AwT, N0_Aw, BA_Aw0, f_Aw, simulation_choice)
        BA_0_to_data_Sb = BAfromZeroToDataSb (startTage, startTageSb, y2bh_Sb, SC_Sb, SI_bh_Sb, N_bh_SbT, N0_Sb, BA_Sb0, f_Sb, simulation_choice)
        BA_0_to_data_Sw = BAfromZeroToDataSw (startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0, f_Sw, simulation_choice)
        BA_0_to_data_Pl = BAfromZeroToDataPl (startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, f_Pl, simulation_choice)
    
        
        continue
    
    
        
    '''simulating growth forwards in time starting from the time at which data was taken '''
    t = startTage    
    while t < max_Age :
        '''Ages at time t + 1'''    

    
        tage_AwF = startTageAwF    
        tage_SwF = startTageSwF    
        tage_PlF = startTagePlF   
        tage_SbF = startTageSbF    
       
        
        bhage_AwF = tage_AwF - y2bh_Aw 
        bhage_SwF = tage_SwF - y2bh_Sw 
        bhage_PlF = tage_PlF - y2bh_Pl
        bhage_SbF = tage_SbF - y2bh_Sb
        
        
        N_bh_AwT = densityAw (SDF_Aw0, bhage_AwF, SI_bh_Aw)
        N_bh_SbT = densitySb (SDF_Sb0, tage_SbF, SI_bh_Sb)
        N_bh_SwT = densitySw (SDF_Sw0, SDF_Aw0, tage_SwF, SI_bh_Sw)
        N_bh_PlT = densityPl (SDF_Aw0, SDF_Sw0, SDF_Sb0, SDF_Pl0, tage_PlF, SI_bh_Pl)
        
        #print N_bh_SwT

     
        #print bhage_Aw, bhage_Sw, BA_AwB,  BA_AwT
            
        #print  N_bh_AwT, N_bh_SbT, N_bh_SwT, N_bh_PlT
     

        SC_F = SCestimate (N_bh_AwT,  N_bh_SbT, N_bh_SwT, N_bh_PlT)

        SC_AwF = SC_F[0]
        SC_SwF = SC_F[1]
        SC_SbF = SC_F[2]
        SC_PlF = SC_F[3]
        
                
        if N_bh_AwT>0:
            BAinc_Aw = BasalAreaIncrementNonSpatialAw('Aw', SC_AwF, SI_bh_Aw, N_bh_AwT, N0_Aw, bhage_AwF, BA_AwT)
            BA_AwT = BA_AwT + BAinc_Aw
            topHeight_Aw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Aw',  SI_bh_Aw,  tage_AwF)
            #print  'bhage Aw ', bhage_AwF, 'BA Aw ', BA_AwT

        else:
            BA_AwT = 0
            topHeight_Aw = 0
        
        if N_bh_SbT>0:
            BA_SbT = BA_SbT + BasalAreaIncrementNonSpatialSb ('Sb', SC_SbF, SI_bh_Sb, N_bh_SbT, N0_Sb, bhage_SbF, BA_SbT)
            topHeight_Sb=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sb',  SI_bh_Sb,  tage_SbF)
            #print 'bhageSb ',  bhage_SbF, 'BA Sb ',  BA_SbT
        else:
            BA_SbT = 0
            topHeight_Sb = 0
            
            
        if N_bh_SwT>0:
            BA_SwT = BA_SwT + BasalAreaIncrementNonSpatialSw ('Sw', SC_SwF, SI_bh_Sw, N_bh_SwT, N0_Sw, bhage_SwF, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_SwT)
            topHeight_Sw=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Sw',  SI_bh_Sw,  tage_SwF)
            print 'bhageSw ', bhage_SwF, 'BA Sw ', BA_SwT
        else:
            BA_SwT = 0
            topHeight_Sw = 0
            
        if N_bh_PlT>0:
            BA_PlT = BA_PlT + BasalAreaIncrementNonSpatialPl('Pl', SC_PlF, SI_bh_Pl, N_bh_PlT, N0_Pl, bhage_PlF, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_PlT)
            topHeight_Pl=ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge('Pl',  SI_bh_Pl,  tage_PlF)
            #print 'bhagePl ', bhage_PlF, 'BA Pl', BA_PlT
        else:
            BA_PlT = 0
            topHeight_Pl = 0
            
        Tvol = GrossTotalVolume ( BA_AwT, BA_SbT, BA_SwT, BA_PlT, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl)

        Tvol_Aw = Tvol[0]
        Tvol_Sb = Tvol[1]
        Tvol_Sw = Tvol[2]
        Tvol_Pl = Tvol[3]
    
        
        MVol_Aw = MerchantableVolumeAw(N_bh_AwT, BA_AwT, topHeight_Aw, StumpDOB_Aw, StumpHeight_Aw , TopDib_Aw, Tvol_Aw)   
        
        MVol_Sb = MerchantableVolumeSb(N_bh_SbT, BA_SbT, topHeight_Sb, StumpDOB_Sb, StumpHeight_Sb , TopDib_Sb, Tvol_Sb) 
        
        MVol_Sw = MerchantableVolumeSw(N_bh_SwT, BA_SwT, topHeight_Sw, StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, Tvol_Sw)
        
        MVol_Pl = MerchantableVolumePl(N_bh_PlT, BA_PlT, topHeight_Pl, StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, Tvol_Pl)
        
        #print startTageAwF, N_bh_PlT, N_bh_AwT,  N_bh_SwT, N_bh_SbT 
        
        #print startTage_forward, SC_PlF, SC_AwF, SC_SwF, SC_SbF
            
        #print startTage, Tvol_Aw, Tvol_Sb, Tvol_Sw, Tvol_Pl
        #print startTage, BA_PlT, BA_AwT, BA_SwT, BA_SbT  
        
        #print startTage, topHeight_Aw, topHeight_Sb, topHeight_Sw, topHeight_Pl
        
        #print startTage, MVol_Aw, MVol_Sb, MVol_Sw, MVol_Pl

        
        t += 1
        startTageAwF += 1
        startTageSwF += 1
        startTagePlF += 1
        startTageSbF += 1
        
 