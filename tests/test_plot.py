import os
import pytest
import pandas as pd
from glob import glob

from gypsy import DATA_DIR
from gypsy.plot import save_plot


CHART_FILES = glob(os.path.join(DATA_DIR, 'output', 'comparisons*.csv'))
CHART_FILES = [(item) for item in CHART_FILES]


@pytest.mark.parametrize("chart_file", CHART_FILES)
def test_plot(chart_file):
    chart_df = pd.read_csv(chart_file)
    outputfile = os.path.splitext(chart_file)[0] + '.png'
    figure_path = os.path.join(
        DATA_DIR, 'figures', 'chartGR_{}'.format(os.path.basename(outputfile))
    )
    assert save_plot(chart_df, path=figure_path)
