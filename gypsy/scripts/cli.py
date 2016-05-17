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
def run(count):
    """Echo a value `count` number of times"""
    log.info('running has_legs %d times', count)
    for i in range(count):
        click.echo(has_legs())
