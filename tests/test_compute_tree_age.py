#pylint: disable=missing-docstring

from pygypsy.asaCompileAgeGivenSpSiHt import computeTreeAge

def test_compute_tree_age():
    assert computeTreeAge(siSp='Aw', treeHt=20, treeSi=15, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 82.544655456378891
    assert computeTreeAge(siSp='Pl', treeHt=25, treeSi=15, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 153.29542915884193
    assert computeTreeAge(siSp='Sw', treeHt=25, treeSi=15, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 102.1856914602515
    assert computeTreeAge(siSp='Sb', treeHt=25, treeSi=15, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 136.17108952176432


def test_compute_nonconvergent_tree_age():
    assert computeTreeAge(siSp='Pl', treeHt=25, treeSi=10, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 250
    assert computeTreeAge(siSp='Aw', treeHt=25, treeSi=1, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 200
    assert computeTreeAge(siSp='Sb', treeHt=25, treeSi=1, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 450
    assert computeTreeAge(siSp='Sw', treeHt=25, treeSi=1, maxTreeAge=450,
                          rowIndex=0, printWarnings=True) == 450
