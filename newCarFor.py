#-*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

import requests
import shutil
import os
import time

import datetime
from fake_useragent import UserAgent

from selenium import webdriver

TODAY = datetime.datetime.today().strftime("%Y%m")
BEFOREDAY = datetime.datetime.today() - datetime.timedelta(days=1) # 시작일 선정
STARTDT = BEFOREDAY.strftime('%Y-%m-%d')
ENDDT = TODAY
now = datetime.datetime.now()

domain = "http://auto.danawa.com"
url = "http://auto.danawa.com/auto/"
downloadPricePath = "../download/price/"
downloadCatalogPath = "../download/catalog"


# 1. Danawa 수입차
def get_link_from():

    soup = getSoup(url)
    brandList = soup.findAll("ul", class_="brandList imageLarge")

    europe = brandList[1]
    asia = brandList[2]
    usa = brandList[3]

    for index, item in enumerate(europe.findAll('li')):
        get_brand_page(domain+item.find('a').get('href'), "europe", item.text)

    for index, item in enumerate(asia.findAll('li')):
        get_brand_page(domain+item.find('a').get('href'), "asia", item.text)

    for index, item in enumerate(usa.findAll('li')):
        get_brand_page(domain+item.find('a').get('href'), "usa", item.text)



def get_brand_page(brandUrl, region, brand):
    soup = getSoup(brandUrl)
    modelList = soup.find("div", class_="brandModel newcar")

    for index, item in enumerate(modelList.findAll('a')):

        model = item.find("span", class_="name").text
        href = item.get('href')
        print(brand + " >> " + model)

        soupview = getSoup(domain+href)

        isExisting = soupview.find("div", class_="modelSection container_modelprice")

        if None != isExisting:
            screenshot(domain + href, region, brand, model)
            time.sleep(8)




def screenshot(url, region, brand, model):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1440")
    options.add_argument("disable-gpu")

    dir = "../download/importedCar/" + region + "/" + brand + "/"
    filename = TODAY + "_" + model + ".png"
    browser = webdriver.Chrome("./chromedriver", chrome_options=options)

    try:
        if not os.path.isdir(dir):
            os.makedirs(dir)

        if os.path.isfile(dir + filename):
            os.remove(dir + filename)

        browser.get(url)
        browser.implicitly_wait(3)
        browser.find_element_by_class_name("button_updown").click()
        elements = browser.find_elements_by_css_selector(".button_updown")
        for e in elements:
            e.click()
            time.sleep(1)

        browser.get_screenshot_as_file(dir+filename)
    finally:
        browser.quit()



def getSoup(URLlink):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.chrome}
        req = urllib.request.Request(URLlink, headers=headers)
        source_code_from__url = urllib.request.urlopen(req).read()
    except:
        return None
    else:
        return BeautifulSoup(source_code_from__url, 'html.parser')

def main():

    get_link_from()


if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())
