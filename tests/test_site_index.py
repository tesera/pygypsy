import pytest

from pygypsy.site_index import (
    get_site_indices_from_dominant_species,
    _get_temporary_dominant_species,
    _estimate_site_index,
    )


def test_get_site_indices_from_dominant_species():
    indices = get_site_indices_from_dominant_species('aw', 1)
    expected = {
        'Sb': 5.48,
        'Sw': -1.33,
        'Pl': 4.25,
        'Aw': 1
    }

    assert indices == expected


def test_get_site_indices_from_dominant_species_raises():
    with pytest.raises(ValueError) as err:
        get_site_indices_from_dominant_species('nosuchspecies', 1)

    assert str(err.value) == ('No function is available to calculate '
                              'site index from species nosuchspecies')


def test__get_temporary_dominant_species():
    assert _get_temporary_dominant_species('Pb') == 'Aw'
    assert _get_temporary_dominant_species('Fd') == 'Sw'
    assert _get_temporary_dominant_species('Fb') == 'Sw'


def test_estimate_site_index():
    assert _estimate_site_index('Aw', 10, 10) == 27.089299487182057
    assert _estimate_site_index('Sb', 10, 10) == 37.472425731733637
    assert _estimate_site_index('Aw', 100, 10) == 5.7588933884113027
    assert _estimate_site_index('Aw', 10, 100) == 107.39828771776254


def test_estimate_site_index_with_invalid_species():
    with pytest.raises(UnboundLocalError) as err:
        _estimate_site_index('aa', 10, 100)

    assert '\'SI_t\' referenced before assignment' in err.value.message
