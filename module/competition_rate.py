import requests
import json
import math

serviceKey = "atBg7rbptorSzUtwV/MjumAmZg36BgCXqwY503dOtogkbgA/4XV3qGXXutHfW4LxKo7eVk7oX3UYXjICS68n+g=="
url = "https://api.odcloud.kr/api/ApplyhomeInfoCmpetRtSvc/v1/"
api_list = ['getAPTLttotPblancCmpet', 'getUrbtyOfctlLttotPblancCmpet', 'getPblPvtRentLttotPblancCmpet', 'getCancResplLttotPblancCmpet', 'getRemndrLttotPblancCmpet']


def make_params(page=1, perPage=1):
    temp_param = {"page": page, "perPage": perPage, "serviceKey": serviceKey}
    return temp_param


def make_url(apiNum=0):
    return url+api_list[apiNum]


def find_count(apiNum=0):
    temp_url = url + api_list[apiNum]
    temp_response = requests.get(temp_url, params=make_params()).json()
    return temp_response['matchCount']


def delete_delta(data):
    temp_list = list()
    for i in data:
        if i['CMPET_RATE'] == "-":
            continue
        if (i['CMPET_RATE'] is not None) and (i['CMPET_RATE'].find("△") > 0):
            i['CMPED_RATE'] = "lacked"
        temp_list.append(i)
    return temp_list


def save_data(apiNum = 0):
    saved_data = []
    json_data = {}
    matchCount = find_count()
    param = make_params(perPage=10000)
    data_page = matchCount // 10000 + 1

    for i in range(data_page):
        param['page'] = i
        temp_data = requests.get(make_url(apiNum), params=param).json()['data']
        if apiNum != 3:
            saved_data.append(delete_delta(temp_data))
        else:
            saved_data.append(temp_data)
    # {"data" : [,,]}
    saved_data = sum(saved_data, [])

    for i in saved_data:
        i['area_grade'] = str(round(float((i.pop("HOUSE_TY"))[0:-1])) // 10) + '단위'

    with open('../data/json/competitionData'+str(apiNum)+'.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(saved_data, ensure_ascii=False))


if __name__ == '__main__':
    save_data(0)









