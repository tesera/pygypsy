import os
import pandas as pd
import numpy.testing as npt

from pygypsy.data_prep import prep_standtable

from conftest import DATA_DIR


def test_prep_standtable():
    data_file_name = 'raw_standtable.csv'
    plot_data = pd.read_csv(os.path.join(DATA_DIR, data_file_name))
    expected_data_path = os.path.join(
        DATA_DIR, 'output', 'dataprepped_standtable.csv'
    )

    result = prep_standtable(plot_data)
    expected = pd.read_csv(expected_data_path, index_col=0)

    assert isinstance(result, pd.DataFrame)
    assert npt.assert_allclose(
        expected.values, result.values,
        rtol=0.01, atol=0.1,
        equal_nan=True
    ) is None

    # regenerate output files
    # result.to_csv(expected_data_path)

def test_prep_omits_young_plots():
    data_file_name = 'raw_standtable_young.csv'
    plot_data = pd.read_csv(os.path.join(DATA_DIR, data_file_name))
    result = prep_standtable(plot_data)

    assert result.shape[0] == 1

def test_prep_omits_all_plots():
    data_file_name = 'raw_standtable_young.csv'
    plot_data = pd.read_csv(os.path.join(DATA_DIR, data_file_name))
    result = prep_standtable(plot_data, minimum_age=5000)

    assert result.shape[0] == 0
