import os
import pytest
import pandas as pd

from gypsy import DATA_DIR
from gypsy.forward_simulation import simulate_forwards_df
from gypsy.GypsyDataPrep import dataPrepGypsy


#def test_forward_simulation():
#    data_file_name = '1841096_raw.csv'
#    plot_data = pd.read_csv(os.path.join(DATA_DIR, data_file_name))
#
#    fplotSim = dataPrepGypsy(plot_data)[0]
#    inputDF = pd.DataFrame(fplotSim)
#    inputDF = inputDF.transpose()
#    
#    inputDF.to_csv (os.path.join(DATA_DIR, 'output', '1841096.csv' ))
    


    #assert simulate_forwards_df(inputDF, simulation_choice='no')
    #assert simulate_forwards_df(inputDF, simulation_choice='yes')


def test_compare_forward_simulation():
    data_file_name = '508159.csv'
    inputDF = pd.read_csv(os.path.join(DATA_DIR, data_file_name))
    
    result = simulate_forwards_df(inputDF, simulation_choice='no')
    assert type(result) == pd.DataFrame
    result.to_csv (os.path.join(DATA_DIR, 'output', 'comparisons.csv' ))
