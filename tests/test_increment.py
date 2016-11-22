# TODO: 0 as an input
# TODO: negative as an input
from gypsy import basal_area_increment as incr

def test_increment_basal_area_aw():
    args = []
    expected = 0.010980296350305301

    params = [
        ('sp', ['Aw']),
        ('SI_bh', 7.3878921344490012),
        ('bhage', 32.32),
        ('N_bh', 817.46),
        ('SC', .25),
        ('BA', 7.20),
        ('N0', 964.41),
    ]
    for i in params:
        args.append(i[1])

    result = incr.increment_basal_area_aw(*args)
    assert result == expected


def test_increment_basal_area_sb():
    args = []
    expected = 0.0040928537767126495

    params = [
        ('sp', ['Sb']),
        ('SI_bh', 7.3878921344490012),
        ('bhage', 32.32),
        ('N_bh', 817.46),
        ('SC', .25),
        ('BA', 7.20),
        ('N0', 964.41),
    ]
    for i in params:
        args.append(i[1])

    result = incr.increment_basal_area_sb(*args)
    assert result == expected


def test_increment_basal_area_pl():
    args = []
    expected = 0.17167634370570872

    params = [
        ('sp', ['Pl']),
        ('SC', .5),
        ('SI_bh', 7.3878921344490012),
        ('N_bh', 817.46),
        ('N0_bh', 400.46),
        ('bhage', 32.32),
        ('SDF_Aw0', 10),
        ('SDF_Sw0', 10),
        ('SDF_Sb0', 10),
        ('BA', 7.20),
    ]
    for i in params:
        args.append(i[1])

    result = incr.increment_basal_area_pl(*args)
    assert result == expected


def test_increment_basal_area_sw():
    args = []
    expected = 0.21723711770142046

    params = [
        ('sp', ['Sw']),
        ('SC', .5),
        ('SI_bh', 7.3878921344490012),
        ('N_bh', 817.46),
        ('N0_bh', 400.46),
        ('bhage', 32.32),
        ('SDF_Aw0', 10),
        ('SDF_Pl0', 10),
        ('SDF_Sb0', 10),
        ('BA', 7.20),
    ]
    for i in params:
        args.append(i[1])

    result = incr.increment_basal_area_sw(*args)
    assert result == expected
