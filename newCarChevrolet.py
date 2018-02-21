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
chevrolet = "http://www.chevrolet.co.kr"
pricedomain = "http://www.chevrolet.co.kr/purchase/car-line-price.gm"
catalogdomain = "http://www.chevrolet.co.kr/e-catalog/car-catalog.gm"

# 1. Genesis
def getPrice():

    soup = getSoup(pricedomain)
    script = soup.findAll('script', type='text/javascript')

    for index, item in enumerate(script):
        if "#carPrice" in item.text:
            link = re.findall(r"[/:\w]+download.gm[?\w:=]+\d", item.text)
            download_files("../download/price/Chevrolet/", chevrolet + link[0], TODAY + "_chevrolet_all_price.pdf")

            time.sleep(10)


def getCatalog():
    soup = getSoup(catalogdomain)
    carList = soup.find('ul', class_='cataList')
    links = carList.findAll('a')

    for item in links:
        link = item.get('href')
        if "pdf" in link:
            download_files("../download/catalog/Chevrolet/", chevrolet + link, TODAY + "_catalog_" + link[link.rfind('/')+1:])

            time.sleep(10)




def download_files(dir, url, filename):
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
