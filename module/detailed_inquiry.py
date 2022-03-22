# 전국 청약 분양정보 상세조회 서비스 api
# 각각의 api 객체마다 json 파일 형태로 데이터 받아 오기
# 함수로 변수 받아 사용
# json 파일 형식
# 날짜 'CNTRCT_CNCLS_BGNDE'
"""
{
   "currentCount":1,
   "data":[
      {
         "BSNS_MBY_NM":"건설사",
        ...
      },
      ...,
      {"BSNS_MBY_NM":"건설사", ...}
   ],
   "matchCount":1187,
   "page":1,
   "perPage":1,
   "totalCount":1187
}
"""
import requests
import json
import time


# api => https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15098547
# api 주소, 키
api_key = 'serviceKey=jVKpVOT7kMRWzMIqSZbUMTByhcmYH1qvPSCXu%2FwXFtNlDKCdQcchWibsqysFadWPnIOSGsB4%2BchzqJTyw%2BybuQ%3D%3D'
api_add = 'https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/'

api_names = [
    'getAPTLttotPblancDetail',
    'getUrbtyOfctlLttotPblancDetail',
    'getRemndrLttotPblancDetail',
    'getAPTLttotPblancMdl',
    'getUrbtyOfctlLttotPblancMdl',
    'getRemndrLttotPblancMdl'
]

location = './json/'

def date_comp(first_date, second_date):
    date1 = time.strptime(first_date, "%Y-%m-%d")
    date2 = time.strptime(second_date, "%Y-%m-%d")

    return date1 < date2

# 사용할 api 이름, 저장 경로
def getDetailedAPI(api_name=api_names[0], location=location):
    # 이 api의 총 데이터 갯수 구하기
    total_count = api_add + api_name + '?page=1&perPage=1&' + api_key
    cnt_resp = requests.get(total_count)
    cnt_json = cnt_resp.json()
    cnt = cnt_json['totalCount']

    # 모든 데이터 가지고 오기
    url = api_add + api_name + f'?page=1&perPage={cnt}&' + api_key
    resp = requests.get(url)
    datas = resp.json()

    # 파일 저장
    with open((location+api_name[3:6]+api_name[-3:]+'.json'), 'w', encoding='utf8') as file:
        json.dump(datas, file, indent=4, ensure_ascii=False)



def del_date(api_name=api_names[0], location=location):
    with open((location+api_name[3:6]+api_name[-3:]+'.json'), 'r', encoding='utf8') as file:
        json_file = json.load(file)

    datas = dict(json_file)
    del_index = list()

    for data in datas['data']:
        if date_comp('2022-01-31', data['CNTRCT_CNCLS_BGNDE']):
            del_index.append(datas['data'].index(data))

    del_index.reverse()

    for i in del_index:
        del datas['data'][i]

    # 파일 저장
    with open((location + api_name[3:6] + api_name[-3:] + '.json'), 'w', encoding='utf8') as file:
        json.dump(datas, file, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    getDetailedAPI()
    # del_date()