import os
import pytest
import pandas as pd
from glob import glob
import numpy as np

from gypsy import DATA_DIR
from gypsy.forward_simulation import simulate_forwards_df


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

    plot_id = str(int(input_df.loc[0, 'PlotID']))

    result = simulate_forwards_df(input_df, simulation_choice='yes')[plot_id]
    expected = pd.read_csv(expected_data_path, index_col=0)

    assert isinstance(result, pd.DataFrame)
    assert np.allclose(
        expected.values.astype(np.float64), result.values.astype(np.float64),
        equal_nan=True
    )

    # regenerate output files
    # result.to_csv(expected_data_path)
