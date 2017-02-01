#pylint: disable=missing-docstring, no-member, invalid-name
import os
import pytest
from glob import glob

import numpy as np
import pandas as pd

from pygypsy.forward_simulation import (
    simulate_forwards_df,
    simulate_densities_speciescomp_topheight
)

from conftest import DATA_DIR


TEST_FILES = glob(os.path.join(DATA_DIR, 'forward_simulation_files', '*.csv'))
TEST_FILES = [(item) for item in TEST_FILES]
CHART_FILES = glob(os.path.join(DATA_DIR, 'output', 'comparisons*.csv'))
CHART_FILES = [(item) for item in CHART_FILES]


@pytest.mark.parametrize("test_file", TEST_FILES)
def test_compare_forward_simulation(test_file):
    input_df = pd.read_csv(test_file)
    expected_data_path = os.path.join(
        DATA_DIR, 'output',
        'comparisons_{}'.format(os.path.basename(test_file))
    )

    result = simulate_forwards_df(input_df, backwards=True, n_years=250)
    expected = pd.read_csv(expected_data_path, index_col=[0,1])

    assert isinstance(result, pd.DataFrame)
    assert result.shape[0]==250
    np.testing.assert_allclose(
        expected.values, result.values,
        rtol=0.01, atol=0.1,
        equal_nan=True
    )

    #regenerate output files
#    result.to_csv(expected_data_path)

def test_forward_simulation_duration_without_backwards():
    input_data_path = os.path.join(DATA_DIR, 'forward_simulation_files',
                                   '1049300.csv')
    input_df = pd.read_csv(input_data_path)
    result = simulate_forwards_df(input_df, backwards=False, n_years=5)

    assert result.shape[0] == 5

# this can be cleaned up if the tree height, density, and species comp were
# self sufficient (i.e. behaved OK) with a density of 0
def test_simulate_densities_speciescomp_topheight_duration():
    kwargs = {
        'SDF_Aw0': 160.4249489, 'SDF_Pl0': 2224.0681509299998,
        'SDF_Sb0': 0.0, 'SDF_Sw0': 417.084487712,
        'SI_bh_Aw': 5.1790722387499999,
        'SI_bh_Pl': 7.7958239311399993,
        'SI_bh_Sb': 7.7493273159300005,
        'SI_bh_Sw': 6.5731557601199997,
        'startTage': 56, 'startTageAw': 56.351482955500003,
        'startTagePl': 37.0, 'startTageSb': 0.0,
        'startTageSw': 44.545032732899998,
        'y2bh_Aw': 12.365087300999999, 'y2bh_Pl': 12.2784422109,
        'y2bh_Sb': 0.0, 'y2bh_Sw': 15.174260170999998
    }

    expected = {
        'N_bh_AwT': 160.57212836196911, 'N_bh_PlT': 2508.6942590269987,
        'N_bh_SbT': 0, 'N_bh_SwT': 417.38593678448535,
        'SC_Aw': 0.052021449615310099, 'SC_Pl': 0.81275569631859312,
        'SC_Sb': 0.0, 'SC_Sw': 0.1352228540660968,
        'bhage_Aw': 47.9863956545, 'bhage_Pl': 28.7215577891,
        'bhage_Sb': 4.0, 'bhage_Sw': 33.3707725619,
        'tage_Aw': 60.3514829555, 'tage_Pl': 41.0,
        'tage_Sb': 4.0, 'tage_Sw': 48.5450327329,
        'topHeight_Aw': 6.0839968002432867,
        'topHeight_Pl': 6.4075470318185364,
        'topHeight_Sb': 0, 'topHeight_Sw': 6.352684564592578
    }

    expected2 = {
        'N_bh_AwT': 0, 'N_bh_PlT': 0, 'N_bh_SbT': 0, 'N_bh_SwT': 0,
        'SC_Aw': 0, 'SC_Pl': 0, 'SC_Sb': 0, 'SC_Sw': 0,
        'bhage_Aw': -8.013604345499996, 'bhage_Pl': -27.2784422109,
        'bhage_Sb': -52.0, 'bhage_Sw': -22.629227438100003,
        'tage_Aw': 4.351482955500003, 'tage_Pl': -15.0,
        'tage_Sb': -52.0, 'tage_Sw': -7.4549672671000025,
        'topHeight_Aw': 0, 'topHeight_Pl': 0,
        'topHeight_Sb': 0, 'topHeight_Sw': 0
    }

    result = simulate_densities_speciescomp_topheight(n_years=5,
                                                      start_at_data_year=True,
                                                      **kwargs)
    result2 = simulate_densities_speciescomp_topheight(n_years=5,
                                                       start_at_data_year=False,
                                                       **kwargs)

    assert len(result) == 5
    assert len(result2) == 5
    assert result[4] == expected
    assert result2[4] == expected2

def test_year_index():
    input_data_path = os.path.join(DATA_DIR, 'forward_simulation_files',
                                   '1049300.csv')
    input_df = pd.read_csv(input_data_path)
    result = simulate_forwards_df(input_df, backwards=False, n_years=4,
                                  year_of_data_acquisition=2000)

    assert result.index.values[-1][1] == 2004
