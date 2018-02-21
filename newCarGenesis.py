#-*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

import requests
import shutil
import os
import time
import datetime

TODAY = datetime.datetime.today().strftime("%Y%m")
BEFOREDAY = datetime.datetime.today() - datetime.timedelta(days=1) # 시작일 선정
STARTDT = BEFOREDAY.strftime('%Y-%m-%d')
ENDDT = TODAY
now = datetime.datetime.now()
download_url = 'https://www.genesis.com/content/genesis/kr/ko/func/dam_dn.html'

# 1. Genesis
def get_link_from(URL):

    soup = getSoup(URL)
    carLists = soup.findAll('div', class_='tab-cont')

    for index, item in enumerate(carLists):
        download_area = item.find('div', class_='download-area')
        get_car_detail(URL, download_area)

        time.sleep(10)

def get_car_detail(url, area):

    for index, item in enumerate(area.findAll('a')):
        uri = item.get('onclick')
        download_uri = download_url + (uri[uri.find("('")+2:uri.rfind("');")])
        item_text = item.text
        if '카달로그' in item_text:
            download_files('../download/catalog/Genesis/', download_uri)
        if '가격표' in item_text:
            download_files('../download/price/Genesis/', download_uri)


def download_files(dir, url):
    filename = TODAY + '_' + url[url.rfind('/')+1:].replace('-', '_')
    res = requests.get(url, stream=True)

    if not os.path.isdir(dir):
        os.makedirs(dir)

    if os.path.isfile(dir+filename):
        os.remove(dir+filename)

    with open(dir+filename, 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)

    print(dir+filename)

def getSoup(URLlink):
    try:
        source_code_from__u_r_l = urllib.request.urlopen(URLlink)
    except:
        return None
    else:
        return BeautifulSoup(source_code_from__u_r_l, 'html.parser')

def main():

        target_URL = 'https://www.genesis.com/kr/ko/download-center.html'
        get_link_from(target_URL)


if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())
