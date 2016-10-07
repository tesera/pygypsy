import click
import pandas as pd

from gypsy.forward_simulation import simulate_forwards_df
from gypsy.GypsyDataPrep import dataPrepGypsy
from gypsy.log import log


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def create_output_path(ctx, param, value):
    path = value
    if path is None:
        path = ctx.params.get('standtable')
        path += '.prepped'
        return path

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', '-v', is_flag=True)
def cli(verbose):
    """Growth and Yield Projection System

    Data prep must be run before simulating

    """
    log.debug('cli invoked')

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('standtable', type=click.Path(exists=True))
@click.option('--stand-id', '-n', multiple=True, type=int)
@click.option('--id-field', '-i', type=str)
@click.option('--output-path', '-o', type=click.Path(), callback=create_output_path)
def prep(standtable, stand_id, id_field, output_path):
    """Prepare stand table for use in GYPSY simulation"""
    log.info('running prep')
    import ipdb; ipdb.set_trace()
    standtable_df = pd.read_csv(standtable)

    # TODO: filter id by stand id

    prepped_data = dataPrepGypsy(standtable_df)
    prepped_data.to_csv(output_path)

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('data', type=int)
@click.option('--output-fields', '-f', multiple=True, type=str)
@click.option('--stand-id', '-n', multiple=True, type=int)
@click.option('--output-timestep', '-t', type=int)
@click.option('--id-field', '-i', type=str)
@click.option('--generate-plots', '-p', is_flag=True)
@click.option('--write-id', '-w', is_flag=True)
@click.option('--output-dir', '-o', type=click.Path()) # add a default directory
def simulate(data, stand_id, generate_plots, output_fields, output_timestep,
             id_field, write_id):
    """Run GYPSY simulation"""
    log.info('running simulate')
    # read input data
    # validate that its had dataprep
    # filter id by stand id
    # run simulate_df
    # subset to timestep
    # add id column to data
    # save data to output dir
    # generate plot if necessary

