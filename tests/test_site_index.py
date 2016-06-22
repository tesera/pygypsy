import pytest

from gypsy.site_index import (
    get_site_indices_from_dominant_species,
    _get_temporary_dominant_species,
    _estimate_dominant_species_site_index,
    _generate_fplot_dict
    )


def test_get_site_indices_from_dominant_species():
    indices = get_site_indices_from_dominant_species('aw', 1)
    expected = {
        'sb': 5.48,
        'sw': -1.33,
        'pl': 4.25,
        'aw': 1
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


@pytest.mark.skip(reason="TODO!")
def test__estimate_dominant_species_site_index():
    species = 'aa'
    height = 1
    age = 200
    expected = None
    assert _estimate_dominant_species_site_index(species, age, height) == expected


def test__generate_fplot():
    dominant_species = 'Aw'
    dominant_species_site_index = 100
    all_species_site_indices = {
        'sb': 5.48,
        'sw': -1.33,
        'pl': 4.25,
        'aw': 1
    }
    result = _generate_fplot_dict(dominant_species, dominant_species_site_index,
                                  all_species_site_indices)

    site_index_key = 'SI'
    expected_species_keys = ['Aw', 'Pl', 'Sb', 'Sw']
    expected_plot_keys = ['topHeight', 'tage', 'bhage', 'N', 'BA', 'PS', 'StumpDOB',
                          'StumpHeight', 'TopDib', 'SI', 'PCT']

    assert all(
        [species in result.keys() for species in expected_species_keys]
    )

    for species, plot_dict in result.items():
        assert all(
            [key in plot_dict for key in expected_plot_keys]
        )
        if species != dominant_species:
            assert result[species][site_index_key] == \
                all_species_site_indices[species.lower()]
        else:
            assert result[species][site_index_key] == dominant_species_site_index
