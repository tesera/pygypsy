import os
import pytest

from pygypsy.scripts.callbacks import _load_and_validate_config

@pytest.mark.skipif(os.getenv('GYPSY_BUCKET') is None,
                   reason="S3 tests are not configured locally")
def test_load_and_validate_s3_config(config_on_s3):
    conf = _load_and_validate_config(None, None, config_on_s3)
    assert isinstance(conf, dict)
