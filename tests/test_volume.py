# TODO: test merchantable volume with 0 and negative values

from pygypsy.volume import (
    gross_total_volume as gtv,
    merchantable_volume as mv,
)


def test_gross_total_volume():
    assert gtv('Aw', 10, 10) == 36.768662679281313
    assert gtv('Sw', 10, 10) == 36.98733892882017
    assert gtv('Sb', 10, 10) == 38.058477267092755
    assert gtv('Pl', 10, 10) == 44.190847304747535

    assert gtv('Aw', 0, 10) == 0
    assert gtv('Sw', 0, 10) == 0
    assert gtv('Sb', 0, 10) == 0
    assert gtv('Pl', 0, 10) == 0

    assert gtv('Aw', 10, 0) == 0
    assert gtv('Sw', 10, 0) == 0
    assert gtv('Sb', 10, 0) == 0
    assert gtv('Pl', 10, 0) == 0

def test_merchantable_volume():
    tot_vol = 40
    assert mv('Aw', 1000, 100, 8, tot_vol) == 22.426383085353788
    assert mv('Sw', 1000, 100, 8, tot_vol) == 32.589572112087865
    assert mv('Pl', 1000, 100, 8, tot_vol) == 38.574281306299596
    assert mv('Sb', 1000, 100, 8, tot_vol) == 37.11263901030228
