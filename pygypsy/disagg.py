# -*- coding: utf-8 -*-
"""disaggregation of outpu_df into original species"""

from __future__ import division

import pandas as pd


original_file = pd.read_csv('/Users/juliannosambatti/Documents/Projects/gypsy/10-plots.csv')
simulated_data = pd.read_csv('/Users/juliannosambatti/Documents/Projects/gypsy/2012.csv')


def sp_prop_total(perc_sp):
    total_prop = {'PER_Aw_data':0, 'PER_Pb_data':0, 'PER_Sw_data':0, 'PER_Fb_data':0, 'PER_Fd_data':0, 'PER_Pl_data':0, 'PER_Sb_data':0}
    for sp, prop  in perc_sp:
        if sp == '' or sp == 0:
            break
        elif sp == 'Fd': 
            total_prop['PER_Fd_data'] = prop/100
        elif sp == 'Aw':
            total_prop['PER_Aw_data'] = prop/100
        elif sp == 'Pb':
            total_prop['PER_Pb_data'] = prop/100
        elif sp == 'Sw':
            total_prop['PER_Sw_data'] = prop/100
        elif sp == 'Fb':
            total_prop['PER_Fb_data'] = prop/100
    return  total_prop
            
#per_sp = [('Aw', 0.5), ('Pl', 0.3), ('Sb', 0.2), ('Sw', 0), ('Fb', 0)]    

#def prepare_sp_prop(original_file):
#    sp_prop_df['id_l1'] = original_file['id_l1']
#    return sp_prop_df

def fill_sp_prop (original_file):
    perc_sp = [
                (original_file['SP1'], original_file['PCT1']), (original_file['SP2'], original_file['PCT2']), 
                (original_file['SP3'], original_file['PCT3']), (original_file['SP4'], original_file['PCT4']), 
                (original_file['SP5'], original_file['PCT5'])
               ]
              
#    per_sp = original_file.apply ( [('SP1', 'PCT1'), ('SP2', 'PCT2'), ('SP3', 'PCT3'), ('SP4', 'PCT4'), ('SP5', 'PCT'], axis=1)
    total_prop = sp_prop_total(perc_sp)
    #print total_prop

    for orig_sp, orig_prop in total_prop.items():
        original_file[orig_sp] = orig_prop

    return original_file


def merge_simulated_gypsy_df_with_original_sp_prop_df(simulated_data, original_file):
    original_file_plus = original_file.apply(fill_sp_prop, axis=1)
    original_file_sliced = original_file_plus[['id_l1','PER_Aw_data','PER_Pb_data', 'PER_Sw_data', 
                                          'PER_Fb_data', 'PER_Fd_data']]
    original_file_sliced['prop_Aw_class'] = original_file_sliced.PER_Aw_data + original_file_sliced.PER_Pb_data 
    original_file_sliced['prop_Sw_class'] = original_file_sliced.PER_Sw_data + original_file_sliced.PER_Fb_data + original_file_sliced.PER_Fd_data
    simulated_data_with_sp_original_prop = pd.merge(simulated_data, original_file_sliced, on='id_l1', how='left', sort=False)
    return simulated_data_with_sp_original_prop

