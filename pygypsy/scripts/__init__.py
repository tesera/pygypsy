#pylint: disable=missing-docstring
import os

CONF_DIR = os.path.join(os.path.dirname(__file__), 'config')
DEFAULT_CONF_FILE = os.path.join(CONF_DIR, 'default-conf.json')
CONF_SCHEMA_FILE = os.path.join(CONF_DIR, 'conf.schema')
