import click

from gypsy import has_legs
from gypsy.log import log


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', '-v', is_flag=True)
def cli(verbose):
    log.debug('cli invoked')


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('count', type=int)
@click.option('--output-fields', '-f', multiple=True, type=str)
@click.option('--stand-id', '-n', multiple=True, type=int)
@click.option('--output-timestep', '-t', type=int)
@click.option('--id-field', '-i', type=str)
@click.option('--generate-plots', '-p', is_flag=True)
@click.option('--write-id', '-w', is_flag=True)
def run(count, stand_id, generate_plots, output_fields, output_timestep,
        id_field, write_id):
    """Echo a value `count` number of times"""
    log.info('running has_legs %d times', count)
    for _ in range(count):
        click.echo(has_legs())
