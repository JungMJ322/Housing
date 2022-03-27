# 전국 병원 데이터를 가지고 오는 모듈
# api => https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000736

import requests
import json
import xmltodict

# from bs4 import BeautifulSoup
# import xml.etree.ElementTree as ET

api_add = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncFullDown'
api_key = '?serviceKey=jVKpVOT7kMRWzMIqSZbUMTByhcmYH1qvPSCXu%2FwXFtNlDKCdQcchWibsqysFadWPnIOSGsB4%2BchzqJTyw%2BybuQ%3D%3D'
location = '../../data/hadoop_upload/'
file_name = 'hospital.json'

def getHospital(file_name=file_name, location=location):
    url = api_add + api_key + '&pageNo=1&numOfRows=1'
    result = requests.get(url)

    dict_soup = xmltodict.parse(result.text)
    json_soup = json.dumps(dict_soup)
    dict2_soup = json.loads(json_soup)
    cnt = int(dict2_soup['response']['body']['totalCount'])

    hospital_list = list()
    for i in range(1, (cnt//100)+2):
        url = api_add + api_key + f'&pageNo={i}&numOfRows=100'
        result = requests.get(url)
        dict_soup = xmltodict.parse(result.text)
        json_soup = json.dumps(dict_soup)
        dict2_soup = json.loads(json_soup)
        # print(i)
        # print(dict2_soup)
        hospital_list.extend(list(dict2_soup['response']['body']['items']['item']))
        # print(i)

    with open((location+file_name), 'w', encoding='utf8') as f:
        json.dump(hospital_list, f, ensure_ascii=False)

if __name__ == '__main__':
    getHospital()

