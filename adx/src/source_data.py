import os
import boto3
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from zipfile import ZipFile

import datetime 
import pandas as pd
import shutil
import uuid
import logging
from bs4 import BeautifulSoup
from selenium import webdriver

from s3_md5_compare import md5_compare

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# source_url = os.getenv(source_data_url)  # 'https://nces.ed.gov/ipeds/datacenter/Default.aspx?gotoReportId=7&amp;fromIpeds=true',
button_xpath = '//*[@id="contentPlaceHolder_ibtnContinue"]',
base_data_url = 'https://nces.ed.gov/ipeds/datacenter/',
table_id = 'contentPlaceHolder_tblResult',
table_class = 'idc_gridview',
tr_class = 'idc_gridviewrow',
tr_header_class = 'idc_gridviewheader'


def get_default_chrome_options():
    chrome_options = webdriver.ChromeOptions()

    chrome_tmp_dir = '/tmp-chrome'
    if not os.path.exists(chrome_tmp_dir):
        os.mkdir(chrome_tmp_dir)

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.add_argument('--window-size={}x{}'.format(1280, 1024))
    chrome_options.add_argument('--user-data-dir={}'.format(chrome_tmp_dir + '/user-data'))
    chrome_options.add_argument('--data-path={}'.format(chrome_tmp_dir+ '/data-path'))
    chrome_options.add_argument('--homedir={}'.format(chrome_tmp_dir))
    chrome_options.add_argument('--disk-cache-dir={}'.format(chrome_tmp_dir + '/cache-dir'))

    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium" 

    return chrome_options 

def get_page_source_after_click(page_url):

    chrome_options = get_default_chrome_options()

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(page_url)
    driver.find_element_by_xpath(button_xpath).click()
    page_source = driver.page_source

    driver.quit()

    return page_source

def get_file_info(page_source):
    """given a page_source, get download links to all desired files"""
    soup = BeautifulSoup(page_source, 'lxml')
    data = []

    table_selector = soup.find_all('table', class_=table_class)
    print(len(table_selector))
    header_selector = table_selector[0].find_all('tr', class_=tr_header_class)
    print(len(header_selector))
    header_th_selectors = header_selector[0].find_all('th')
    headers = [item.get_text().strip() for item in header_td_selectors]
    print(headers)

    tr_selectors = soup.find_all('tr', class_=tr_class)
    headers = headers[-len(tr_selectors[0])+2:]
    print(headers)
    for tr_selector in tr_selectors:
        td_selectors = tr_selector.find_all('td')
        row = {}
        for i, header in enumerate(headers):
    #         text = td_selectors[i].get_text().strip()
            a_selectors = td_selectors[i].find_all('a')
            if not a_selectors:
                row[header] = text
            else:
                row[header] = []
                for a_selector in a_selectors:
                    attr_name = a_selector.get_text().strip()
                    tmp = {}
                    tmp['name'] = attr_name
                    tmp['href'] = a_selector['href']
                    row[header].append(tmp)
        data.append(row)

    for i, row in enumerate(data):
        data[i]['Data File'][0]['link'] = os.path.join(self.source_info['base_data_url'], row['Data File'][0]['href'])
        data[i]['Dictionary'][0]['link'] = os.path.join(self.source_info['base_data_url'], row['Dictionary'][0]['href'])

    print(len(data))
    print(data[0])]

    return data

def download_file(file_url, target_dir):
    response = None
    retries = 5
    for attempt in range(retries):
        try:
            response = urlopen(file_url)
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

    filename = file_url.split('/')[-1]
    filepath = os.path.join(target_dir, filename)

    with open(filepath, 'wb') as f:
        f.write(response.read())

    if filename.endswith('.zip'):
        with ZipFile(filepath, 'r') as z:
            z.extractall(data_dir)

        os.remove(filepath)

def source_dataset(source_data_url, s3_bucket, dataset_name):
    """Download the source data from URL and put it in S3"""
    logger.info('Environment Variables: \n{}'.format(os.environ))

    logger.info('Getting page source')
    page_source = get_page_source_after_click(source_data_url)

    logger.info('Getting data file info')
    data = get_file_info(page_source)

    s3 = boto3.client('s3')

    data_dir = '/tmp'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    for row in data:
        data_link = row['Data File'][0]['link']
        meta_link = row['Dictionary'][0]['link']

        download_file(data_link, data_dir)
        download_file(meta_link, data_dir)


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
