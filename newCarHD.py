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

# 1. Hyundai
def get_link_from(URL):

    soup = getSoup(URL)
    find_car = soup.find('dl', class_='find_car')
    href_list = find_car.findAll('a')

    for index, item in enumerate(href_list):
        if(index < len(href_list)/2):
            href = item.get('href')
            if('https' not in href):
                get_car_detail(URL, href.replace('/highlights', '') + '/price')
                time.sleep(10)

def get_car_detail(url, href):
    print(url+href)
    dnsoup = getSoup(url+href)
    if None != dnsoup:
        dnhref = dnsoup.find('div', class_='pip_button_area align_right')
        if None != dnhref:
            dnArr = dnhref.findAll('a')

            for index, item in enumerate(dnArr):
                item_word = item.find('span').text
                if '카탈로그 다운로드' == item_word:
                    catalog = url + dnArr[index].get('href')
                    download_files('../download/catalog/Hyundai/', catalog)
                if '가격표 다운로드' == item_word:
                    price = url+dnArr[index].get('href')
                    download_files('../download/price/Hyundai/', price)


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

        target_URL = 'https://www.hyundai.com'
        get_link_from(target_URL)


if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())
