import pandas as pd
import json
import getLocation
from pyspark.sql.functions import col
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[1]').appName('getInfra').getOrCreate()

location = '../output_json/'
file_name = 'subway.json'
json_name = 'subway2.json'

def subwayPer(location=location, file_name=file_name, json_name=json_name):

    df_json = spark.read.json('/housing/data/'+file_name, encoding='utf8')
    df_json.createOrReplaceTempView('subway')
    
    df_json3 = df_json.collect()

    json_file = list()
    for doc in df_json3:
        json_file.append(doc.asDict())

    cnt = 0
    json_file2 = list()
    for data in json_file:
        json_dict = dict()
        json_dict['id'] = cnt
        json_dict['stn_name'] = data['역사명']
        json_dict['route_name'] = data['노선명']
        if data['역경도'] == None:
            loca_dict = getLocation.kakao_location(data['역사 도로명주소'])
            json_dict['lot'] = loca_dict['lot']
            json_dict['lat'] = loca_dict['lat']
        else:
            json_dict['lat'] = data['역위도']
            json_dict['lot'] = data['역경도']
        json_dict['place'] = data['역사 도로명주소']
        cnt = cnt + 1
        json_file2.append(json_dict)

    with open((location + json_name), 'w', encoding='utf8') as f:
        json.dump(json_file2, f, ensure_ascii=False)

if __name__ == '__main__':
    subwayPer()
