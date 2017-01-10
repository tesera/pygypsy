from pygypsy.utils import (
    _generate_fplot_dict,
    _get_gypsy_valid_species,
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
