import os
import pytest
import pandas as pd

from gypsy import DATA_DIR
from gypsy.forward_simulation import simulate_forwards_df
from gypsy.data_prep import prep_standtable


__TEST_FILE_PATH__ = os.path.join(DATA_DIR, 'private/large_standtable.csv')

@pytest.mark.skip(reason='Very slow, run manually')
@pytest.mark.skipif(not os.path.exists(__TEST_FILE_PATH__),
                    reason="--db was not specified")
def test_forward_simulation():
    input_df = pd.read_csv(__TEST_FILE_PATH__)

    plot_id = str(int(input_df.loc[0, 'PlotID']))
    prepped = prep_standtable(input_df)
    result = simulate_forwards_df(prepped, simulation_choice='yes')[plot_id]

    assert isinstance(result, pd.DataFrame)