def build_disaggregated_simulated_df(simulated_data_with_sp_original_prop):
    df = simulated_data_with_sp_original_prop
    
    df['N_Aw'] = df.N_bh_AwT * df.PER_Aw_data * df.prop_Aw_class
    df['N_Sw'] = df.N_bh_SwT * df.PER_Sw_data * df.prop_Sw_class
    df['N_Fb'] = df.N_bh_SwT * df.PER_Fb_data * df.prop_Sw_class
    df['N_Fd'] = df.N_bh_SwT * df.PER_Fd_data * df.prop_Sw_class
    df['N_Pb'] = df.N_bh_AwT * df.PER_Pb_data * df.prop_Aw_class
    
    df['SC_Aw'] = df.SC_Aw * df.PER_Aw_data * df.prop_Aw_class
    df['SC_Sw'] = df.SC_Sw * df.PER_Sw_data * df.prop_Sw_class
    df['SC_Fb'] = df.SC_Sw * df.PER_Fb_data * df.prop_Sw_class
    df['SC_Fd'] = df.SC_Sw * df.PER_Fd_data * df.prop_Sw_class
    df['SC_Pb'] = df.SC_Aw * df.PER_Pb_data * df.prop_Aw_class
    
    df['bhage_Aw'] = df.bhage_Aw * df.PER_Aw_data * df.prop_Aw_class
    df['bhage_Sw'] = df.bhage_Sw * df.PER_Sw_data * df.prop_Sw_class
    df['bhage_Fb'] = df.bhage_Sw * df.PER_Fb_data * df.prop_Sw_class
    df['bhage_Fd'] = df.bhage_Sw * df.PER_Fd_data * df.prop_Sw_class
    df['bhage_Pb'] = df.bhage_Aw * df.PER_Pb_data * df.prop_Aw_class
    
    df['tage_Aw'] = df.tage_Aw * df.PER_Aw_data * df.prop_Aw_class
    df['tage_Sw'] = df.tage_Sw * df.PER_Sw_data * df.prop_Sw_class
    df['tage_Fb'] = df.tage_Sw * df.PER_Fb_data * df.prop_Sw_class
    df['tage_Fd'] = df.tage_Sw * df.PER_Fd_data * df.prop_Sw_class
    df['tage_Pb'] = df.tage_Aw * df.PER_Pb_data * df.prop_Aw_class
    
    df['topHeight_Aw'] = df.topHeight_Aw * df.PER_Aw_data * df.prop_Aw_class
    df['topHeight_Sw'] = df.topHeight_Sw * df.PER_Sw_data * df.prop_Sw_class
    df['topHeight_Fb'] = df.topHeight_Sw * df.PER_Fb_data * df.prop_Sw_class
    df['topHeight_Fd'] = df.topHeight_Sw * df.PER_Fd_data * df.prop_Sw_class
    df['topHeight_Pb'] = df.topHeight_Aw * df.PER_Pb_data * df.prop_Aw_class
    
    df['BA_Aw'] = df.BA_Aw * df.PER_Aw_data * df.prop_Aw_class
    df['BA_Sw'] = df.BA_Sw * df.PER_Sw_data * df.prop_Sw_class
    df['BA_Fb'] = df.BA_Sw * df.PER_Fb_data * df.prop_Sw_class
    df['BA_Fd'] = df.BA_Sw * df.PER_Fd_data * df.prop_Sw_class
    df['BA_Pb'] = df.BA_Aw * df.PER_Pb_data * df.prop_Aw_class
    
    df['Gross_Total_Volume_Aw'] = df.Gross_Total_Volume_Aw * df.PER_Aw_data * df.prop_Aw_class
    df['Gross_Total_Volume_Sw'] = df.Gross_Total_Volume_Sw * df.PER_Sw_data * df.prop_Sw_class
    df['Gross_Total_Volume_Fb'] = df.Gross_Total_Volume_Sw * df.PER_Fb_data * df.prop_Sw_class
    df['Gross_Total_Volume_Fd'] = df.Gross_Total_Volume_Sw * df.PER_Fd_data * df.prop_Sw_class
    df['Gross_Total_Volume_Pb'] = df.Gross_Total_Volume_Aw * df.PER_Pb_data * df.prop_Aw_class
    
    df['MerchantableVolumeAw'] = df.MerchantableVolumeAw * df.PER_Aw_data * df.prop_Aw_class
    df['MerchantableVolumeSw'] = df.MerchantableVolumeSw * df.PER_Sw_data * df.prop_Sw_class
    df['MerchantableVolumeFb'] = df.MerchantableVolumeSw * df.PER_Fb_data * df.prop_Sw_class
    df['MerchantableVolumeFd'] = df.MerchantableVolumeSw * df.PER_Fd_data * df.prop_Sw_class
    df['MerchantableVolumePb'] = df.MerchantableVolumeAw * df.PER_Pb_data * df.prop_Aw_class
    
    df.reindex_axis(sorted(df.columns), axis=1)
    
    
    return df

#build_disaggregated_simulated_df(simulated_data_with_sp_original_prop)





