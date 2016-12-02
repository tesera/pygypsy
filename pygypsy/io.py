"""IO"""
from StringIO import StringIO


def df_to_s3_bucket(df, bucket_conn, key):
    """Write dataframe to s3 bucket

    :param df: data frame
    :param bucket_conn: boto3 bucket object
    :param key: object key
    """
    mem_file = StringIO()
    df.to_csv(mem_file)
    bucket_conn.put_object(Body=mem_file.getvalue(), Key=key)
    mem_file.close()
