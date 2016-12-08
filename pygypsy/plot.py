"""Plotting Convenience Functions"""
import os
import matplotlib.pyplot as plt

from utils import _mkdir_p


def _plot_simulation_variables(simulation_df, axis=None, plot_vars=None, y_lab=''):
    """
    :param simulation_df: output of pygypsy simulation
    :param axis: axes object
    :param plot_vars: list of strings identifying variable (column names) to plot
    :param y_lab: y axis label
    """

    if plot_vars is None:
        raise ValueError('Variable to plot must be specified')

    simulation_vars = simulation_df.loc[:, plot_vars]
    simulation_vars.plot(ax=axis)
    axis.set_xlabel('Year', fontsize=10)
    axis.set_ylabel(y_lab, fontsize=10)
    axis.legend(loc=2, prop={'size':6})
    axis.tick_params(axis='both', which='major', labelsize=8)

def _plot_basal_area(simulation_dataframe, axis=None): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['BA_Aw', 'BA_Sw', 'BA_Sb', 'BA_Pl'],
                               y_lab='BA (m2)')

def _plot_merch_volume(simulation_dataframe, axis): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['MerchantableVolumeAw', 'MerchantableVolumeSw',
                                          'MerchantableVolumeSb', 'MerchantableVolumePl'],
                               y_lab='Merc. Vo. (m3)')

def _plot_merch_volume_conif_decid(simulation_dataframe, axis): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['MerchantableVolume_Con',
                                          'MerchantableVolume_Dec',
                                          'MerchantableVolume_Tot'],
                               y_lab='Merc. Vo. (m3)')

def _plot_top_height(simulation_dataframe, axis=None): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['topHeight_Aw', 'topHeight_Sw',
                                          'topHeight_Sb', 'topHeight_Pl'],
                               y_lab='Top Height (m)')


def _plot_gross_total_volume(simulation_dataframe, axis): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['Gross_Total_Volume_Aw', 'Gross_Total_Volume_Sw',
                                          'Gross_Total_Volume_Sb', 'Gross_Total_Volume_Pl'],
                               y_lab='Gr. Tot. Vol. (m3)')

def _plot_gross_total_volume_conif_decid(simulation_dataframe, axis): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['Gross_Total_Volume_Con',
                                          'Gross_Total_Volume_Dec',
                                          'Gross_Total_Volume_Tot'],
                               y_lab='Gr. Tot. Vol. (m3)')


def _plot_species_composition(simulation_dataframe, axis): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['SC_Aw', 'SC_Sw', 'SC_Sb', 'SC_Pl'],
                               y_lab='Sp. Comp.')

def _plot_density(simulation_dataframe, axis): #pylint: disable=missing-docstring
    _plot_simulation_variables(simulation_dataframe, axis=axis,
                               plot_vars=['N_bh_AwT', 'N_bh_SwT', 'N_bh_SbT', 'N_bh_PlT'],
                               y_lab='Density')

def save_plot(simulation_dataframe, path):
    '''Save plots of pygypsy simulation output

    Creates a panel and includes all plots generated as pygypsy outputs
    (simulation_dataframe) and saves the panel on a folder determined byt path

    '''
    _mkdir_p(os.path.dirname(path))
    fig = plt.figure(1)
    sub1 = fig.add_subplot(321)
    sub2 = fig.add_subplot(322)
    sub3 = fig.add_subplot(323)
    sub4 = fig.add_subplot(324)
    sub5 = fig.add_subplot(325)
    sub6 = fig.add_subplot(326)

    _plot_basal_area(simulation_dataframe, axis=sub1)
    _plot_merch_volume_conif_decid(simulation_dataframe, axis=sub2)
    _plot_top_height(simulation_dataframe, axis=sub3)
    _plot_gross_total_volume_conif_decid(simulation_dataframe, axis=sub4)
    _plot_species_composition(simulation_dataframe, axis=sub5)
    _plot_density(simulation_dataframe, axis=sub6)

    plt.tight_layout()
    plt.savefig(path) #TODO: specify page size here to reduce legend size
    plt.close()

    return True
