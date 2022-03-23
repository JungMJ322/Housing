from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json


def crawling():
    service = webdriver.chrome.service.Service('./chromedriver')
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(2)

    url = "http://cu.bgfretail.com/store/list.do?category=store#"
    driver.get(url)
    time.sleep(5)

    driver.find_element(By.CLASS_NAME, 'emblem').click()
    time.sleep(5)

    cu_list=[]

    for j in range(2625):
        n_list = driver.find_elements(By.CLASS_NAME, 'name')
        p_list = driver.find_elements(By.XPATH, '//div[@class="detail_info"]/address/a')
        time.sleep(0.5)
        for i in range(len(n_list)):
            temp_dict = {}
            temp_dict['sname']=n_list[i].text
            temp_dict['place']=p_list[i].text
            cu_list.append(temp_dict)
        driver.find_elements(By.XPATH, '//a[@class="Current"]/following-sibling::a[1]')[0].click()
        time.sleep(1.5)

    return cu_list

def js_save():
    cu_list = crawling()
    cu_json={}
    cu_json['cu']=cu_list
    with open('../data/json/cu.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(cu_json, ensure_ascii=False))



if __name__=='__main__':
    js_save()

