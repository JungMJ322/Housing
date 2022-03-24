# kakao map API
# detailed에서 생성한 json파일의 'HSSPLY_ADRES'를 add로 입력
# kakao_location(add)에서 {'lat': 위도, 'lot': 경도, 'b_code': 법정동} 추출
# append_location()으로 json 파일에 위경도, 법정동 코드 항목 추가
import requests
import json
import putLocaGetBCode          # 사용자 모듈


# api => https://developers.kakao.com/product/map
# api 주소, 키
api_key = 'e126277d90cde2cd49d01f2697c761b8'
api_add = 'https://dapi.kakao.com/v2/local/search/address.json'

# 저장 위치
location = '../data/json/'

# kakao API를 이용해 주소의 lot, lat, b_code를 dict의 형태로 retrun
def kakao_location(add):
    # api 설정
    url = api_add# + '?query=' + add
    headers = {"Authorization": f"KakaoAK {api_key}"}
    query = {'query': add}

    # api result
    result_json = json.loads(str(requests.get(url, headers=headers, params=query).text))

    result_json = dict(result_json)

    # api로 주소의 data를 받았는데 data가 없는 경우
    if len(result_json['documents']) == 0:
        # '충청남도 공주시 금흥동 ....'이라면
        # '공주시 금흥동' 으로 검색하도록
        add1 = add.split(' ')
        query = {'query': add1[1] + ' ' + add1[2]}
        result_json = json.loads(str(requests.get(url, headers=headers, params=query).text))

    # 위의 방법으로 검색에 실패했을 때
    # '()'주소에 괄호가 있다면 그 괄호안의 내용으로 검색
    if len(result_json['documents']) == 0:
        cnt1 = add.find('(')
        cnt2 = add.find(')')
        query = {'query': add[cnt1+1:cnt2]}
        result_json = json.loads(str(requests.get(url, headers=headers, params=query).text))

    # 위의 두 방법 모두 실패했을 때
    # kakao API로 검색할 수 없는 주소라고 판단하고 좌표값과 법정동코드를 NULL값으로
    if len(result_json['documents']) == 0:
        dict_fail = {'lot': None, 'lat': None, 'b_code': None}
        return dict_fail

    addr = result_json['documents'][0]['address']

    # 주소를 검색했는데 도로명주소만 데이터를 제공하고,
    # 도,시,동으로는 데이터를 제공하지 않는 경우
    # 좌표값(lot, lat)만 받아와 putLocaGetBCode.get_bcode()함수로 좌표를 이용해 법정동코드(b_code)를 받아옴
    if addr == None:
        addr = result_json['documents']
        loca = dict()
        loca['x'] = addr[0]['x']
        loca['y'] = addr[0]['y']
        location = dict(putLocaGetBCode.get_bcode(loca))
        return location

    # 검색이 제대로 된경우 좌표값과 법정동코드 리턴
    result = dict()
    result['lat'] = addr['y']
    result['lot'] = addr['x']
    result['b_code'] = addr['b_code']

    return result

# if __name__ == '__main__':
#     # add = '충청남도 공주시 한적2길 51-14'
#     # add1 = '공주시 한적2길'
#     # # print(add)
#     # kakao_loca = kakao_location(add1)
#     # print(kakao_loca)
#





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