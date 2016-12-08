"""CLI option callbacks"""
# this should probably not be tied to click exceptions
import json
import codecs
import logging

import click
import boto3
import jsonschema

from pygypsy.scripts import CONF_SCHEMA_FILE, DEFAULT_CONF_FILE
from pygypsy.log import CONSOLE_LOGGER_NAME
from pygypsy.utils import _parse_s3_url


LOGGER = logging.getLogger(CONSOLE_LOGGER_NAME)


def _load_and_validate_config(ctx, param, value): #pylint: disable=unused-argument, missing-docstring
    with open(CONF_SCHEMA_FILE) as schema_file:
        schema = json.load(schema_file)

    if value == DEFAULT_CONF_FILE:
        LOGGER.warning(
            'Using pygypsy default config file.'
        )

    try:
        if value.startswith('s3://'):
            s3_params = _parse_s3_url(value)
            client = boto3.client('s3')
            data = client.get_object(
                Bucket=s3_params['bucket'],
                Key=s3_params['prefix']
            )["Body"].read().decode('utf-8')
            conf = json.loads(data)
        else:
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
