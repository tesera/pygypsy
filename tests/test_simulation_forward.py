import os
import pytest
import pandas as pd
from glob import glob
import numpy as np

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

    plot_id = str(int(input_df.loc[0, 'id_l1']))

    result = simulate_forwards_df(input_df)[plot_id]
    expected = pd.read_csv(expected_data_path, index_col=0)

    assert isinstance(result, pd.DataFrame)
    np.testing.assert_allclose(
        expected.values, result.values,
        rtol=0.01, atol=0.1,
        equal_nan=True
    )

    # regenerate output files
    # result.to_csv(expected_data_path)

def test_simulate_densities_speciescomp_topheight_duration():
    kwargs = {
        'SDF_Aw0': 160.4249489,
        'SDF_Pl0': 2224.0681509299998,
        'SDF_Sb0': 0.0,
        'SDF_Sw0': 417.084487712,
        'SI_bh_Aw': 5.1790722387499999,
        'SI_bh_Pl': 7.7958239311399993,
        'SI_bh_Sb': 7.7493273159300005,
        'SI_bh_Sw': 6.5731557601199997,
        'startTage': 56,
        'startTageAw': 56.351482955500003,
        'startTagePl': 37.0,
        'startTageSb': 0.0,
        'startTageSw': 44.545032732899998,
        'y2bh_Aw': 12.365087300999999,
        'y2bh_Pl': 12.2784422109,
        'y2bh_Sb': 0.0,
        'y2bh_Sw': 15.174260170999998
    }

    result = simulate_densities_speciescomp_topheight(years=5, **kwargs)
    assert len(result) == 5
    # TODO: reconcile this duration, and time-zero, time of data with basal area simulation
