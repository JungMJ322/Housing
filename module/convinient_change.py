import json
import csv
from getLocation import kakao_location

def bus_change():
    with open("../data/TransportData/bus.csv", 'r', encoding='cp949') as f:
        rdr = csv.reader(f)
        count = 0
        temp_list = []
        current = None
        for i in rdr:
            if current == i[1]:
                continue
            temp_dict = {}
            temp_dict['id'] = count
            temp_dict['stn_name'] = i[1]
            temp_dict['lat'] = i[5]
            temp_dict['lot'] = i[6]
            current = i[1]
            # print(temp_dict)
            temp_list.append(temp_dict)
            count += 1

        savefile('bus_stop', 'busStop', temp_list)


def mart_change():
    with open("../data/InfraData/mart_raw.csv", 'r', encoding='cp949') as f:
        rdr = csv.reader(f)
        temp_list = []
        count = 0
        for i in rdr:
            temp_dict = {}
            try:
                if i[8] != "영업/정상" or ((len(i[18]) < 5) and (len(i[18]))) != 0:
                    continue
                if i[18] == '' and i[19] == '':
                    continue
                elif i[18] == '':
                    coordi = kakao_location(i[19])
                else:
                    coordi = kakao_location(i[18])
            except IndexError:
                continue

            temp_dict['id'] = count
            temp_dict['start_date'] = i[5]
            temp_dict['mart_name'] = i[21]
            temp_dict['lat'] = coordi['lat']
            temp_dict['lot'] = coordi['lot']
            temp_list.append(temp_dict)
            count += 1

        savefile("martData", "mart", temp_list[1:])


def park_change():
    with open("../data/InfraData/park_raw.json", 'r', encoding='utf-8') as f:
        rdr = json.load(f)
        temp_list = []
        count = 1
        for i in rdr['records']:
            temp_dict = {}
            temp_dict['id'] = count
            temp_dict['park_name'] = i['공원명']
            temp_dict['park_type'] = i['공원구분']
            if i['위도'] == '':
                temp_dict['lat'] = None
                temp_dict['lot'] = None
            else:
                temp_dict['lat'] = i['위도']
                temp_dict['lot'] = i['경도']
            temp_dict['start_date'] = i['지정고시일']
            if i['소재지지번주소'] == '':
                temp_dict['place'] = i['소재지도로명주소']
            elif i['소재지도로명주소'] == '':
                temp_dict['place'] = i['소재지지번주소']
            else:
                continue
            count += 1
            temp_list.append(temp_dict)

        savefile("park", "park", temp_list)


def school_change():
    with open("../data/InfraData/school_raw.json", 'r', encoding='utf-8') as f:
        rdr = json.load(f)
        temp_list = []
        count = 1
        for i in rdr['records']:
            temp_dict = {}
            temp_dict['id'] = count
            temp_dict['school_name'] = i['학교명']
            temp_dict['school_kind'] = i['학교급구분']
            temp_dict['start_date'] = i['설립일자']
            temp_dict['lat'] = i['위도']
            temp_dict['lot'] = i['경도']
            temp_dict['place'] = i['소재지지번주소']
            temp_list.append(temp_dict)
            count += 1
        savefile("school", "school", temp_list)

def savefile(json_key, filename, data):
    with open("../data/json/"+filename+".json", 'w', encoding='utf-8') as f:

        f.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    # bus_change()
    # mart_change()
    park_change()
    # school_change()

