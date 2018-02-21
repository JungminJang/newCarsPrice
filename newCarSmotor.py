#-*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

import requests
import shutil
import os
import time

import datetime
import re

TODAY = datetime.datetime.today().strftime("%Y%m")
BEFOREDAY = datetime.datetime.today() - datetime.timedelta(days=1) # 시작일 선정
STARTDT = BEFOREDAY.strftime('%Y-%m-%d')
ENDDT = TODAY
now = datetime.datetime.now()
domain = "http://www.smotor.com"
indexurl = "/kr/index.html"

priceurl = "http://www.smotor.com/kr/purchase/service/pricelist/index.html"
catalogurl = "http://www.smotor.com/kr/purchase/index.html"


# 1. smotor
def getPrice():
    soup = getSoup(priceurl)
    find_car = soup.find("ul", class_="priceList")
    find_links = find_car.findAll('a')
    for item in find_links:

        href = item.get('href')
        if '.pdf' in href:
            download_files("../download/price/Smotor/", domain+href)

        time.sleep(10)


def getCatalog():
    soup = getSoup(catalogurl)
    find_car = soup.find("div", class_="buy_slide_box padding_type1")

    find_links = find_car.findAll('li')
    for item in find_links:

        href = item.get('ahref')
        if '.pdf' in href:
            download_files("../download/catalog/Smotor/", domain+href)

        time.sleep(10)




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

        getPrice()
        getCatalog()


if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())
