import csv
import json

def hospital_change():
    with open("../data/json/hospital.json", 'r', encoding='utf-8') as f:
        rdr = json.load(f)
        temp_list = []
        count = 0
        for i in rdr:
            temp_dict = {}
            temp_dict['place'] = i['dutyAddr']
            temp_dict['duty_code'] = i['dutyDiv']
            temp_dict['duty_Emcls_code'] = i['dutyEmcls']
            temp_dict['dutyEryn_code'] = i['dutyEryn']
            temp_dict['hname'] = i['dutyName']
            temp_dict['lat'] = i['wgs84Lat']
            temp_dict['lot'] = i['wgs84Lon']
            temp_list.append(temp_dict)
            count += 1
        savefile("hospital_change", temp_list)

def savefile(filename, data):
    with open("../data/json/"+filename+".json", 'w', encoding='utf-8') as f:
        temp_dict = {data}
        f.write(json.dumps(temp_dict, ensure_ascii=False))

if __name__ == "__main__":
    hospital_change()