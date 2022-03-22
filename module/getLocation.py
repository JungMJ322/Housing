# kakao map API
# detailed에서 생성한 json파일의 'HSSPLY_ADRES'를 add로 입력
# kakao_location(add)에서 {'lat': 위도, 'lot': 경도, 'b_code': 법정동}

import requests
import json


# api => https://developers.kakao.com/product/map
# api 주소, 키
api_key = '3ede87edc2f779bef86eca021e732474'
api_add = 'https://dapi.kakao.com/v2/local/search/address.json'

location = './json/'

def kakao_location(add):
    url = api_add + '?query=' + add
    headers = {"Authorization": f"KakaoAK {api_key}"}
    query = {'query': add}
    result_json = json.loads(str(requests.get(url, headers=headers, data=query).text))

    result_json = dict(result_json)
    print(len(result_json['documents']))

    if len(result_json['documents']) == 0:
        cnt = add.find('(')
        # cnt2
        url = api_add + '?query=' + add[cnt+1:cnt+4]
        result_json = json.loads(str(requests.get(url, headers=headers).text))

        if cnt == -1:
            url = api_add + '?query=' + add
            result_json = json.loads(str(requests.get(url, headers=headers).text))

    if len(result_json['documents']) == 0:
        cnt = add.find('길')
        url = api_add + '?query=' + add[0:cnt+1]
        result_json = json.loads(str(requests.get(url, headers=headers).text))

        if cnt == -1:
            url = api_add + '?query=' + add
            result_json = json.loads(str(requests.get(url, headers=headers).text))

    if len(result_json['documents']) == 0:
        cnt = add.find('로')
        url = api_add + '?query=' + add[0:cnt+1]
        result_json = json.loads(str(requests.get(url, headers=headers).text))

        if cnt == -1:
            url = api_add + '?query=' + add
            result_json = json.loads(str(requests.get(url, headers=headers).text))

    if len(result_json['documents']) == 0:
        cnt = add.find('동')
        url = api_add + '?query=' + add[0:cnt+1]
        result_json = json.loads(str(requests.get(url, headers=headers).text))

    # print(result_json)

    if list(result_json.keys())[0] == 'errorType':
        dict_fail = {'lon': None, 'lat': None, 'b_code': None}
        return dict_fail

    if len(result_json['documents']) == 0:
        dict_fail = {'lon': None, 'lat': None, 'b_code': None}
        return dict_fail

    if result_json['documents'][0]['address'] == None:
        dict_fail = {'lon': None, 'lat':None, 'b_code': None}
        return dict_fail

    print(result_json)

    addr = result_json['documents'][0]['address']

    result = dict()
    result['lat'] = addr['y']
    result['lon'] = addr['x']
    result['b_code'] = addr['b_code']

    return result


def append_location(file_name='APTail.json', location=location):
    with open((location+file_name), 'r', encoding='utf8') as f:
        json_file = json.load(f)

    json_dict = dict(json_file)
    json_datas = json_dict['data']

    # 'HSSPLY_ADRES' 주소
    # for data in json_datas:
    for data in json_datas:
        add = data['HSSPLY_ADRES']
        print(add)

        loca = kakao_location(add)

        data['lat'] = loca['lat']
        data['lon'] = loca['lon']
        data['b_code'] = loca['b_code']

    with open((location+file_name), 'w', encoding='utf8') as f:
        json.dump(json_datas, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # add = '인천광역시 서구 청라사파이어로'
    # print(add)
    # kakao_loca = kakao_location(add)
    # print(kakao_loca)

    append_location()




"""
{
   "documents":[
      {
         "address":{
            "address_name":"서울 강동구 강일동 717",
            "b_code":"1174011000",
            "h_code":"1174051500",
            "main_address_no":"717",
            "mountain_yn":"N",
            "region_1depth_name":"서울",
            "region_2depth_name":"강동구",
            "region_3depth_h_name":"강일동",
            "region_3depth_name":"강일동",
            "sub_address_no":"",
            "x":"127.173182162867",
            "y":"37.5587972921376"
         },
         "address_name":"서울 강동구 고덕로 427",
         "address_type":"ROAD_ADDR",
         "road_address":{
            "address_name":"서울 강동구 고덕로 427",
            "building_name":"고덕리엔파크2단지아파트",
            ...
            "x":"127.173182162867",
            "y":"37.5587972921376",
            "zone_no":"05217"
         },
         "x":"127.173182162867",
         "y":"37.5587972921376"
      }
   ],
   "meta":{
      "is_end":true,
      "pageable_count":1,
      "total_count":1
   }
}

"""