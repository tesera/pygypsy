# -*- coding: utf-8 -*-
"""disaggregation of outpu_df into original species"""

from __future__ import division

import pandas as pd


original_file = pd.read_csv('/Users/juliannosambatti/Documents/Projects/gypsy/10-plots.csv')
prepped_data = pd.read_csv('/Users/juliannosambatti/Documents/Projects/gypsy/2012.csv')


def sp_prop_total(perc_sp):
    total_prop = {'PER_Aw_data':0, 'PER_Pb_data':0, 'PER_Sw_data':0, 'PER_Fb_data':0, 'PER_Fd_data':0, 'PER_Pl_data':0, 'PER_Sb_data':0}
    for sp, prop  in perc_sp:
        if sp == '' or sp == 0:
            break
        elif sp == 'Fd': 
            total_prop['PER_Fd_data'] = prop
        elif sp == 'Sb':
            total_prop['PER_Sb_data'] = prop
        elif sp == 'Aw':
            total_prop['PER_Aw_data'] = prop
        elif sp == 'Pb':
            total_prop['PER_Pb_data'] = prop
        elif sp == 'Sw':
            total_prop['PER_Sw_data'] = prop
        elif sp == 'Fb':
            total_prop['PER_Fb_data'] = prop
        elif sp == 'Pl':
            total_prop['PER_Pl_data'] = prop
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

original_file_plus = original_file.apply(fill_sp_prop, axis=1)
original_file_sliced = original_file_plus[['id_l1','PER_Aw_data','PER_Pb_data', 'PER_Sw_data', 
                                          'PER_Fb_data', 'PER_Fd_data', 'PER_Pl_data', 'PER_Sb_data']]

