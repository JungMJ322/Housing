import json
import requests
from bs4 import BeautifulSoup

# url = "https://www.7-eleven.co.kr/util/storeLayerPop.asp"
# data = {"storeLaySido": "서울", "storeLayGu": "관악구", "hiddentext":"none"}
# res = requests.post(url, data=data)
# print(res.text)


def find_gugun(si_name):
    url = "https://www.7-eleven.co.kr/library/asp/StoreGetGugun.asp"
    data = {"Sido": si_name, "selBane": "storeLayGu"}
    res = requests.post(url, data=data)
    return_list = []

    soup = BeautifulSoup(res.text, 'html.parser')
    for i in soup.find_all('option'):
        if i['value']=='':
            continue
        return_list.append(i['value'])
    return return_list


def find_store(si_name, gu_name):
    url = "https://www.7-eleven.co.kr/util/storeLayerPop.asp"
    data = {"storeLaySido": si_name, "storeLayGu": gu_name, "hiddentext":"none"}
    res = requests.post(url, data=data)
    soup = BeautifulSoup(res.text, 'html.parser')

    if soup.find("li", class_="no_data") is not None:
        return None

    return extract_data(res)


def extract_data(data):
    return_list = list()
    soup = BeautifulSoup(data.text, 'html.parser')
    list_div = soup.find("div", class_="list_stroe")

    for i in list_div.find_all('li'):
        temp_dict = dict()
        temp = i.find_all('span')
        temp_dict['sname'] = temp[0].get_text()[0:-3].strip()
        temp_dict['place'] = temp[1].get_text()
        return_list.append(temp_dict)

    return return_list


def data_save():
    si = ["강원도", '경기도', '경상남도', '경상북도', '광주', '대구', '대전', '부산', '서울', '세종', '울산', '인천', '전라남도', '전라북도', '제주도', '충청남도', '충청북도']
    total_list = []
    for_json = {}

    for i in si:
        for j in find_gugun(i):
            temp = find_store(i, j)
            if temp is not None:
                total_list.append(temp)
    for_json['sevenEleven'] = sum(total_list, [])

    with open('../data/json/sevenEleven.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(for_json, ensure_ascii=False))


if __name__ == '__main__':
    data_save()





