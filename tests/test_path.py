from pygypsy.path import _join

def test_join():
    assert _join('s3://', 'bucket', 'prefix') == 's3://bucket/prefix'
    assert _join('s3://bucket', 'prefix') == 's3://bucket/prefix'
    assert _join('bucket', 'prefix') == 'bucket/prefix'
