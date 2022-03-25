import csv
import json
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[1]').appName('hosp_change').getOrCreate()

def hospital_change():
    data = spark.read.json("/Housing/data/hadoop_upload/hospital.json", encoding='utf-8')
    data_coll = data.collect()
    rdr = list()
    for i in data_coll:
        rdr.append(i.asDict())
    temp_list = []
    count = 0
    for i in rdr:
        temp_dict = {}
        temp_dict['id'] = count
        temp_dict['place'] = i['dutyAddr']
        temp_dict['duty_code'] = i['dutyDiv']
        temp_dict['duty_Emcls_code'] = i['dutyEmcls']
        temp_dict['dutyEryn_code'] = i['dutyEryn']
        temp_dict['hname'] = i['dutyName']
        temp_dict['lat'] = i['wgs84Lat']
        temp_dict['lot'] = i['wgs84Lon']
        temp_list.append(temp_dict)
        count += 1

        savefile("hospital", temp_list)

def savefile(filename, data):
    with open("../data/json/"+filename+".json", 'w', encoding='utf-8') as f:
        temp_dict = {data}
        f.write(json.dumps(temp_dict, ensure_ascii=False))

if __name__ == "__main__":
    hospital_change()