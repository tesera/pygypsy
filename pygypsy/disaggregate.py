# -*- coding: utf-8 -*-
"""disaggregation of outpu_df into original species"""

from __future__ import division

import pandas as pd


def sp_prop_total(perc_sp):
    '''This creates a dictionary of original species proportions
        :param perc_sp: is tuple with sp name and its proportions

    '''

    total_prop = {'PER_Aw_data':0, 'PER_Pb_data':0,
                  'PER_Sw_data':0, 'PER_Fb_data':0, 'PER_Fd_data':0}
    for sp, prop in perc_sp:
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
    return total_prop

def fill_sp_prop(plot_data):
    '''
    retrieving species original proportions

    This prepares a tuple with sp names and percentages
    and adds columns with its original proportions to the
    original data
    :param plot_data: is the original data plus the new columns including
                sp names and their original proportions
    '''
    perc_sp = [
        (plot_data['SP1'], plot_data['PCT1']),
        (plot_data['SP2'], plot_data['PCT2']),
        (plot_data['SP3'], plot_data['PCT3']),
        (plot_data['SP4'], plot_data['PCT4']),
        (plot_data['SP5'], plot_data['PCT5'])
    ]

    total_prop = sp_prop_total(perc_sp)

    for orig_sp, orig_prop in total_prop.items():
        plot_data[orig_sp] = orig_prop
    return plot_data


def merge_simulated_with_original_sp_prop(simulated_data, plot_data):
    '''
    Merge simulation and plot data

    This applies fill_sp_prop function to the entire simulation data
    :param simulated_data: simulation results table
    :param plot_data: original data including retrieve sp proportions
    '''
    plot_data = plot_data.apply(fill_sp_prop, axis=1)
    selection = ['id_l1', 'PER_Aw_data', 'PER_Pb_data', 'PER_Sw_data',
                 'PER_Fb_data', 'PER_Fd_data']
    plot_data_sliced = plot_data.loc[:, selection]
    plot_data_sliced['prop_Aw_class'] = plot_data_sliced.PER_Aw_data + plot_data_sliced.PER_Pb_data
    plot_data_sliced['prop_Sw_class'] = plot_data_sliced.PER_Sw_data \
        + plot_data_sliced.PER_Fb_data + plot_data_sliced.PER_Fd_data
    simulated_data_with_sp_original_prop = pd.merge(
        simulated_data, plot_data_sliced, on='id_l1', how='left', sort=False)
    return simulated_data_with_sp_original_prop


def disaggregate_simulation(simulated_data, plot_data):
    '''
    disagregation function
    This multiplies variables by its respective original proportions

    :param simulated_data: simulation results table
    :param plot_data: original data including retrieve sp proportions
    '''

    df = merge_simulated_with_original_sp_prop(simulated_data, plot_data)

    species = [('Aw', 'Aw'), ('Aw', 'Pb'), ('Sw', 'Fb'), ('Sw', 'Fd'), ('Sw', 'Sw')]
    variables = ['SC', 'bhage', 'tage', 'topHeight', 'BA',
                 'Gross_Total_Volume', 'Merchantable_Volume']

    for gypsy_s, data_s in species:
        df['N_bh_%sT' % (data_s)] = df['N_bh_%sT' % gypsy_s] \
            * df['PER_%s_data' % data_s] / df['prop_%s_class' %gypsy_s]
        for var in variables:
            df['%s_%s' %(var, data_s)] = df['%s_%s' % (var, gypsy_s)] \
                * df['PER_%s_data' % data_s] / df['prop_%s_class' %gypsy_s]
    df = df.reindex_axis(sorted(df.columns), axis=1)
    df.fillna(value=0, inplace=True)

    return df
