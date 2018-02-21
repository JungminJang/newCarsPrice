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
domain = "https://www.renaultsamsungm.com"

url = "https://www.renaultsamsungm.com/2017/side/catalog_download.jsp"
downloadurl = "https://www.renaultsamsungm.com/2017/side/catalogue_down.jsp"


# 1. Samsung
def get_link_from():
    soup = getSoup(url)
    menu = soup.find("div", class_="model_each-list")
    if None != menu:

        menu_li = menu.findAll("li")
        for item in menu_li:
            
            if '카탈로그' == item.text:
                download = item.find('button').get('onclick')
                downloadArr = download[download.find("(")+1:download.rfind(")")].replace("'", "")
                model = downloadArr[downloadArr.rfind(",")+1:].strip()
                download_files("../download/catalog/Samsung/", downloadurl+"?gb=catalogue&model="+model, model, "catalog")

                time.sleep(10)

            if '가격표' == item.text:
                download = item.find('button').get('onclick')
                downloadArr = download[download.find("(") + 1:download.rfind(")")].replace("'", "")
                model = downloadArr[downloadArr.rfind(",") + 1:].strip()
                download_files("../download/price/Samsung/", downloadurl + "?gb=price&model=" + model, model, "price")

                time.sleep(10)


def download_files(dir, url, model, type):
    filename = TODAY + '_' + type + "_" + model + ".pdf"
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

    get_link_from()


if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())
