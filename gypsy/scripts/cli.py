"""Command Line Interface"""
import os
import logging
from glob import glob

import boto3
import click
import pandas as pd

from gypsy.scripts import DEFAULT_CONF_FILE
from gypsy.scripts.callbacks import _load_and_validate_config
from gypsy.plot import save_plot
from gypsy.utils import (
    _log_loop_progress,
    _filter_young_stands,
    _append_file,
    _parse_s3_url,
    _copy_file,
)
from gypsy.data_prep import prep_standtable
from gypsy.log import setup_logging, CONSOLE_LOGGER_NAME
from gypsy.forward_simulation import simulate_forwards_df
import gypsy.path as gyppath


LOGGER = logging.getLogger(CONSOLE_LOGGER_NAME)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
LOG_FILE_NAME = 'gypsy.log'


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', '-v', is_flag=True)
@click.option('--output-dir', '-o', type=click.Path(exists=False),
              default='gypsy-output')
@click.pass_context
def cli(ctx, verbose, output_dir):
    """Growth and Yield Projection System

    Note: 'prep' subcommand must be run before 'simulate'

    """
    setup_logging()
    if verbose:
        LOGGER.setLevel(logging.DEBUG)
        for handler in LOGGER.handlers:
            handler.setLevel(logging.DEBUG)
    LOGGER.debug('Starting gypsy')

    s3_params = _parse_s3_url(output_dir)
    bucket_name = s3_params['bucket']
    key_prefix = s3_params['prefix']
    bucket_conn = None

    if bucket_name and key_prefix:
        s3 = boto3.resource('s3')
        bucket_conn = s3.Bucket(bucket_name)
    elif bucket_name is None and key_prefix is None:
        if not os.path.isdir(output_dir):
            LOGGER.info('Output directory %s does not exist. Creating it.')
            os.mkdir(output_dir)
    else:
        click.Abort('s3 output-dir: %s, is missing a prefix')

    ctx.obj = {
        'output-dir': output_dir,
        's3-bucket-name': bucket_name,
        's3-prefix': key_prefix,
        's3-bucket-conn': bucket_conn,
    }


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def generate_config(ctx):
    """Generate a configuration file

    Generates a configuration file, gypsy-config.json, under DEST directory.

    """
    s3_prefix = ctx.obj['s3-prefix']
    output_dir = s3_prefix if s3_prefix else ctx.obj['output-dir']
    output_path = gyppath._join(output_dir, 'gypsy-config.json') #pylint: disable=protected-access
    _copy_file(DEFAULT_CONF_FILE, output_path, bucket_conn=ctx.obj['s3-bucket-conn'])
    LOGGER.info('Config file saved at %s', output_path)

    # TODO: won't work with s3
    if ctx.obj['s3-bucket-name'] is None:
        _append_file(LOG_FILE_NAME, os.path.join(output_dir, LOG_FILE_NAME))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('standtable', type=click.Path(exists=False))
@click.option('--config-file', '-c', type=click.Path(exists=False),
              default=DEFAULT_CONF_FILE,
              callback=_load_and_validate_config)
@click.pass_context
def prep(ctx, standtable, config_file):
    """Prepare stand data for use in GYPSY simulation"""
    LOGGER.info('Running prep...')
    output_dir = ctx.obj['output-dir']
    output_path = os.path.join(output_dir, 'plot_table_prepped.csv')

    standtable_df = pd.read_csv(standtable)
    prepped_data = prep_standtable(standtable_df)

    prepped_data.to_csv(output_path)
    _append_file(LOG_FILE_NAME, os.path.join(output_dir, LOG_FILE_NAME))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('data', type=click.Path(exists=True))
@click.option('--config-file', '-c', type=click.Path(exists=False),
              default=DEFAULT_CONF_FILE,
              callback=_load_and_validate_config)
@click.pass_context
def simulate(ctx, data, config_file):
    """Run GYPSY simulation"""
    output_dir = ctx.obj['output-dir']
    standtable = pd.read_csv(data)

    min_age = 25
    LOGGER.info('Filtering plots to those with a species older than %d years',
                min_age)
    standtable_old, standtable_young = _filter_young_stands(standtable,
                                                            min_age=25)

    if standtable_young.shape[0] > 0:
        skipped_plots_filename = 'skipped-plots.csv'
        LOGGER.info('%d young plots were removed. IDs saved to %s',
                    standtable_young.shape[0],
                    skipped_plots_filename)
        standtable_young_path = os.path.join(output_dir,
                                             skipped_plots_filename)
        standtable_young.to_csv(standtable_young_path,
                                columns=['PlotID'])
    else:
        LOGGER.info('No plots less than %d years old present', min_age)

    LOGGER.info('Running simulation...')
    result = simulate_forwards_df(standtable_old,
                                  utiliz_params=config_file['utilization'])

    LOGGER.info('Saving output data')
    simulation_output_dir = os.path.join(output_dir, 'simulation-data')
    os.mkdir(simulation_output_dir)
    for plot_id, data in result.items():
        filename = '%s.csv' % plot_id
        output_path = os.path.join(simulation_output_dir, filename)
        data.to_csv(output_path)

    _append_file(LOG_FILE_NAME, os.path.join(output_dir, LOG_FILE_NAME))

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('simulation-output-dir', type=click.Path(exists=True))
@click.option('--config-file', '-c', type=click.Path(exists=False),
              default=DEFAULT_CONF_FILE,
              callback=_load_and_validate_config)
@click.pass_context
def plot(ctx, simulation_output_dir, config_file):
    """Create charts for all files in gypsy simulation output directory

    """
    output_dir = ctx.obj['output-dir']
    chart_files = glob(os.path.join(simulation_output_dir, '*.csv'))
    LOGGER.info('Plotting all csv files at %s...', simulation_output_dir)

    for i, chart_file in enumerate(chart_files):
        _log_loop_progress(i, len(chart_files))
        chart_df = pd.read_csv(chart_file)
        output_filename = os.path.splitext(os.path.split(chart_file)[-1])[0] + '.png'
        figure_path = os.path.join(simulation_output_dir, 'figures', output_filename)

        save_plot(chart_df, path=figure_path)

    _append_file(LOG_FILE_NAME, os.path.join(output_dir, LOG_FILE_NAME))
