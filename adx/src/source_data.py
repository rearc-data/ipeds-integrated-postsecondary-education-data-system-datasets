import os
import boto3
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from zipfile import ZipFile
from s3_md5_compare import md5_compare


def source_dataset(source_data_url, s3_bucket, dataset_name):
    """Download the source data from URL and put it in S3"""
    s3 = boto3.client('s3')

    data_dir = '/tmp'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    response = None
    retries = 5
    for attempt in range(retries):
        try:
            response = urlopen(source_data_url)
        except HTTPError as e:
            if attempt == retries:
                raise Exception('HTTPError: ', e.code)
            time.sleep(0.2 * attempt)
        except URLError as e:
            if attempt == retries:
                raise Exception('URLError: ', e.reason)
            time.sleep(0.2 * attempt)
        else:
            break

    if response is None:
        raise Exception('There was an issue downloading the dataset')

    zip_location = os.path.join(data_dir, dataset_name+'.zip')

    with open(zip_location, 'wb') as f:
        f.write(response.read())

    with ZipFile(zip_location, 'r') as z:
        z.extractall(data_dir)

    os.remove(zip_location)

    s3_uploads = []
    asset_list = []

    for r, d, f in os.walk(data_dir):
        for filename in f:
            obj_name = os.path.join(r, filename).split('/', 3).pop().replace(' ', '_').lower()
            file_location = os.path.join(r, filename)
            new_s3_key = os.path.join(dataset_name, 'dataset', obj_name)

            has_changes = md5_compare(s3, s3_bucket, new_s3_key, file_location)
            if has_changes:
                s3.upload_file(file_location, s3_bucket, new_s3_key)
                print('Uploaded: ' + filename)
            else:
                print('No changes in: ' + filename)

            asset_source = {'Bucket': s3_bucket, 'Key': new_s3_key}
            s3_uploads.append({'has_changes': has_changes, 'asset_source': asset_source})

    count_updated_data = sum(upload['has_changes'] is True for upload in s3_uploads)
    if count_updated_data > 0:
        asset_list = list(map(lambda upload: upload['asset_source'], s3_uploads))
        if len(asset_list) == 0:
            raise Exception('Something went wrong when uploading files to s3')

    # asset_list is returned to be used in create_dataset_revision function
    # if it is empty, lambda_handler will not republish
    return asset_list
