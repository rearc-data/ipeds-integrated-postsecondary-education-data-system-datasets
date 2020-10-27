# Compare the md5 of a file to the s3 etag md5
# Source: li xin on StackOverflow
# https://stackoverflow.com/questions/1775816/how-to-get-the-md5sum-of-a-file-on-amazons-s3

import hashlib
import botocore.exceptions


def md5_checksum(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            m.update(data)
    return m.hexdigest()


def etag_checksum(filename, chunk_size=8 * 1024 * 1024):
    md5s = []
    with open(filename, 'rb') as f:
        for data in iter(lambda: f.read(chunk_size), b''):
            md5s.append(hashlib.md5(data).digest())
    m = hashlib.md5(b"".join(md5s))
    return '{}-{}'.format(m.hexdigest(), len(md5s))


def etag_compare(filename, etag):
    et = etag[1:-1]  # strip quotes
    if '-' in et and et == etag_checksum(filename):
        return False
    if '-' not in et and et == md5_checksum(filename):
        return False
    return True


def md5_compare(s3, bucket_name, s3_key, filename):
    # Get the file metadata from s3
    # If the file does not exist, return True for changes found
    try:
        obj_dict = s3.head_object(Bucket=bucket_name, Key=s3_key)
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return True

    etag = (obj_dict['ETag'])

    md5_matches = etag_compare(filename, etag)

    return md5_matches