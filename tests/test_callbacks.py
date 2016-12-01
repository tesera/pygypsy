from gypsy.scripts.callbacks import _load_and_validate_config

def test_load_and_validate_config(config_on_s3):
    conf = _load_and_validate_config(None, None, config_on_s3)
    assert isinstance(conf, dict)
