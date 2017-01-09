 #pylint: disable=protected-access
"""Command Line Interface"""
# TODO: handling s3/local is clumsy/repetitive in this module
# should factor it out
import os
import logging
from glob import glob

import boto3
import click
import pandas as pd

from pygypsy.scripts import DEFAULT_CONF_FILE
from pygypsy.scripts.callbacks import _load_and_validate_config
from pygypsy.plot import save_plot
from pygypsy.utils import (
    _log_loop_progress,
    _filter_young_stands,
    _append_file,
    _parse_s3_url,
    _copy_file,
)
from pygypsy.io import df_to_s3_bucket
from pygypsy.data_prep import prep_standtable
from pygypsy.log import setup_logging, CONSOLE_LOGGER_NAME
from pygypsy.forward_simulation import simulate_forwards_df
from pygypsy._version import get_versions
import pygypsy.path as gyppath


LOGGER = logging.getLogger(CONSOLE_LOGGER_NAME)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
LOG_FILE_NAME = 'pygypsy.log'


@click.group(context_settings=CONTEXT_SETTINGS)
@click.decorators.version_option(version=get_versions()['version'])
@click.option('--verbose', '-v', is_flag=True)
@click.option('--version', is_flag=True)
@click.option('--output-dir', '-o', type=click.Path(exists=False),
              default='pygypsy-output')
@click.pass_context
def cli(ctx, verbose, output_dir, version):  #pylint: disable=unused-argument
    """Growth and Yield Projection System

    Note: 'prep' subcommand must be run before 'simulate'

    """
    setup_logging()
    if verbose:
        LOGGER.setLevel(logging.DEBUG)
        for handler in LOGGER.handlers:
            handler.setLevel(logging.DEBUG)
    LOGGER.debug('Starting pygypsy')

    s3_params = _parse_s3_url(output_dir)
    bucket_name = s3_params['bucket']
    key_prefix = s3_params['prefix']
    bucket_conn = None

    if bucket_name and key_prefix:
        s3 = boto3.resource('s3')
        bucket_conn = s3.Bucket(bucket_name)
    elif bucket_name is None and key_prefix is None:
        if not os.path.isdir(output_dir):
            LOGGER.info('Output directory %s does not exist. Creating it.',
                        output_dir)
            os.mkdir(output_dir)
    else:
        click.Abort('s3 output-dir: %s, is missing a prefix')

    output_dir = key_prefix if key_prefix else output_dir

    ctx.obj = {
        'output-dir': output_dir,
        's3-bucket-name': bucket_name,
        's3-bucket-conn': bucket_conn,
    }


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def generate_config(ctx):
    """Generate a configuration file

    Generates a configuration file, pygypsy-config.json, under DEST directory.

    """
    try:
        output_dir = ctx.obj['output-dir']
        bucket_name = ctx.obj['s3-bucket-name']
        bucket_conn = ctx.obj['s3-bucket-conn']
        output_path = gyppath._join(output_dir, 'pygypsy-config.json')
        _copy_file(DEFAULT_CONF_FILE, output_path, bucket_conn=bucket_conn)
        LOGGER.info('Config file saved at %s', output_path)
    except:
        _copy_file(LOG_FILE_NAME,
                   os.path.join(output_dir, 'generate-config.log'),
                   bucket_conn)
        raise

    _copy_file(LOG_FILE_NAME,
               os.path.join(output_dir, 'generate-config.log'),
               bucket_conn)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('standtable', type=click.Path(exists=False))
@click.option('--config-file', '-c', type=click.Path(exists=False),
              default=DEFAULT_CONF_FILE,
              callback=_load_and_validate_config)
@click.pass_context
def prep(ctx, standtable, config_file):
    """Prepare stand data for use in pygpysy simulation"""
    LOGGER.info('Running prep...')
    bucket_name = ctx.obj['s3-bucket-name']
    bucket_conn = ctx.obj['s3-bucket-conn']
    output_dir = ctx.obj['output-dir']
    output_path = gyppath._join(output_dir, 'plot_table_prepped.csv')
    index_label = 'id_l1'

    try:
        standtable_df = pd.read_csv(standtable)
        prepped_data = prep_standtable(standtable_df)

        if bucket_name:
            df_to_s3_bucket(prepped_data, bucket_conn, output_path,
                            index_label=index_label)
        else:
            prepped_data.to_csv(output_path, index_label=index_label)

    except:
        _copy_file(LOG_FILE_NAME,
                   gyppath._join(output_dir, 'prep.log'),
                   bucket_conn)
        raise

    _copy_file(LOG_FILE_NAME,
               gyppath._join(output_dir, 'prep.log'),
               bucket_conn)



# TODO: needs refactor
@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('data', type=click.Path(exists=False))
@click.option('--config-file', '-c', type=click.Path(exists=False),
              default=DEFAULT_CONF_FILE,
              callback=_load_and_validate_config)
@click.pass_context
def simulate(ctx, data, config_file):
    """Run pygypsy simulation"""
    bucket_name = ctx.obj['s3-bucket-name']
    bucket_conn = ctx.obj['s3-bucket-conn']
    output_dir = ctx.obj['output-dir']
    index_label = 'id_l1'

    try:
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
            if bucket_name:
                df_to_s3_bucket(standtable_young, bucket_conn,
                                standtable_young_path, index_label=index_label)
            else:
                standtable_young.to_csv(standtable_young_path,
                                        columns=['PlotID'],
                                        idex_label=index_label)
        else:
            LOGGER.info('No plots less than %d years old present', min_age)

        LOGGER.info('Running simulation...')
        result = simulate_forwards_df(standtable_old,
                                      utiliz_params=config_file['utilization'],
                                      n_years=config_file['simulation']['years'],
                                      backwards=config_file['simulation']['backwards'])

        LOGGER.info('Saving output data')

        simulation_output_dir = os.path.join(output_dir, 'simulation-data')

        if bucket_name is None:
            os.mkdir(simulation_output_dir)

        for plot_id, data in result.items():
            filename = '%s.csv' % plot_id
            output_path = os.path.join(simulation_output_dir, filename)
            if bucket_name:
                df_to_s3_bucket(data, bucket_conn, output_path,
                                index_label=index_label)
            else:
                data.to_csv(output_path, index_label=index_label)
    except:
        _copy_file(LOG_FILE_NAME, gyppath._join(output_dir, 'simulate.log'),
                   bucket_conn)
        raise

    _copy_file(LOG_FILE_NAME, gyppath._join(output_dir, 'simulate.log'),
               bucket_conn)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('simulation-output-dir', type=click.Path(exists=True))
@click.option('--config-file', '-c', type=click.Path(exists=False),
              default=DEFAULT_CONF_FILE,
              callback=_load_and_validate_config)
@click.pass_context
def plot(ctx, simulation_output_dir, config_file):
    """Create charts for all files in pygypsy simulation output directory

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
