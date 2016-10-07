import os
import pytest
import pandas as pd

from gypsy import DATA_DIR
from gypsy.forward_simulation import simulate_forwards_df
from gypsy.GYPSYNonSpatial import save_plot


TEST_FILES = os.listdir(os.path.join(DATA_DIR, 'forward_simulation_files'))
TEST_FILES = [(item) for item in TEST_FILES]
CHART_FILES = os.listdir(os.path.join(DATA_DIR, 'output'))
CHART_FILES = [(item) for item in CHART_FILES]

@pytest.mark.parametrize("test_file", TEST_FILES)
def test_compare_forward_simulation(test_file):
    data_file_name = test_file
    inputDF = pd.read_csv(os.path.join(DATA_DIR, 'forward_simulation_files',
                                       data_file_name))

    plotID = inputDF.loc[0, 'PlotID']
    result = simulate_forwards_df(inputDF, simulation_choice='yes')[plotID]
    assert type(result) == pd.DataFrame

    result.to_csv(os.path.join(DATA_DIR, 'output',
                               'comparisons_{}'.format(test_file)))

@pytest.mark.parametrize("chart_file", CHART_FILES)
def test_plot(chart_file):
    chart_DF = pd.read_csv(os.path.join(DATA_DIR, 'output', chart_file))
    outputfile = os.path.splitext(chart_file)[0] + '.png'
    figure_path = os.path.join(DATA_DIR, 'figures', 'chartGR_{}'.format(outputfile))
    assert save_plot(chart_DF, path=figure_path)
