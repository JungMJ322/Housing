import json
import csv
from getLocation import kakao_location

def bus_change():
    with open("../data/지하철_버스/bus.csv", 'r', encoding='cp949') as f:
        rdr = csv.reader(f)
        count = 0
        temp_list = []
        current = None
        for i in rdr:
            if current == i[1]:
                continue
            temp_dict = {}
            temp_dict['bus_code'] = i[0]
            temp_dict['stn_name'] = i[1]
            temp_dict['lat'] = i[5]
            temp_dict['lot'] = i[6]
            current = i[1]
            # print(temp_dict)
            temp_list.append(temp_dict)

        save_file('bus_stop', 'busStop', temp_list)


def save_file(json_key, filename, data):
    with open("./json/"+filename+".json", 'w', encoding='utf-8') as f:
        temp_dict = {json_key: data[1:]}
        f.write(json.dumps(temp_dict, ensure_ascii=False))


if __name__ == "__main__":
    pass
