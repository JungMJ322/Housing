import pandas as pd
import json
import getLocation
import xlsxToJson

location = '../data/json/'
file_name = 'subway.json'
json_name = 'subway2.json'

def subwayPer(location=location, file_name=file_name, json_name=json_name):
    xlsxToJson.getXlsxToJson()

    with open((location + file_name), 'r', encoding='utf8') as f:
        json_file = json.load(f)

    df = pd.DataFrame(json_file['data'])
    subway = df.loc[:,['역번호', '역사명', '노선명', '역위도', '역경도', '역사 도로명주소']]
    subway.columns  = ['subway_code', 'stn_name', 'route_name', 'lat', 'lon', 'place']

    json_data = subway.to_json(location+json_name, orient = 'table', indent=4, force_ascii=False)

    with open((location+json_name), 'r', encoding='utf8') as f:
        json_file = json.load(f)

    cnt = 1
    for data in json_file['data']:
        if data['lot'] == None:
            loca_dict = getLocation.kakao_location(data['place'])
            data['lot'] = loca_dict['lot']
            data['lat'] = loca_dict['lat']
            data['id'] = cnt
            cnt = cnt + 1

    with open((location + json_name), 'w', encoding='utf8') as f:
        json.dump(json_file['data'], f, ensure_ascii=False)

if __name__ == '__main__':
    subwayPer()
