"""CLI option callbacks"""
import json
import codecs
import logging

import click
import jsonschema

from gypsy.scripts import CONF_SCHEMA_FILE
from gypsy.log import CONSOLE_LOGGER_NAME


LOGGER = logging.getLogger(CONSOLE_LOGGER_NAME)


def _load_and_validate_config(ctx, param, value): #pylint: disable=unused-argument, missing-docstring
    with open(CONF_SCHEMA_FILE) as schema_file: #pylint: disable=invalid-name
        schema = json.load(schema_file)

    try:
        with codecs.open(value, encoding='utf-8') as conf_file:
            conf = json.load(conf_file)
    except IOError as err:
        LOGGER.warning(
            'Error reading config file: %s, using default config.',
            value
        )

    try:
        jsonschema.validate(conf, schema)
    except Exception as err:
        LOGGER.error((
            'There was an error validating the config file. '
            'See the log file for more details.'
        ))
        LOGGER.debug(err)
        raise click.BadParameter()

    return conf
