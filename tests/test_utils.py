from pygypsy.utils import (
    _generate_fplot_dict,
    _get_gypsy_valid_species,
    _reclassify_and_sort_species
    )


def test_get_gypsy_valid_species():
    assert _get_gypsy_valid_species('Pb') == 'Aw'
    assert _get_gypsy_valid_species('Fd') == 'Sw'
    assert _get_gypsy_valid_species('Fb') == 'Sw'


def test_generate_fplot():
    result = _generate_fplot_dict()

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

def test_reclassify_and_sort_species():
    args = [('Pl', 24), ('Sw', 10), ('Pb', 6), ('Aw', 60)]
    result = _reclassify_and_sort_species(args)
    assert result[0] == [('Aw', 66), ('Pl', 24), ('Sw', 10), ('Sb', 0)]
    assert result[1] == {'Sb': 0, 'Sw': 10, 'Pl': 24, 'Aw': 66}
