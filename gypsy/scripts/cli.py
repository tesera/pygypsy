"""Command Line Interface"""
import os
import json
import click
import logging
import jsonschema
import pandas as pd
from glob import glob

from gypsy.scripts import DEFAULT_CONF_FILE, CONF_SCHEMA_FILE
from gypsy.plot import save_plot
from gypsy.utils import _log_loop_progress
from gypsy.data_prep import prep_standtable
from gypsy.log import setup_logging, CONSOLE_LOGGER_NAME
from gypsy.forward_simulation import simulate_forwards_df


LOGGER = logging.getLogger(CONSOLE_LOGGER_NAME)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def _create_output_path(ctx, param, value): #pylint: disable=unused-argument, missing-docstring
    path = value
    if path is None:
        path = ctx.params.get('standtable')
        basename = os.path.splitext(path)[0]
        new_name = basename + '_prepped.csv'
        return new_name


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', '-v', is_flag=True)
@click.option('--config-file', '-c', type=click.File(encoding='utf8'),
              default=DEFAULT_CONF_FILE)
@click.pass_context
def cli(ctx, verbose, config_file):
    """Growth and Yield Projection System

    Note: 'prep' subcommand must be run before 'simulate'

    """
    setup_logging()

    if verbose:
        LOGGER.setLevel(logging.DEBUG)
        for handler in LOGGER.handlers:
            handler.setLevel(logging.DEBUG)

    LOGGER.debug('Starting gypsy')
    LOGGER.debug('Using config file: %s', config_file)

    # TODO: have a handler callback for this parameter
    # instead of putting this logic here. then we can also
    # use bada parameter exception
    with open(CONF_SCHEMA_FILE) as f:
        schema = json.load(f)
    try:
        conf = json.load(config_file)
        jsonschema.validate(conf, schema)
    except Exception as err:
        LOGGER.error((
            'There was an error reading the config file. '
            'See the log file for more details.'
        ))
        LOGGER.debug(err)
        raise click.Abort()

    ctx.obj = {'config': conf}
    ctx.params['config_file'] = config_file

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('standtable', type=click.Path(exists=True))
@click.option('--stand-id', '-n', multiple=True, type=int)
@click.option('--id-field', '-i', type=str)
@click.option('--output-path', '-o', type=click.Path(),
              callback=_create_output_path)
@click.pass_context
def prep(ctx, standtable, stand_id, id_field, output_path):
    """Prepare stand data for use in GYPSY simulation"""
    LOGGER.info('Running prep...')
    standtable_df = pd.read_csv(standtable)

    # TODO: filter id by stand id

    prepped_data = prep_standtable(standtable_df)
    prepped_data.to_csv(output_path)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('data', type=click.Path(exists=True))
@click.option('--output-fields', '-f', multiple=True, type=str)
@click.option('--stand-id', '-n', multiple=True, type=int)
@click.option('--output-timestep', '-t', type=int)
@click.option('--id-field', '-i', type=str)
@click.option('--generate-plots', '-p', is_flag=True)
@click.option('--write-id', '-w', is_flag=True)
@click.option('--output-dir', '-o', type=click.Path(exists=False),
              default='./gypsy-output')
@click.option('--output-filename', type=str, default='gypsy-projection.csv')
@click.pass_context
def simulate(ctx, data, stand_id, generate_plots, output_fields,
             output_timestep, id_field, write_id, output_dir,
             output_filename):
    """Run GYPSY simulation

    """
    if os.path.exists(output_dir):
        raise click.UsageError('output_dir: %s must not exist!' % output_dir)

    standtable = pd.read_csv(data)

    # TODO: filter stand data to ages > 25
    min_age = 25

    old_query_str = 'tage_Sw > {a} or tage_Sb > {a} or tage_Pl > {a} or tage_Aw > {a}' .format(a=min_age)
    old_ids = standtable.query(old_query_str).index
    standtable_old = standtable[standtable.index.isin(old_ids)]
    standtable_young = standtable[~standtable.index.isin(old_ids)]

    # TODO: validate that its had dataprep filter id by stand id

    LOGGER.info('Running simulation...')
    result = simulate_forwards_df(standtable_old)

    # TODO: subset to timestep add id column to data and fix output path

    LOGGER.info('Saving output data')
    os.makedirs(output_dir)
    for plot_id, df in result.items():
        filename = '%s.csv' % plot_id
        output_path = os.path.join(output_dir, filename)
        df.to_csv(output_path)

    standtable_young_path = os.path.join(output_dir, 'skipped_plots.csv')
    standtable_young.to_csv(standtable_young_path, columns=['PlotID'])

    # TODO: plot must have onlu plot ID

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('simulation-output-dir', type=click.Path(exists=True))
def plot(simulation_output_dir):
    """Create charts for all files in gypsy simulation output directory

    """
    chart_files = glob(os.path.join(simulation_output_dir, '*.csv'))
    LOGGER.info('Plotting all csv files at %s...', simulation_output_dir)

    for i, chart_file in enumerate(chart_files):
        _log_loop_progress(i, len(chart_files))
        chart_df = pd.read_csv(chart_file)
        output_filename = os.path.splitext(os.path.split(chart_file)[-1])[0] + '.png'
        figure_path = os.path.join(simulation_output_dir, 'figures', output_filename)

        save_plot(chart_df, path=figure_path)
