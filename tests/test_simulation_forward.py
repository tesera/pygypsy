import os
import pytest
import pandas as pd
from glob import glob
import numpy.testing as npt

from gypsy import DATA_DIR
from gypsy.forward_simulation import simulate_forwards_df
from gypsy.GYPSYNonSpatial import save_plot


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

    plotID = str(int(input_df.loc[0, 'PlotID']))

    result = simulate_forwards_df(input_df, simulation_choice='yes')[plotID]
    expected = pd.read_csv(expected_data_path, index_col=0)

    assert type(result) == pd.DataFrame
    assert npt.assert_almost_equal(
        expected.values, result.values, decimal=3
    ) is None

    # regenerate output files
    # result.to_csv(expected_data_path)

@pytest.mark.parametrize("chart_file", CHART_FILES)
def test_plot(chart_file):
    chart_df = pd.read_csv(chart_file)
    outputfile = os.path.splitext(chart_file)[0] + '.png'
    figure_path = os.path.join(
        DATA_DIR, 'figures', 'chartGR_{}'.format(os.path.basename(outputfile))
    )
    assert save_plot(chart_df, path=figure_path)
