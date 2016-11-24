"""CLI option callbacks"""
import json
import codecs
import logging

import click
import jsonschema

from gypsy.scripts import CONF_SCHEMA_FILE, DEFAULT_CONF_FILE
from gypsy.log import CONSOLE_LOGGER_NAME


LOGGER = logging.getLogger(CONSOLE_LOGGER_NAME)


def _load_and_validate_config(ctx, param, value): #pylint: disable=unused-argument, missing-docstring
    with open(CONF_SCHEMA_FILE) as schema_file: #pylint: disable=invalid-name
        schema = json.load(schema_file)

    if value == DEFAULT_CONF_FILE:
        LOGGER.warning(
            'Using gypsy default config file.'
        )

    try:
        with codecs.open(value, encoding='utf-8') as conf_file:
            conf = json.load(conf_file)
    except (IOError, ValueError) as err:
        LOGGER.error('Error reading config file: %s', value)
        raise click.BadParameter('Missing or incorrect filetype.')

    validator = jsonschema.Draft4Validator(schema)
    num_err = 0
    for error in sorted(validator.iter_errors(conf), key=str):
        msg = '/'.join(error.relative_path) + ': ' + error.message
        LOGGER.error(msg)
        num_err += 1

    if num_err > 0:
        raise click.BadParameter('Invalid config')

    return conf
