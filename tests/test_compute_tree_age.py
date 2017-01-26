#pylint: disable=missing-docstring,invalid-name

import pytest
import numpy.testing as npt

from pygypsy.asaCompileAgeGivenSpSiHt import computeTreeAge


@pytest.mark.parametrize("kwargs,expected", [
    ({'siSp': 'Aw', 'treeHt': 20, 'treeSi': 15}, 82.544),
    ({'siSp': 'Pl', 'treeHt': 25, 'treeSi': 15}, 153.295),
    ({'siSp': 'Sw', 'treeHt': 25, 'treeSi': 15}, 102.186),
    ({'siSp': 'Sb', 'treeHt': 25, 'treeSi': 15}, 136.171)
])
def test_compute_tree_age(kwargs, expected):
    npt.assert_almost_equal(
        computeTreeAge(**kwargs),
        expected,
        decimal=3
    )

@pytest.mark.parametrize("kwargs,expected", [
    ({'siSp': 'Pl', 'treeHt': 25, 'treeSi': 10}, 250),
    ({'siSp': 'Aw', 'treeHt': 25, 'treeSi': 1}, 200),
    ({'siSp': 'Sb', 'treeHt': 25, 'treeSi': 1}, 450),
    ({'siSp': 'Sw', 'treeHt': 25, 'treeSi': 1}, 450)
])
def test_compute_nonconvergent_tree_age(kwargs, expected):
    npt.assert_almost_equal(
        computeTreeAge(**kwargs),
        expected,
        decimal=3
    )
