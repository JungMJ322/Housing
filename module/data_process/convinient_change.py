import json
import csv
from getLocation import kakao_location
from pyspark.sql import SparkSession
import save_mysql

spark = SparkSession.builder.master('local[1]').appName('convin_change').getOrCreate()

def bus_change():
    data = spark.read.csv("/Housing/data/hadoop_upload/bus.csv", encoding="cp949", header=True)
    data_coll = data.collect()
    rdr = list()
    for i in data_coll:
        rdr.append(i.asDict())
    count = 0
    temp_list = []
    current = None
    for i in rdr:
        if current == i["정류장 명칭"]:
            continue
        temp_dict = {}
        temp_dict['id'] = count
        temp_dict['stn_name'] = i["정류장 명칭"]
        temp_dict['lat'] = i["위도"]
        temp_dict['lot'] = i["경도"]
        current = i["정류장 명칭"]
        # print(temp_dict)
        temp_list.append(temp_dict)
        count += 1

    savefile('bus_stop', 'busStop', temp_list[1:])
    save_mysql.save_list_to_db(temp_list[1:], "busStop")

def mart_change():
    data = spark.read.csv("/Housing/data/hadoop_upload/mart_raw.csv", encoding="cp949", header=True)
    data_coll = data.collect()
    rdr = list()
    for i in data_coll:
        rdr.append(i.asDict())
    temp_list = []
    count = 0
    for i in rdr:
        temp_dict = {}
        try:
            if (len(i['영업상태명']) != 5) or ((len(i["소재지전체주소"]) < 5) and (len(i["도로명전체주소"]) < 5)):
                continue
            if i["소재지전체주소"] == '' and i["도로명전체주소"] == '':
                continue
            elif i["소재지전체주소"] == '':
                coordi = kakao_location(i["도로명전체주소"])
            else:
                coordi = kakao_location(i["소재지전체주소"])
        except IndexError:
            continue
        temp_dict['id'] = count
        temp_dict['start_date'] = i["인허가일자"]
        temp_dict['mart_name'] = i["사업장명"]
        temp_dict['lat'] = coordi['lat']
        temp_dict['lot'] = coordi['lot']
        temp_list.append(temp_dict)
        count += 1

    savefile("martData", "mart", temp_list[1:])
    save_mysql.save_list_to_db(temp_list[1:], "mart")


def park_change():
    data = spark.read.json("/Housing/data/hadoop_upload/park_raw.json", encoding='utf-8')
    data_coll = data.collect()
    rdr = list()
    for i in data_coll:
        rdr.append(i.asDict())

    temp_list = []
    count = 1
    for i in rdr:
        temp_dict = {}
        temp_dict['id'] = count
        temp_dict['park_name'] = i['공원명']
        temp_dict['park_type'] = i['공원구분']
        temp_dict['start_date'] = i['지정고시일']

        if i['소재지지번주소'] == '':
            temp_dict['place'] = i['소재지도로명주소']
        elif i['소재지도로명주소'] == '':
            temp_dict['place'] = i['소재지지번주소']
        else:
            continue

        if (len(i["위도"]) == 0) or (len(i["경도"]) == 0):
            try:
                loc = kakao_location(temp_dict['place'])
            except:
                continue
            temp_dict['lat'] = loc['lat']
            temp_dict['lot'] = loc['lot']
        else:
            temp_dict['lat'] = i['위도']
            temp_dict['lot'] = i['경도']

        temp_dict['start_date'] = i['지정고시일']

        count += 1
        temp_list.append(temp_dict)

    savefile("park", "park", temp_list)
    save_mysql.save_list_to_db(temp_list, "park")


def school_change():
    data = spark.read.json("/Housing/data/hadoop_upload/school_raw.json", encoding='utf-8')
    data_coll = data.collect()
    rdr = list()
    for i in data_coll:
        rdr.append(i.asDict())

    temp_list = []
    count = 1
    for i in rdr:
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
    save_mysql.save_list_to_db(temp_list, "school")

def savefile(json_key, filename, data):
    with open("../../data/output_json/"+filename+".json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    bus_change()
    mart_change()
    park_change()
    school_change()


