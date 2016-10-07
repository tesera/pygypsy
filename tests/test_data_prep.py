import os
import pytest
import pandas as pd
import numpy.testing as npt

from gypsy import DATA_DIR
from gypsy.GypsyDataPrep import dataPrepGypsy


def test_forward_simulation():
    data_file_name = 'raw_standtable.csv'
    plot_data_path = pd.read_csv(os.path.join(DATA_DIR, data_file_name))
    expected_data_path = os.path.join(DATA_DIR, 'output', 'dataprepped_standtable.csv')

    result = dataPrepGypsy(plot_data_path)[0]
    expected = pd.read_csv(expected_data_path, index_col=0)

    assert isinstance(result, pd.DataFrame)
    assert npt.assert_almost_equal(expected.values, result.values, decimal=3) is None
    # this numpy function returns None if assertion passes
