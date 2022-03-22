# 좌표를 입력 받아 b_code(법정동 코드)를 retrun해 주도록 하는 함수
import json
import requests

# api => https://developers.kakao.com/product/map
api_key = '3ede87edc2f779bef86eca021e732474'
api_add = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'


def get_bcode(loca):
    # api 설정
    url = api_add
    headers = {"Authorization": f"KakaoAK {api_key}"}
    query = loca

    # api 결과 받기
    result_json = json.loads(str(requests.get(url, headers=headers, params=query).text))

    result_dict = dict(result_json)

    # 좌표값 법정동 코드 dict만들어서 return
    location = dict()
    location['lat'] = loca['y']
    location['lon'] = loca['x']
    location['b_code'] = result_dict['documents'][0]['code']

    return location


# if __name__ == '__main__':
#     query = {'x': '126.495768248769', 'y': '33.4877203371834'}
#     a = get_bcode(query)
#     print(a)