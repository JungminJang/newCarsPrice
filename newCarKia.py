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
domain = "http://www.kia.com"

# 1. Genesis
def get_link_from(URL):

    soup = getSoup(URL)
    carLists = soup.findAll('script', type='text/javascript')
    json = carLists[16].text
    link = re.findall(r"[/\w+:-]+.pdf", json)
    for item in link:
        if "price" in item:
            download_files("../download/price/Kia/", domain + item)
        else:
            download_files("../download/catalog/Kia/", domain + item)

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

        target_URL = 'http://www.kia.com/kr/shopping-tools/catalog-price.html'
        get_link_from(target_URL)


if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())
