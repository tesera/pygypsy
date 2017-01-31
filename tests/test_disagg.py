#pylint: disable=missing-docstring, no-member
import os
import pandas as pd
import numpy as np

from pygypsy.disaggregate import (
    sp_prop_total,
    disaggregate_simulation
    )
from conftest import DATA_DIR



def test_sp_prop_total():
    perc_sp = [
        ('Aw', 50), ('Sw', 30),
        ('Pb', 20), ('', 0),
        ('', 0)
    ]

    assert sp_prop_total(perc_sp) == {'PER_Aw_data':0.5,
                                      'PER_Pb_data':0.2, 'PER_Sw_data':0.3,
                                      'PER_Fb_data':0, 'PER_Fd_data':0}



def test_disaggregate_simulation():
    plot_data_path = os.path.join(DATA_DIR, 'test_disag_plot.csv')
    simulation_data_path = os.path.join(DATA_DIR, 'test_disagg_simulation.csv')
    input_df = pd.read_csv(plot_data_path)
    simulation_df = pd.read_csv(simulation_data_path)
    expected_data_path = os.path.join(
        DATA_DIR, 'output',
        'test_disag_results.csv'
    )

    result = disaggregate_simulation(simulation_df, input_df)
    expected = pd.read_csv(expected_data_path, index_col=0)

    np.testing.assert_allclose(
        expected.values, result.values,
        rtol=0.01, atol=0.1,
        equal_nan=True)

    #regenerate output files
    #result.to_csv(expected_data_path)
