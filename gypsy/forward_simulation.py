# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:06:29 2016

@author: juliannosambatti
"""
import logging
import pandas as pd
import os
import matplotlib.pyplot as plt

from asaCompileAgeGivenSpSiHt import ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge
from GypsyDataPrep import dataPrepGypsy
from GYPSYNonSpatial import (BasalAreaIncrementNonSpatialAw,
                             BasalAreaIncrementNonSpatialSw,
                             BasalAreaIncrementNonSpatialSb,
                             BasalAreaIncrementNonSpatialPl,
                             densityAw, densitySw,
                             densitySb, densityPl,
                             SCestimate,
                             BAfactorFinder_Aw,
                             BAfromZeroToDataAw,
                             BAfactorFinder_Sb,
                             BAfromZeroToDataSb,
                             BAfactorFinder_Sw,
                             BAfromZeroToDataSw,
                             BAfactorFinder_Pl,
                             BAfromZeroToDataPl,
                             MerchantableVolumeAw,
                             MerchantableVolumeSw,
                             MerchantableVolumeSb,
                             MerchantableVolumePl,
                             densities_and_SCs_to_250,
                             GrossTotalVolume_Aw,
                             GrossTotalVolume_Sw,
                             GrossTotalVolume_Sb,
                             GrossTotalVolume_Pl)
logger = logging.getLogger(__name__)

# input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion

def BA_zeroAw (BA_Aw0, BA_AwT):
    while BA_Aw0 >BA_AwT * 0.5:     
        BA_Aw0 = BA_Aw0 * 0.5
    return BA_Aw0

def BA_zeroSw (BA_Sw0, BA_SwT):
    while BA_Sw0 > BA_SwT * 0.5:
        BA_Sw0 = BA_Sw0 * 0.5
    return BA_Sw0

def BA_zeroSb (BA_Sb0, BA_SbT):
    while BA_Sb0 > BA_SbT * 0.5:
        BA_Sb0 = BA_Sb0 * 0.5
    return BA_Sb0

def BA_zeroPl (BA_Pl0, BA_PlT):
    while BA_Pl0 > BA_PlT * 0.5:
        BA_Pl0 = BA_Pl0 * 0.5
    return BA_Pl0
    
def BA0_lower_BAT_Aw (BA_AwT):
    BA_Aw0 = 0.001
    if BA_Aw0 > BA_AwT:
            BA_Aw0 = BA_zeroAw (BA_Aw0, BA_AwT)
    else:
        pass
    return BA_Aw0
    
def BA0_lower_BAT_Sw (BA_SwT):
    BA_Sw0 = 0.001
    if BA_Sw0 > BA_SwT:
            BA_Sw0 = BA_zeroSw (BA_Sw0, BA_SwT)
    else:
        pass
    return BA_Sw0

def BA0_lower_BAT_Sb (BA_SbT):
    BA_Sb0 = 0.001
    if BA_Sb0 > BA_SbT:
            BA_Sb0 = BA_zeroSb (BA_Sb0, BA_SbT)
    else:
        pass
    return BA_Sb0

def BA0_lower_BAT_Pl (BA_PlT):
    BA_Pl0 = 0.001
    if BA_Pl0 > BA_PlT:
            BA_Pl0 = BA_zeroPl (BA_Pl0, BA_PlT)
    else:
        pass
    return BA_Pl0

def get_factors_for_all_species(**kwargs):
        logger.debug('Getting factors for all species')

        f_Sb = 0
        f_Aw = 0
        f_Sw = 0
        f_Pl = 0
#        if kwargs['N0_Aw'] > 0:
#            f_Aw = BAfactorFinder_Aw (**kwargs)
            
        if kwargs['N0_Aw'] > 0:
            f_Aw = BAfactorFinder_Aw (**kwargs)

        if kwargs['N0_Sb'] > 0:
            f_Sb = BAfactorFinder_Sb (**kwargs)

        if kwargs['N0_Sw'] > 0:
            f_Sw = BAfactorFinder_Sw (**kwargs)

        if kwargs['N0_Pl'] > 0:
            f_Pl = BAfactorFinder_Pl (**kwargs)

        #print startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, BA_Sw0, f_Sw
        return {'f_Aw':f_Aw,
                'f_Sb':f_Sb,
                'f_Sw':f_Sw,
                'f_Pl':f_Pl,
                            }

def simulate_forwards_df(plot_df, simulation_choice='yes'):
    """Run forwards simulation

    Keyword Arguments:
    plot_df -- pandas.DataFrame with plot data

    Return:
    !TODO!
    """
    logger.debug('Starting forwards simulation')
    inputDF=plot_df
    for plotID, row in inputDF.iterrows():
        # TODO: use row
        # SI_bh_Aw = row['SI_Aw']
        SI_bh_Aw = row['SI_Aw']
        SI_bh_Sw = row['SI_Sw']
        SI_bh_Pl = row['SI_Pl']
        SI_bh_Sb = row['SI_Sb']

        N_bh_AwT  = row['N_Aw']
        N_bh_SwT  = row['N_Sw']
        N_bh_PlT  = row['N_Pl']
        N_bh_SbT  = row['N_Sb']

        y2bh_Aw = row['y2bh_Aw']
        y2bh_Sw = row['y2bh_Sw']
        y2bh_Sb = row['y2bh_Sb']
        y2bh_Pl = row['y2bh_Pl']

        tage_AwT  = row['tage_Aw']
        tage_SwT  = row['tage_Sw']
        tage_PlT  = row['tage_Pl']
        tage_SbT  = row['tage_Sb']

        bhage_AwT = tage_AwT  - y2bh_Aw
        bhage_SwT = tage_SwT  - y2bh_Sw
        bhage_PlT = tage_PlT  - y2bh_Pl
        bhage_SbT = tage_SbT  - y2bh_Sb


        BA_AwT  = row['BA_Aw']
        BA_SwT  = row['BA_Sw']
        BA_PlT  = row['BA_Pl']
        BA_SbT  = row['BA_Sb']

        BAinc_AwT  = row['BAinc_Aw']
        BAinc_SwT  = row['BAinc_Sw']
        BAinc_PlT  = row['BAinc_Pl']
        BAinc_SbT  = row['BAinc_Sb']

        BAinc_AwB = BAinc_AwT
        BAinc_SwB = BAinc_SwT
        BAinc_PlB = BAinc_PlT
        BAinc_SbB = BAinc_SbT

        SDF_Aw0  = row['SDF_Aw']
        SDF_Sw0  = row['SDF_Sw']
        SDF_Pl0  = row['SDF_Pl']
        SDF_Sb0  = row['SDF_Sb']

        N0_Aw  = row['N0_Aw']
        N0_Sw  = row['N0_Sw']
        N0_Pl  = row['N0_Pl']
        N0_Sb  = row['N0_Sb']

        SCT = SCestimate (N_bh_AwT,  N_bh_SbT, N_bh_SwT, N_bh_PlT)

        SC_AwT = SCT[0]
        SC_SwT = SCT[1]
        SC_SbT = SCT[2]
        SC_PlT = SCT[3]

        DB_BhageAw = 0.1
        DB_BhageSw = 0.1
        DB_BhageSb = 0.1
        DB_BhagePl = 0.1

        BA_Aw0 = BA0_lower_BAT_Aw (BA_AwT)
        BA_Sw0 = BA0_lower_BAT_Sw (BA_SwT)
        BA_Sb0 = BA0_lower_BAT_Sb (BA_SbT)
        BA_Pl0 = BA0_lower_BAT_Pl (BA_PlT)

        SC_0 = SCestimate (N0_Aw, N0_Sb, N0_Sw, N0_Pl )
        SC_Aw0 = SC_0[0]
        SC_Sw0 = SC_0[1]
        SC_Sb0 = SC_0[2]
        SC_Pl0 = SC_0[3]

        SC_Aw = SC_Aw0
        SC_Sw = SC_Sw0
        SC_Sb = SC_Sb0
        SC_Pl = SC_Pl0


        StumpDOB_Aw = row['StumpDOB_Aw']
        StumpHeight_Aw = row['StumpHeight_Aw']
        TopDib_Aw = row['TopDib_Aw']

        StumpDOB_Sb = row['StumpDOB_Sb']
        StumpHeight_Sb = row['StumpHeight_Sb']
        TopDib_Sb = row['TopDib_Sb']

        StumpDOB_Sw = row['StumpDOB_Sw']
        StumpHeight_Sw = row['StumpHeight_Sw']
        TopDib_Sw = row['TopDib_Sw']

        StumpDOB_Pl = row['StumpDOB_Pl']
        StumpHeight_Pl  = row['StumpHeight_Pl']
        TopDib_Pl = row['TopDib_Pl']

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

        startTage = int(tageData[0])

        startTage_forward = tageData[0] - 1

        densities = densities_and_SCs_to_250 (
                                startTage = startTage,
                                startTageAw = startTageAw,
                                y2bh_Aw = y2bh_Aw,
                                startTageSw = startTageSw,
                                y2bh_Sw = y2bh_Sw,
                                startTageSb = startTageSb,
                                y2bh_Sb = y2bh_Sb,
                                startTagePl = startTagePl,
                                y2bh_Pl = y2bh_Pl,
                                SDF_Aw0 = SDF_Aw0,
                                SDF_Sw0 = SDF_Sw0,
                                SDF_Pl0 = SDF_Pl0,
                                SDF_Sb0 = SDF_Sb0,
                                SI_bh_Aw = SI_bh_Aw,
                                SI_bh_Sw = SI_bh_Sw,
                                SI_bh_Sb = SI_bh_Sb,
                                SI_bh_Pl = SI_bh_Pl)
        #print startTage, startTageAw, y2bh_Aw, SC_Aw, SI_bh_Aw, N_bh_AwT, N0_Aw, BA_Aw0
        #print densities

     # input - species, top height, total age, BHage (from the function), N (or density), current Basal Area,  Measured Percent Stocking, StumpDOB , StumpHeight, TopDib, SI, sp proportion
  
        

        '''estimating correction factor to fit BA at t0 and BA at t and choosing whether simulating with multiplication factor
           or starting at t recalculating the densities and SC'''
        species_factors = get_factors_for_all_species(
                startTage = startTage,
                startTageAw = startTageAw, 
                y2bh_Aw = y2bh_Aw, 
                SC_Aw = SC_Aw, 
                SI_bh_Aw = SI_bh_Aw, 
                N_bh_AwT = N_bh_AwT, 
                N0_Aw = N0_Aw, 
                BA_Aw0 = BA_Aw0, 
                BA_AwT = BA_AwT,
                startTageSb = startTageSb, 
                y2bh_Sb = y2bh_Sb, 
                SC_Sb = SC_Sb, 
                SI_bh_Sb = SI_bh_Sb, 
                N_bh_SbT = N_bh_SbT, 
                N0_Sb = N0_Sb, 
                BA_Sb0 = BA_Sb0, 
                BA_SbT = BA_SbT,
                startTageSw = startTageSw, 
                y2bh_Sw = y2bh_Sw,  
                SC_Sw = SC_Sw, 
                SI_bh_Sw = SI_bh_Sw, 
                N_bh_SwT = N_bh_SwT, 
                N0_Sw = N0_Sw,  
                SDF_Pl0 = SDF_Pl0, 
                SDF_Sb0 = SDF_Sb0, 
                BA_Sw0 = BA_Sw0, 
                BA_SwT = BA_SwT,
                startTagePl = startTagePl, 
                y2bh_Pl = y2bh_Pl,  
                SC_Pl = SC_Pl, 
                SI_bh_Pl = SI_bh_Pl, 
                N_bh_PlT = N_bh_PlT, 
                N0_Pl = N0_Pl,  
                SDF_Aw0 = SDF_Aw0, 
                SDF_Sw0 = SDF_Sw0,  
                BA_Pl0 = BA_Pl0, 
                BA_PlT = BA_PlT,
                densities= densities,
                printWarnings=True)
        
        output_DF_Aw = pd.DataFrame (columns=['BA_Aw'])      
        output_DF_Sw = pd.DataFrame (columns=['BA_Sw'])   
        output_DF_Sb = pd.DataFrame (columns=['BA_Sb'])   
        output_DF_Pl = pd.DataFrame (columns=['BA_Pl'])   
        
        f_Aw = species_factors['f_Aw']
        f_Sw = species_factors['f_Sw']
        f_Sb = species_factors['f_Sb']
        f_Pl = species_factors['f_Pl']
       # print f_Aw

        '''choosing no implies in simulating forward after time t using the same factor estimated and used to simulate until time t
           choosing yes, implies in simulating forward ignoring the factor estimated and used until time t and estimate, at every cycle, densities,
           SCs etc
        '''

        logger.debug('Getting basal area from time 0 to time of data')
        BA_0_to_data_Aw = BAfromZeroToDataAw (startTage, SI_bh_Aw, N0_Aw, BA_Aw0, SDF_Aw0, f_Aw, densities, simulation_choice = 'no', simulation = False)
        BA_0_to_data_Sb = BAfromZeroToDataSb (startTage, startTageSb, y2bh_Sb, SC_Sb, SI_bh_Sb, N_bh_SbT, N0_Sb, BA_Sb0, f_Sb, simulation_choice,  simulation = False)
        BA_0_to_data_Sw = BAfromZeroToDataSw (startTage, startTageSw, y2bh_Sw, SC_Sw, SI_bh_Sw, N_bh_SwT, N0_Sw, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_Sw0, f_Sw, simulation_choice, simulation = False)
        BA_0_to_data_Pl = BAfromZeroToDataPl (startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, f_Pl, simulation_choice, simulation = False)
        
        #print startTage, startTageAw, y2bh_Aw, SC_Aw, SI_bh_Aw, N_bh_AwT, N0_Aw, BA_Aw0, BA_AwT, simulation_choice
        #print startTage, startTagePl, y2bh_Pl, SC_Pl, SI_bh_Pl, N_bh_PlT, N0_Pl, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_Pl0, BA_PlT
        
        output_DF_Aw = pd.concat([BA_0_to_data_Aw[1] ], axis=1)
        output_DF_Sw = pd.concat([BA_0_to_data_Sw[1] ], axis=1)
        output_DF_Sb = pd.concat([BA_0_to_data_Sb[1] ], axis=1)
        output_DF_Pl = pd.concat([BA_0_to_data_Pl[1] ], axis=1)
        
        #output_DF = output_DF.append ({'BA_Aw':BA_0_to_data_Aw[0], 'BA_Sw':BA_0_to_data_Sw, 'BA_Sb':BA_0_to_data_Sb, 'BA_Pl':BA_0_to_data_Pl}, ignore_index=True) 

        if simulation_choice == 'no':
            continue

        '''simulating growth forwards in time starting from the time at which data was taken '''
        t = startTage

        logger.debug('Starting main simulation')
        for SC_Dict in densities [t-1: ]:
            tage_SwF = SC_Dict ['tage_Sw']  
            bhage_SwF = SC_Dict ['bhage_Sw']
            SC_SwF = SC_Dict ['SC_Sw']
            N_bh_SwT = SC_Dict ['N_bh_SwT']
            
            tage_SbF = SC_Dict ['tage_Sb']  
            bhage_SbF = SC_Dict ['bhage_Sb']
            SC_SbF = SC_Dict ['SC_Sb']        
            N_bh_SbT = SC_Dict ['N_bh_SbT']
            
            tage_PlF = SC_Dict ['tage_Pl']  
            bhage_PlF = SC_Dict ['bhage_Pl']
            SC_PlF = SC_Dict ['SC_Pl']
            N_bh_PlT = SC_Dict ['N_bh_PlT']
            '''Ages at time t + 1'''
            logger.debug('Simulating year %d', t)



            if N_bh_SbT>0:
                BA_SbT = BA_SbT + BasalAreaIncrementNonSpatialSb ('Sb', SC_SbF, SI_bh_Sb, N_bh_SbT, N0_Sb, bhage_SbF, BA_SbT)
                if BA_SbT < 0:
                    BA_SbT=0
                #print 'bhageSb ',  bhage_SbF, 'BA Sb ',  BA_SbT
            else:
                BA_SbT = 0
                topHeight_Sb = 0


            if N_bh_SwT>0:
                BA_SwT = BA_SwT + BasalAreaIncrementNonSpatialSw ('Sw', SC_SwF, SI_bh_Sw, N_bh_SwT, N0_Sw, bhage_SwF, SDF_Aw0, SDF_Pl0, SDF_Sb0, BA_SwT)
                if BA_SwT < 0:
                    BA_SwT=0
                #print 'bhageSw ', bhage_SwF, 'BA Sw ', BA_SwT
            else:
                BA_SwT = 0
                topHeight_Sw = 0

            if N_bh_PlT>0:
                BA_PlT = BA_PlT + BasalAreaIncrementNonSpatialPl('Pl', SC_PlF, SI_bh_Pl, N_bh_PlT, N0_Pl, bhage_PlF, SDF_Aw0, SDF_Sw0, SDF_Sb0, BA_PlT)
                if BA_PlT < 0:
                    BA_PlT=0
                #print 'bhagePl ', bhage_PlF, 'BA Pl', BA_PlT
            else:
                BA_PlT = 0
                topHeight_Pl = 0

            
            output_DF_Sw = output_DF_Sw.append({ 'BA_Sw':BA_SwT}, ignore_index=True)
            output_DF_Sb = output_DF_Sb.append({ 'BA_Sb':BA_SbT}, ignore_index=True)
            output_DF_Pl = output_DF_Pl.append({ 'BA_Pl':BA_PlT}, ignore_index=True)

            t += 1
            startTageAwF += 1
            startTageSwF += 1
            startTagePlF += 1
            startTageSbF += 1
            
        densities_DF = pd.DataFrame(densities)
        output_DF = pd.concat([densities_DF, output_DF_Aw, output_DF_Sw, output_DF_Sb, output_DF_Pl ], axis=1)
        
        output_DF ['Gross_Total_Volume_Aw'] = output_DF.apply (lambda x: GrossTotalVolume_Aw (x['BA_Aw'], x['topHeight_Aw']), axis = 1) 
        output_DF ['Gross_Total_Volume_Sw'] = output_DF.apply (lambda x: GrossTotalVolume_Sw (x['BA_Sw'], x['topHeight_Sw']), axis = 1) 
        output_DF ['Gross_Total_Volume_Sb'] = output_DF.apply (lambda x: GrossTotalVolume_Sb (x['BA_Sb'], x['topHeight_Sb']), axis = 1) 
        output_DF ['Gross_Total_Volume_Pl'] = output_DF.apply (lambda x: GrossTotalVolume_Pl (x['BA_Pl'], x['topHeight_Pl']), axis = 1) 
        
        output_DF ['MerchantableVolumeAw'] = output_DF.apply (lambda x: MerchantableVolumeAw (x['N_bh_AwT'], x['BA_Aw'], x['topHeight_Aw'], StumpDOB_Aw, StumpHeight_Aw, TopDib_Aw, x['Gross_Total_Volume_Aw']), axis = 1) 
        output_DF ['MerchantableVolumeSw'] = output_DF.apply (lambda x: MerchantableVolumeSw (x['N_bh_SwT'], x['BA_Sw'], x['topHeight_Sw'], StumpDOB_Sw, StumpHeight_Sw, TopDib_Sw, x['Gross_Total_Volume_Sw']), axis = 1) 
        output_DF ['MerchantableVolumeSb'] = output_DF.apply (lambda x: MerchantableVolumeSb (x['N_bh_SbT'], x['BA_Sb'], x['topHeight_Sb'], StumpDOB_Sb, StumpHeight_Sb, TopDib_Sb, x['Gross_Total_Volume_Sb']), axis = 1) 
        output_DF ['MerchantableVolumePl'] = output_DF.apply (lambda x: MerchantableVolumePl (x['N_bh_PlT'], x['BA_Pl'], x['topHeight_Pl'], StumpDOB_Pl, StumpHeight_Pl, TopDib_Pl, x['Gross_Total_Volume_Pl']), axis = 1)  
        

    return output_DF
