import os
import boto3
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


class WebDriver:
    def __init__(self, source_info):
        self._tmp_folder = '/tmp/{}'.format(uuid.uuid4())
        self.source_info = source_info
        self.data = []

        if not os.path.exists(self._tmp_folder):
            os.makedirs(self._tmp_folder)

        if not os.path.exists(self._tmp_folder + '/user-data'):
            os.makedirs(self._tmp_folder + '/user-data')

        if not os.path.exists(self._tmp_folder + '/data-path'):
            os.makedirs(self._tmp_folder + '/data-path')

        if not os.path.exists(self._tmp_folder + '/cache-dir'):
            os.makedirs(self._tmp_folder + '/cache-dir')

    def __get_default_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--user-data-dir={}'.format(self._tmp_folder + '/user-data'))
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir={}'.format(self._tmp_folder))
        chrome_options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        chrome_options.add_argument('--window-size={}x{}'.format(1280, 1024))

        chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium" 

        return chrome_options      

    def __get_page_source(self):

        chrome_options=self.__get_default_chrome_options()

        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(self.source_info['url'])
        driver.find_element_by_xpath(self.source_info['button_xpath']).click()
        page_source = driver.page_source

        driver.quit()

        return page_source

    def get_file_info(self):

        page_source = self.__get_page_source()

        soup = BeautifulSoup(page_source, 'lxml')
        data = []

        table_selector = soup.find_all('table', class_=self.source_info['table_class'])
        print(len(table_selector))
        header_selector = table_selector[0].find_all('tr', class_=self.source_info['tr_header_class'])
        print(len(header_selector))
        header_th_selectors = header_selector[0].find_all('th')
        headers = [item.get_text().strip() for item in header_td_selectors]
        print(headers)

        tr_selectors = soup.find_all('tr', class_=self.source_info['tr_class'])
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
            link = os.path.join(self.source_info['base_data_url'], row['Data File'][0]['href'])
            data[i]['Data File'][0]['link'] = link

        print(len(data))
        print(data[0])]

        self.data = data

        return data

    def close(self):
        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)

        # Remove possible core dumps
        folder = '/tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if 'core.headless-chromi' in file_path and os.path.exists(file_path) and os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

def source_dataset():
    logger.info('## Environment Variables: \n{}'.format(os.environ))

    source_info = {
        'source_url' = 'https://nces.ed.gov/ipeds/datacenter/Default.aspx?gotoReportId=7&amp;fromIpeds=true',
        'button_xpath'='//*[@id="contentPlaceHolder_ibtnContinue"]',
        'base_data_url'='https://nces.ed.gov/ipeds/datacenter/',

        'table_id' = 'contentPlaceHolder_tblResult',
        'table_class' = 'idc_gridview',
        'tr_class' = 'idc_gridviewrow',
        'tr_header_class'='idc_gridviewheader'
    }

    data_dir = '/tmp'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    driver = WebDriver(source_info)

    logger.info('Getting data file info')
    data = driver.get_file_info()

    for row in data:
        link = row['Data File'][0]['link']

    driver.close()

    # upload to s3
    data_set_name = os.environ['DATA_SET_NAME']

    s3_bucket = os.environ['S3_BUCKET']
    s3 = boto3.client('s3')

    s3_uploads = []
    asset_list = []

    for r, d, f in os.walk(data_dir):
        for filename in f:
            obj_name = os.path.join(r, filename).split('/', 3).pop().replace(' ', '_').lower()
            file_location = os.path.join(r, filename)
            new_s3_key = data_set_name + '/dataset/' + obj_name

            has_changes = md5_compare(s3, s3_bucket, new_s3_key, file_location)
            if has_changes:
                s3.upload_file(file_location, s3_bucket, new_s3_key)
                print('Uploaded: ' + filename)
            else:
                print('No changes in: ' + filename)

            asset_source = {'Bucket': s3_bucket, 'Key': new_s3_key}
            s3_uploads.append({'has_changes': has_changes, 'asset_source': asset_source})

    count_updated_data = sum(upload['has_changes'] == True for upload in s3_uploads)
    if count_updated_data > 0:
        asset_list = list(map(lambda upload: upload['asset_source'], s3_uploads))
        if len(asset_list) == 0:
            raise Exception('Something went wrong when uploading files to s3')

    # asset_list is returned to be used in lamdba_handler function
    # if it is empty, lambda_handler will not republish
    return asset_list

# if __name__ == '__main__':
#     source_dataset()