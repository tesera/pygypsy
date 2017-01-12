from pygypsy.basal_area_factor import estimate_basal_area_factor_sw

def test_increment_basal_area_factor_sw():
    bhages = [-26.629227438100003 + i for i in xrange(249)]

    new_params = {
        'BA_Sw0': 0.001,
        'N0_Sw': 423.23699170300006,
        'startTage': 56,
        'BA_SwT': 2.2156105400000001,
        'SDF_Aw0': 160.4249489,
        'SDF_Pl0': 2224.0681509299998,
        'SDF_Sb0': 0.0,
        'SI_bh_Sw': 6.5731557601199997,
        'SC_Sw': 0.1052773581823121,
        'densities': [{'bhage_Sw': i} for i in bhages],
        'N_bh_SwT': 418.18239203000002,
    }

    expected = 1.1352489115533175

    result = estimate_basal_area_factor_sw(**new_params)

    assert result == expected
