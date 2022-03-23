from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json


from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from collections import OrderedDict

def crawling() :
    service = webdriver.chrome.service.Service('./chromedriver')
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(1)

    url = "http://gs25.gsretail.com/gscvs/ko/store-services/locations#;"
    driver.get(url)

# 매장 정보 id
    table = driver.find_element_by_id('storeInfoList')

    name = []
    juso = []

    for i in range(3085):
        for tr in table.find_elements_by_tag_name("tr"):
            td = tr.find_elements_by_tag_name("td>a")
            name.append(td[0].text)
            juso.append(td[1].text)
        driver.find_element_by_css_selector('#pagingTagBox > a.next').click()
        time.sleep(0.5)
    return name, juso

def data_save(name, juso):
    dict_list = []
    for_json = {}
    for i in range (len(name)-1):
        dict = {'sname' : name[i], 'place' : juso[i]}
        dict_list.append(dict)
    for_json['GS25'] = dict_list
    with open('GS25.json', 'w', encoding="utf-8") as make_file:
        make_file.write(json.dumps(for_json,ensure_ascii=False))
